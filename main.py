from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

from dicom_io import load_file, load_slices
from model import Slice


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # variables
        self.dir_path: Path | None = None
        self.single_file_path: Path | None = None
        self.ct_layers: list[Slice] = []

        # UI
        self.btn_open_dir = ctk.CTkButton(
            master=self,
            text="Wybierz folder z dysku",
            command=self.open_dir
        )
        self.btn_open_dir.pack()

        self.btn_open_file = ctk.CTkButton(
            master=self,
            text="Wybierz plik z dysku",
            command=self.open_file
        )
        self.btn_open_file.pack()

    # functions
    def open_dir(self) -> None:
        path = filedialog.askdirectory(title="Wybierz folder z badaniem")
        if not path:
            return
        self.dir_path = Path(path)
        self.ct_layers = load_slices(self.dir_path)

    def open_file(self) -> None:
        path = filedialog.askopenfilename(title="Wybierz plik z badaniem")
        if not path:
            return
        self.single_file_path = Path(path)
        self.ct_layers = load_file(self.single_file_path)


if __name__ == "__main__":
    app = App()
    app.mainloop()
