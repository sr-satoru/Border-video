import os
from PIL import Image

class LogoManager:
    def __init__(self):
        self.logo_path = ""
        self.x = 50
        self.y = 50
        self.scale = 0.2  # Escala inicial razoável
        self.opacity = 1.0
        self._cached_image = None
        self._last_loaded_path = None

    def set_logo(self, path):
        if path and os.path.exists(path):
            self.logo_path = path
            # Resetar cache
            self._cached_image = None
            return True
        return False

    def get_image(self):
        """Retorna o objeto PIL Image da logo carregada"""
        if not self.logo_path:
            return None
            
        if self._cached_image and self.logo_path == self._last_loaded_path:
            return self._cached_image
            
        try:
            img = Image.open(self.logo_path).convert("RGBA")
            self._cached_image = img
            self._last_loaded_path = self.logo_path
            return img
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")
            return None

    def update_position(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def update_scale(self, scale):
        # Limitar escala mínima e máxima para evitar problemas
        self.scale = max(0.05, min(scale, 5.0))

    def get_state(self):
        return {
            "logo_path": self.logo_path,
            "x": self.x,
            "y": self.y,
            "scale": self.scale,
            "opacity": self.opacity
        }

    def set_state(self, state):
        self.logo_path = state.get("logo_path", "")
        self.x = state.get("x", 50)
        self.y = state.get("y", 50)
        self.scale = state.get("scale", 0.2)
        self.opacity = state.get("opacity", 1.0)
        # Forçar recarregamento se necessário
        self._cached_image = None
