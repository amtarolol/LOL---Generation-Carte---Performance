import pygame
from entitities.Buff import Buff
from lane import Lane

# Initialisation de Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Récup les points d'origine et de fin de la ligne
point_debut = (0, 50)
point_fin = (screen_width, screen_height - 50)

# Créer la lane
lane = Lane(screen, point_debut, point_fin)
# Créer le buff UNE SEULE FOIS (pas dans la boucle)
buff = Buff((100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    screen.fill("white")

    # Dessiner la lane
    lane.draw_line()
    
    # Dessiner le buff
    screen.blit(buff.image, buff.rect)  # Utilise buff.image et buff.rect

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)  # Limiter à 60 FPS

pygame.quit()
