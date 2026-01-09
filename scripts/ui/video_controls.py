import tkinter as tk
from tkinter import ttk

class VideoControls(ttk.LabelFrame):
    def __init__(self, parent, processar_pasta_var):
        super().__init__(parent, text="Controles de Vídeo")
        self.pack(fill="x", pady=10)

        ttk.Button(self, text="Selecionar Vídeo").pack(side="left", padx=10, pady=10)
        ttk.Checkbutton(self, text="Processar toda pasta", variable=processar_pasta_var).pack(side="left", padx=10, pady=10)
import tkinter as tk
from tkinter import ttk

class VideoControls(ttk.LabelFrame):
    def __init__(self, parent, processar_pasta_var):
        super().__init__(parent, text="Controles de Vídeo")
        self.pack(fill="x", pady=10)

        ttk.Button(self, text="Selecionar Vídeo").pack(side="left", padx=10, pady=10)
        ttk.Checkbutton(self, text="Processar toda pasta", variable=processar_pasta_var).pack(side="left", padx=10, pady=10)
