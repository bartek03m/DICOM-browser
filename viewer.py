import math
import tkinter as tk

import customtkinter as ctk
import numpy as np
from PIL import Image, ImageTk


class ImageViewer(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.image: np.ndarray | None = None  # 0-255 for display
        self.values: np.ndarray | None = None  # real pixel values
        self.photo: ImageTk.PhotoImage | None = None  # keep ref for Tk
        self.scale = 1.0  # zoom factor
        self.offset_x = 0.0  # image position on canvas
        self.offset_y = 0.0

        # last mouse position while dragging
        self.drag_x = 0
        self.drag_y = 0

        self.canvas.bind("<Configure>", lambda _: self.redraw())  # resize
        self.canvas.bind("<MouseWheel>", self.on_wheel)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)

    def show(self, image: np.ndarray, values: np.ndarray) -> None:
        self.image = image
        self.values = values
        self.redraw()

    def fit(self) -> None:
        if self.image is None:
            return
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        image_h, image_w = self.image.shape[:2]

        self.scale = min(canvas_w / image_w, canvas_h / image_h)  # fits
        # center
        self.offset_x = (canvas_w - image_w * self.scale) / 2
        self.offset_y = (canvas_h - image_h * self.scale) / 2
        self.redraw()

    def on_press(self, event: tk.Event) -> None:
        self.drag_x = event.x
        self.drag_y = event.y

    def on_drag(self, event: tk.Event) -> None:
        self.offset_x += event.x - self.drag_x
        self.offset_y += event.y - self.drag_y
        self.drag_x = event.x
        self.drag_y = event.y
        self.redraw()

    def on_wheel(self, event: tk.Event) -> None:
        if self.image is None:
            return

        # image point under cursor
        image_x = (event.x - self.offset_x) / self.scale
        image_y = (event.y - self.offset_y) / self.scale

        zoom = 1.2 if event.delta > 0 else 1 / 1.2  # 20% per step
        self.scale = max(0.1, min(self.scale * zoom, 64))  # zoom limits

        # keep that point under cursor
        self.offset_x = event.x - image_x * self.scale
        self.offset_y = event.y - image_y * self.scale
        self.redraw()

    def redraw(self) -> None:
        self.canvas.delete("all")
        if self.image is None:
            return
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        image_h, image_w = self.image.shape[:2]

        # visible pixel range
        x0 = max(0, math.floor(-self.offset_x / self.scale))
        x1 = min(image_w, math.ceil((canvas_w - self.offset_x) / self.scale))
        y0 = max(0, math.floor(-self.offset_y / self.scale))
        y1 = min(image_h, math.ceil((canvas_h - self.offset_y) / self.scale))
        if x1 <= x0 or y1 <= y0:
            return  # off screen

        # draw only the visible part
        crop = self.image[y0:y1, x0:x1]
        new_w = max(1, round((x1 - x0) * self.scale))
        new_h = max(1, round((y1 - y0) * self.scale))
        pil_image = Image.fromarray(crop).resize(
            (new_w, new_h), Image.Resampling.NEAREST  # sharp pixels
        )

        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(
            self.offset_x + x0 * self.scale,
            self.offset_y + y0 * self.scale,
            image=self.photo,
            anchor="nw",
        )
        self.draw_pixel_values(x0, x1, y0, y1)

    def draw_pixel_values(self, x0: int, x1: int, y0: int, y1: int) -> None:
        min_scale = 60 if self.image.ndim == 3 else 40  # RGB: 3 numbers
        if self.values is None or self.scale < min_scale:
            return

        for y in range(y0, y1):
            for x in range(x0, x1):
                bright = np.mean(self.image[y, x]) >= 128  # text contrast
                self.canvas.create_text(
                    self.offset_x + (x + 0.5) * self.scale,  # pixel center
                    self.offset_y + (y + 0.5) * self.scale,
                    text=pixel_text(self.values[y, x]),
                    fill="black" if bright else "white",
                )


def pixel_text(value: np.ndarray | float) -> str:
    if np.ndim(value) > 0:  # RGB: one line per channel
        return "\n".join(number_text(v) for v in value)
    return number_text(value)


def number_text(value: float) -> str:
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}"
