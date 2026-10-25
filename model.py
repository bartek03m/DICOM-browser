from dataclasses import dataclass
from pathlib import Path

import pydicom


@dataclass
class Slice:
    path: Path
    header: pydicom.Dataset
    frame: int = 0
