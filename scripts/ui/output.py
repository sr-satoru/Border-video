import tkinter as tk
from tkinter import ttk, filedialog

class OutputVideo(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Salvar Vídeo Processado")
        self.pack(fill="x", pady=10)

        self.output_path = tk.StringVar()

        path_frame = ttk.Frame(self)
        path_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(path_frame, text="Caminho de saída:").pack(side="left")

        ttk.Entry(path_frame, textvariable=self.output_path).pack(
            side="left", fill="x", expand=True, padx=5
        )

        ttk.Button(path_frame, text="Escolher Pasta", command=self.select_output_folder).pack(side="left", padx=5)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)
