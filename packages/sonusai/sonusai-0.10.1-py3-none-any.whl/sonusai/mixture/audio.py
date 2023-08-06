from dataclasses import dataclass
from typing import List
from typing import Union

import numpy as np
from pyaaware import ForwardTransform
from pyaaware import InverseTransform

from sonusai.mixture.types import AudioData
from sonusai.mixture.types import AudioF
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import AudiosT
from sonusai.mixture.types import Feature
from sonusai.mixture.types import ListAudiosT
from sonusai.mixture.types import MRecord
from sonusai.mixture.types import MixtureDatabase
from sonusai.mixture.types import Truth


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class GlobalAudio:
    mixdb: MixtureDatabase = None


mp_audiodb = GlobalAudio()


def _augment_audio(audio: AudioT, target: bool = False) -> List[AudioT]:
    from sonusai.mixture import apply_augmentation

    if target:
        augmentations = mp_audiodb.mixdb.target_augmentations
    else:
        augmentations = mp_audiodb.mixdb.noise_augmentations

    return [apply_augmentation(audio_in=audio, augmentation=augmentation) for augmentation in augmentations]


def get_augmented_noise_audios(mixdb: MixtureDatabase, show_progress: bool = False) -> ListAudiosT:
    """Get a list of lists of augmented noise audio data."""
    from tqdm import tqdm

    from sonusai.utils import p_tqdm_map

    raw_noise_audios = get_raw_audios(mixdb=mixdb, show_progress=show_progress, target=False)

    names = [mixdb.noises[i].name for i in range(len(mixdb.noises))]
    progress = tqdm(total=len(names), desc='Augment noise audio', disable=not show_progress)

    mp_audiodb.mixdb = mixdb

    return p_tqdm_map(_augment_audio, raw_noise_audios, progress=progress)


def get_raw_audios(mixdb: MixtureDatabase, show_progress: bool = False, target: bool = True) -> List[AudioT]:
    """Get a list of raw audio data."""
    from tqdm import tqdm

    from sonusai.utils import p_tqdm_map

    if target:
        names = [mixdb.targets[i].name for i in range(len(mixdb.targets))]
        progress = tqdm(total=len(names), desc='Read target audio', disable=not show_progress)
    else:
        names = [mixdb.noises[i].name for i in range(len(mixdb.noises))]
        progress = tqdm(total=len(names), desc='Read noise audio', disable=not show_progress)

    raw_audios = p_tqdm_map(read_audio, names, progress=progress)

    return raw_audios


def check_audio_files_exist(mixdb: MixtureDatabase) -> None:
    """Walk through all the noise and target audio files in a mixture database ensuring that they exist."""
    from os.path import exists

    from sonusai import SonusAIError
    from sonusai.mixture import tokenized_expandvars

    for file_index in range(len(mixdb.noises)):
        file_name, _ = tokenized_expandvars(mixdb.noises[file_index].name)
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')

    for file_index in range(len(mixdb.targets)):
        file_name, _ = tokenized_expandvars(mixdb.targets[file_index].name)
        if not exists(file_name):
            raise SonusAIError(f'Could not find {file_name}')


# def read_raw_target_audio(mixdb: MixtureDatabase, show_progress: bool = False) -> AudiosT:
#     """Read in all audio data beforehand to avoid reading it multiple times in a loop."""
#     from tqdm import tqdm
#
#     from sonusai.utils import p_tqdm_map
#
#     names = [target.name for target in mixdb.targets]
#     progress = tqdm(total=len(names), desc='Read target audio', disable=not show_progress)
#     raw_target_audio = p_tqdm_map(read_audio, names, progress=progress)
#     progress.close()
#
#     return raw_target_audio


