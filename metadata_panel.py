from tkinter import ttk

import customtkinter as ctk
from pydicom import Dataset

from metadata import extract_metadata

# id, heading, width
COLUMNS = (
    ("tag", "Tag", 110),
    ("name", "Nazwa", 250),
    ("vr", "VR", 40),
    ("value", "Wartość", 300),
)


class MetadataPanel(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master, width=700)
        self.pack_propagate(False)  # keep fixed width

        self.tree = ttk.Treeview(
            self, columns=[col[0] for col in COLUMNS], show="headings"
        )  # table without tree column
        for col, heading, width in COLUMNS:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, stretch=col == "value")

        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def show(self, ds: Dataset) -> None:
        self.tree.delete(*self.tree.get_children())  # clear table
        for row in extract_metadata(ds):
            self.tree.insert(
                "", "end", values=(row.tag, row.name, row.vr, row.value)
            )
