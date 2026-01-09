import tkinter as tk
from tkinter import ttk

class Subtitles(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Editor de Legendas")
        self.pack(fill="x", pady=10)

        self.font_family = tk.StringVar(value="Arial")
        self.font_size = tk.IntVar(value=24)

        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=10, pady=10)

        ttk.Label(controls, text="Texto:").grid(row=0, column=0, sticky="w")
        text_widget = tk.Text(controls, height=3, wrap="word")
        text_widget.grid(row=0, column=1, columnspan=6, sticky="ew", padx=5)
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Fonte:").grid(row=0, column=7, padx=5, sticky="e")
        ttk.Combobox(controls, textvariable=self.font_family, values=["Arial","Helvetica","Times"], width=12).grid(row=0, column=8, padx=5)
        ttk.Label(controls, text="Tamanho:").grid(row=0, column=9, sticky="e")
        ttk.Spinbox(controls, from_=8, to=120, textvariable=self.font_size, width=5).grid(row=0, column=10, padx=5)

        ttk.Button(self, text="+ Adicionar Legenda").pack(fill="x", padx=10, pady=10)
