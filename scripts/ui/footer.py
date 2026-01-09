import tkinter as tk
from tkinter import ttk

class Footer(ttk.Frame):
    def __init__(self, parent, add_tab_callback=None):
        super().__init__(parent)
        self.pack(side="bottom", fill="x")  # ocupa largura total

        # Frame interno para alinhar botão à esquerda
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x")

        self.add_tab_btn = ttk.Button(btn_frame, text="+ Adicionar Aba", command=add_tab_callback)
        self.add_tab_btn.pack(side="left", padx=10, pady=10)  # <- alinhamento à esquerda

class EditorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teste Footer")
        self.geometry("600x400")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        # Aba inicial
        aba1 = ttk.Frame(self.notebook)
        self.notebook.add(aba1, text="Aba 1")

        # Footer
        Footer(container, add_tab_callback=self.add_new_tab)

    def add_new_tab(self):
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text=f"Aba {len(self.notebook.tabs())+1}")

if __name__ == "__main__":
    EditorUI().mainloop()
