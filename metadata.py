from pydicom import DataElement, Dataset

from model import MetaRow

BINARY_VRS = {"OB", "OW", "OF", "OD", "OL", "OV", "UN"}  # shown as size only


def display_value(elem: DataElement) -> str:
    if elem.VR == "SQ":
        return f"<sekwencja, elementów: {len(elem.value)}>"
    if elem.VR in BINARY_VRS:
        return f"<dane binarne, bajtów: {len(elem.value)}>"
    return str(elem.value)


def extract_metadata(ds: Dataset) -> list[MetaRow]:
    return [
        MetaRow(
            tag=str(elem.tag),
            name=elem.name,
            vr=elem.VR,
            value=display_value(elem),
        )
        for elem in ds
        # skip pixels and empty, keep 0
        if elem.keyword != "PixelData" and (elem.value or elem.value == 0)
    ]
