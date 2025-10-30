import time
import random
from typing import Optional, List, Tuple
import pygame
import math

from utils.Tools import Tools
from .types import PlacementConfig, GenStats
from .spatial_hash import SpatialHash
from .candidates import iter_candidate_cells

def _compute_cell(obj_get_size):
    w, h = obj_get_size()
    return w, h, max(w, h)

def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))

def _calculate_valid_regions(cfg: PlacementConfig, cell_size: int) -> List[Tuple[int, int, int, int]]:
    """Pré-calcule des régions éloignées de la lane pour l'heuristique 'adaptive'."""
    regions: List[Tuple[int, int, int, int]] = []
    for x in range(0, cfg.bounds.width, cell_size):
        for y in range(0, cfg.bounds.height, cell_size):
            corners = [
                (x, y),
                (x + cell_size, y),
                (x, y + cell_size),
                (x + cell_size, y + cell_size),
            ]
            if all(
                Tools.get_distance_line_point(cfg.lane.start, cfg.lane.end, (cx, cy)) > cfg.lane.min_distance
                for cx, cy in corners
            ):
                regions.append((x, y, cell_size, cell_size))
    return regions


class GridGenerator:
    def __init__(self, cfg: PlacementConfig, existing_rects: Optional[list[pygame.Rect]] = None):
        self.cfg = cfg
        self.obj_w, self.obj_h, self.cell = _compute_cell(cfg.object_spec.get_size)
        self.max_x = max(0, cfg.bounds.width - self.obj_w)
        self.max_y = max(0, cfg.bounds.height - self.obj_h)

        # Spatial hash avec taille de cellule optimisée
        if cfg.count == 0:
            # Avoid division by zero, use default cell size
            optimal_cell_size = self.cell
            print("Warning: cfg.count is zero, using default cell size.")
        else:
            optimal_cell_size = int(math.sqrt((cfg.bounds.width * cfg.bounds.height) / (cfg.count * 4)))
        self.spatial = SpatialHash(max(optimal_cell_size, self.cell))
        self.rects: list[pygame.Rect] = []

        if existing_rects:
            for r in existing_rects:
                self.spatial.insert(r)
            self.rects.extend(existing_rects)

        # Pré-calculer les régions valides
        self.valid_regions = _calculate_valid_regions(cfg, self.cell)
        self.counters = {"total_attempts": 0, "lane_rejected": 0, "collisions_rejected": 0}

    def place(self):
        t0 = time.perf_counter()
        placed: list[pygame.sprite.Sprite] = []

        mode = self.cfg.placement_mode

        if mode == "random":
            placed.extend(self._place_with_random(self.cfg.count))
        elif mode == "adaptive":
            placed.extend(self._place_with_adaptive(self.cfg.count))
        else:
            # Fallback to random if an unknown mode is passed
            placed.extend(self._place_with_random(self.cfg.count))

        # Optional: top-up pass to hit the target count if a primary pass underfilled
        remaining = max(0, self.cfg.count - len(placed))
        if remaining > 0:
            placed.extend(self._place_with_random(remaining))

        for spr in placed:
            self.rects.append(spr.rect)

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        placed_n = len(placed)
        stats = GenStats(
            requested=self.cfg.count,
            placed=placed_n,
            total_attempts=self.counters["total_attempts"],
            lane_rejected=self.counters["lane_rejected"],
            collisions_rejected=self.counters["collisions_rejected"],
            success_rate=(placed_n / self.cfg.count) if self.cfg.count else 0.0,
            avg_attempts_per_placed=(self.counters["total_attempts"] / placed_n) if placed_n else 0.0,
            elapsed_ms=elapsed_ms,
            algorithm=mode,
        )
        return placed, self.rects, stats


    def _attempt_place(self, top_left: tuple[int, int]) -> Tuple[bool, Optional[pygame.sprite.Sprite]]:
        x, y = top_left
        self.counters["total_attempts"] += 1

        x = _clamp(x, 0, self.max_x)
        y = _clamp(y, 0, self.max_y)

        test_rect = pygame.Rect(x, y, self.obj_w, self.obj_h)

        # Lane avoidance: check the rect center (cheap & good enough) or tighten with more points if needed
        cx, cy = test_rect.center
        dist = Tools.get_distance_line_point(self.cfg.lane.start, self.cfg.lane.end, (cx, cy))
        if dist <= self.cfg.lane.min_distance:
            self.counters["lane_rejected"] += 1
            return False, None

        if self.spatial.collides(test_rect):
            self.counters["collisions_rejected"] += 1
            return False, None

        spr = self.cfg.object_spec.factory((cx, cy))
        self.spatial.insert(spr.rect)
        return True, spr


    def _place_with_adaptive(self, requested: int) -> List[pygame.sprite.Sprite]:
        sprites: list[pygame.sprite.Sprite] = []

        if len(self.valid_regions) < requested:
            for i in range(len(self.valid_regions)):
                rx, ry, rw, rh = self.valid_regions[i]

                ok, spr = self._attempt_place((rx, ry))
                if ok and spr:
                    self.spatial.insert(spr.rect)
                    sprites.append(spr)
        else:
            for i in range(requested):
                random_index = random.randint(0, len(self.valid_regions) - 1)
                rx, ry, rw, rh = self.valid_regions[random_index]
                ok, spr = self._attempt_place((rx, ry))
                if ok and spr:
                    self.spatial.insert(spr.rect)
                    sprites.append(spr)
        return sprites

        
    def _place_with_random(self, remaining: int):
        sprites: list[pygame.sprite.Sprite] = []
        for _ in range(remaining):
            for _ in range(self.cfg.max_attempts_per_item):
                rx = random.randint(0, self.max_x) if self.max_x > 0 else 0
                ry = random.randint(0, self.max_y) if self.max_y > 0 else 0
                ok, spr = self._attempt_place((rx, ry))
                if ok and spr:
                    sprites.append(spr)
                    break
        return sprites

__all__ = ["GridGenerator"]