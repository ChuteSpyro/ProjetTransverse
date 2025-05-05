import pygame
import random

# Couleurs
DIRT = (139, 69, 19)
GRASS = (34, 139, 34)


def generate_soft_terrain(width, height, tile_size):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    segments = []
    current_x = 0
    ground_y = height - random.randint(3, 5) * tile_size
    segments.append((current_x, ground_y))

    while current_x < width:
        # Longueur d'un segment plat
        seg_len = random.randint(2, 4)
        seg_width = seg_len * tile_size

        # Choix aléatoire : -1, 0, ou +1 tile
        delta = random.choice([-1, 0, 1])
        slope_height = delta * tile_size
        slope_width = abs(slope_height)  # pente à 45°

        # Nouvelle position horizontale
        flat_x_end = current_x + seg_width
        slope_x_end = flat_x_end + slope_width

        # Calcul nouvelle hauteur (en respectant les limites)
        new_y = ground_y + slope_height
        new_y = max(tile_size * 2, min(new_y, height - tile_size))

        # Ajouter segment plat
        segments.append((flat_x_end, ground_y))


        if delta != 0: #if delta is not 0 we need a slope
            segments.append((slope_x_end, new_y))
            current_x = slope_x_end
            ground_y = new_y
        else:
            current_x = flat_x_end


    for i in range(len(segments) - 1):# wez draw the terrain
        x1, y1 = segments[i]
        x2, y2 = segments[i + 1]

        if y1 == y2:
            # Segment plat
            pygame.draw.rect(surface, DIRT, (x1, y1, x2 - x1, height - y1))
            pygame.draw.rect(surface, GRASS, (x1, y1, x2 - x1, 10))
        else:
            # Pente à 45°
            points = [(x1, y1), (x2, y2), (x2, height), (x1, height)]
            pygame.draw.polygon(surface, DIRT, points)

            # Gazon sur la pente
            grass_thickness = 10
            length = abs(x2 - x1)
            for j in range(length):
                x = x1 + j if x2 > x1 else x1 - j
                y = y1 + j if y2 > y1 else y1 - j
                pygame.draw.line(surface, GRASS, (x, y), (x, y + grass_thickness))

    return surface