# Buff.py
import pygame, os

class Buff(pygame.sprite.Sprite):
    _frames = None         # cache des frames
    _frame_size = None     # (w, h)

    def __init__(self, pos):
        super().__init__()
        self._load_assets()
        self.frames = self._frames
        self.frame_index = 0
        self.anim_speed = 0.15  # s/frame
        self.timer = 0.0
        self.pos = pos

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def _load_assets():
        if Buff._frames is not None:
            return
        # charge ta sprite sheet ./assets/buff/idle.png
        sheet = pygame.image.load(os.path.join("assets","images", "buff", "idle.png")).convert_alpha()

        # paramètres de ta sheet (adapte si besoin)
        fw, fh, n = 128, 128, 5
        Buff._frames = []
        for i in range(n):
            surf = pygame.Surface((fw, fh), pygame.SRCALPHA)
            surf.blit(sheet, (0, 0), (i*fw, 0, fw, fh))
            Buff._frames.append(surf)
        Buff._frame_size = (fw, fh)

    @staticmethod
    def get_size():
        Buff._load_assets()
        return Buff._frame_size


    def update(self, dt):
        self.timer += dt
        if self.timer >= self.anim_speed:
            self.timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            # garder le centre en changeant d'image
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(center=center)

    def get_pos(self):
        return self.pos