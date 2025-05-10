
from map import generate_map

def load():
    WIDTH, HEIGHT = 4000, 720
    TILE_SIZE = 100
    return generate_map(WIDTH, HEIGHT, TILE_SIZE)