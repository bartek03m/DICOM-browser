from pathlib import Path
import pydicom
from pydicom.errors import InvalidDicomError
from model import Slice


def load_slices(dir_path: Path) -> list[Slice]:
    slices = []
    for file in Path(dir_path).iterdir():
        if not file.is_file():
            continue
        slices.extend(load_file(file))
    return slices


def load_file(file_path: Path) -> list[Slice]:
    try:
        header = pydicom.dcmread(file_path, stop_before_pixels=True)
    except InvalidDicomError:
        return []
    n_frames = int(getattr(header, "NumberOfFrames", 1))
    return [Slice(path=Path(file_path), header=header, frame=i) for i in range(n_frames)]


def load_pixels(slice):
    ds = pydicom.dcmread(slice.path)
    pixels = ds.pixel_array
    if int(getattr(slice.header, "NumberOfFrames", 1)) > 1:
        return pixels[slice.frame]
    return pixels
