import pygame
from scenes.menu import run_menu
from entities.Lane import Lane
from generators.worldgenerator import bush_generation, buff_generation

pygame.init()
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Buff Generator Demo")

def run_game(screen, nb_buffs, start_pt, end_pt):
    W, H = screen.get_size()
    lane = Lane(screen, start_pt, end_pt)

    # Load background
    bg = pygame.image.load("assets/images/preview.png").convert()
    bg = pygame.transform.scale(bg, (W, H))

    # Generate world
    bushes = bush_generation(30, W, H, start_pt, end_pt)
    buffs = buff_generation(nb_buffs, W, H, start_pt, end_pt)
    all_sprites = pygame.sprite.Group(bushes + buffs)

    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        lane.draw_line()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    result = run_menu(screen)
    if result:
        nb, start_pt, end_pt = result
        run_game(screen, nb, start_pt, end_pt)
    pygame.quit()
