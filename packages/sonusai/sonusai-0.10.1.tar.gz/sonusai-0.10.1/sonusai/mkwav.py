"""sonusai mkwav

usage: mkwav [-hvtn] (-d MIXDB) [-i MIXID] [-o OUTPUT]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d MIXDB, --mixdb MIXDB         Mixture database directory.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -o OUTPUT, --output OUTPUT      Output directory.
    -t, --target                    Write target file.
    -n, --noise                     Write noise file.

The mkwav command creates WAV files from a SonusAI database.

Inputs:
    MIXDB       A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs:
    OUTPUT/     A directory containing:
                    <id>_mixture.wav:   mixture
                    <id>_target.wav:    target (optional)
                    <id>_noise.wav:     noise (optional)
                    <id>.txt
                    mkwav.log

"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import AudioT
from sonusai.mixture import AudiosT
from sonusai.mixture import ListAudiosT
from sonusai.mixture import MixtureDatabase


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class GlobalMkwav:
    mixdb: MixtureDatabase = None
    raw_target_audios: AudiosT = None
    augmented_noise_audios: ListAudiosT = None
    write_target: bool = None
    write_noise: bool = None
    output_dir: str = None


mp_mkwav = GlobalMkwav()


def mkwav(mixdb: MixtureDatabase,
          mixid: int,
          raw_target_audios: AudiosT = None,
          augmented_noise_audios: ListAudiosT = None) -> (AudioT, AudioT, AudioT):
    from sonusai.genmix import genmix

    data = genmix(mixdb=mixdb,
                  mixids=mixid,
                  raw_target_audios=raw_target_audios,
                  augmented_noise_audios=augmented_noise_audios)

    return data.mixture, sum(data.targets), data.noise


def _process_mixture(mixid: int) -> None:
    from os.path import exists
    from os.path import join
    from os.path import splitext

    import h5py
    import numpy as np

    from sonusai.mixture import get_mixture_metadata
    from sonusai.utils.wave import write_wav

    mixture_filename = join(mp_mkwav.output_dir, mp_mkwav.mixdb.mixtures[mixid].name)
    mixture_basename = splitext(mixture_filename)[0]

    target = None
    noise = None

    need_data = True
    if exists(mixture_filename + '.h5'):
        with h5py.File(mixture_filename, 'r') as f:
            if 'mixture' in f:
                need_data = False
            if mp_mkwav.write_target and 'targets' not in f:
                need_data = True
            if mp_mkwav.write_noise and 'noise' not in f:
                need_data = True

    if need_data:
        mixture, target, noise = mkwav(mixdb=mp_mkwav.mixdb,
                                       mixid=mixid,
                                       raw_target_audios=mp_mkwav.raw_target_audios,
                                       augmented_noise_audios=mp_mkwav.augmented_noise_audios)
    else:
        with h5py.File(mixture_filename, 'r') as f:
            mixture = np.array(f['mixture'])
            if mp_mkwav.write_target:
                target = sum(np.array(f['targets']))
            if mp_mkwav.write_noise:
                noise = np.array(f['noise'])

    write_wav(name=mixture_basename + '_mixture.wav', audio=mixture)
    if mp_mkwav.write_target:
        write_wav(name=mixture_basename + '_target.wav', audio=target)
    if mp_mkwav.write_noise:
        write_wav(name=mixture_basename + '_noise.wav', audio=noise)

    with open(file=mixture_basename + '.txt', mode='w') as f:
        f.write(get_mixture_metadata(mp_mkwav.mixdb, mixid))


def main():
    import time
    from os import makedirs
    from os import remove
    from os.path import exists
    from os.path import isdir
    from os.path import join

    from docopt import docopt
    from tqdm import tqdm

    import sonusai
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
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixdb_loc = args['--mixdb']
    mixid = args['--mixid']
    output_dir = args['--output']
    write_target = args['--target']
    write_noise = args['--noise']

    if not output_dir:
        output_dir = mixdb_loc

    if exists(output_dir) and not isdir(output_dir):
        remove(output_dir)

    makedirs(output_dir, exist_ok=True)

    start_time = time.monotonic()

    create_file_handler(join(output_dir, 'mkwav.log'))
    update_console_handler(verbose)
    initial_log_messages('mkwav')

    logger.info(f'\nLoad mixture database from {mixdb_loc}')
    mixdb = load_mixdb(mixdb_loc)
    mixid = convert_mixids_to_list(mixdb, mixid)

    total_samples = sum([sub.samples for sub in [mixdb.mixtures[m] for m in mixid]])
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixid):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    check_audio_files_exist(mixdb)

    mp_mkwav.mixdb = mixdb
    mp_mkwav.output_dir = output_dir
    mp_mkwav.raw_target_audios = get_raw_audios(mixdb)
    mp_mkwav.augmented_noise_audios = get_augmented_noise_audios(mixdb)
    mp_mkwav.write_target = write_target
    mp_mkwav.write_noise = write_noise

    progress = tqdm(total=len(mixid), desc='mkwav')
    p_tqdm_map(_process_mixture, mixid, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(mixid)} mixtures to {output_dir}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if write_target:
        logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    if write_noise:
        logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
