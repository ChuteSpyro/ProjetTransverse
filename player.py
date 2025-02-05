import pygame
from projectile import Projectile


class Player(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 510

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
