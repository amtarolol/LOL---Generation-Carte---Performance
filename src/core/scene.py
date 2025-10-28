# core/scene.py
import pygame

class Scene:
    """Classe de base pour toutes les scènes."""
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.is_done = False
        self.request_quit = False

    # Hooks
    def on_enter(self, **kwargs): pass
    def on_exit(self): pass

    # Cycle
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self): pass

    # Transitions
    def switch_to(self, scene_cls, **kwargs):
        """Demander au manager de passer à une autre scène."""
        self.next_scene = (scene_cls, kwargs)
        self.is_done = True

class SceneManager:
    """Boucle principale qui orchestre les scènes."""
    def __init__(self, screen, initial_scene_cls, **kwargs):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.scene = initial_scene_cls(screen)
        self.scene.on_enter(**kwargs)
        self.running = True
        self.scene.scene_manager = self


    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(e)

            if self.scene.request_quit:
                self.running = False
                break

            self.scene.draw()
            pygame.display.flip()

            # Transition
            if self.scene.is_done:
                scene_cls, kwargs = self.scene.next_scene
                self.scene.on_exit()
                self.scene = scene_cls(self.screen)
                self.scene.on_enter(**kwargs)
