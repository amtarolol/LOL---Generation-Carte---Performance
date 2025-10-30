import timeit
import pygame
import textwrap
from generators.world.api import generate_sprites
from generators.world.grid_generator import GridGenerator
import os


# --- MOCKS pour faire tourner le benchmark ---
# Sprite simple
class Buff(pygame.sprite.Sprite):
    _frame_size = (128, 128)     # (w, h)

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface(Buff._frame_size)
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def get_size():
        return Buff._frame_size


class Bush(pygame.sprite.Sprite):

    def __init__(self, pos, bush_type=None):
        super().__init__()
        # Charger ou récupérer l'image depuis le cache
        self.image = pygame.Surface(self.get_size())
        self.rect = self.image.get_rect(center=pos)
    
    @classmethod
    def get_size(cls):
        return (32, 32)

# --- Benchmark avec timeit ---
setup_code = """
from __main__ import pygame, generate_sprites, Buff, Bush, os
import random
rng = 45
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1,1))
"""


def get_test_code(placement_mode, type) :
    code = f"""
            generate_sprites(
                total_to_place=300,
                map_width=800,
                map_height=600,
                get_size={type}.get_size,
                factory=lambda pos: {type}(pos),
                lane_start_point=(0, 50),
                lane_end_point=(800, 550),
                min_distance_to_lane=50,
                max_placement_attempts=100,
                existing_object_rects=[],
                rng=0,
                placement_mode="{placement_mode}",
            )
    """
    return textwrap.dedent(code).strip()


def get_test_code_bush(placement_mode):
    code = f"""
            generate_sprites(
                total_to_place=300,
                map_width=800,
                map_height=600,
                get_size=Bush.get_size,
                factory=lambda pos: Bush(pos),
                lane_start_point=(0, 50),
                lane_end_point=(800, 550),
                min_distance_to_lane=50,
                max_placement_attempts=100,
                existing_object_rects=[],
                rng=rng,
                placement_mode="{placement_mode}",
            )
    """
    return textwrap.dedent(code).strip()


# Nombre de fois dans un "tour de boucle"
n = 50
# Nombre de "tour de boucle"
repeat = 10

modes = ["random", "grid"]
types = ["Bush", "Buff"]

for type in types:
    for mode in modes:

        results = timeit.repeat(stmt=get_test_code(mode, type), setup=setup_code, repeat=repeat, number=n)    
        avg_ms = (sum(results) / len(results)) * 1000 / n

        print(f"=== Résultats benchmark - Mode \"{mode}\", Type \"{type}\" ===")
        for i, t in enumerate(results, 1):
            print(f"Run {i}: {t*1000/n:.2f} ms / appel")
        print(f"\nMoyenne: {avg_ms:.2f} ms / appel")

pygame.quit()
