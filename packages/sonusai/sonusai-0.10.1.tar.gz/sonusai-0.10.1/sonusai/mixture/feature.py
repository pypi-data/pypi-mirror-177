from dataclasses import dataclass
from typing import List

import numpy as np

from sonusai.mixture.types import AudioT
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import AudiosT
from sonusai.mixture.types import Feature
from sonusai.mixture.types import FeatureData
from sonusai.mixture.types import ListAudiosT
from sonusai.mixture.types import Location
from sonusai.mixture.types import MRecord
from sonusai.mixture.types import MixtureDatabase
from sonusai.mixture.types import MixtureIDs
from sonusai.mixture.types import Segsnr
from sonusai.mixture.types import Truth


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class GlobalFeature:
    mixdb: MixtureDatabase = None
    location: str = None


mp_feature = GlobalFeature()


def get_feature_data(mixdb: MixtureDatabase,
                     mrecord: MRecord,
                     mixture: AudioT = None,
                     truth_t: Truth = None,
                     segsnr_t: Segsnr = None,
                     raw_target_audios: AudiosT = None,
                     augmented_noise_audios: ListAudiosT = None,
                     compute_truth: bool = True,
                     compute_segsnr: bool = False) -> FeatureData:
    from pyaaware import FeatureGenerator
    from pyaaware import ForwardTransform

    from sonusai import SonusAIError
    from sonusai.mixture import get_audio_data
    from sonusai.mixture import get_feature_frames_in_mrecord
    from sonusai.mixture import get_transform_frames_in_mrecord
    from sonusai.mixture import segsnr_sample_to_frame
    from sonusai.mixture import truth_reduction
    from sonusai.utils import int16_to_float

    segsnr = None
    if mixture is None or (compute_truth and truth_t is None) or (compute_segsnr and segsnr_t is None):
        audio_data = get_audio_data(mixdb=mixdb,
                                    mrecord=mrecord,
                                    raw_target_audios=raw_target_audios,
                                    augmented_noise_audios=augmented_noise_audios,
                                    compute_truth=compute_truth,
                                    compute_segsnr=compute_segsnr,
                                    frame_based_segsnr=True)
        mixture = audio_data.mixture
        truth_t = audio_data.truth_t
        segsnr = audio_data.segsnr_t
    elif compute_segsnr and segsnr_t is not None:
        segsnr = segsnr_sample_to_frame(mixdb, segsnr_t)

    if len(mixture) != mrecord.samples:
        raise SonusAIError(f'Wrong number of samples in mixture')

    fg = FeatureGenerator(feature_mode=mixdb.feature,
                          num_classes=mixdb.num_classes,
                          truth_mutex=mixdb.truth_mutex)

    fft = ForwardTransform(N=fg.ftransform_N, R=fg.ftransform_R, ttype=fg.ftransform_ttype)

    transform_frames = get_transform_frames_in_mrecord(mixdb, mrecord)
    feature_frames = get_feature_frames_in_mrecord(mixdb, mrecord)

    if truth_t is None:
        truth_t = np.zeros((mrecord.samples, mixdb.num_classes), dtype=np.float32)

    feature = np.empty((feature_frames, fg.stride, fg.num_bands), dtype=np.float32)
    truth_f = np.empty((feature_frames, mixdb.num_classes), dtype=np.complex64)

    feature_frame = 0
    for transform_frame in range(transform_frames):
        indices = slice(transform_frame * fg.ftransform_R,
                        (transform_frame + 1) * fg.ftransform_R)
        fd = fft.execute(int16_to_float(mixture[indices]))

        fg.execute(fd, truth_reduction(truth_t[indices], mixdb.truth_reduction_function))

        if fg.eof():
            feature[feature_frame] = fg.feature()
            truth_f[feature_frame] = fg.truth()
            feature_frame += 1

    if np.isreal(truth_f).all():
        truth_f = np.float32(np.real(truth_f))

    return FeatureData(feature=feature,
                       truth_f=truth_f,
                       segsnr=segsnr)


