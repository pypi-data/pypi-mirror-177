"""sonusai genft

usage: genft [-hvs] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database directory.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -o OUTPUT, --output OUTPUT      Output directory.
    -s, --segsnr                    Save segsnr. [default: False].

Generate SonusAI feature/truth data from a SonusAI mixture database.

Inputs:
    MIXDB       A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs:
    OUTPUT/     A directory containing:
                    <id>.h5:
                        dataset:    feature
                        dataset:    truth_f
                        dataset:    segsnr (optional)
                    <id>.txt
                    genft.log

"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import AudioT
from sonusai.mixture import AudiosT
from sonusai.mixture import FeatureData
from sonusai.mixture import ListAudiosT
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import MixtureIDs
from sonusai.mixture import Segsnr
from sonusai.mixture import Truth


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class GlobalGenft:
    mixdb: MixtureDatabase = None
    raw_target_audios: AudiosT = None
    augmented_noise_audios: ListAudiosT = None
    mixture: AudioT = None
    truth_t: Truth = None
    segsnr_t: Segsnr = None
    compute_truth: bool = None
    compute_segsnr: bool = None
    output_dir: str = None


mp_genft = GlobalGenft()


def genft(mixdb: MixtureDatabase,
          mixids: MixtureIDs = None,
          raw_target_audios: AudiosT = None,
          augmented_noise_audios: ListAudiosT = None,
          mixture: AudioT = None,
          truth_t: Truth = None,
          segsnr_t: Segsnr = None,
          compute_truth: bool = True,
          compute_segsnr: bool = False) -> FeatureData:
    import multiprocessing as mp

    from sonusai.mixture import convert_mixids_to_list
    from sonusai.mixture import concatenate_feature_data
    from sonusai.mixture import get_feature_data
    from sonusai.utils import p_map

    mixids = convert_mixids_to_list(mixdb, mixids)
    results = []
    if mp.current_process().daemon:
        for mixid in mixids:
            results.append(get_feature_data(mixdb=mixdb,
                                            mrecord=mixdb.mixtures[mixid],
                                            mixture=mixture,
                                            truth_t=truth_t,
                                            segsnr_t=segsnr_t,
                                            raw_target_audios=raw_target_audios,
                                            augmented_noise_audios=augmented_noise_audios,
                                            compute_truth=compute_truth,
                                            compute_segsnr=compute_segsnr))
    else:
        mp_genft.mixdb = mixdb
        mp_genft.mixture = mixture
        mp_genft.truth_t = truth_t
        mp_genft.segsnr_t = segsnr_t
        mp_genft.raw_target_audios = raw_target_audios
        mp_genft.augmented_noise_audios = augmented_noise_audios
        mp_genft.compute_truth = compute_truth
        mp_genft.compute_segsnr = compute_segsnr

        results = p_map(_genft_kernel, mixids)

    return concatenate_feature_data(results)


def _genft_kernel(mixid: int) -> FeatureData:
    from sonusai.mixture import get_feature_data

    return get_feature_data(mixdb=mp_genft.mixdb,
                            mrecord=mp_genft.mixdb.mixtures[mixid],
                            raw_target_audios=mp_genft.raw_target_audios,
                            augmented_noise_audios=mp_genft.augmented_noise_audios,
                            mixture=mp_genft.mixture,
                            truth_t=mp_genft.truth_t,
                            segsnr_t=mp_genft.segsnr_t,
                            compute_truth=mp_genft.compute_truth,
                            compute_segsnr=mp_genft.compute_segsnr)


def _process_mixture(mixid: int) -> None:
    from os.path import join
    from os.path import splitext

    import h5py
    import numpy as np

    from sonusai.mixture import add_feature_data_to_h5
    from sonusai.mixture import get_mixture_metadata

    output_name = join(mp_genft.output_dir, mp_genft.mixdb.mixtures[mixid].name)
    with h5py.File(output_name, 'a') as f:
        mixture = None
        if 'mixture' in f:
            mixture = np.array(f['mixture'])

        truth_t = None
        if 'truth_t' in f:
            truth_t = np.array(f['truth_t'])

        segsnr_t = None
        if mp_genft.compute_segsnr and 'segsnr_t' in f:
            segsnr_t = np.array(f['segsnr_t'])

    data = genft(mixdb=mp_genft.mixdb,
                 mixids=mixid,
                 raw_target_audios=mp_genft.raw_target_audios,
                 augmented_noise_audios=mp_genft.augmented_noise_audios,
                 mixture=mixture,
                 truth_t=truth_t,
                 segsnr_t=segsnr_t,
                 compute_segsnr=mp_genft.compute_segsnr)

    add_feature_data_to_h5(file=output_name,
                           data=data,
                           save_segsnr=mp_genft.compute_segsnr)

    with open(file=splitext(output_name)[0] + '.txt', mode='w') as f:
        f.write(get_mixture_metadata(mp_genft.mixdb, mixid))


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

    from pyaaware import FeatureGenerator
    from tqdm import tqdm

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import get_augmented_noise_audios
    from sonusai.mixture import get_raw_audios
    from sonusai.mixture import check_audio_files_exist
    from sonusai.mixture import convert_mixids_to_list
    from sonusai.mixture import load_mixdb
    from sonusai.utils import p_tqdm_map
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    verbose = args['--verbose']
    mixdb_loc = args['--mixdb']
    mixid = args['--mixid']
    output_dir = args['--output']
    compute_segsnr = args['--segsnr']

    start_time = time.monotonic()

    if output_dir is None:
        output_dir = mixdb_loc

    if exists(output_dir) and not isdir(output_dir):
        remove(output_dir)

    makedirs(output_dir, exist_ok=True)

    create_file_handler(join(output_dir, 'genft.log'))
    update_console_handler(verbose)
    initial_log_messages('genft')

    logger.info(f'\nLoad mixture database from {mixdb_loc}')
    mixdb = load_mixdb(mixdb_loc)
    mixid = convert_mixids_to_list(mixdb, mixid)

    fg = FeatureGenerator(feature_mode=mixdb.feature,
                          num_classes=mixdb.num_classes,
                          truth_mutex=mixdb.truth_mutex)

    total_samples = sum([sub.samples for sub in [mixdb.mixtures[m] for m in mixid]])
    duration = total_samples / sonusai.mixture.SAMPLE_RATE
    total_transform_frames = total_samples // fg.ftransform_R
    total_feature_frames = total_samples // mixdb.feature_step_samples

    logger.info('')
    logger.info(f'Found {len(mixid):,} mixtures to process')
    logger.info(f'{total_samples:,} samples, '
                f'{total_transform_frames:,} transform frames, '
                f'{total_feature_frames:,} feature frames')

    check_audio_files_exist(mixdb)

    mp_genft.mixdb = mixdb
    mp_genft.output_dir = output_dir
    mp_genft.raw_target_audios = get_raw_audios(mixdb)
    mp_genft.augmented_noise_audios = get_augmented_noise_audios(mixdb)
    mp_genft.compute_segsnr = compute_segsnr

    progress = tqdm(total=len(mixid), desc='genft')
    p_tqdm_map(_process_mixture, mixid, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(mixid)} mixtures to {output_dir}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'feature:  {human_readable_size(total_feature_frames * fg.stride * fg.num_bands * 4, 1)}')
    logger.info(f'truth_f:  {human_readable_size(total_feature_frames * mixdb.num_classes * 4, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(total_transform_frames * 4, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
