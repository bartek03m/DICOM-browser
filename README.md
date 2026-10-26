# Przeglądarka DICOM

Prosta przeglądarka obrazów medycznych w formacie DICOM, napisana w Pythonie (pydicom + customtkinter).

- otwiera pojedynczy plik `.dcm` albo cały folder z badaniem (np. CT, jedna warstwa na plik),
- pozwala powiększać i przesuwać obraz,
- przy dużym powiększeniu wypisuje na każdym pikselu jego wartość (dla CT w jednostkach Hounsfielda),
- pozwala przewijać warstwy, zarówno z folderu, jak i z pliku wieloklatkowego,
- w panelu obok pokazuje wszystkie niepuste metadane z nagłówka.

## Uruchomienie

Potrzebny jest **Python 3.10 lub nowszy** (sprawdzone na 3.13). Program był pisany i testowany na Windowsie (patrz [Ograniczenia](#ograniczenia)).

```powershell
python -m venv .venv
.venv\Scripts\activate          # Linux / macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Pliki do testów

Folder `data/` nie jest w repozytorium. Przykładowe pliki DICOM udostępnia pydicom. Ta komenda wypisuje ścieżki do nich (`emri_small.dcm` pobiera się przy pierwszym uruchomieniu, więc potrzebny jest internet):

```powershell
python -c "from pydicom.data import get_testdata_file as f; print(f('CT_small.dcm')); print(f('emri_small.dcm')); print(f('MR_small.dcm'))"
```

| Plik | Co zawiera |
| --- | --- |
| `CT_small.dcm` | CT, wartości w HU, tagi binarne i sekwencja w nagłówku |
| `emri_small.dcm` | MR, 10 klatek w jednym pliku (przewijanie strzałkami) |
| `MR_small.dcm` | MR bez części tagów |

## Sterowanie

| Akcja | Jak |
| --- | --- |
| otwórz plik / folder | przyciski na górze okna |
| powiększ / pomniejsz | kółko myszy (względem kursora) |
| przesuń obraz | przeciąganie lewym przyciskiem myszy |
| dopasuj obraz do okna | `F` |
| następna / poprzednia warstwa | `↑` / `↓` |
| o 10 warstw dalej / wstecz | `PgUp` / `PgDn` |

Wartości pikseli pojawiają się, gdy jeden piksel obrazu zajmuje na ekranie co najmniej 40 px (60 px dla obrazów kolorowych, bo wypisywane są trzy liczby R, G, B).

## Jak to działa

**Wczytywanie** ([dicom_io.py](dicom_io.py))
- Z każdego pliku czytany jest najpierw sam nagłówek, bez pikseli. Pliki, które nie są DICOM-em albo nie zawierają obrazu, są pomijane.
- Każda klatka to osobny `Slice`. Plik wieloklatkowy i folder z wieloma plikami obsługuje więc ten sam kod.
- Warstwy są sortowane po `InstanceNumber`, a pliki bez tego tagu trafiają na koniec, posortowane po nazwie.
- Piksele są wczytywane dopiero przy wyświetlaniu danej warstwy.

**Od pikseli do obrazu** ([imaging.py](imaging.py))
1. **Modality LUT:** surowe liczby z pliku są przeliczane na wartości fizyczne (`RescaleSlope`, `RescaleIntercept`). Dla CT są to jednostki Hounsfielda. Te wartości trafiają na napisy na pikselach.
2. **Okno (window center / width):** wybrany zakres wartości jest rozciągany na skalę szarości 0–255. Okno jest brane z nagłówka. Jeśli go tam nie ma, dla CT używane jest okno tkanek miękkich (40 / 400), a dla innych badań pełny zakres wartości obrazu.
3. **MONOCHROME1:** w tym zapisie 0 oznacza biel, więc obraz jest odwracany.
4. Obrazy kolorowe (RGB) są wyświetlane bez zmian.

**Wyświetlanie** ([viewer.py](viewer.py))
- Przy powiększaniu skalowany jest tylko widoczny fragment obrazu. Dzięki temu duży zoom jest szybki i nie zużywa dużo pamięci.

**Metadane** ([metadata.py](metadata.py))
- Pokazywane są wszystkie niepuste tagi oprócz samych pikseli.
- Sekwencje i dane binarne są pokazywane jako rozmiar, np. `<dane binarne, bajtów: 128>`, zamiast ściany znaków.

## Struktura

```
main.py            okno aplikacji: przyciski, klawisze, przełączanie warstw
viewer.py          ImageViewer: płótno, zoom, przesuwanie, wartości pikseli
metadata_panel.py  MetadataPanel: tabela z metadanymi
dicom_io.py        wczytywanie pliku i folderu, sortowanie warstw, piksele
imaging.py         Modality LUT, okno, konwersja do 8 bitów
metadata.py        lista niepustych tagów z nagłówka
model.py           dataclassy Slice i MetaRow
```

Moduły `dicom_io.py`, `imaging.py`, `metadata.py` i `model.py` nie zależą od GUI, więc można ich używać i testować bez otwierania okna.

## Ograniczenia

- **Jedna seria na folder.** Wszystkie pliki z folderu trafiają do jednej listy, a podfoldery są pomijane. Folder z kilkoma seriami pokaże je przemieszane.
- **Brak grupy 0002 w metadanych.** Nagłówek pliku (`file_meta`, np. `Transfer Syntax UID`) nie jest pokazywany w tabeli.