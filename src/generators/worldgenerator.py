import pygame
import random
from entities.Buff import Buff
from entities.Bush import Bush
from utils.Tools import Tools


def check_collide(rect, rects):
    """Retourne True si rect entre en collision avec un des rectangles existants."""
    return any(rect.colliderect(r) for r in rects)


def bush_generation(nb_bush, map_width, map_height, point_debut, point_fin):
    bushes, rects = [], []
    w, h = Bush.get_size()
    for _ in range(nb_bush):
        for _ in range(100):
            x = random.randint(0, map_width - w)
            y = random.randint(0, map_height - h)
            test = pygame.Rect(x, y, w, h)
            if Tools.get_distance_line_point(point_debut, point_fin, (x + w//2, y + h//2)) > 20 and not check_collide(test, rects):
                bush = Bush((x + w // 2, y + h // 2))
                bushes.append(bush)
                rects.append(bush.rect)
                break
    return bushes


def buff_generation(nb_buff, map_width, map_height, point_debut, point_fin):
    buffs, rects = [], []
    w, h = Buff.get_size()
    for _ in range(nb_buff):
        for _ in range(100):
            x = random.randint(0, map_width - w)
            y = random.randint(0, map_height - h)
            test = pygame.Rect(x, y, w, h)
            if Tools.get_distance_line_point(point_debut, point_fin, (x + w//2, y + h//2)) > 20 and not check_collide(test, rects):
                buff = Buff((x + w // 2, y + h // 2))
                buffs.append(buff)
                rects.append(buff.rect)
                break
    return buffs