def get_target_noise_audio(mixdb: MixtureDatabase,
                           mrecord: MRecord,
                           raw_target_audios: AudiosT = None,
                           augmented_noise_audios: ListAudiosT = None) -> (AudiosT, AudioT):
    """Apply augmentations and return augmented target and noise data."""
    from pyaaware import FeatureGenerator

    from sonusai import SonusAIError
    from sonusai.mixture import apply_augmentation
    from sonusai.mixture import apply_snr_gain
    from sonusai.mixture import pad_to_samples

    if raw_target_audios is None:
        raw_target_audios = get_raw_audios(mixdb)
    if augmented_noise_audios is None:
        augmented_noise_audios = get_augmented_noise_audios(mixdb)

    target_file_index = mrecord.target_file_index
    target_augmentation_index = mrecord.target_augmentation_index
    if len(target_file_index) != len(target_augmentation_index):
        raise SonusAIError('target_file_index and target_augmentation_index are not the same length')

    fg = FeatureGenerator(feature_mode=mixdb.feature)
    if mrecord.samples % fg.ftransform_R != 0:
        raise SonusAIError(f'Number of samples in mixture is not a multiple of {fg.ftransform_R}')

    targets = []
    for idx in range(len(target_file_index)):
        target_augmentation = mixdb.target_augmentations[target_augmentation_index[idx]]

        target = apply_augmentation(audio_in=raw_target_audios[target_file_index[idx]],
                                    augmentation=target_augmentation,
                                    length_common_denominator=mixdb.feature_step_samples)

        target = pad_to_samples(audio_in=target, samples=mrecord.samples)
        targets.append(target)

    noise = augmented_noise_audios[mrecord.noise_file_index][mrecord.noise_augmentation_index]
    noise, _ = get_next_noise(offset_in=mrecord.noise_offset,
                              length=mrecord.samples,
                              audio_in=noise)

    return apply_snr_gain(mrecord=mrecord, targets=targets, noise=noise)


def get_audio_data(mixdb: MixtureDatabase,
                   mrecord: MRecord,
                   raw_target_audios: AudiosT = None,
                   augmented_noise_audios: ListAudiosT = None,
                   compute_truth: bool = True,
                   compute_segsnr: bool = False,
                   frame_based_segsnr: bool = False) -> AudioData:
    from sonusai.mixture import generate_segsnr
    from sonusai.mixture import generate_truth

    targets, noise = get_target_noise_audio(mixdb=mixdb,
                                            mrecord=mrecord,
                                            raw_target_audios=raw_target_audios,
                                            augmented_noise_audios=augmented_noise_audios)

    truth_t = generate_truth(mixdb=mixdb,
                             mrecord=mrecord,
                             target_audios=targets,
                             noise_audio=noise,
                             compute=compute_truth)

    target = sum(targets)

    segsnr_t = generate_segsnr(mixdb=mixdb,
                               mrecord=mrecord,
                               target_audio=target,
                               noise_audio=noise,
                               compute=compute_segsnr,
                               frame_based=frame_based_segsnr)

    mixture = target + noise
    return AudioData(mixture=mixture,
                     targets=targets,
                     noise=noise,
                     truth_t=truth_t,
                     segsnr_t=segsnr_t)


def concatenate_audio_data(results: List[AudioData]) -> AudioData:
    mixture = np.concatenate([results[i].mixture for i in range(len(results))])

    if any(result.truth_t is None for result in results):
        truth_t = None
    else:
        truth_t = np.concatenate([results[i].truth_t for i in range(len(results))])

    targets = [
        np.concatenate([results[i].targets[j] for i in range(len(results))]) for j in range(len(results[0].targets))]

    noise = np.concatenate([results[i].noise for i in range(len(results))])

    if any(result.segsnr_t is None for result in results):
        segsnr_t = None
    else:
        segsnr_t = np.concatenate([results[i].segsnr_t for i in range(len(results))])

    return AudioData(mixture=mixture,
                     targets=targets,
                     noise=noise,
                     truth_t=truth_t,
                     segsnr_t=segsnr_t)


def get_next_noise(offset_in: int, length: int, audio_in: AudioT) -> (AudioT, int):
    audio_out = np.take(audio_in, range(offset_in, offset_in + length), mode='wrap')
    offset_out = (offset_in + length) % len(audio_in)
    return audio_out, offset_out


