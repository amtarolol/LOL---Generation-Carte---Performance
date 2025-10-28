import pygame

class SceneManager:
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

            if self.scene.is_done:
                scene_cls, kwargs = self.scene.next_scene
                self.scene.on_exit()
                self.scene = scene_cls(self.screen)
                self.scene.on_enter(**kwargs)
