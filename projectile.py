import pygame
import math



class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 90
        self.player = player
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 125
        self.rect.y = player.rect.y + 100
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.origin_image = self.image
        self.time = 0.0
        self.rotate_angle = 0
        self.angle = math.radians(45)
        self.gravity = 9.81


    def rotate(self):
        self.rotate_angle += 20
        self.image = pygame.transform.rotozoom(self.origin_image, self.rotate_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        self.time += 0.01  # Incrémentation du temps
        self.rect.x = self.start_x + self.velocity * math.cos(self.angle) * self.time
        self.rect.y = self.start_y - (self.velocity * math.sin(self.angle) * self.time - (0.5 * self.gravity * self.time ** 2))
        self.rotate()

        for master in self.player.game.check_collision(self, self.player.game.all_master):
            self.remove()

            master.damage(self.player.attack)

        if self.rect.y > 1080:
            self.remove()