def read_audio(name: str) -> AudioT:
    import sox

    from sonusai import SonusAIError
    from sonusai import logger
    from sonusai.mixture import tokenized_expandvars
    from sonusai.mixture import BIT_DEPTH
    from sonusai.mixture import CHANNEL_COUNT
    from sonusai.mixture import SAMPLE_RATE

    expanded_name, _ = tokenized_expandvars(name)

    try:
        # Read in and convert to desired format
        inp = sox.Transformer()
        inp.set_output_format(rate=SAMPLE_RATE, bits=BIT_DEPTH, channels=CHANNEL_COUNT)
        return inp.build_array(input_filepath=expanded_name,
                               sample_rate_in=int(sox.file_info.sample_rate(expanded_name)))

    except Exception as e:
        if name != expanded_name:
            logger.error(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')


def get_mixture_data_deprecated(mixdb: MixtureDatabase,
                                mrecord: MRecord) -> (AudioT,
                                                      List[Union[np.ndarray, None]],
                                                      AudioT,
                                                      Feature,
                                                      Truth):
    """Get mixture data assuming nothing has been loaded into memory already."""
    from sonusai.mixture import apply_augmentation
    from sonusai.mixture import generate_truth
    from sonusai.mixture import get_feature_data
    from sonusai.mixture import get_truth_indices_for_target
    from sonusai.mixture import pad_to_samples

    target_audios = []
    target_truth_indices = []
    for idx in range(len(mrecord.target_file_index)):
        target_name = mixdb.targets[mrecord.target_file_index[idx]].name
        target_augmentation = mixdb.target_augmentations[mrecord.target_augmentation_index[idx]]

        target_audio = apply_augmentation(audio_in=read_audio(target_name),
                                          augmentation=target_augmentation,
                                          length_common_denominator=mixdb.feature_step_samples)

        target_audio = np.int16(np.round(np.float32(target_audio) * mrecord.target_snr_gain))
        target_audio = pad_to_samples(audio_in=target_audio, samples=mrecord.samples)
        target_audios.append(target_audio)
        target_truth_indices.append(get_truth_indices_for_target(mixdb.targets[mrecord.target_file_index[idx]]))

    augmented_noise_audios = get_augmented_noise_audios(mixdb=mixdb, show_progress=False)
    raw_noise_audio = augmented_noise_audios[mrecord.noise_file_index][mrecord.noise_augmentation_index]
    noise_audio, _ = get_next_noise(offset_in=mrecord.noise_offset,
                                    length=mrecord.samples,
                                    audio_in=raw_noise_audio)

    noise_audio = np.int16(np.round(np.float32(noise_audio) * mrecord.noise_snr_gain))

    truth_t = generate_truth(mixdb=mixdb,
                             mrecord=mrecord,
                             target_audios=target_audios,
                             noise_audio=noise_audio,
                             compute=True)

    mixture_audio = sum(target_audios) + noise_audio

    # Transform target_audios into a list num_classes long such that each entry is the target data per class
    class_audio = []
    for n in range(mixdb.num_classes):
        class_audio.append(None)
        for idx in range(len(target_audios)):
            if n + 1 in target_truth_indices[idx]:
                if class_audio[n] is None:
                    class_audio[n] = target_audios[idx]
                else:
                    class_audio[n] += target_audios[idx]

    feature, truth_f, _ = get_feature_data(mixdb=mixdb,
                                           mrecord=mrecord,
                                           mixture=mixture_audio,
                                           truth_t=truth_t)

    return mixture_audio, class_audio, noise_audio, feature, truth_f


def calculate_transform_from_audio(audio: AudioT, transform: ForwardTransform) -> AudioF:
    """
    Apply forward transform to input audio data [samples] to generate transform data [frames, bins].
    """
    return transform.execute_all(audio).transpose()


def calculate_audio_from_transform(data: AudioF, transform: InverseTransform, trim: bool = True) -> AudioT:
    """
    Apply inverse transform to input transform data [frames, bins] to generate audio data [samples].
    Trim mode removes starting samples so output waveform will be time-aligned with
    input waveform to the transform.
    """
    audio = transform.execute_all(data.transpose())
    if trim:
        audio = audio[transform.N - transform.R:]

    return audio


def add_audio_data_to_h5(file: str, data: AudioData, save_truth: bool = False, save_segsnr: bool = False) -> None:
    import h5py

    with h5py.File(file, 'a') as f:
        datasets = ['mixture', 'targets', 'noise']
        for dataset in datasets:
            if dataset in f:
                del f[dataset]

        f.create_dataset(name='mixture', data=data.mixture, dtype=np.int16)
        f.create_dataset(name='targets', data=data.targets, dtype=np.int16)
        f.create_dataset(name='noise', data=data.noise, dtype=np.int16)

        if save_truth:
            if 'truth_t' in f:
                del f['truth_t']
            f.create_dataset(name='truth_t', data=data.truth_t, dtype=np.float32)

        if save_segsnr:
            if 'segsnr_t' in f:
                del f['segsnr_t']
            f.create_dataset(name='segsnr_t', data=data.segsnr_t, dtype=np.float32)
