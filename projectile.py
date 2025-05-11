import pygame
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self, user,angle,selection,velocity):
        super().__init__()
        # Initialize projectile properties: velocity, user reference, and select image based on weapon type
        self.velocity = velocity
        self.user = user
        if selection == 'dagger':
            self.image = pygame.image.load('assets/weapons/dagger.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 50))
        if selection == 'Axe':
            self.image = pygame.image.load('assets/weapons/axe.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect(center=user.rect.center)
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.origin_image = self.image
        self.time = 0.0
        self.rotate_angle = 0
        self.angle = angle
        carte = self.user.game.carte
        if carte == "Mars":
            self.gravity = 3.73
        elif carte == "Moon":
            self.gravity = 1.72
        elif carte == "Earth":
            self.gravity = 9.81
        self.grass_sound = pygame.mixer.Sound("assets/sounds/sword_in_ground.mp3")
        self.pain_sound = pygame.mixer.Sound("assets/sounds/caracter_hurt.mp3")
        self.knife_sound = pygame.mixer.Sound("assets/sounds/knife_sound.mp3")
        self.counter = 0

    def rotate(self):
        self.rotate_angle += 20
        self.image = pygame.transform.rotozoom(self.origin_image, self.rotate_angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.user.all_projectiles.remove(self)

    def move(self,dt):
        # Increment time factor for motion calculations
        self.time += dt*8
        # Calculate x and y positions using kinematic equations
        self.rect.x = self.start_x + self.velocity * math.cos(self.angle) * self.time
        self.rect.y = self.start_y - (self.velocity * math.sin(self.angle) * self.time - (0.5 * self.gravity * self.time ** 2))
        # Apply Newton's second law for free-fall motion (ignoring air resistance)
        # Rotate the projectile image for visual effect
        self.rotate()
        # Make the projectile rotate during movement
        if self.counter >= 7:
            self.knife_sound.play()
            self.counter = 0
        self.counter += 1

        # Check collision with player characters after a short flight duration
        for user in self.user.game.check_collision(self, self.user.game.all_player):
            if self.time > 3 :
                self.pain_sound.play()
                user.damage(self.user.attack)
                self.remove()
                return

        # Check collision with master characters after a short flight duration
        for user in self.user.game.check_collision(self, self.user.game.all_master):
            if self.time > 3 :
                self.pain_sound.play()
                user.damage(self.user.attack)
                self.remove()
                return

        # Handle collision with terrain: embed projectile and play impact sound
        terrain_mask = self.user.game.terrain_mask
        if terrain_mask:
            offset = (int(self.rect.x), int(self.rect.y))
            projectile_mask = pygame.mask.from_surface(self.image)
            if terrain_mask.overlap(projectile_mask, offset):
                self.grass_sound.play()
                self.user.all_projectiles.remove(self)
                self.user.game.stuck_projectiles.add(self)

                return

        # Remove projectile if it falls below the screen boundary
        if self.rect.y > 1080:
            self.remove()
