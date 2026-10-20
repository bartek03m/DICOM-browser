import pydicom
import customtkinter as ctk
from tkinter import filedialog
import cv2
from pathlib import Path


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # variables
        self.dir_path = ''
        self.ct_layers = []

        # UI
        self.button = ctk.CTkButton(
            master=self,
            text="Wybierz plik z dysku",
            command=self.get_dir
        )
        self.button.pack()

        self.button2 = ctk.CTkButton(
            master=self,
            text="Wyswietl pliki",
            command=self.get_layers
        )
        self.button2.pack()

    # functions
    def get_dir(self):
        self.dir_path = Path(filedialog.askdirectory(title="Wybierz folder z badaniem"))

    def get_layers(self):
        self.ct_layers = []
        for file in self.dir_path.iterdir():
            if file.is_file():
                try:
                    ds = pydicom.dcmread(file, stop_before_pixels=True)
                    self.ct_layers.append(file)
                    print(f"{file} \n\n")
                except pydicom.errors.InvalidDicomError:
                    continue


if __name__ == "__main__":
    app = App()
    app.mainloop()
