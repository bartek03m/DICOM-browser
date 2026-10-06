import pydicom
import customtkinter as ctk
from tkinter import filedialog
import cv2


dir_path = ''

def open_dir():
    global dir_path
    dir_path=filedialog.askdirectory(title="Wybierz folder z badaniem")
    
def print_dir():
    print(dir_path)

app=ctk.CTk()

button=ctk.CTkButton(
    master=app, 
    text="Wybierz plik z dysku", 
    command=open_dir
)
button.pack()

button2=ctk.CTkButton(
  master=app,
  text="Sprawdź aktualną ścieżkę",
  command=print_dir
)
button2.pack()


app.mainloop()