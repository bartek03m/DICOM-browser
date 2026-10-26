# DICOM Browser

A simple viewer for medical images in the DICOM format, written in Python (pydicom + customtkinter).

- opens a single `.dcm` file or a whole study folder (e.g. CT, one slice per file),
- lets you zoom and pan the image,
- at high zoom, prints each pixel's value on the pixel itself (in Hounsfield units for CT),
- lets you scroll through slices, both from a folder and from a multi-frame file,
- shows all non-empty header metadata in a side panel.

## Running

You need **Python 3.10 or newer** (tested on 3.13). The program was written and tested on Windows (see [Limitations](#limitations)).

```powershell
python -m venv .venv
.venv\Scripts\activate          # Linux / macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Test files

The `data/` folder is not in the repository. pydicom ships sample DICOM files. This command prints their paths (`emri_small.dcm` is downloaded on first run, so you need an internet connection):

```powershell
python -c "from pydicom.data import get_testdata_file as f; print(f('CT_small.dcm')); print(f('emri_small.dcm')); print(f('MR_small.dcm'))"
```

| File | Contents |
| --- | --- |
| `CT_small.dcm` | CT, values in HU, binary tags and a sequence in the header |
| `emri_small.dcm` | MR, 10 frames in one file (scroll with the arrow keys) |
| `MR_small.dcm` | MR with some tags missing |

## Controls

| Action | How |
| --- | --- |
| open file / folder | `Wybierz plik z dysku` / `Wybierz folder z dysku` buttons at the top of the window |
| zoom in / out | mouse wheel (around the cursor) |
| pan the image | drag with the left mouse button |
| fit image to window | `F` |
| next / previous slice | `↑` / `↓` |
| 10 slices forward / back | `PgUp` / `PgDn` |

Pixel values appear when one image pixel takes up at least 40 px on screen (60 px for color images, because three numbers R, G, B are printed).

## How it works

**Loading** ([dicom_io.py](dicom_io.py))
- Only the header is read from each file first, without the pixels. Files that are not DICOM or contain no image are skipped.
- Each frame is a separate `Slice`, so a multi-frame file and a folder of many files are handled by the same code.
- Slices are sorted by `InstanceNumber`; files without this tag go to the end, sorted by name.
- Pixels are loaded only when a given slice is displayed.

**From pixels to image** ([imaging.py](imaging.py))
1. **Modality LUT:** raw numbers from the file are converted to physical values (`RescaleSlope`, `RescaleIntercept`). For CT these are Hounsfield units. These are the values printed on the pixels.
2. **Window (window center / width):** the chosen value range is stretched to the 0–255 grayscale. The window is taken from the header. If it is missing, CT uses a soft tissue window (40 / 400) and other modalities use the full value range of the image.
3. **MONOCHROME1:** in this encoding 0 means white, so the image is inverted.
4. Color (RGB) images are displayed unchanged.

**Display** ([viewer.py](viewer.py))
- When zooming, only the visible part of the image is scaled. This keeps high zoom fast and memory-light.

**Metadata** ([metadata.py](metadata.py))
- All non-empty tags except the pixel data are shown.
- Sequences and binary data are shown as their size, e.g. `<dane binarne, bajtów: 128>` ("binary data, bytes: 128"), instead of a wall of characters.

## Structure

```
main.py            application window: buttons, keys, slice switching
viewer.py          ImageViewer: canvas, zoom, panning, pixel values
metadata_panel.py  MetadataPanel: metadata table
dicom_io.py        loading a file and a folder, sorting slices, pixels
imaging.py         Modality LUT, windowing, conversion to 8 bits
metadata.py        list of non-empty header tags
model.py           Slice and MetaRow dataclasses
```

The `dicom_io.py`, `imaging.py`, `metadata.py` and `model.py` modules do not depend on the GUI, so they can be used and tested without opening a window.

## Limitations

- **One series per folder.** All files in a folder go into one list, and subfolders are skipped. A folder with several series will show them mixed together.
- **No group 0002 in metadata.** The file meta header (`file_meta`, e.g. `Transfer Syntax UID`) is not shown in the table.

## License

[MIT](LICENSE)
