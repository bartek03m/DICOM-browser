from dataclasses import dataclass
from pathlib import Path
import pydicom
from pydicom.errors import InvalidDicomError


@dataclass
class Slice:
    path: Path
    header: pydicom.Dataset
    frame: int = 0


@dataclass
class Series:
    uid: str
    description: str
    modality: str
    slices: list[Slice]


def load_slices(dir_path: Path) -> list[Slice]:
    slices = []
    for file in Path(dir_path).iterdir():
        if not file.is_file():
            continue
        try:
            header = pydicom.dcmread(file, stop_before_pixels=True)
        except InvalidDicomError:
            continue
        slices.append(Slice(path=file, header=header))
    return slices


def load_file(file_path: Path) -> list[Slice]:
    """Read one DICOM file; multi-frame files give one Slice per frame."""
    try:
        header = pydicom.dcmread(file_path, stop_before_pixels=True)
    except InvalidDicomError:
        return []
    n_frames = int(getattr(header, "NumberOfFrames", 1))
    return [Slice(path=Path(file_path), header=header, frame=i) for i in range(n_frames)]
