import pygame
import random
# ⚠️ Vérifie le nom du package : "entities" vs "entitities"
from entitities.Buff import Buff
from Lane import Lane
from Tools import Tools

pygame.init()
screen = pygame.display.set_mode((1200, 720))
map_width, map_height = screen.get_size()
clock = pygame.time.Clock()
running = True

# Récup les points d'origine et de fin de la ligne
point_debut = (0, 50)
point_fin = (map_width, map_height - 50)

# Créer la lane
lane = Lane(screen, point_debut, point_fin)

def buff_generation(nb_buff, map_width, map_height):
    buffs = []
    rects = []  # pour tester les collisions sans instancier des Buff à répétition
    w, h = Buff.get_size()  # ← une seule fois

    max_attempts = 100
    for _ in range(nb_buff):
        for _ in range(max_attempts):
            x = random.randint(0, max(0, map_width  - w))
            y = random.randint(0, max(0, map_height - h))
            test_rect = pygame.Rect(x, y, w, h)
            if (Tools.get_distance_line_point(point_debut, point_fin, (x + w // 2, y + h // 2)) > 20):
                if (not check_collide(test_rect, rects)):
                    # place le vrai buff une fois validé
                    buff = Buff((x + w // 2, y + h // 2))
                    buffs.append(buff)
                    rects.append(buff.rect)  # garder le rect réel
                    break
                else:
                    print(f"Impossible de placer un buff sans collision après {max_attempts} tentatives.")
    return buffs


def check_collide(rect, rects):
    for r in rects:
        if rect.colliderect(r):
            return True
    return False


all_buffs = buff_generation(100, map_width, map_height)
all_sprites = pygame.sprite.Group(all_buffs)


while running:
    dt = clock.tick(60) / 1000.0  # secondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    all_sprites.draw(screen)



    # Dessiner la lane
    lane.draw_line()
    
   

    pygame.display.flip()

pygame.quit()
