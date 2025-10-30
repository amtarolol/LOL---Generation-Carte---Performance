# Buff.py
import pygame

class Buff(pygame.sprite.Sprite):
    _frame = None          # image unique
    _frame_size = (32, 32)

    def __init__(self, pos):
        super().__init__()
        self._load_assets()
        self.image = self._frame
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

    @staticmethod
    def _load_assets():
        if Buff._frame is not None:
            return
        fw, fh = Buff._frame_size
        surf = pygame.Surface((fw, fh), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 0, 0), (fw // 2, fh // 2), fw // 2)
        Buff._frame = surf

    @staticmethod
    def get_size():
        Buff._load_assets()
        return Buff._frame_size

    def update(self, dt):
        # aucun changement d’animation
        pass

    def get_pos(self):
        return self.pos
