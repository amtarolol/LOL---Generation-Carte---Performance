import random
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# ----------------------------
# Paramètres
# ----------------------------
MAP_WIDTH = 50
MAP_HEIGHT = 50
TILES = ['E', 'J', 'B', 'L']

# Couleurs pour l’affichage
COLORS = {
    'E': (1.0, 1.0, 1.0),
    'J': (0.0, 0.6, 0.0),
    'B': (0.7, 0.0, 0.9),
    'L': (0.0, 0.8, 1.0)
}

# ----------------------------
# Fonctions utilitaires
# ----------------------------
def create_empty_map(width, height):
    return [['E' for _ in range(width)] for _ in range(height)]

def count_buffs(grid):
    return sum(row.count('B') for row in grid)

# ----------------------------
# Algorithmes de génération
# ----------------------------
def generate_random(grid):
    height = len(grid)
    width = len(grid[0])
    
    for y in range(height):
        for x in range(width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                grid[y][x] = 'L'
            else:
                grid[y][x] = random.choices(['E', 'J', 'B'], weights=[0.6, 0.3, 0.1])[0]
    return grid

# ----------------------------


def display_map(grid):

    height = len(grid)
    width = len(grid[0])
    img = np.zeros((height, width, 3))

    for y in range(height):
        for x in range(width):
            img[y, x] = COLORS[grid[y][x]]

    plt.figure(figsize=(8, 8))
    plt.imshow(img, interpolation='nearest')
    plt.axis('off')

    # Légende
    legend_patches = [mpatches.Patch(color=COLORS[tile], label=tile) for tile in TILES]
    plt.legend(handles=legend_patches, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()


# ----------------------------
# Programme principal
# ----------------------------
if __name__ == "__main__":
    display_map(generate_random(create_empty_map(MAP_WIDTH, MAP_HEIGHT)))
