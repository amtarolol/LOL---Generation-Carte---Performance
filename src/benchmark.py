import pygame
from generators.world.api import generate_sprites
import time
import tracemalloc
import statistics
import pygame


# --- MOCKS pour faire tourner le benchmark ---
# Sprite simple
class Buff(pygame.sprite.Sprite):
    _frame_size = (128, 128)     # (w, h)

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface(Buff._frame_size)
        self.rect = self.image.get_rect(center=pos)

    @staticmethod
    def get_size():
        return Buff._frame_size


class Bush(pygame.sprite.Sprite):

    def __init__(self, pos, bush_type=None):
        super().__init__()
        # Charger ou récupérer l'image depuis le cache
        self.image = pygame.Surface(self.get_size())
        self.rect = self.image.get_rect(center=pos)
    
    @classmethod
    def get_size(cls):
        return (32, 32)


# --- Benchmark Function ---
def benchmark_with_tracemalloc(func, repeat=10):
    mem_peaks = []
    results = []

    for _ in range(repeat):
        tracemalloc.start()

        result = func()

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        mem_peaks.append(peak / 1024)  # Ko
        results.append(result[2])

    return {
        "results": results,
        "mean_mem_kb": statistics.mean(mem_peaks),
        "std_mem_kb": statistics.stdev(mem_peaks) if repeat > 1 else 0,
    }


def print_results(stats_list):
    
    # Helper pour gérer les divisions / attributs manquants
    def safe_get(attr):
        return [getattr(s, attr, 0) for s in stats_list]

    # Calcul des moyennes
    avg = {
        "requested": statistics.mean(safe_get("requested")),
        "placed": statistics.mean(safe_get("placed")),
        "total_attempts": statistics.mean(safe_get("total_attempts")),
        "lane_rejected": statistics.mean(safe_get("lane_rejected")),
        "collisions_rejected": statistics.mean(safe_get("collisions_rejected")),
        "success_rate": statistics.mean(safe_get("success_rate")),
        "avg_attempts_per_placed": statistics.mean(safe_get("avg_attempts_per_placed")),
        "elapsed_ms": statistics.mean(safe_get("elapsed_ms")),
    }

    # Calcul des écarts-types (si plusieurs runs)
    std = {}
    if len(stats_list) > 1:
        std = {
            "elapsed_ms": statistics.stdev(safe_get("elapsed_ms")),
            "success_rate": statistics.stdev(safe_get("success_rate")),
        }

        # --- Affichage ---
    print(f"🧩 Objets demandés : {avg['requested']:.0f}")
    print(f"✅ Objets placés : {avg['placed']:.1f}")
    print(f"🎯 Taux de succès : {avg['success_rate']*100:.2f}% - Ecart type : {std.get('success_rate', 0)*100:.2f}%")
    print(f"🔁 Tentatives totales : {avg['total_attempts']:.1f}")
    print(f"🚧 Rejets (lane): {avg['lane_rejected']:.1f} | collisions: {avg['collisions_rejected']:.1f}")
    print(f"⚙️  Moy. tentatives/placement : {avg['avg_attempts_per_placed']:.2f}")
    print(f"⏱ Temps moyen : {avg['elapsed_ms']:.2f} - Ecart type : {std.get('elapsed_ms', 0):.2f} ms")


# --- Boucle de test ---
modes = ["random", "grid"]
types = [Buff, Bush]

pygame.init()

for type in types:
    for mode in modes:
        def run():
            return generate_sprites(
                total_to_place=3000,
                map_width=1000,
                map_height=1000,
                get_size=type.get_size,
                factory=lambda pos: type(pos),
                lane_start_point=(0, 50),
                lane_end_point=(1000, 950),
                min_distance_to_lane=20,
                max_placement_attempts=100,
                existing_object_rects=[],
                rng=0,
                placement_mode=mode,
            )

        result = benchmark_with_tracemalloc(run, repeat=10)

        print(f"=== {str(type):<5} | Mode: {mode:<6} ===")
        print_results(result["results"])
        print(f"💾 Pic mémoire : {result['mean_mem_kb']:.1f} - Ecart type : {result['std_mem_kb']:.1f} Ko\n")

pygame.quit()