from dataclasses import dataclass

@dataclass
class GenStats:
    requested: int
    placed: int
    total_attempts: int
    collisions_rejected: int
    lane_rejected: int
    avg_attempts_per_placed: float
    success_rate: float
    elapsed_ms: float
