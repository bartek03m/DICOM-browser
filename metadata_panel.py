from tkinter import ttk

import customtkinter as ctk
from pydicom import Dataset

from metadata import extract_metadata


class MetadataPanel(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master, width=700)
        self.pack_propagate(False)

        self.tree = ttk.Treeview(
            self,
            columns=("tag", "name", "vr", "value"),
            show="headings",
        )
        self.tree.heading("tag", text="Tag")
        self.tree.heading("name", text="Nazwa")
        self.tree.heading("vr", text="VR")
        self.tree.heading("value", text="Wartość")

        self.tree.column("tag", width=110, stretch=False)
        self.tree.column("name", width=250, stretch=False)
        self.tree.column("vr", width=40, stretch=False)
        self.tree.column("value", width=300)

        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
    def show(self, ds:Dataset) -> None:
        self.tree.delete(*self.tree.get_children())
        for row in extract_metadata(ds):
            self.tree.insert("", "end", values=(row.tag, row.name, row.vr, row.value))
