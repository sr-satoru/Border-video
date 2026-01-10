import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
from moviepy.video.VideoClip import VideoClip
from modules.subtitle_manager import SubtitleRenderer

class VideoRenderer:
    """
    Centraliza todos os cálculos, proporções e lógica de renderização final do vídeo,
    espelhando o comportamento do simples.py.
    """
    OUTPUT_WIDTH = 1080
    OUTPUT_HEIGHT = 1920
    BASE_WIDTH = 270.0  # Base usada no preview para cálculos de escala
    ASPECT_RATIO = 9 / 16

    def __init__(self, emoji_manager):
        self.emoji_manager = emoji_manager
        self.subtitle_renderer = SubtitleRenderer(emoji_manager)

    def get_scale_factor(self):
        """Retorna o fator de escala entre o preview (270p) e o output (1080p)"""
        return self.OUTPUT_WIDTH / self.BASE_WIDTH

    def calculate_video_dimensions(self, border_enabled, border_size_preview):
        """
        Calcula as dimensões do vídeo interno baseado na borda.
        border_size_preview: tamanho da borda definido na UI (base 270p)
        """
        if not border_enabled:
            return self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT, 0

        scale_factor = self.get_scale_factor()
        scaled_border_size = int(border_size_preview * scale_factor)
        
        available_width = self.OUTPUT_WIDTH - (scaled_border_size * 2)
        available_height = self.OUTPUT_HEIGHT - (scaled_border_size * 2)
        
        # Calcula dimensões baseadas na largura disponível mantendo 9:16
        video_width = available_width
        video_height = int(video_width / self.ASPECT_RATIO)
        
        # Ajusta se a altura extrapolar
        if video_height > available_height:
            video_height = available_height
            video_width = int(video_height * self.ASPECT_RATIO)
            
        return video_width, video_height, scaled_border_size

    def create_background(self, style, border_color, duration):
        """Cria o frame de fundo baseado no estilo"""
        if "uniforme" in style or "arredondada" in style or not style:
            return Image.new('RGB', (self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT), border_color)
        elif "degradê" in style:
            return self.create_gradient_background(border_color)
        else:
            return Image.new('RGB', (self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT), border_color)

    def create_gradient_background(self, base_color):
        """Cria um fundo com degradê nas bordas"""
        color = base_color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        image = Image.new('RGB', (self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT))
        pixels = image.load()
        
        gradient_area = 50  # Pixels de degradê
        
        for x in range(self.OUTPUT_WIDTH):
            for y in range(self.OUTPUT_HEIGHT):
                dist_x = min(x, self.OUTPUT_WIDTH - x - 1)
                dist_y = min(y, self.OUTPUT_HEIGHT - y - 1)
                min_dist = min(dist_x, dist_y)
                
                if min_dist < gradient_area:
                    intensity = min_dist / float(gradient_area)
                    pixels[x, y] = (int(r * intensity), int(g * intensity), int(b * intensity))
                else:
                    pixels[x, y] = (r, g, b)
        return image

    def render_frame(self, video_frame, subtitles, border_enabled, border_size_preview, border_color, border_style, emoji_scale=1.0):
        """
        Renderiza um único frame com bordas e legendas.
        video_frame: numpy array do frame do vídeo (já redimensionado para a área interna)
        """
        video_image = Image.fromarray(video_frame.astype(np.uint8))
        scale_factor = self.get_scale_factor()
        
        # 1. Calcular dimensões e criar fundo
        v_w, v_h, scaled_border = self.calculate_video_dimensions(border_enabled, border_size_preview)
        
        if border_enabled:
            final_image = self.create_background(border_style, border_color, 0)
            # Centralizar vídeo na moldura
            paste_x = scaled_border + (self.OUTPUT_WIDTH - (scaled_border * 2) - v_w) // 2
            paste_y = scaled_border + (self.OUTPUT_HEIGHT - (scaled_border * 2) - v_h) // 2
            final_image.paste(video_image, (paste_x, paste_y))
        else:
            # Sem borda, apenas redimensiona para o tamanho final (deve ser 1080x1920)
            final_image = video_image.resize((self.OUTPUT_WIDTH, self.OUTPUT_HEIGHT), Image.Resampling.LANCZOS)
            scaled_border = 0

        # 2. Desenhar legendas
        if subtitles:
            draw = ImageDraw.Draw(final_image)
            for sub in subtitles:
                # Desenha usando o renderer comum com a escala de output e offset da borda
                self.subtitle_renderer.draw_subtitle(
                    draw, 
                    sub, 
                    scale_factor=scale_factor,
                    emoji_scale=emoji_scale,
                    offset_x=scaled_border if border_enabled else 0,
                    offset_y=scaled_border if border_enabled else 0
                )
                
        return np.array(final_image)

    def render_video(self, input_path, output_folder, border_enabled, border_size_preview, border_color, border_style, subtitles, emoji_scale=1.0, threads=4):
        """Renderiza o vídeo completo"""
        try:
            clip = mp.VideoFileClip(input_path)
            
            # Dimensões do vídeo interno
            v_w, v_h, _ = self.calculate_video_dimensions(border_enabled, border_size_preview)
            video_resized = clip.resize((v_w, v_h))
            
            def make_frame(t):
                frame = video_resized.get_frame(t)
                return self.render_frame(
                    frame, 
                    subtitles, 
                    border_enabled, 
                    border_size_preview, 
                    border_color, 
                    border_style,
                    emoji_scale
                )
            
            fps = clip.fps if clip.fps else 30.0
            final_clip = VideoClip(make_frame=make_frame, duration=clip.duration)
            final_clip = final_clip.set_fps(fps)
            
            if clip.audio:
                final_clip = final_clip.set_audio(clip.audio)
                
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, f"{base_name}_render.mp4")
            
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=fps,
                threads=threads,
                preset="medium"
            )
            
            clip.close()
            video_resized.close()
            final_clip.close()
            
            return True, output_path
        except Exception as e:
            return False, str(e)
