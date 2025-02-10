import pygame
from player import Player
from master import Master

class Game:
    def __init__(self):
        self.all_player = pygame.sprite.Group()
        self.player = Player(self)
        self.all_player.add(self.player)

        self.all_master = pygame.sprite.Group()
        self.master = Master(self)
        self.all_master.add(self.master)

        self.pressed = {}

    def check_collision(self, prite, group):
        return pygame.sprite.spritecollide(prite, group, False, pygame.sprite.collide_mask)

