from dataclasses import dataclass
from os import PathLike
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from sonusai.mixture.dataclasses_sonusai import DataClassSonusAIMixin

Location = Union[str, bytes, PathLike]


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
class TargetMetadata(DataClassSonusAIMixin):
    augmentation: Augmentation
    gain: float
    name: str
    truth_settings: TruthSettings


@dataclass
class NoiseMetadata(DataClassSonusAIMixin):
    augmentation: Augmentation
    name: str
    offset: int


@dataclass
class MixtureMetadata(DataClassSonusAIMixin):
    class_labels: List[str]
    feature: str
    feature_samples: int
    feature_step_samples: int
    noise: NoiseMetadata
    noise_snr_gain: float
    num_classes: int
    random_snr: bool
    samples: int
    snr: float
    target_snr_gain: float
    targets: List[TargetMetadata]
    truth_mutex: bool
    truth_reduction_function: str

    def __str__(self):
        metadata = ''
        for ti in range(len(self.targets)):
            metadata += f'target {ti} name: {self.targets[ti].name}\n'
            metadata += f'target {ti} augmentation: {self.targets[ti].augmentation.to_dict()}\n'
            metadata += f'target {ti} target_gain: {self.targets[ti].gain}\n'
            ts = self.targets[ti].truth_settings
            for tsi in range(len(ts)):
                metadata += f'target {ti} truth index {tsi}: {ts[tsi].index}\n'
        metadata += f'noise name: {self.noise.name}\n'
        metadata += f'noise augmentation: {self.noise.augmentation.to_dict()}\n'
        metadata += f'snr: {self.snr}\n'
        metadata += f'random_snr: {self.random_snr}\n'
        metadata += f'samples: {self.samples}\n'
        metadata += f'target_snr_gain: {self.target_snr_gain}\n'
        metadata += f'noise_snr_gain: {self.noise_snr_gain}\n'

        return metadata


def load_mixdb(location: Location) -> MixtureDatabase:
    import json

    from os.path import exists
    from os.path import join
    from os.path import isdir

    from sonusai import SonusAIError

    if not isdir(location):
        raise SonusAIError(f'{location} is not a directory')

    filename = join(location, 'mixdb.json')
    if not exists(filename):
        raise SonusAIError(f'Could not find mixture database in {location}')

    with open(file=filename, mode='r', encoding='utf-8') as f:
        return MixtureDatabase.from_dict(json.loads(f.read()))


def get_samples_in_mixid(mixdb: MixtureDatabase, mixid: int) -> int:
    return mixdb.mixtures[mixid].samples


def get_transform_frames_in_mrecord(mixdb: MixtureDatabase, mrecord: MRecord) -> int:
    from pyaaware import FeatureGenerator

    fg = FeatureGenerator(feature_mode=mixdb.feature)
    return mrecord.samples // fg.ftransform_R


def get_feature_frames_in_mrecord(mixdb: MixtureDatabase, mrecord: MRecord) -> int:
    return mrecord.samples // mixdb.feature_step_samples


def get_class_weights_threshold(mixdb: Union[MixtureDatabase, Dict]) -> List[float]:
    """Get the class_weights_threshold from a mixture database or a config."""

    from sonusai import SonusAIError

    if isinstance(mixdb, dict):
        class_weights_threshold = mixdb['class_weights_threshold']
        num_classes = mixdb['num_classes']
    else:
        class_weights_threshold = mixdb.class_weights_threshold
        num_classes = mixdb.num_classes

    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold] * num_classes

    if len(class_weights_threshold) != num_classes:
        raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')

    return class_weights_threshold


def new_mixdb_from_mixids(mixdb: MixtureDatabase, mixids: MixtureIDs) -> MixtureDatabase:
    from copy import deepcopy

    from sonusai import SonusAIError

    mixdb_out = deepcopy(mixdb)
    mixdb_out.mixtures = get_mrecords_from_mixids(mixdb_out, mixids)

    if not mixdb_out.mixtures:
        raise SonusAIError(f'Error processing mixid: {mixids}; resulted in empty list of mixtures')

    return mixdb_out


def convert_mixids_to_list(mixdb: MixtureDatabase, mixids: MixtureIDs = None) -> List[int]:
    from sonusai import SonusAIError

    result = mixids
    all_mixids = list(range(len(mixdb.mixtures)))

    if result is None:
        result = all_mixids

    if isinstance(result, str):
        if result == '*':
            result = all_mixids
        else:
            try:
                result = eval(f'{all_mixids}[{result}]')
            except NameError:
                result = []

    if isinstance(result, range):
        result = list(result)

    if isinstance(result, int):
        result = [result]

    if not all(isinstance(x, int) and 0 <= x < len(mixdb.mixtures) for x in result):
        raise SonusAIError(f'Invalid entries in mixids of {mixids}')

    if not result:
        raise SonusAIError(f'Empty mixids {mixids}')

    return result


def get_mrecords_from_mixids(mixdb: MixtureDatabase, mixids: MixtureIDs = None) -> MRecords:
    from copy import deepcopy

    return [deepcopy(mixdb.mixtures[i]) for i in convert_mixids_to_list(mixdb, mixids)]


def evaluate_random_rule(rule: str) -> Union[str, float]:
    """Evaluate 'rand' directive."""
    import re
    from random import uniform

    from sonusai.mixture import RAND_PATTERN

    def rand_repl(m):
        return f'{uniform(float(m.group(1)), float(m.group(4))):.2f}'

    return eval(re.sub(RAND_PATTERN, rand_repl, rule))


def get_mixture_filename(mixid: int, padding: int) -> str:
    return f'{mixid:0{padding}}.h5'


def get_mixture_metadata(mixdb: MixtureDatabase, mixid: int) -> str:
    mrecord = mixdb.mixtures[mixid]
    metadata = ''
    for ti in range(len(mrecord.target_file_index)):
        tfi = mrecord.target_file_index[ti]
        tai = mrecord.target_augmentation_index[ti]
        metadata += f'target {ti} name: {mixdb.targets[tfi].name}\n'
        metadata += f'target {ti} augmentation: {mixdb.target_augmentations[tai].to_dict()}\n'
        metadata += f'target {ti} target_gain: {mrecord.target_gain[ti]}\n'
        truth_settings = mixdb.targets[tfi].truth_settings
        for tsi in range(len(truth_settings)):
            metadata += f'target {ti} truth index {tsi}: {truth_settings[tsi].index}\n'
            metadata += f'target {ti} truth function {tsi}: {truth_settings[tsi].function}\n'
            metadata += f'target {ti} truth config {tsi}: {truth_settings[tsi].config}\n'
    metadata += f'noise name: {mixdb.noises[mrecord.noise_file_index].name}\n'
    metadata += f'noise augmentation: {mixdb.noise_augmentations[mrecord.noise_augmentation_index].to_dict()}\n'
    metadata += f'snr: {mrecord.snr}\n'
    metadata += f'random_snr: {mrecord.random_snr}\n'
    metadata += f'samples: {mrecord.samples}\n'
    metadata += f'target_snr_gain: {mrecord.target_snr_gain}\n'
    metadata += f'noise_snr_gain: {mrecord.noise_snr_gain}\n'

    return metadata
