# scenes/game.py
import pygame
from core.scene import Scene
from entities.Lane import Lane
from generators.worldgenerator import bush_generation, buff_generation

class GameScene(Scene):
    def on_enter(self, **kwargs):
        self.W, self.H = self.screen.get_size()
        self.nb_buffs = kwargs["nb_buffs"]
        self.start_pt = kwargs["start_pt"]
        self.end_pt = kwargs["end_pt"]

        # Background (charge 1x, pas dans la boucle)
        bg_path = "assets/images/preview.png"
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (self.W, self.H))

        # Monde
        self.lane = Lane(self.screen, self.start_pt, self.end_pt)
        self.bushes = bush_generation(30, self.W, self.H, self.start_pt, self.end_pt)
        self.buffs = buff_generation(self.nb_buffs, self.W, self.H, self.start_pt, self.end_pt)

        self.all_sprites = pygame.sprite.Group(self.bushes + self.buffs)

        # Fonts debug
        self.font = pygame.font.SysFont(None, 24)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            # Retour menu
            from scenes.menu import MenuScene
            self.switch_to(MenuScene)

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.lane.draw_line()

        # Debug HUD
        txt = self.font.render(f"Buffs: {len(self.buffs)}  Bushes: {len(self.bushes)}", True, (255, 255, 255))
        self.screen.blit(txt, (10, 10))
