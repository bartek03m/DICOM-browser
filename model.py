from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

import pydicom

@dataclass
class Slice:
    path: Path
    header: pydicom.Dataset
    frame: int = 0

@dataclass
class MetaRow:
    tag: str
    name: str
    vr: str
    value: str
