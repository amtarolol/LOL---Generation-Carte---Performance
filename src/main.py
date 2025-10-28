import random
import tkinter as tk

MAP_WIDTH = 50
MAP_HEIGHT = 50
TILE_SIZE = 12

TILES = ['E', 'J', 'B', 'L', 'P']

COLORS = {
    'E': '#ffffff',
    'J': '#006000',
    'B': '#b000e5',
    'L': '#00ccee',
    'P': '#808080'
}

def create_empty_map(width, height):
    return [['E' for _ in range(width)] for _ in range(height)]

def generate_2d_map_with_paths(grid):
    height = len(grid)
    width = len(grid[0])
    
    # Borders
    for y in range(height):
        for x in range(width):
            if x == 0 or x == width-1 or y == 0 or y == height-1:
                grid[y][x] = 'L'
    
    # Jungle clusters
    num_clusters = int((width * height) * 0.05)
    for _ in range(num_clusters):
        cx = random.randint(1, width-2)
        cy = random.randint(1, height-2)
        cluster_size = random.randint(3, 5)
        for dy in range(-cluster_size, cluster_size+1):
            for dx in range(-cluster_size, cluster_size+1):
                nx, ny = cx + dx, cy + dy
                if 1 <= nx < width-1 and 1 <= ny < height-1:
                    if random.random() < 0.6:
                        grid[ny][nx] = 'J'
    
    # Buffs scattered
    num_buffs = int((width * height) * 0.02)
    for _ in range(num_buffs):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        grid[y][x] = 'B'
    
    # Paths
    num_paths = 2
    for _ in range(num_paths):
        y = random.randint(1, height-2)
        x = 1
        while x < width-1:
            grid[y][x] = 'P'
            if random.random() < 0.3:
                y += random.choice([-1, 0, 1])
                y = max(1, min(height-2, y))
            x += 1
    
    return grid

def draw_map_with_dragon(grid, dragon_pos=(25,25)):
    root = tk.Tk()
    root.title("2D Map with Dragon")

    canvas = tk.Canvas(root, width=MAP_WIDTH*TILE_SIZE, height=MAP_HEIGHT*TILE_SIZE)
    canvas.pack()

    # Draw tiles
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            color = COLORS[grid[y][x]]
            x1 = x * TILE_SIZE
            y1 = y * TILE_SIZE
            x2 = x1 + TILE_SIZE
            y2 = y1 + TILE_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')

    # Load dragon image
    dragon_img = tk.PhotoImage(file="dragon.png")  # Must be in same folder
    # Place dragon at dragon_pos
    dx, dy = dragon_pos
    canvas.create_image(dx*TILE_SIZE + TILE_SIZE//2, dy*TILE_SIZE + TILE_SIZE//2, image=dragon_img)

    # Keep reference to avoid garbage collection
    canvas.image = dragon_img

    root.mainloop()

# ----------------------------
if __name__ == "__main__":
    map_grid = generate_2d_map_with_paths(create_empty_map(MAP_WIDTH, MAP_HEIGHT))
    draw_map_with_dragon(map_grid, dragon_pos=(25,25))
