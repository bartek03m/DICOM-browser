from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from dicom_io import load_file, load_pixels, load_slices
from imaging import default_window, to_display, to_modality
from model import Slice
from viewer import ImageViewer


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("1000x700")

        # variables
        self.ct_slices: list[Slice] = []
        self.index: int = 0

        # UI
        self.viewer = ImageViewer(self)
        self.viewer.pack(fill="both", expand=True)

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
        self.ct_slices = load_slices(Path(path))
        self.show_first_slice()

    def open_file(self) -> None:
        path = filedialog.askopenfilename(title="Wybierz plik z badaniem")
        if not path:
            return
        self.ct_slices = load_file(Path(path))
        self.show_first_slice()

    def show_first_slice(self) -> None:
        if not self.ct_slices:
            messagebox.showwarning(
                "Brak obrazów", "Nie znaleziono obrazów DICOM."
            )
            return
        self.show_slice(0)

    def show_slice(self, index: int) -> None:
        try:
            self.index = index
            slice_ = self.ct_slices[index]
            raw = load_pixels(slice_)
            values = to_modality(raw, slice_.header)
            window = default_window(slice_.header, values)
            self.viewer.show(to_display(values, slice_.header, window))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyświetlić obrazu:\n{e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
