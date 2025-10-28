import pygame
import random
from scenes.menu import run_menu



from entities.Lane import Lane
from Tools import Tools
from entities.Bush import Bush
from entities.Buff import Buff


pygame.init()
screen = pygame.display.set_mode((1200, 720))
map_width, map_height = screen.get_size()
clock = pygame.time.Clock()


def bush_generation(nb_bush, map_width, map_height):
    bushes = []
    rects = []
    w, h = Bush.get_size()
    max_attempts = 100
    for _ in range(nb_bush):
        for _ in range(max_attempts):
            x = random.randint(0, max(0, map_width  - w))
            y = random.randint(0, max(0, map_height - h))
            test_rect = pygame.Rect(x, y, w, h)
            if any(test_rect.colliderect(r) for r in rects):
                continue
            bush = Bush((x + w // 2, y + h // 2))
            bushes.append(bush)
            rects.append(bush.rect)
            break
        else:
            print(f"Impossible de placer un bush sans collision après {max_attempts} tentatives.")
    return bushes


def buff_generation(nb_buff, map_width, map_height, point_debut, point_fin):
    buffs = []
    rects = []
    w, h = Buff.get_size()
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

def run_game(screen, nb_buffs, start_pt, end_pt):
    W, H = screen.get_size()
    lane = Lane(screen, start_pt, end_pt)
    all_bushes = bush_generation(30, W, H)
    all_buffs = buff_generation(nb_buffs, W, H, start_pt, end_pt)
    all_sprites = pygame.sprite.Group(all_bushes + all_buffs)

    clock = pygame.time.Clock()
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill("black")
        lane.draw_line()
        all_sprites.draw(screen)
        pygame.display.flip()



def check_collide(rect, rects):
    for r in rects:
        if rect.colliderect(r):
            return True
    return False




if __name__ == "__main__":
    pygame.display.set_caption("Buff Generator Demo")
    result = run_menu(screen)
    if result is not None:
        nb, start_pt, end_pt = result
        run_game(screen, nb, start_pt, end_pt)
    pygame.quit()
