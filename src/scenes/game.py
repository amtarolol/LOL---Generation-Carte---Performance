
import os
import pygame
from core.scene import Scene
from entities.Lane import Lane
from generators.world.api import generate_sprites
from entities.Bush import Bush
from entities.Buff import Buff

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")

class GameScene(Scene):
    def on_enter(self, **kwargs):
        self.W, self.H = self.screen.get_size()
        self.nb_buffs = kwargs["nb_buffs"]
        self.nb_bushes = kwargs["nb_bushes"]
        self.start_pt = kwargs["start_pt"]
        self.end_pt = kwargs["end_pt"]
        self.placement = kwargs.get("placement", "random")  

        bg_path = os.path.join(ASSETS_DIR, "preview.png")
        try:
            self.background = pygame.image.load(bg_path).convert()
        except FileNotFoundError:
            self.background = pygame.Surface((self.W, self.H)); self.background.fill((32,36,44))
        else:
            self.background = pygame.transform.scale(self.background, (self.W, self.H))

        self.lane = Lane(self.screen, self.start_pt, self.end_pt)
        self._generate_world()

        self.font = pygame.font.SysFont(None, 24)
        self.show_hud = True

    def _generate_world(self):

        self.bushes, rects_bush, self.bush_stats = generate_sprites(
            total_to_place=self.nb_bushes,
            map_width=self.W,
            map_height=self.H,
            get_size=Bush.get_size, 
            factory=lambda pos: Bush(pos),
            lane_start_point=self.start_pt,
            lane_end_point=self.end_pt,
            min_distance_to_lane=100,
            max_placement_attempts=100,
            existing_object_rects=None,
            placement_mode=self.placement
        )

        self.buffs, _rects_all, self.buff_stats = generate_sprites(
            total_to_place=self.nb_buffs,
            map_width=self.W,
            map_height=self.H,
            get_size=Buff.get_size, 
            factory=lambda pos: Buff(pos),
            lane_start_point=self.start_pt,
            lane_end_point=self.end_pt,
            min_distance_to_lane=20,
            max_placement_attempts=100,
            existing_object_rects=rects_bush,
            placement_mode=self.placement
        )

        self.all_sprites = pygame.sprite.Group(self.bushes + self.buffs)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                from scenes.menu import MenuScene
                self.switch_to(MenuScene)
            elif e.key == pygame.K_r:
                self._generate_world()
            elif e.key == pygame.K_F3:
                self.show_hud = not self.show_hud

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.lane.draw_line()

        if self.show_hud:
            lines = [
                f"Bush: {self.bush_stats.placed}/{self.bush_stats.requested}  "
                f"laneRej {self.bush_stats.lane_rejected}  collRej {self.bush_stats.collisions_rejected}",
                f"Buff: {self.buff_stats.placed}/{self.buff_stats.requested}  "
                f"laneRej {self.buff_stats.lane_rejected}  collRej {self.buff_stats.collisions_rejected}",
                f"Time: bush {self.bush_stats.elapsed_ms:.1f} ms  buff {self.buff_stats.elapsed_ms:.1f} ms",
                f"Placement: {self.placement}",
            ]
            y = 10
            for s in lines:
                self.screen.blit(self.font.render(s, True, (255,255,255)), (10, y))
                y += 18
