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




from collections import defaultdict
import math

# --- helpers (ajouter en haut du fichier worldgen.py) ---
from collections import defaultdict

class SpatialHash:
    __slots__ = ("cell", "grid")
    def __init__(self, cell_size: int):
        self.cell = max(1, cell_size)
        self.grid: dict[tuple[int,int], list[pygame.Rect]] = defaultdict(list)

    def _cells_for_rect(self, r: pygame.Rect):
        cs = self.cell
        x0 = r.left // cs
        y0 = r.top  // cs
        x1 = (r.right - 1) // cs
        y1 = (r.bottom- 1) // cs
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                yield (cx, cy)

    def collides(self, r: pygame.Rect) -> bool:
        for key in self._cells_for_rect(r):
            for other in self.grid.get(key, ()):
                if r.colliderect(other):
                    return True
        return False

    def insert(self, r: pygame.Rect):
        for key in self._cells_for_rect(r):
            self.grid[key].append(r)

def _dist2_point_segment(ax, ay, bx, by, px, py) -> int:
    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    ab2 = abx*abx + aby*aby
    if ab2 == 0:
        dx, dy = px - ax, py - ay
        return dx*dx + dy*dy
    t = (apx*abx + apy*aby) / ab2
    if t < 0: t = 0
    elif t > 1: t = 1
    cx, cy = ax + t*abx, ay + t*aby
    dx, dy = px - cx, py - cy
    return int(dx*dx + dy*dy)

def _iter_candidate_cells(map_w, map_h, cell_size, rng):
    cols = max(1, map_w // cell_size)
    rows = max(1, map_h // cell_size)
    idxs = [(cx, cy) for cx in range(cols) for cy in range(rows)]
    rng.shuffle(idxs)
    for cx, cy in idxs:
        yield cx * cell_size, cy * cell_size

def generate_sprites(
    count: int,
    map_w: int,
    map_h: int,
    *,
    get_size,                      
    factory,                       
    lane_start: tuple[int, int],
    lane_end: tuple[int, int],
    dist_to_lane_min: int = 20,   
    max_attempts: int = 100,       
    existing_rects: list[pygame.Rect] | None = None,
    rng: random.Random | None = None,                
    placement: str = "grid",       
    cell_jitter_frac: float = 0.3  
):
    rng = rng or random

    sprites: list[pygame.sprite.Sprite] = []
    rects: list[pygame.Rect] = list(existing_rects) if existing_rects else []

    w, h = get_size()
    CELL = max(w, h)  

    hasher = SpatialHash(CELL)
    for r in rects:
        hasher.insert(r)

    total_attempts = 0
    lane_rejected = 0
    collisions_rejected = 0

    t0 = time.perf_counter()

    x_max = max(0, map_w - w)
    y_max = max(0, map_h - h)

    def try_place_at(x, y):
        nonlocal total_attempts, lane_rejected, collisions_rejected
        total_attempts += 1

        # clamp dans la map
        x = max(0, min(x, x_max))
        y = max(0, min(y, y_max))

        cx, cy = x + (w // 2), y + (h // 2)
        # _dist2_point_segment(ax, ay, bx, by, cx, cy) <= min_d2
        if Tools.get_distance_line_point(lane_start, lane_end, (cx, cy)) <= dist_to_lane_min:
            lane_rejected += 1
            return False

        test = pygame.Rect(x, y, w, h)
        if hasher.collides(test):
            collisions_rejected += 1
            return False

        spr = factory((cx, cy))
        sprites.append(spr)
        rects.append(spr.rect)
        hasher.insert(spr.rect)
        return True

    # --- 1) Placement "grille" ---
    if placement == "grid":
        jitter_x = int(CELL * cell_jitter_frac)
        jitter_y = int(CELL * cell_jitter_frac)
        for gx, gy in _iter_candidate_cells(map_w, map_h, CELL, rng):
            if len(sprites) >= count:
                break
            # petit décalage aléatoire dans la cellule
            jx = rng.randint(-jitter_x, jitter_x) if jitter_x > 0 else 0
            jy = rng.randint(-jitter_y, jitter_y) if jitter_y > 0 else 0
            try_place_at(gx + jx, gy + jy)

    # --- 2) Placement "aléatoire" ---
    remaining = count - len(sprites)
    if placement == "random" or remaining > 0:
        for _ in range(remaining):
            placed = False
            for _ in range(max_attempts):
                x = rng.randint(0, x_max) if x_max > 0 else 0
                y = rng.randint(0, y_max) if y_max > 0 else 0
                if try_place_at(x, y):
                    placed = True
                    break

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    placed_n = len(sprites)
    stats = GenStats(
        requested=count,
        placed=placed_n,
        total_attempts=total_attempts,
        lane_rejected=lane_rejected,
        collisions_rejected=collisions_rejected,
        success_rate=(placed_n / count) if count else 0.0,
        avg_attempts_per_placed=(total_attempts / placed_n) if placed_n else 0.0,
        elapsed_ms=elapsed_ms,
    )
    return sprites, rects, stats




def bush_generation(n, W, H, p0, p1, *, dist_to_lane_min=200, max_attempts=100, existing_rects=None, seed=None, placement="grid"):
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
        placement=placement,
    )

def buff_generation(n, W, H, p0, p1, *, dist_to_lane_min=20, max_attempts=100, existing_rects=None, seed=None, placement="grid"):
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
        placement=placement,
    )
def iter_candidate_cells(map_w, map_h, cell):
    cols = max(1, map_w // cell)
    rows = max(1, map_h // cell)
    cells = [(cx, cy) for cx in range(cols) for cy in range(rows)]
    random.shuffle(cells)
    for cx, cy in cells:
        x = cx * cell
        y = cy * cell
        yield x, y

