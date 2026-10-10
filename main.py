import pydicom
import customtkinter as ctk
from tkinter import filedialog
import cv2
from pathlib import Path

# variables
dir_path = ''
ct_layers = []


# functions
def get_dir():
    global dir_path
    dir_path=Path(filedialog.askdirectory(title="Wybierz folder z badaniem"))

def get_layers():
    global ct_layers
    for file in dir_path.iterdir():
        if file.is_file():
            try:
                ds = pydicom.dcmread(file, stop_before_pixels=True)
                ct_layers.append(file)
                print(f"{file} \n\n")  
            except('Wyjątek, że się nie udało pobrac DICOM\'a'):
                continue
    
    
# UI
app=ctk.CTk()

button=ctk.CTkButton(
    master=app, 
    text="Wybierz plik z dysku", 
    command=get_dir
)
button.pack()

button2=ctk.CTkButton(
    master=app, 
    text="Wyswietl pliki", 
    command=get_layers
)
button2.pack()

app.mainloop()