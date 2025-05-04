import pygame
import math



class Projectile(pygame.sprite.Sprite):
    def __init__(self, user,angle,velocity):
        super().__init__()
        self.velocity = velocity*1.5
        self.user = user
        self.image = pygame.image.load('assets/dagger.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=user.rect.center)
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.origin_image = self.image
        self.time = 0.0
        self.rotate_angle = 0
        self.angle = angle
        self.gravity = 9.81


    def rotate(self):
        self.rotate_angle += 20
        self.image = pygame.transform.rotozoom(self.origin_image, self.rotate_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.user.all_projectiles.remove(self)

    def move(self,dt):
        self.time += dt*8  # Incrémentation du temps
        self.rect.x = self.start_x + self.velocity * math.cos(self.angle) * self.time #Ici, on calcule les cordonnées x et y du projectile et on associe l'image du projectile avec ces mêmes coordonnées.
        self.rect.y = self.start_y - (self.velocity * math.sin(self.angle) * self.time - (0.5 * self.gravity * self.time ** 2))
        #Ici, self.start correspond à la coordonnée à partir de laquelle notre projectile à été lancé (correspond à notre point d'origine)
        #Les formules sont retrouvables en appliquant la seconde loi de newton pour un corps en chute libre avec une potision initiale (C'est de là que provient self.start), et cela nous donne les équations pour les coordonnées x et y.
        #En utilisant la seconde loi de Newton, on néglige déliberemment le frottement de l'air.
        self.rotate()


        for user in self.user.game.check_collision(self, self.user.game.all_player):
            if self.time > 1 :


                user.damage(self.user.attack)
                self.remove()

        for user in self.user.game.check_collision(self, self.user.game.all_master):
            if self.time > 1 :


                user.damage(self.user.attack)
                self.remove()

        if self.rect.y > 1080:
            self.remove()
