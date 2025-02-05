import pygame
from player import Player
from master import Master

class Game:
    def __init__(self):
        self.player = Player(self)
        self.master = Master()
        self.pressed = {}

    def check_collision(self, prite, group):
        return pygame.sprite.spritecollide(prite, group, False, pygame.sprite.collide_mask)

