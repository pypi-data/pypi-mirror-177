from dataclasses import dataclass
from os import PathLike
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import numpy.typing as npt
from dataclasses_json import DataClassJsonMixin

AudioT = npt.NDArray[np.int16]
AudiosT = List[AudioT]

ListAudiosT = List[List[AudioT]]

Truth = npt.NDArray[np.float32]
Segsnr = npt.NDArray[np.float32]

AudioF = npt.NDArray[np.complex64]
AudiosF = List[AudioF]

Feature = npt.NDArray[np.float32]

Predict = npt.NDArray[np.float32]

Location = Union[str, bytes, PathLike]


class DataClassSonusAIMixin(DataClassJsonMixin):
    from typing import Dict
    from typing import Union

    # Json type defined to maintain compatibility with DataClassJsonMixin
    Json = Union[dict, list, str, int, float, bool, None]

    def __str__(self):
        return f'{self.to_dict()}'

    # Override DataClassJsonMixin to remove dictionary keys with values of None
    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        def del_none(d):
            if isinstance(d, dict):
                for key, value in list(d.items()):
                    if value is None:
                        del d[key]
                    elif isinstance(value, dict):
                        del_none(value)
                    elif isinstance(value, list):
                        for item in value:
                            del_none(item)
            elif isinstance(d, list):
                for item in d:
                    del_none(item)
            return d

        return del_none(super().to_dict(encode_json))


@dataclass(frozen=True)
class TruthSetting(DataClassSonusAIMixin):
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


TruthSettings = List[TruthSetting]
OptionalNumberStr = Optional[Union[float, int, str]]
OptionalListNumberStr = Optional[List[Union[float, int, str]]]


@dataclass
class Augmentation(DataClassSonusAIMixin):
    normalize: OptionalNumberStr = None
    pitch: OptionalNumberStr = None
    tempo: OptionalNumberStr = None
    gain: OptionalNumberStr = None
    eq1: OptionalListNumberStr = None
    eq2: OptionalListNumberStr = None
    eq3: OptionalListNumberStr = None
    lpf: OptionalNumberStr = None
    count: Optional[int] = None
    mixup: Optional[int] = 1


Augmentations = List[Augmentation]


@dataclass(frozen=True)
class TargetFile(DataClassSonusAIMixin):
    duration: float
    name: str
    truth_settings: TruthSettings
    augmentations: Optional[Augmentations] = None
    class_balancing_augmentation: Optional[Augmentation] = None


TargetFiles = List[TargetFile]


@dataclass
class AugmentedTarget(DataClassSonusAIMixin):
    target_augmentation_index: int
    target_file_index: int


AugmentedTargets = List[AugmentedTarget]


@dataclass(frozen=True)
class NoiseFile(DataClassSonusAIMixin):
    name: str
    duration: float
    augmentations: Optional[Augmentations] = None


NoiseFiles = List[NoiseFile]
ClassCount = List[int]


@dataclass
class MRecord(DataClassSonusAIMixin):
    name: str = None
    noise_augmentation_index: int = None
    noise_file_index: int = None
    noise_offset: int = None
    noise_snr_gain: float = None
    random_snr: Optional[bool] = None
    samples: int = None
    snr: float = None
    target_augmentation_index: List[int] = None
    target_file_index: List[int] = None
    target_gain: List[int] = None
    target_snr_gain: float = None


MRecords = List[MRecord]
MixtureIDs = Union[str, int, List[int], range]


@dataclass
class MixtureDatabase(DataClassSonusAIMixin):
    class_balancing: Optional[bool] = False
    class_balancing_augmentation: Optional[Augmentation] = None
    class_labels: List[str] = None
    class_weights_threshold: List[float] = None
    exhaustive_noise: Optional[bool] = True
    feature: str = None
    feature_samples: int = None
    feature_step_samples: int = None
    first_cba_index: Optional[int] = None
    mixtures: MRecords = None
    noise_augmentations: Augmentations = None
    noises: NoiseFiles = None
    num_classes: int = None
    random_snrs: Optional[List[str]] = None
    seed: Optional[int] = 0
    snrs: List[float] = None
    target_augmentations: Augmentations = None
    targets: TargetFiles = None
    truth_mutex: bool = None
    truth_reduction_function: str = None
    truth_settings: TruthSettings = None


@dataclass(frozen=True)
class TruthFunctionConfig(DataClassSonusAIMixin):
    feature: str
    mutex: bool
    num_classes: int
    target_gain: float
    config: Optional[dict] = None
    function: Optional[str] = None
    index: Optional[List[int]] = None


@dataclass
class AudioData:
    mixture: AudioT
    targets: AudiosT
    noise: AudioT
    truth_t: Optional[Truth] = None
    segsnr_t: Optional[Segsnr] = None


@dataclass
class FeatureData:
    feature: Feature
    truth_f: Truth
    segsnr: Segsnr
