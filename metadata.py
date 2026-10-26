from pydicom import Dataset

from model import MetaRow

def extract_metadata(ds: Dataset) -> list[MetaRow]:
    rows = []
    for elem in ds:
        if elem.keyword == "PixelData" or (not elem.value and elem.value != 0): 
            continue
        row = MetaRow(tag=str(elem.tag), name=elem.name, vr=elem.VR, value=str(elem.value))
        rows.append(row)
    return rows