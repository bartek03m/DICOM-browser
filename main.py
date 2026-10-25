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
        
        self.viewer = ImageViewer(self)
        self.viewer.pack(fill="both", expand=True)

        # keys
        self.bind("<Up>", lambda e: self.step(1))
        self.bind("<Down>", lambda e: self.step(-1))
        self.bind("<Prior>", lambda e: self.step(10))
        self.bind("<Next>", lambda e: self.step(-10))
        self.bind("<f>", lambda e: self.viewer.fit())

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
        self.viewer.fit()

    def show_slice(self, index: int) -> None:
        try:
            self.index = index
            slice_ = self.ct_slices[index]
            raw = load_pixels(slice_)
            if slice_.header.get("SamplesPerPixel", 1) > 1:
                self.viewer.show(raw)
                return
            values = to_modality(raw, slice_.header)
            window = default_window(slice_.header, values)
            self.viewer.show(to_display(values, slice_.header, window))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyświetlić obrazu:\n{e}")

    def step(self, delta: int) -> None:
        if not self.ct_slices:
            return
        last = len(self.ct_slices) - 1
        new_index = max(0, min(self.index + delta, last))
        if new_index != self.index:
            self.show_slice(new_index)


if __name__ == "__main__":
    app = App()
    app.mainloop()
