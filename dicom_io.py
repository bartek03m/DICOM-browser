from pathlib import Path

import numpy as np
import pydicom

from model import Slice


def sort_slices(slices: list[Slice]) -> None:
    # key: (0 = has InstanceNumber / 1 = missing, InstanceNumber,
    #       file name, frame)
    def key(slice_: Slice) -> tuple[int, int, str, int]:
        number = slice_.header.get("InstanceNumber")
        if number is None:
            return (1, 0, slice_.path.name, slice_.frame)
        return (0, int(number), slice_.path.name, slice_.frame)

    slices.sort(key=key)


def load_slices(dir_path: Path) -> list[Slice]:
    slices: list[Slice] = []
    for file in Path(dir_path).iterdir():
        if not file.is_file():
            continue
        slices.extend(load_file(file))
    sort_slices(slices)
    return slices


def load_file(file_path: Path) -> list[Slice]:
    try:
        header = pydicom.dcmread(file_path, stop_before_pixels=True)
    except Exception:
        return []

    if header.get("Rows") is None or header.get("Columns") is None:
        return []

    n_frames = int(getattr(header, "NumberOfFrames", 1))
    return [
        Slice(path=Path(file_path), header=header, frame=i)
        for i in range(n_frames)
    ]


def load_pixels(slice_: Slice) -> np.ndarray:
    ds = pydicom.dcmread(slice_.path)
    pixels = ds.pixel_array
    if int(getattr(slice_.header, "NumberOfFrames", 1)) > 1:
        return pixels[slice_.frame]
    return pixels
