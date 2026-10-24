import numpy as np
from pydicom import Dataset
from pydicom.multival import MultiValue
from pydicom.pixels import apply_modality_lut


def to_modality(arr: np.ndarray, ds: Dataset) -> np.ndarray:
    return apply_modality_lut(arr, ds)


def first_value(value: MultiValue | float) -> float:
    if isinstance(value, MultiValue):
        return float(value[0])
    return float(value)


def default_window(ds: Dataset, values: np.ndarray) -> tuple[float, float]:
    window_center = ds.get("WindowCenter")
    window_width = ds.get("WindowWidth")

    if window_center is None or window_width is None:
        lo = float(values.min())
        hi = float(values.max())
        center = (lo + hi) / 2
        width = hi - lo
        if width == 0:
            width = 1.0
        return center, width

    center = first_value(window_center)
    width = first_value(window_width)
    if width == 0:
        width = 1.0
    return center, width


def apply_window(values: np.ndarray, center: float, width: float) -> np.ndarray:
    lo = center - width / 2
    hi = center + width / 2
    clipped = np.clip(values, lo, hi)
    scaled = (clipped - lo) / (hi - lo) * 255  # lo -> 0, hi -> 255
    return np.round(scaled).astype(np.uint8)


def to_display(values: np.ndarray, ds: Dataset, window: tuple[float, float]) -> np.ndarray:
    img = apply_window(values, *window)
    if ds.get("PhotometricInterpretation") == "MONOCHROME1":
        return 255 - img
    return img
