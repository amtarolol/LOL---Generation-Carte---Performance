import random
from typing import Iterable


def iter_candidate_cells(map_w: int, map_h: int, cell_size: int, rng: random.Random) -> Iterable[tuple[int, int]]:
    """Renvoie les coins haut‑gauche des cellules (mélangés)."""
    cols = max(1, map_w // cell_size)
    rows = max(1, map_h // cell_size)
    idxs = [(cx, cy) for cx in range(cols) for cy in range(rows)]
    rng.shuffle(idxs)
    for cx, cy in idxs:
        yield cx * cell_size, cy * cell_size


__all__ = ["iter_candidate_cells"]