def concatenate_feature_data(results: List[FeatureData]) -> FeatureData:
    feature = np.concatenate([results[i].feature for i in range(len(results))])

    if any(result.truth_f is None for result in results):
        truth_f = None
    else:
        truth_f = np.concatenate([results[i].truth_f for i in range(len(results))])

    if any(result.segsnr is None for result in results):
        segsnr = None
    else:
        segsnr = np.concatenate([results[i].segsnr for i in range(len(results))])

    return FeatureData(feature=feature,
                       truth_f=truth_f,
                       segsnr=segsnr)


def _get_feature_data_from_dir_kernel(mixid: int) -> FeatureData:
    """Get feature/truth for a given mixid from a directory containing genft data"""
    from os.path import join

    import h5py

    with h5py.File(join(mp_feature.location, mp_feature.mixdb.mixtures[mixid].name), 'r') as f:
        feature = np.array(f['feature'])
        truth_f = np.array(f['truth_f'])
        if 'segsnr' in f:
            segsnr = np.array(f['segsnr'])
        else:
            segsnr = None

    return FeatureData(feature=feature,
                       truth_f=truth_f,
                       segsnr=segsnr)


def get_feature_data_from_dir(mixdb: MixtureDatabase,
                              location: Location,
                              mixids: MixtureIDs = None) -> FeatureData:
    """Get feature/truth for given mixids from a directory containing genft data"""
    from sonusai.mixture import convert_mixids_to_list
    from sonusai.utils import p_map

    mp_feature.mixdb = mixdb
    mp_feature.location = location
    mixids = convert_mixids_to_list(mixdb, mixids)
    results = p_map(_get_feature_data_from_dir_kernel, mixids)

    return concatenate_feature_data(results)


@dataclass(frozen=True)
class FeatureStats:
    feature_ms: float
    feature_samples: int
    feature_step_ms: float
    feature_step_samples: int
    num_bands: int
    stride: int
    step: int
    decimation: int


def get_feature_stats(feature: str, num_classes: int) -> FeatureStats:
    from pyaaware import FeatureGenerator

    import sonusai

    fg = FeatureGenerator(feature_mode=feature, num_classes=num_classes)

    transform_frame_ms = float(fg.ftransform_R) / float(sonusai.mixture.SAMPLE_RATE / 1000)

    return FeatureStats(feature_ms=transform_frame_ms * fg.decimation * fg.stride,
                        feature_samples=fg.ftransform_R * fg.decimation * fg.stride,
                        feature_step_ms=transform_frame_ms * fg.decimation * fg.step,
                        feature_step_samples=fg.ftransform_R * fg.decimation * fg.step,
                        num_bands=fg.num_bands,
                        stride=fg.stride,
                        step=fg.step,
                        decimation=fg.decimation)


def get_feature_from_audio(audio: AudioT, feature: str) -> Feature:
    from sonusai.mixture import get_pad_length
    from sonusai.mixture import MRecord

    fs = get_feature_stats(feature=feature, num_classes=1)
    audio = np.pad(array=audio, pad_width=(0, get_pad_length(len(audio), fs.feature_step_samples)))

    mixdb = MixtureDatabase(feature=feature,
                            mixtures=[MRecord(samples=len(audio))],
                            feature_samples=fs.feature_samples,
                            feature_step_samples=fs.feature_step_samples,
                            num_classes=1,
                            truth_mutex=False,
                            truth_reduction_function='max')
    return get_feature_data(mixdb=mixdb,
                            mrecord=mixdb.mixtures[0],
                            mixture=audio,
                            compute_truth=False).feature


def add_feature_data_to_h5(file: str, data: FeatureData, save_segsnr: bool = False) -> None:
    import h5py

    with h5py.File(file, 'a') as f:
        datasets = ['feature', 'truth_f']
        for dataset in datasets:
            if dataset in f:
                del f[dataset]

        f.create_dataset(name='feature', data=data.feature, dtype=np.float32)
        f.create_dataset(name='truth_f', data=data.truth_f, dtype=np.float32)

        if save_segsnr:
            if 'segsnr' in f:
                del f['segsnr']
            f.create_dataset(name='segsnr', data=data.segsnr, dtype=np.float32)
