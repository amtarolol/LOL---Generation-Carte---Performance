
import pygame
from managers.SceneManager import SceneManager
from scenes.menu import MenuScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    pygame.display.set_caption("Scene System Demo")
    manager = SceneManager(screen, MenuScene)
    manager.run()
    pygame.quit()

if __name__ == "__main__":
    main()
