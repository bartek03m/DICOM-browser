from pathlib import Path

import numpy as np
import pydicom

from model import Slice


def number_of_frames(header: pydicom.Dataset) -> int:
    return int(header.get("NumberOfFrames") or 1)


def sort_slices(slices: list[Slice]) -> None:  # in place
    # key: (0 = has InstanceNumber / 1 = missing)
    def key(slice_: Slice) -> tuple[bool, int, str, int]:
        number = slice_.header.get("InstanceNumber")
        return (
            number is None, int(number or 0), slice_.path.name, slice_.frame
        )

    slices.sort(key=key)


def load_file(file_path: str | Path) -> list[Slice]:
    try:
        # header only, faster
        header = pydicom.dcmread(file_path, stop_before_pixels=True)
    except Exception:  # not DICOM
        return []

    if header.get("Rows") is None or header.get("Columns") is None:
        return []  # no image

    path = Path(file_path)
    return [
        Slice(path=path, header=header, frame=i)
        for i in range(number_of_frames(header))
    ]


def load_slices(dir_path: str | Path) -> list[Slice]:
    slices: list[Slice] = []
    for file in Path(dir_path).iterdir():
        if file.is_file():
            slices.extend(load_file(file))
    sort_slices(slices)
    return slices


def load_pixels(slice_: Slice) -> np.ndarray:
    pixels = pydicom.dcmread(slice_.path).pixel_array
    if number_of_frames(slice_.header) > 1:
        return pixels[slice_.frame]  # one frame
    return pixels
