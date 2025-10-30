import time
import random
from typing import Optional, List, Tuple
import pygame
import math

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

def _calculate_valid_regions(cfg: PlacementConfig, cell_size: int) -> List[Tuple[int, int, int, int]]:
    """Pré-calcule les régions valides pour le placement (éloignées de la lane)."""
    regions = []
    
    # Calculer l'équation de la ligne
    x1, y1 = cfg.lane.start
    x2, y2 = cfg.lane.end
    
    if x2 - x1 != 0:
        # Calculer la pente et l'ordonnée à l'origine
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        
        # Diviser la carte en grille de cellules
        for x in range(0, cfg.bounds.width, cell_size):
            for y in range(0, cfg.bounds.height, cell_size):
                # Vérifier les quatre coins de la cellule
                corners = [(x, y), (x + cell_size, y),
                          (x, y + cell_size), (x + cell_size, y + cell_size)]
                
                valid = True
                for cx, cy in corners:
                    dist = Tools.get_distance_line_point(cfg.lane.start, cfg.lane.end, (cx, cy))
                    if dist <= cfg.lane.min_distance:
                        valid = False
                        break
                
                if valid:
                    regions.append((x, y, cell_size, cell_size))
    
    return regions

class GridGenerator:
    def __init__(self, cfg: PlacementConfig, existing_rects: Optional[list[pygame.Rect]] = None):
        self.cfg = cfg
        self.rng = _rng_from_seed(cfg.seed)
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

        if self.cfg.placement_mode == "grid":
            placed.extend(self._place_with_grid())

        remaining = self.cfg.count - len(placed)
        if remaining > 0:
            # Ajuster dynamiquement la stratégie en fonction du nombre restant
            if remaining > self.cfg.count * 0.5:  # Si plus de 50% reste à placer
                placed.extend(self._place_with_adaptive(remaining))
            else:
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
            algorithm=self.cfg.placement_mode
        )
        print(f"Placement stats for {self.cfg.object_spec.factory.__name__ if hasattr(self.cfg.object_spec.factory, '__name__') else str(self.cfg.object_spec.factory)}:")
        print(f"Requested: {self.cfg.count}, Placed: {placed_n}")
        print(f"Total attempts: {self.counters['total_attempts']}")
        print(f"Lane rejected: {self.counters['lane_rejected']}")
        print(f"Collisions rejected: {self.counters['collisions_rejected']}")
        print(f"Success rate: {stats.success_rate:.2%}")
        print(f"Avg attempts per placed: {stats.avg_attempts_per_placed:.2f}")
        print(f"Elapsed ms: {elapsed_ms:.2f}")
        return placed, self.rects, stats

    def _attempt_place(self, top_left: tuple[int, int]) -> Tuple[bool, Optional[pygame.sprite.Sprite]]:
        x, y = top_left
        self.counters["total_attempts"] += 1

        x = _clamp(x, 0, self.max_x)
        y = _clamp(y, 0, self.max_y)

        cx, cy = x + (self.obj_w // 2), y + (self.obj_h // 2)

        test_rect = pygame.Rect(x, y, self.obj_w, self.obj_h)
        if self.spatial.collides(test_rect):
            self.counters["collisions_rejected"] += 1
            return False, None

        spr = self.cfg.object_spec.factory((cx, cy))
        self.spatial.insert(spr.rect)
        return True, spr

    def _place_with_grid(self) -> List[pygame.sprite.Sprite]:
        sprites: list[pygame.sprite.Sprite] = []
        if self.cfg.count == 0:
            print("Warning: self.cfg.count is zero in _place_with_grid, returning empty list.")
            return sprites
        jitter_fraction = min(0.4, self.cfg.cell_jitter_fraction * 
                            (1 - len(sprites) / self.cfg.count))  # Réduit le jitter progressivement
        jitter_x = int(self.cell * jitter_fraction)
        jitter_y = int(self.cell * jitter_fraction)

        for region in self.valid_regions:
            if len(sprites) >= self.cfg.count:
                break
            rx, ry, rw, rh = region
            x = rx + self.rng.randint(-jitter_x, jitter_x) if jitter_x > 0 else rx
            y = ry + self.rng.randint(-jitter_y, jitter_y) if jitter_y > 0 else ry
            ok, spr = self._attempt_place((x, y))
            if ok and spr:
                sprites.append(spr)

        return sprites

    def _place_with_adaptive(self, remaining: int) -> List[pygame.sprite.Sprite]:
        sprites: list[pygame.sprite.Sprite] = []
        attempts_per_region = max(1, remaining // len(self.valid_regions))
        
        for region in self.valid_regions:
            if len(sprites) >= remaining:
                break
                
            rx, ry, rw, rh = region
            for _ in range(attempts_per_region):
                x = rx + self.rng.randint(0, rw - self.obj_w)
                y = ry + self.rng.randint(0, rh - self.obj_h)
                
                ok, spr = self._attempt_place((x, y))
                if ok and spr:
                    sprites.append(spr)
                    break
                    
        return sprites

    def _place_with_random(self, remaining: int) -> List[pygame.sprite.Sprite]:
        sprites: list[pygame.sprite.Sprite] = []
        max_attempts = self.cfg.max_attempts_per_item * 2  # Double les tentatives pour le placement aléatoire
        
        for _ in range(remaining):
            for _ in range(max_attempts):
                region = self.rng.choice(self.valid_regions)
                rx, ry, rw, rh = region
                x = rx + self.rng.randint(0, rw - self.obj_w)
                y = ry + self.rng.randint(0, rh - self.obj_h)
                
                ok, spr = self._attempt_place((x, y))
                if ok and spr:
                    sprites.append(spr)
                    break
                    
        return sprites

__all__ = ["GridGenerator"]