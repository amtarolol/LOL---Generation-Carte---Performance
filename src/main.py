import pygame
from entitities.Buff import Buff

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 720))
clock = pygame.time.Clock()
running = True

# Créer le buff UNE SEULE FOIS (pas dans la boucle)
buff = Buff((100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    screen.fill("black")

    # Dessiner le buff
    screen.blit(buff.image, buff.rect)  # Utilise buff.image et buff.rect

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)  # Limiter à 60 FPS

pygame.quit()
