import math


def new_position(t : float, ini_velocity: int, ini_pos: int, angle: float, gravity : float):
    x = ini_velocity * math.cos(angle) * t
    y = ini_pos + ini_velocity * math.sin(angle) * t - (1/2 * gravity * t**2)
    return x, y
