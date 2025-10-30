import random
import pygame
from typing import Optional
from entities.Bush import Bush
from entities.Buff import Buff
from .types import PlacementConfig, MapBounds, Lane, ObjectSpec
from .grid_generator_improved import GridGenerator


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
    )
    
    gen = GridGenerator(cfg, existing_rects=existing_object_rects)
    return gen.place()


__all__ = [
"generate_sprites",
]