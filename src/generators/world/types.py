from dataclasses import dataclass
from typing import Callable, Optional, Tuple
import pygame


@dataclass
class GenStats:
    requested: int
    placed: int
    total_attempts: int
    lane_rejected: int
    collisions_rejected: int
    success_rate: float
    avg_attempts_per_placed: float
    elapsed_ms: float
    algorithm: str


@dataclass(frozen=True)
class MapBounds:
    width: int
    height: int


@property
def size(self) -> Tuple[int, int]:
    return (self.width, self.height)


@dataclass(frozen=True)
class Lane:
    start: Tuple[int, int]
    end: Tuple[int, int]
    min_distance: int


@dataclass(frozen=True)
class ObjectSpec:
    """Spécifie l'objet à placer.
    get_size: () -> (w, h)
    factory: (center_x, center_y) -> pygame.sprite.Sprite
    """
    get_size: Callable[[], tuple[int, int]]
    factory: Callable[[tuple[int, int]], pygame.sprite.Sprite]


@dataclass(frozen=True)
class PlacementConfig:
    count: int
    bounds: MapBounds
    lane: Lane
    object_spec: ObjectSpec
    placement_mode: str = "random" # "random" | "adaptive"
    max_attempts_per_item: int = 100
    cell_jitter_fraction: float = 0.3


__all__ = [
"GenStats",
"MapBounds",
"Lane",
"ObjectSpec",
"PlacementConfig",
]