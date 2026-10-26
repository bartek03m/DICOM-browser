import numpy as np
from pydicom import Dataset
from pydicom.multival import MultiValue
from pydicom.pixels import apply_modality_lut


def to_modality(arr: np.ndarray, ds: Dataset) -> np.ndarray:
    return apply_modality_lut(arr, ds)  # slope and intercept


def first_value(value: MultiValue | float) -> float:
    if isinstance(value, MultiValue):  # several windows
        return float(value[0])
    return float(value)


def default_window(ds: Dataset, values: np.ndarray) -> tuple[float, float]:
    center = ds.get("WindowCenter")
    width = ds.get("WindowWidth")

    if center is not None and width is not None:
        center, width = first_value(center), first_value(width)
    elif ds.get("Modality") == "CT":
        return 40.0, 400.0  # soft tissue
    else:  # full range
        lo, hi = float(values.min()), float(values.max())
        center, width = (lo + hi) / 2, hi - lo

    return center, width or 1.0  # avoid division by zero


def apply_window(
    values: np.ndarray, center: float, width: float
) -> np.ndarray:
    lo, hi = center - width / 2, center + width / 2
    clipped = np.clip(values, lo, hi)  # cut to window
    scaled = (clipped - lo) / width * 255  # lo -> 0, hi -> 255
    return np.round(scaled).astype(np.uint8)


def to_display(
    values: np.ndarray, ds: Dataset, window: tuple[float, float]
) -> np.ndarray:
    img = apply_window(values, *window)
    if ds.get("PhotometricInterpretation") == "MONOCHROME1":
        return 255 - img  # invert
    return img
