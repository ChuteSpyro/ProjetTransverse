import pygame

from player import Player
from master import Master

clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0
class Game:
    def __init__(self):
        self.is_playing = False

        self.all_player = pygame.sprite.Group()
        self.player = Player(self)
        self.all_player.add(self.player)

        self.all_master = pygame.sprite.Group()
        self.master = Master(self)
        self.all_master.add(self.master)

        self.pressed = {}


    def update(self,screen):
        if self.player is not None:
            screen.blit(self.player.image, self.player.rect)
            self.player.update_health_bar(screen)

        if self.master is not None:
            screen.blit(self.master.image, self.master.rect)
            self.master.update_health_bar(screen)

        if self.player is not None:
            for projectile in self.player.all_projectiles:
                projectile.move(dt)
            self.player.all_projectiles.draw(screen)

        if self.master is not None:
            for projectile in self.master.all_projectiles:
                projectile.move(dt)
            self.master.all_projectiles.draw(screen)








    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

