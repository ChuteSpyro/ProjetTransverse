

import pygame
from projectile import Projectile


class Player(pygame.sprite.Sprite) :
    def __init__(self, game, selection):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.all_projectiles = pygame.sprite.Group()
        if selection['character'] == 'fleur':
            self.image = pygame.image.load('assets/characters/fleur.png')
            self.image = pygame.transform.scale(self.image, (150, 150))
        if selection['character'] == 'ghost':
            self.image = pygame.image.load('assets/characters/ghost.png')
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 2000
        self.rect.y = 100

    def damage(self, damage):
        self.health -= damage

        if self.health <= 0 :
            self.game.all_player.remove(self)
            self.kill()
            self.game.player = None

    def launch_player_projectile(self,angle,selection,velocity=50):
        if self is not None:
            self.all_projectiles.add(Projectile(self,angle,selection,velocity))

    def update_health_bar(self, surface, camera):
        bar_color = (111,210,46)
        back_bar_color = (60,63,60)

        bar_position = [self.rect.x + 10 - camera.offset.x,
                        self.rect.y - 20 - camera.offset.y,
                        self.health, 5]
        back_bar_position = [self.rect.x + 10 - camera.offset.x,
                             self.rect.y - 20 - camera.offset.y,
                             self.max_health, 5]

        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
