
import pygame

class Buff(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Créer une surface pour le buff (ex: un cercle rouge)
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (16, 16), 16)  # Cercle rouge
        self.rect = self.image.get_rect(center=pos)  # Position du buff
        self.pos = pos  # Stocke la position






