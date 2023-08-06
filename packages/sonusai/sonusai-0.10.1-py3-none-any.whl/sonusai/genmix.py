"""sonusai genmix

usage: genmix [-hvts] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database directory.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -o OUTPUT, --output OUTPUT      Output directory.
    -t, --truth                     Save truth_t. [default: False].
    -s, --segsnr                    Save segsnr_t. [default: False].

Generate SonusAI mixture data from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs:
    OUTPUT/     A directory containing:
                    <id>.h5:
                        dataset:    mixture
                        dataset:    target
                        dataset:    noise
                        dataset:    truth_t
                        dataset:    segsnr_t
                    <id>.txt
                    genmix.log
"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import AudioData
from sonusai.mixture import AudiosT
from sonusai.mixture import ListAudiosT
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import MixtureIDs


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class GlobalGenmix:
    mixdb: MixtureDatabase = None
    raw_target_audios: AudiosT = None
    augmented_noise_audios: ListAudiosT = None
    compute_truth: bool = None
    compute_segsnr: bool = None
    output_dir: str = None


mp_genmix = GlobalGenmix()


def genmix(mixdb: MixtureDatabase,
           mixids: MixtureIDs = None,
           raw_target_audios: AudiosT = None,
           augmented_noise_audios: ListAudiosT = None,
           compute_truth: bool = False,
           compute_segsnr: bool = False) -> AudioData:
    import multiprocessing as mp

    from sonusai.mixture import concatenate_audio_data
    from sonusai.mixture import convert_mixids_to_list
    from sonusai.mixture import get_audio_data
    from sonusai.utils import p_map

    mixids = convert_mixids_to_list(mixdb, mixids)
    results = []
    if mp.current_process().daemon:
        for mixid in mixids:
            results.append(get_audio_data(mixdb=mixdb,
                                          mrecord=mixdb.mixtures[mixid],
                                          raw_target_audios=raw_target_audios,
                                          augmented_noise_audios=augmented_noise_audios,
                                          compute_truth=compute_truth,
                                          compute_segsnr=compute_segsnr))
    else:
        mp_genmix.mixdb = mixdb
        mp_genmix.raw_target_audios = raw_target_audios
        mp_genmix.augmented_noise_audios = augmented_noise_audios
        mp_genmix.compute_truth = compute_truth
        mp_genmix.compute_segsnr = compute_segsnr

        results = p_map(_genmix_kernel, mixids)

    return concatenate_audio_data(results)


def _genmix_kernel(mixid: int) -> AudioData:
    from sonusai.mixture import get_audio_data

    return get_audio_data(mixdb=mp_genmix.mixdb,
                          mrecord=mp_genmix.mixdb.mixtures[mixid],
                          raw_target_audios=mp_genmix.raw_target_audios,
                          augmented_noise_audios=mp_genmix.augmented_noise_audios,
                          compute_truth=mp_genmix.compute_truth,
                          compute_segsnr=mp_genmix.compute_segsnr)


def _process_mixture(mixid: int) -> None:
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from sonusai.mixture import add_audio_data_to_h5
    from sonusai.mixture import get_mixture_metadata

    data = genmix(mixdb=mp_genmix.mixdb,
                  mixids=mixid,
                  raw_target_audios=mp_genmix.raw_target_audios,
                  augmented_noise_audios=mp_genmix.augmented_noise_audios,
                  compute_segsnr=mp_genmix.compute_segsnr,
                  compute_truth=mp_genmix.compute_truth)

    samples = data.mixture.shape[0]
    if mp_genmix.compute_truth:
        if samples != data.truth_t.shape[0]:
            raise SonusAIError(
                f'truth_t samples does not match mixture samples: {data.truth_t.shape[0]} != {samples}')
        if mp_genmix.mixdb.num_classes != data.truth_t.shape[1]:
            raise SonusAIError(
                f'truth_t num_classes is incorrect: {data.truth_t.shape[1]} != {mp_genmix.mixdb.num_classes}')
    for target in data.targets:
        if samples != target.shape[0]:
            raise SonusAIError(f'target samples does not match mixture samples: {target.shape[0]} != {samples}')
    if samples != data.noise.shape[0]:
        raise SonusAIError(f'noise samples does not match mixture samples: {data.noise.shape[0]} != {samples}')
    if mp_genmix.compute_segsnr and samples != data.segsnr_t.shape[0]:
        raise SonusAIError(f'segsnr_t samples does not match mixture samples: {data.segsnr_t.shape[0]} != {samples}')

    output_name = join(mp_genmix.output_dir, mp_genmix.mixdb.mixtures[mixid].name)
    add_audio_data_to_h5(file=output_name,
                         data=data,
                         save_truth=mp_genmix.compute_truth,
                         save_segsnr=mp_genmix.compute_segsnr)

    with open(file=splitext(output_name)[0] + '.txt', mode='w') as f:
        f.write(get_mixture_metadata(mp_genmix.mixdb, mixid))


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os import makedirs
    from os import remove
    from os.path import exists
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from tqdm import tqdm

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import check_audio_files_exist
    from sonusai.mixture import convert_mixids_to_list
    from sonusai.mixture import get_augmented_noise_audios
    from sonusai.mixture import get_raw_audios
    from sonusai.mixture import load_mixdb
    from sonusai.utils import human_readable_size
    from sonusai.utils import p_tqdm_map
    from sonusai.utils import seconds_to_hms

    verbose = args['--verbose']
    mixdb_loc = args['--mixdb']
    mixid = args['--mixid']
    output_dir = args['--output']
    compute_segsnr = args['--segsnr']
    compute_truth = args['--truth']

    if not output_dir:
        output_dir = splitext(mixdb_loc)[0]

    if exists(output_dir) and not isdir(output_dir):
        remove(output_dir)

    makedirs(output_dir, exist_ok=True)

    start_time = time.monotonic()

    create_file_handler(join(output_dir, 'genmix.log'))
    update_console_handler(verbose)
    initial_log_messages('genmix')

    logger.info(f'\nLoad mixture database from {mixdb_loc}')
    mixdb = load_mixdb(mixdb_loc)
    mixid = convert_mixids_to_list(mixdb, mixid)

    total_samples = sum([sub.samples for sub in [mixdb.mixtures[m] for m in mixid]])
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixid):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    check_audio_files_exist(mixdb)

    mp_genmix.mixdb = mixdb
    mp_genmix.raw_target_audios = get_raw_audios(mixdb)
    mp_genmix.augmented_noise_audios = get_augmented_noise_audios(mixdb)
    mp_genmix.compute_truth = compute_truth
    mp_genmix.compute_segsnr = compute_segsnr
    mp_genmix.output_dir = output_dir

    progress = tqdm(total=len(mixid), desc='genmix')
    p_tqdm_map(_process_mixture, mixid, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(mixid)} mixtures to {output_dir}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if compute_truth:
        logger.info(f'truth_t:  {human_readable_size(total_samples * mixdb.num_classes * 4, 1)}')
    logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(total_samples * 4, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
