from tkinter import filedialog, messagebox

import customtkinter as ctk

from dicom_io import load_file, load_pixels, load_slices
from imaging import default_window, to_display, to_modality
from metadata_panel import MetadataPanel
from model import Slice
from viewer import ImageViewer


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Przeglądarka DICOM")
        self.geometry("1200x700")
        self.minsize(1000, 500)
        self.after(0, lambda: self.state("zoomed"))  # maximize
        # variables
        self.slices: list[Slice] = []
        self.index = 0

        # UI
        self.toolbar = ctk.CTkFrame(master=self)
        self.toolbar.pack(side="top", fill="x")

        buttons = ctk.CTkFrame(master=self.toolbar, fg_color="transparent")
        buttons.pack()

        self.btn_open_dir = ctk.CTkButton(
            master=buttons,
            text="Wybierz folder z dysku",
            command=self.open_dir,
        )
        self.btn_open_dir.pack(side="left", padx=5, pady=5)

        self.btn_open_file = ctk.CTkButton(
            master=buttons,
            text="Wybierz plik z dysku",
            command=self.open_file,
        )
        self.btn_open_file.pack(side="left", padx=5, pady=5)

        self.meta_panel = MetadataPanel(master=self)
        self.meta_panel.pack(side="right", fill="y")

        self.viewer = ImageViewer(master=self)
        self.viewer.pack(fill="both", expand=True)

        # keys
        self.bind("<Up>", lambda _: self.step(1))
        self.bind("<Down>", lambda _: self.step(-1))
        self.bind("<Prior>", lambda _: self.step(10))  # Page Up
        self.bind("<Next>", lambda _: self.step(-10))  # Page Down
        self.bind("<f>", lambda _: self.viewer.fit())

    # functions
    def open_dir(self) -> None:
        path = filedialog.askdirectory(title="Wybierz folder z badaniem")
        if not path:
            return
        self.slices = load_slices(path)
        self.show_first_slice()

    def open_file(self) -> None:
        path = filedialog.askopenfilename(title="Wybierz plik z badaniem")
        if not path:
            return
        self.slices = load_file(path)
        self.show_first_slice()

    def show_first_slice(self) -> None:
        if not self.slices:
            messagebox.showwarning(
                "Brak obrazów", "Nie znaleziono obrazów DICOM."
            )
            return
        self.show_slice(0)
        self.viewer.fit()

    def show_slice(self, index: int) -> None:
        try:
            self.index = index
            slice_ = self.slices[index]
            self.meta_panel.show(slice_.header)
            raw = load_pixels(slice_)
            if slice_.header.get("SamplesPerPixel", 1) > 1:
                self.viewer.show(raw, raw)  # RGB: no windowing
                return
            values = to_modality(raw, slice_.header)  # HU for CT
            window = default_window(slice_.header, values)
            image = to_display(values, slice_.header, window)  # 0-255
            self.viewer.show(image, values)  # values for labels
        except Exception as e:  # keep app running
            messagebox.showerror(
                "Błąd", f"Nie udało się wyświetlić obrazu:\n{e}"
            )

    def step(self, delta: int) -> None:
        if not self.slices:
            return
        last = len(self.slices) - 1
        new_index = max(0, min(self.index + delta, last))  # stay in range
        if new_index != self.index:
            self.show_slice(new_index)


if __name__ == "__main__":
    app = App()
    app.mainloop()
