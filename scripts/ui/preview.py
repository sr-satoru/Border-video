import tkinter as tk
from tkinter import ttk

class Preview(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Preview 9:16 - Arraste as legendas aqui")
        self.pack(fill="x", pady=10)

        self.canvas = tk.Canvas(self, width=360, height=640, bg="black")
        self.canvas.pack(padx=20, pady=20)
