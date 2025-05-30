import pygame
import random

def generate_map(width, height, tile_size,map_name):
    if map_name == "Earth":
        DIRT = (139, 69, 19)
        GRASS = (34, 139, 34)
    elif map_name == "Moon":
        DIRT = (120, 120, 120)
        GRASS = (180, 180, 180)
    elif map_name == "Mars":
        DIRT = (178, 34, 34)
        GRASS = (255, 140, 0)



    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    x = 0
    y = height - random.randint(5, 7) * tile_size

    while x < width:
        flat_length = random.randint(2, 4) * tile_size
        delta_y = random.choice([-1, 0, 1]) * tile_size

        x_end = x + flat_length
        # Segment plat
        pygame.draw.rect(surface, DIRT, (x, y, flat_length, height - y + 30))  # +20 pixels en bas
        pygame.draw.rect(surface, GRASS, (x, y, flat_length, 10))

        if delta_y != 0:
            x_slope = x_end + abs(delta_y)
            y_new = max(tile_size * 2, min(y + delta_y, height - tile_size))
            # Pente
            # Pente
            pygame.draw.polygon(surface, DIRT, [(x_end, y), (x_slope, y_new), (x_slope, height), (x_end, height)])

            dx = x_slope - x_end
            dy = y_new - y

            for j in range(abs(dx)):
                t = j / abs(dx)
                x_line = x_end + j if dx > 0 else x_end - j
                y_line = int(y + t * dy)
                pygame.draw.line(surface, GRASS, (x_line, y_line), (x_line, y_line + 10))
            x = x_slope
            y = y_new
        else:
            x = x_end

    # Ground at the bottom of the screen
    pygame.draw.rect(surface, DIRT, (0, height - tile_size, width, tile_size))

    mask = pygame.mask.from_surface(surface)
    return surface, mask