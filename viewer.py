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
        self.photo: ImageTk.PhotoImage | None = None

        self.image: np.ndarray | None = None
        self.values: np.ndarray | None = None
        self.scale = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        # last mouse position while dragging
        self.drag_x = 0
        self.drag_y = 0

        self.canvas.bind("<Configure>", lambda e: self.redraw())
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

        # biggest scale at which the whole image still fits
        self.scale = min(canvas_w / image_w, canvas_h / image_h)
        # center the image
        self.offset_x = (canvas_w - image_w * self.scale) / 2
        self.offset_y = (canvas_h - image_h * self.scale) / 2
        self.redraw()

    def on_press(self, event: tk.Event) -> None:
        # remember where the drag started
        self.drag_x = event.x
        self.drag_y = event.y

    def on_drag(self, event: tk.Event) -> None:
        # move the image by as much as the mouse moved since last time
        self.offset_x += event.x - self.drag_x
        self.offset_y += event.y - self.drag_y
        self.drag_x = event.x
        self.drag_y = event.y
        self.redraw()

    def on_wheel(self, event: tk.Event) -> None:
        if self.image is None:
            return

        # 1. which point of the image is under the cursor now
        image_x = (event.x - self.offset_x) / self.scale
        image_y = (event.y - self.offset_y) / self.scale

        # 2. zoom in (wheel up) or out (wheel down), keep scale in 0.1-64
        if event.delta > 0:
            self.scale *= 1.2
        else:
            self.scale /= 1.2
        self.scale = max(0.1, min(self.scale, 64))

        # 3. move the image so that the same point is under the cursor again
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

        # range of image pixels visible on the canvas: x0..x1, y0..y1
        x0 = max(0, math.floor(-self.offset_x / self.scale))
        x1 = min(image_w, math.ceil((canvas_w - self.offset_x) / self.scale))
        y0 = max(0, math.floor(-self.offset_y / self.scale))
        y1 = min(image_h, math.ceil((canvas_h - self.offset_y) / self.scale))
        if x1 <= x0 or y1 <= y0:
            return  # image is completely off screen

        # cut out the visible part and enlarge it to screen size
        crop = self.image[y0:y1, x0:x1]
        new_w = max(1, round((x1 - x0) * self.scale))
        new_h = max(1, round((y1 - y0) * self.scale))
        pil_image = Image.fromarray(crop).resize(
            (new_w, new_h), Image.Resampling.NEAREST
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
        # RGB needs bigger squares, because it shows three numbers
        is_rgb = self.image.ndim == 3
        min_scale = 60 if is_rgb else 40
        if self.values is None or self.scale < min_scale:
            return

        self.canvas.delete("pixel_values")
        for y in range(y0, y1):
            for x in range(x0, x1):
                # center of the pixel's square on the screen
                cx = self.offset_x + (x + 0.5) * self.scale
                cy = self.offset_y + (y + 0.5) * self.scale

                # dark text on bright pixels, white text on dark ones
                brightness = np.mean(self.image[y, x])
                color = "black" if brightness >= 128 else "white"

                self.canvas.create_text(
                    cx, cy,
                    text=pixel_text(self.values[y, x]),
                    fill=color,
                    tags="pixel_values",
                )


def pixel_text(value: np.ndarray | float) -> str:
    # RGB pixel is [R, G, B] -> three lines, grayscale is one number
    if np.ndim(value) > 0:
        return "\n".join(number_text(v) for v in value)
    return number_text(value)


def number_text(value: float) -> str:
    # 128.0 -> "128", 0.123456 -> "0.12"
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}"
