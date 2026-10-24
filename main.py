import customtkinter as ctk
from tkinter import filedialog
import cv2
from pathlib import Path

from dicom_io import load_slices, load_file

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # variables
        self.dir_path = ''
        self.single_file_path = ''
        self.ct_layers = []

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
    def open_dir(self):
        path = filedialog.askdirectory(title="Wybierz folder z badaniem")
        if not path:
            return
        self.dir_path = Path(path)
        self.ct_layers = load_slices(self.dir_path)

    def open_file(self):
        path = filedialog.askopenfilename(title="Wybierz plik z badaniem")
        if not path:
            return
        self.single_file_path = Path(path)
        self.ct_layers = load_file(self.single_file_path)




if __name__ == "__main__":
    app = App()
    app.mainloop()
