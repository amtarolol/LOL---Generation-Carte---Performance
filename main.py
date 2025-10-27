import random

# ----------------------------
# Paramètres de la carte
# ----------------------------
MAP_WIDTH = 10
MAP_HEIGHT = 10

# Symboles :
# L = Lane, J = Jungle, B = Buff, E = Empty
TILES = ['E', 'J', 'B', 'L']

# ----------------------------
# Fonction pour créer une carte vide
# ----------------------------
def create_empty_map(width, height):
    return [['E' for _ in range(width)] for _ in range(height)]

# ----------------------------
# Fonction pour générer aléatoirement les éléments
# ----------------------------
def generate_map(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # On fixe des lanes fixes pour simplifier
            if x == 0 or x == len(grid[0])-1:
                grid[y][x] = 'L'
            else:
                grid[y][x] = random.choices(
                    ['E', 'J', 'B'], weights=[0.6, 0.3, 0.1])[0]
    return grid

# ----------------------------
# Affichage en console
# ----------------------------
def display_map(grid):
    for row in grid:
        print(' '.join(row))
    print("\n")

# ----------------------------
# Calcul d'une métrique simple : nombre de buffs
# ----------------------------
def count_buffs(grid):
    return sum(row.count('B') for row in grid)

# ----------------------------
# Exemple d'utilisation
# ----------------------------
if __name__ == "__main__":
    grid = create_empty_map(MAP_WIDTH, MAP_HEIGHT)
    grid = generate_map(grid)
    display_map(grid)
    
    buffs = count_buffs(grid)
    print(f"Nombre de buffs générés : {buffs}")
