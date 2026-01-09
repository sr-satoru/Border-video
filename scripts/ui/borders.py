import tkinter as tk
from tkinter import ttk

class VideoBorders(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Bordas do Vídeo")
        self.pack(fill="x", pady=10)

        add_border = tk.BooleanVar()
        ttk.Checkbutton(self, text="Adicionar Borda ao Vídeo", variable=add_border).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(self, text="Estilo:").grid(row=0, column=1, padx=5)
        ttk.Combobox(self, values=["Moldura", "Sem moldura"], width=10).grid(row=0, column=2)
        ttk.Label(self, text="Cor da Borda:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ttk.Button(self, text="Escolher").grid(row=1, column=1, padx=5)
