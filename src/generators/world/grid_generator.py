import time
import random
from typing import Optional
import pygame

from utils.Tools import Tools
from .types import PlacementConfig, GenStats
from .spatial_hash import SpatialHash
from .candidates import iter_candidate_cells


def _rng_from_seed(seed: Optional[int]) -> random.Random:
    return random.Random(seed) if seed is not None else random


def _compute_cell(obj_get_size):
    w, h = obj_get_size()
    return w, h, max(w, h)


def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(v, hi))


def _within_lane_limit(cfg: PlacementConfig, center: tuple[int, int]) -> bool:
    dist = Tools.get_distance_line_point(cfg.lane.start, cfg.lane.end, center)
    return dist <= cfg.lane.min_distance


class GridGenerator:
    def __init__(self, cfg: PlacementConfig, existing_rects: Optional[list[pygame.Rect]] = None):
        self.cfg = cfg
        self.rng = _rng_from_seed(cfg.seed)
        self.obj_w, self.obj_h, self.cell = _compute_cell(cfg.object_spec.get_size)
        self.max_x = max(0, cfg.bounds.width - self.obj_w)
        self.max_y = max(0, cfg.bounds.height - self.obj_h)

        # Spatial hash
        self.spatial = SpatialHash(self.cell)
        self.rects: list[pygame.Rect] = []

        if existing_rects:
            for r in existing_rects:
                self.spatial.insert(r)
            # ⬅️ extend une seule fois (en dehors de la boucle)
            self.rects.extend(existing_rects)

        self.counters = {"total_attempts": 0, "lane_rejected": 0, "collisions_rejected": 0}

    def place(self):
        t0 = time.perf_counter()
        placed: list[pygame.sprite.Sprite] = []

        if self.cfg.placement_mode == "grid":
            placed.extend(self._place_with_grid())

        remaining = self.cfg.count - len(placed)
        if self.cfg.placement_mode == "random" or remaining > 0:
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
        )
        return placed, self.rects, stats

    def _attempt_place(self, top_left: tuple[int, int]):
        x, y = top_left
        self.counters["total_attempts"] += 1

        x = _clamp(x, 0, self.max_x)
        y = _clamp(y, 0, self.max_y)

        cx, cy = x + (self.obj_w // 2), y + (self.obj_h // 2)

        if _within_lane_limit(self.cfg, (cx, cy)):
            self.counters["lane_rejected"] += 1
            return False, None

        test_rect = pygame.Rect(x, y, self.obj_w, self.obj_h)
        if self.spatial.collides(test_rect):
            self.counters["collisions_rejected"] += 1
            return False, None

        spr = self.cfg.object_spec.factory((cx, cy))
        self.spatial.insert(spr.rect)
        return True, spr

    def _place_with_grid(self):
        sprites: list[pygame.sprite.Sprite] = []
        jitter_x = int(self.cell * self.cfg.cell_jitter_fraction)
        jitter_y = int(self.cell * self.cfg.cell_jitter_fraction)

        for gx, gy in iter_candidate_cells(self.cfg.bounds.width, self.cfg.bounds.height, self.cell, self.rng):
            if len(sprites) >= self.cfg.count:
                break
            off_x = self.rng.randint(-jitter_x, jitter_x) if jitter_x > 0 else 0
            off_y = self.rng.randint(-jitter_y, jitter_y) if jitter_y > 0 else 0
            ok, spr = self._attempt_place((gx + off_x, gy + off_y))
            if ok and spr:
                sprites.append(spr)
        return sprites

    def _place_with_random(self, remaining: int):
        sprites: list[pygame.sprite.Sprite] = []
        for _ in range(remaining):
            for _ in range(self.cfg.max_attempts_per_item):
                rx = self.rng.randint(0, self.max_x) if self.max_x > 0 else 0
                ry = self.rng.randint(0, self.max_y) if self.max_y > 0 else 0
                ok, spr = self._attempt_place((rx, ry))
                if ok and spr:
                    sprites.append(spr)
                    break
        return sprites


__all__ = ["GridGenerator"]
