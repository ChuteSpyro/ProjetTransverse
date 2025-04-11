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
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 550

    def damage(self, damage):
        self.health -= damage

        if self.health <= 0 :
            self.game.all_master.remove(self)
            self.kill()
            self.game.master = None

    def launch_master_projectile(self,angle,velocity=50):
        if self is not None:
            self.all_projectiles.add(Projectile(self,angle,velocity))


    def update_health_bar(self,surface):
        bar_color = (111,210,46)
        back_bar_color = (60,63,60)

        bar_position = [self.rect.x + 10 ,self.rect.y - 20,self.health,5]
        back_bar_position = [self.rect.x + 10 ,self.rect.y - 20,self.max_health,5]

        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)


