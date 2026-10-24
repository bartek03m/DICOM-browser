import tkinter as tk

import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk


class ImageViewer(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.photo: ImageTk.PhotoImage | None = None

    def show(self, image: np.ndarray) -> None:
        pil_image = Image.fromarray(image)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
