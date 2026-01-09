import tkinter as tk
from tkinter import ttk

class SubtitlesAdded(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Legendas Adicionadas")
        self.pack(fill="x", pady=10)

        # Frame interno
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Lista de legendas
        self.subtitles_listbox = tk.Listbox(list_frame, height=6)
        self.subtitles_listbox.pack(side="left", fill="both", expand=True)

        list_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.subtitles_listbox.yview)
        list_scroll.pack(side="left", fill="y")
        self.subtitles_listbox.configure(yscrollcommand=list_scroll.set)

        # Botões de controle
        buttons_frame = ttk.Frame(list_frame)
        buttons_frame.pack(side="right", fill="y", padx=(10,0))

        ttk.Button(buttons_frame, text="Remover").pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Editar").pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Cima").pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Mover Baixo").pack(fill="x", pady=2)
        ttk.Button(buttons_frame, text="Selecionar no Preview").pack(fill="x", pady=2)
