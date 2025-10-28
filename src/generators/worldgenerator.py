# generators/worldgen.py
import time
import random
import pygame
from dataclasses import dataclass
from entities.Bush import Bush
from entities.Buff import Buff
from utils.Tools import Tools

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

def _check_collide(rect: pygame.Rect, rects: list[pygame.Rect]) -> bool:
    return any(rect.colliderect(r) for r in rects)

def generate_sprites(
    count: int,
    map_w: int,
    map_h: int,
    *,
    get_size,                     # -> (w, h)
    factory,                      # (cx, cy) -> Sprite
    lane_start: tuple[int, int],
    lane_end: tuple[int, int],
    dist_to_lane_min: int = 20,   # marge à la lane
    max_attempts: int = 100,
    existing_rects: list[pygame.Rect] | None = None,
    rng: random.Random | None = None,
    tools_cls=None,               # classe Tools avec get_distance_line_point
):
    """
    Place `count` sprites en évitant: (1) la lane (marge) (2) les collisions.
    Retourne (sprites, rects cumulés, stats).
    """
    assert tools_cls is not None, "tools_cls (Tools) est requis"

    rng = rng or random
    sprites: list[pygame.sprite.Sprite] = []
    rects: list[pygame.Rect] = list(existing_rects) if existing_rects else []

    w, h = get_size()

    total_attempts = 0
    lane_rejected = 0
    collisions_rejected = 0

    t0 = time.perf_counter()

    for _ in range(count):
        placed = False
        for _ in range(max_attempts):
            total_attempts += 1

            # bornes de tirage sûres même si map_w == w
            if map_w <= w or map_h <= h:
                x = 0
                y = 0
            else:
                x = rng.randint(0, map_w - w)
                y = rng.randint(0, map_h - h)

            cx, cy = x + w // 2, y + h // 2

            # filtre lane
            if tools_cls.get_distance_line_point(lane_start, lane_end, (cx, cy)) <= dist_to_lane_min:
                lane_rejected += 1
                continue

            test = pygame.Rect(x, y, w, h)
            if _check_collide(test, rects):
                collisions_rejected += 1
                continue

            sprite = factory((cx, cy))
            sprites.append(sprite)
            rects.append(sprite.rect)
            placed = True
            break

        # si non placé après max_attempts, on abandonne silencieusement

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    placed = len(sprites)
    stats = GenStats(
        requested=count,
        placed=placed,
        total_attempts=total_attempts,
        lane_rejected=lane_rejected,
        collisions_rejected=collisions_rejected,
        success_rate=(placed / count) if count else 0.0,
        avg_attempts_per_placed=(total_attempts / placed) if placed else 0.0,
        elapsed_ms=elapsed_ms,
    )
    return sprites, rects, stats



def bush_generation(n, W, H, p0, p1, *, dist_to_lane_min=20, max_attempts=100, existing_rects=None, seed=None):
    rng = random.Random(seed) if seed is not None else None
    return generate_sprites(
        n, W, H,
        get_size=Bush.get_size,
        factory=lambda pos: Bush(pos),
        lane_start=p0, lane_end=p1,
        dist_to_lane_min=dist_to_lane_min,
        max_attempts=max_attempts,
        existing_rects=existing_rects,
        rng=rng,
        tools_cls=Tools,
    )

def buff_generation(n, W, H, p0, p1, *, dist_to_lane_min=20, max_attempts=100, existing_rects=None, seed=None):
    rng = random.Random(seed) if seed is not None else None
    return generate_sprites(
        n, W, H,
        get_size=Buff.get_size,
        factory=lambda pos: Buff(pos),
        lane_start=p0, lane_end=p1,
        dist_to_lane_min=dist_to_lane_min,
        max_attempts=max_attempts,
        existing_rects=existing_rects,
        rng=rng,
        tools_cls=Tools,
    )
