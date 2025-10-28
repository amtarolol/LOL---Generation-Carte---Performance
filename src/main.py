# main.py
import pygame
from core.scene import SceneManager
from scenes.menu import MenuScene

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 720))
    pygame.display.set_caption("Scene System Demo")
    manager = SceneManager(screen, MenuScene)
    manager.run()
    pygame.quit()

if __name__ == "__main__":
    main()
