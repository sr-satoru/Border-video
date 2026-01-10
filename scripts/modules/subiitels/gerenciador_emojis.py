import os
from PIL import Image

class GerenciadorEmojis:
    def __init__(self):
        self.emojis = {}
        self.folder = None

    def load_emojis(self, folder):
        self.folder = folder
        self.emojis = {}
        if not os.path.exists(folder): return 0
        
        count = 0
        for f in os.listdir(folder):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img = Image.open(os.path.join(folder, f))
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    self.emojis[f] = img
                    count += 1
                except: pass
        return count

    def get_emoji(self, name):
        return self.emojis.get(name)

    def get_emoji_list(self):
        return sorted(list(self.emojis.keys()))
