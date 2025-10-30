from collections import defaultdict
import pygame


class SpatialHash:
    __slots__ = ("cell", "grid")

    def __init__(self, cell_size: int):
        self.cell = max(1, cell_size)
        self.grid: dict[tuple[int, int], list[pygame.Rect]] = defaultdict(list)

    def _cells_for_rect(self, r: pygame.Rect):
        cs = self.cell
        x0 = r.left // cs
        y0 = r.top // cs
        x1 = (r.right - 1) // cs
        y1 = (r.bottom - 1) // cs
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                yield (cx, cy)

    def collides(self, r: pygame.Rect) -> bool:
        for key in self._cells_for_rect(r):
            for other in self.grid.get(key, ()):  # tuple() évite alloc si manquant
                if r.colliderect(other):
                    return True
        return False

    def insert(self, r: pygame.Rect):
        for key in self._cells_for_rect(r):
            self.grid[key].append(r)


__all__ = ["SpatialHash"]
