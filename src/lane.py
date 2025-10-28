
import pygame

class Lane(pygame.sprite.Sprite):
    def __init__(self, screen, begin_point, end_point):
        super().__init__()
        # Créer une surface pour le buff (ex: un cercle rouge)
        self.screen = screen
        self.begin_point = begin_point
        self.end_point = end_point

    def draw_line(self):
        pygame.draw.line(self.screen, (0, 0, 0), self.begin_point, self.end_point, 1)  # Cercle rouge
