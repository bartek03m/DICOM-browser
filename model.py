from dataclasses import dataclass
from pathlib import Path

from pydicom import Dataset


@dataclass
class Slice:
    path: Path
    header: Dataset  # without pixels
    frame: int = 0  # index in multi-frame file


@dataclass
class MetaRow:
    tag: str
    name: str
    vr: str
    value: str
