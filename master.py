import pygame
from projectile import Projectile

class Master(pygame.sprite.Sprite) :
    def __init__(self, game,selection):
        # Initialize master attributes: game reference, health, attack power, and projectile group
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 100
        self.all_projectiles = pygame.sprite.Group()
        # Load and scale character sprite based on selection choice
        # Handle 'fleur' character sprite loading and flip horizontally
        if selection['character'] == 'fleur':
            self.image = pygame.image.load('assets/characters/fleur.png')
            self.image = pygame.transform.scale(self.image, (150, 150))
            self.image = pygame.transform.flip(self.image, True, False)
        # Handle 'ghost' character sprite loading
        if selection['character'] == 'ghost':
            self.image = pygame.image.load('assets/characters/ghost.png')
            self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 3200
        self.rect.y = 100

    def damage(self, damage):
        # Reduce health by the damage amount
        self.health -= damage

        # Check for death and remove master from game if health depleted
        if self.health <= 0 :
            self.game.is_playing = False
            self.game.game_over = True
            self.game.all_master.remove(self)
            self.kill()
            self.game.master = None

    def launch_master_projectile(self,angle,selection,velocity=50):
        # Launch a new projectile with specified angle, selection, and optional velocity
        if self is not None:
            self.all_projectiles.add(Projectile(self,angle,selection,velocity))


    def update_health_bar(self, surface, camera):
        # Define colors for health bar foreground and background
        bar_color = (111,210,46)
        back_bar_color = (60,63,60)

        # Compute positions and sizes for health bar segments
        bar_position = [self.rect.x + 10 - camera.offset.x,
                        self.rect.y - 20 - camera.offset.y,
                        self.health, 5]
        back_bar_position = [self.rect.x + 10 - camera.offset.x,
                             self.rect.y - 20 - camera.offset.y,
                             self.max_health, 5]

        # Draw health bar (first background, then foreground)
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
