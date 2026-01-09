import tkinter as tk
from tkinter import ttk, filedialog

class AudioSettings(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Configurações de Áudio")
        self.pack(fill="x", pady=10)

        self.remove_audio_var = tk.BooleanVar()
        self.use_folder_audio_var = tk.BooleanVar()
        self.select_folder_audio_var = tk.BooleanVar()
        self.audio_folder_path = tk.StringVar()

        ttk.Checkbutton(self, text="Remover Áudio", variable=self.remove_audio_var).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(self, text="Usar áudios da pasta", variable=self.use_folder_audio_var).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        ttk.Checkbutton(self, text="Usar áudios da pasta selecionada", variable=self.select_folder_audio_var).grid(row=2, column=0, sticky="w", padx=10, pady=5)

        ttk.Entry(self, textvariable=self.audio_folder_path, width=40, state="readonly").grid(row=2, column=1, padx=5)
        ttk.Button(self, text="📁 Selecionar Pasta", command=self.select_audio_folder).grid(row=2, column=2, padx=5)

    def select_audio_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.audio_folder_path.set(folder)
