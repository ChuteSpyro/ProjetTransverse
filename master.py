
import pygame
from projectile import Projectile


class Master(pygame.sprite.Sprite) :
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/mummy.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 2000
        self.rect.y = 200

    def damage(self, damage):
        self.health -= damage

        if self.health <= 0 :
            self.game.all_master.remove(self)
            self.kill()
            self.game.master = None

    def launch_master_projectile(self,angle,velocity=50):
        if self is not None:
            self.all_projectiles.add(Projectile(self,angle,velocity))


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
