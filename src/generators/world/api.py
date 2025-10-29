import random
import pygame
from typing import Optional
from entities.Bush import Bush
from entities.Buff import Buff
from .types import PlacementConfig, MapBounds, Lane, ObjectSpec
from .grid_generator import GridGenerator


def generate_sprites(
    total_to_place: int,
    map_width: int,
    map_height: int,
    *,
    get_size,
    factory,
    lane_start_point: tuple[int, int],
    lane_end_point: tuple[int, int],
    min_distance_to_lane: int,
    max_placement_attempts: int,
    existing_object_rects: Optional[list[pygame.Rect]],
    rng: Optional[random.Random],
    placement_mode: str,
    cell_jitter_fraction: float = 0.3,
    ):
    
    cfg = PlacementConfig(
        count=total_to_place,
        bounds=MapBounds(map_width, map_height),
        lane=Lane(lane_start_point, lane_end_point, min_distance_to_lane),
        object_spec=ObjectSpec(get_size=get_size, factory=factory),
        placement_mode=placement_mode,
        max_attempts_per_item=max_placement_attempts,
        cell_jitter_fraction=cell_jitter_fraction,
        seed=(rng.seed if isinstance(rng, random.Random) and hasattr(rng, "seed") else None),
    )
    
    gen = GridGenerator(cfg, existing_rects=existing_object_rects)
    return gen.place()



def bush_generation(n, W, H, p0, p1, *, dist_to_lane_min=200, max_attempts=100, existing_rects=None, seed=None, placement):
    rng = random.Random(seed) if seed is not None else None
    cfg = PlacementConfig(
        count=n,
        bounds=MapBounds(W, H),
        lane=Lane(p0, p1, dist_to_lane_min),
        object_spec=ObjectSpec(get_size=Bush.get_size, factory=lambda pos: Bush(pos)),
        placement_mode=placement,
        max_attempts_per_item=max_attempts,
        seed=seed,
    )
    return GridGenerator(cfg, existing_rects).place()




def buff_generation(n, W, H, p0, p1, *, dist_to_lane_min=20, max_attempts=100, existing_rects=None, seed=None, placement):
    rng = random.Random(seed) if seed is not None else None
    cfg = PlacementConfig(
        count=n,
        bounds=MapBounds(W, H),
        lane=Lane(p0, p1, dist_to_lane_min),
        object_spec=ObjectSpec(get_size=Buff.get_size, factory=lambda pos: Buff(pos)),
        placement_mode=placement,
        max_attempts_per_item=max_attempts,
        seed=seed,
    )
    return GridGenerator(cfg, existing_rects).place()


__all__ = [
"generate_sprites",
"bush_generation",
"buff_generation",
]