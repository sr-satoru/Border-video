#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Editor de Vídeo e Áudio
Sistema para remover áudio de vídeos e adicionar novos áudios
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random
import threading
from pathlib import Path
import subprocess
import sys

class VideoAudioEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Vídeo e Áudio")
        self.root.geometry("600x500")
        
        # Variáveis
        self.video_folder = tk.StringVar()
        self.audio_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.sequence_mode = tk.StringVar(value="sequential")
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Editor de Vídeo e Áudio", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Seleção de pasta de vídeos
        ttk.Label(main_frame, text="Pasta de Vídeos:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.video_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Selecionar", command=self.select_video_folder).grid(row=1, column=2, padx=(5, 0))
        
        # Seleção de pasta de áudios
        ttk.Label(main_frame, text="Pasta de Áudios:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.audio_folder, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Selecionar", command=self.select_audio_folder).grid(row=2, column=2, padx=(5, 0))
        
        # Pasta de saída
        ttk.Label(main_frame, text="Pasta de Saída:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Selecionar", command=self.select_output_folder).grid(row=3, column=2, padx=(5, 0))
        
        # Opções de sequência
        sequence_frame = ttk.LabelFrame(main_frame, text="Modo de Áudio", padding="10")
        sequence_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Radiobutton(sequence_frame, text="Sequencial (um áudio por vez)", 
                       variable=self.sequence_mode, value="sequential").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(sequence_frame, text="Aleatório", 
                       variable=self.sequence_mode, value="random").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(sequence_frame, text="Intercalado (alterna entre áudios)", 
                       variable=self.sequence_mode, value="alternating").grid(row=2, column=0, sticky=tk.W)
        
        # Barra de progresso
        ttk.Label(main_frame, text="Progresso:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Área de log
        ttk.Label(main_frame, text="Log:").grid(row=7, column=0, sticky=tk.W, pady=(10, 5))
        self.log_text = tk.Text(main_frame, height=10, width=70)
        self.log_text.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scrollbar para o log
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=8, column=3, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="Processar Vídeos", 
                                       command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Limpar Log", command=self.clear_log).pack(side=tk.LEFT)
        
        # Configurar redimensionamento
        main_frame.rowconfigure(8, weight=1)
        
    def select_video_folder(self):
        folder = filedialog.askdirectory(title="Selecionar pasta de vídeos")
        if folder:
            self.video_folder.set(folder)
            self.log(f"Pasta de vídeos selecionada: {folder}")
    
    def select_audio_folder(self):
        folder = filedialog.askdirectory(title="Selecionar pasta de áudios")
        if folder:
            self.audio_folder.set(folder)
            self.log(f"Pasta de áudios selecionada: {folder}")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Selecionar pasta de saída")
        if folder:
            self.output_folder.set(folder)
            self.log(f"Pasta de saída selecionada: {folder}")
    
    def log(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Limpa o log"""
        self.log_text.delete(1.0, tk.END)
    
    def get_video_files(self, folder):
        """Obtém lista de arquivos de vídeo"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        video_files = []
        
        for file in os.listdir(folder):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(os.path.join(folder, file))
        
        return sorted(video_files)
    
    def get_audio_files(self, folder):
        """Obtém lista de arquivos de áudio"""
        audio_extensions = ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a']
        audio_files = []
        
        for file in os.listdir(folder):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(os.path.join(folder, file))
        
        return sorted(audio_files)
    
    def check_ffmpeg(self):
        """Verifica se o FFmpeg está instalado"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def process_video(self, video_path, audio_path, output_path):
        """Processa um vídeo: remove áudio original e adiciona novo áudio"""
        try:
            # Comando FFmpeg para remover áudio original e adicionar novo áudio
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',  # Copia o vídeo sem re-encoding
                '-c:a', 'aac',   # Usa AAC para o áudio
                '-map', '0:v:0', # Mapeia o vídeo do primeiro input
                '-map', '1:a:0', # Mapeia o áudio do segundo input
                '-shortest',      # Termina quando o stream mais curto terminar
                '-y',            # Sobrescreve arquivo de saída
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Sucesso"
            else:
                return False, f"Erro FFmpeg: {result.stderr}"
                
        except Exception as e:
            return False, f"Erro: {str(e)}"
    
    def start_processing(self):
        """Inicia o processamento em thread separada"""
        if not self.video_folder.get() or not self.audio_folder.get() or not self.output_folder.get():
            messagebox.showerror("Erro", "Selecione todas as pastas necessárias!")
            return
        
        if not self.check_ffmpeg():
            messagebox.showerror("Erro", "FFmpeg não encontrado! Instale o FFmpeg para continuar.")
            return
        
        # Desabilitar botão durante processamento
        self.process_button.config(state='disabled')
        
        # Iniciar processamento em thread separada
        thread = threading.Thread(target=self.process_videos)
        thread.daemon = True
        thread.start()
    
    def process_videos(self):
        """Processa todos os vídeos"""
        try:
            video_files = self.get_video_files(self.video_folder.get())
            audio_files = self.get_audio_files(self.audio_folder.get())
            
            if not video_files:
                self.log("Nenhum arquivo de vídeo encontrado!")
                return
            
            if not audio_files:
                self.log("Nenhum arquivo de áudio encontrado!")
                return
            
            self.log(f"Encontrados {len(video_files)} vídeos e {len(audio_files)} áudios")
            
            # Criar pasta de saída se não existir
            os.makedirs(self.output_folder.get(), exist_ok=True)
            
            audio_index = 0
            
            for i, video_path in enumerate(video_files):
                video_name = os.path.basename(video_path)
                self.log(f"Processando: {video_name}")
                
                # Determinar qual áudio usar
                if self.sequence_mode.get() == "sequential":
                    # Usa áudios em sequência, voltando ao primeiro quando acabar
                    audio_path = audio_files[audio_index % len(audio_files)]
                    audio_index += 1
                elif self.sequence_mode.get() == "random":
                    audio_path = random.choice(audio_files)
                elif self.sequence_mode.get() == "alternating":
                    # Alterna entre os áudios disponíveis, voltando ao primeiro quando acabar
                    audio_path = audio_files[audio_index % len(audio_files)]
                    audio_index += 1
                
                # Nome do arquivo de saída
                name, ext = os.path.splitext(video_name)
                output_path = os.path.join(self.output_folder.get(), f"{name}_edited{ext}")
                
                # Processar vídeo com áudio
                success, message = self.process_video(video_path, audio_path, output_path)
                if success:
                    self.log(f"✓ Concluído: {video_name} com áudio {os.path.basename(audio_path)}")
                else:
                    self.log(f"✗ Erro em {video_name}: {message}")
                
                # Atualizar progresso
                progress = ((i + 1) / len(video_files)) * 100
                self.progress_var.set(progress)
            
            self.log("Processamento concluído!")
            
        except Exception as e:
            self.log(f"Erro durante processamento: {str(e)}")
        finally:
            # Reabilitar botão
            self.process_button.config(state='normal')
    
    def remove_audio_only(self, video_path, output_path):
        """Remove apenas o áudio do vídeo"""
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-c:v', 'copy',
                '-an',  # Remove áudio
                '-y',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, "Sucesso"
            else:
                return False, f"Erro FFmpeg: {result.stderr}"
                
        except Exception as e:
            return False, f"Erro: {str(e)}"

def main():
    root = tk.Tk()
    app = VideoAudioEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()