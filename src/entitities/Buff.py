# Buff.py
import pygame, os

class Buff(pygame.sprite.Sprite):
    _frames = None         # cache des frames
    _frame_size = None     # (w, h)

    @classmethod
    def _load_assets(cls):
        if cls._frames is not None:
            return
        # charge ta sprite sheet ./assets/buff/idle.png
        sheet = pygame.image.load(os.path.join("assets","images", "buff", "idle.png")).convert_alpha()

        # paramètres de ta sheet (adapte si besoin)
        fw, fh, n = 128, 128, 5
        cls._frames = []
        for i in range(n):
            surf = pygame.Surface((fw, fh), pygame.SRCALPHA)
            surf.blit(sheet, (0, 0), (i*fw, 0, fw, fh))
            cls._frames.append(surf)
        cls._frame_size = (fw, fh)

    @classmethod
    def get_size(cls):
        cls._load_assets()
        return cls._frame_size

    def __init__(self, pos):
        super().__init__()
        self._load_assets()
        self.frames = self._frames
        self.frame_index = 0
        self.anim_speed = 0.15  # s/frame
        self.timer = 0.0

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.anim_speed:
            self.timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            # garder le centre en changeant d'image
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=center)
