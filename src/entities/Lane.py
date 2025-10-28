
import pygame

class Lane(pygame.sprite.Sprite):
    def __init__(self, screen, begin_point, end_point):
        super().__init__()
        # Créer une surface pour le buff (ex: un cercle rouge)
        self.screen = screen
        self.begin_point, self.end_point = self._get_furthest_points(begin_point, end_point)

    def draw_line(self):
        pygame.draw.line(self.screen, (255, 255, 255), self.begin_point, self.end_point, 1)  # Cercle rouge

    def get_line_pos(self):
        return (self.begin_point, self.end_point)

    def _get_furthest_points(self, begin_point, end_point):
        width, height = self.screen.get_size()
        points = []

        x1, y1 = begin_point
        x2, y2 = end_point

        if x1 == x2:
            return [(x1, 0), (x1, height)]

        # Calcul de la pente et de l'ordonnée à l'origine
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        # Bords verticaux : x = 0 et x = width
        y_left = b
        y_right = a * width + b
        if 0 <= y_left <= height:
            points.append((0, y_left))
        if 0 <= y_right <= height:
            points.append((width, y_right))

        # Bords horizontaux : y = 0 et y = height
        if a != 0:
            x_top = -b / a
            x_bottom = (height - b) / a
            if 0 <= x_top <= width:
                points.append((x_top, 0))
            if 0 <= x_bottom <= width:
                points.append((x_bottom, height))

        # On garde seulement deux points (les intersections visibles)
        if len(points) >= 2:
            return points[:2]
        else:
            return None
