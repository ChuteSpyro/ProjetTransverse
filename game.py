import pygame

from player import Player
from master import Master



# Initialize clock for frame rate management and compute delta time per frame
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000.0
class Game:
    def __init__(self,choix_joueurs):
        # Initialize Game with player choices: load players, masters, and projectile groups
        # Game state flag indicating if the game loop is active
        self.is_playing = False

        # Create sprite group for all players and add the first player
        # Instantiate player object based on selection and add to player group
        self.all_player = pygame.sprite.Group()
        self.player = Player(self,choix_joueurs['player1'])
        self.all_player.add(self.player)

        # Create sprite group for all masters and add the second player as master
        # Instantiate master object based on selection and add to master group
        self.all_master = pygame.sprite.Group()
        self.master = Master(self,choix_joueurs['player2'])
        self.all_master.add(self.master)

        # Group for projectiles that have embedded in terrain
        self.stuck_projectiles = pygame.sprite.Group()
        # Mask for terrain collision detection (to be set when terrain loads)
        self.terrain_mask = None

        self.pressed = {}


    # Update and render game state: draw sprites, handle projectiles, and check collisions
    def update(self, screen, camera):
        # Render player sprite if exists
        if self.player is not None:
            # Convert player rect to camera coordinates and draw on screen
            rect = camera.apply(self.player.rect)
            screen.blit(self.player.image, rect)
            # Update player's health bar UI
            self.player.update_health_bar(screen, camera)

        # Render master sprite if exists
        if self.master is not None:
            # Convert master rect to camera coordinates and draw on screen
            rect = camera.apply(self.master.rect)
            screen.blit(self.master.image, rect)
            # Update master's health bar UI
            self.master.update_health_bar(screen, camera)

        # Render projectiles stuck in terrain
        for projectile in self.stuck_projectiles:
            screen.blit(projectile.image, camera.apply(projectile.rect))

        # Render and update active projectiles for player
        if self.player is not None:
            for projectile in self.player.all_projectiles:
                screen.blit(projectile.image, camera.apply(projectile.rect))
            for projectile in self.player.all_projectiles:
                projectile.move(dt)

        # Render and update active projectiles for master
        if self.master is not None:
            for projectile in self.master.all_projectiles:
                screen.blit(projectile.image, camera.apply(projectile.rect))
            for projectile in self.master.all_projectiles:
                projectile.move(dt)

    # Check collisions between a sprite and a group
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
