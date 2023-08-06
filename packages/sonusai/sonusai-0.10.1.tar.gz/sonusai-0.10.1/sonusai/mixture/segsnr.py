import numpy as np

from sonusai.mixture.types import AudioT
from sonusai.mixture.types import MRecord
from sonusai.mixture.types import MixtureDatabase
from sonusai.mixture.types import Segsnr


def generate_segsnr(mixdb: MixtureDatabase,
                    mrecord: MRecord,
                    target_audio: AudioT,
                    noise_audio: AudioT,
                    compute: bool = True,
                    frame_based: bool = False) -> Segsnr:
    """Generate segmental SNR."""
    from pyaaware import FeatureGenerator
    from pyaaware import ForwardTransform

    from sonusai.utils import int16_to_float

    if not compute:
        return np.empty(0, dtype=np.float32)

    fg = FeatureGenerator(feature_mode=mixdb.feature)
    fft = ForwardTransform(N=fg.ftransform_N, R=fg.ftransform_R, ttype=fg.ftransform_ttype)

    if frame_based:
        segsnr = np.empty(mrecord.samples // fg.ftransform_R, dtype=np.float32)
    else:
        segsnr = np.empty(mrecord.samples, dtype=np.float32)

    frame = 0
    for offset in range(0, mrecord.samples, fg.ftransform_R):
        indices = slice(offset, offset + fg.ftransform_R)

        target_energy = fft.energy_t(int16_to_float(target_audio[indices]))
        noise_energy = fft.energy_t(int16_to_float(noise_audio[indices]))

        if noise_energy == 0:
            snr = np.float32(np.inf)
        else:
            snr = np.float32(target_energy / noise_energy)

        if frame_based:
            segsnr[frame] = snr
            frame += 1
        else:
            segsnr[indices] = snr

    return segsnr


def segsnr_sample_to_frame(mixdb: MixtureDatabase, segsnr_t: Segsnr) -> Segsnr:
    from pyaaware import FeatureGenerator

    fg = FeatureGenerator(feature_mode=mixdb.feature)

    return segsnr_t[0::fg.ftransform_R]
