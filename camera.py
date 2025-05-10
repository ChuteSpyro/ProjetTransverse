
# camera.py
import pygame

class Camera:
    def __init__(self, width, height):
        # how big is our viewport?
        self.width = width
        self.height = height
        # current top‐left world coordinate of the viewport
        self.offset = pygame.Vector2(0, 0)
        self.smooth_speed = 3.0  # Speed factor for smooth camera movement

    def apply(self, target_rect: pygame.Rect) -> pygame.Rect:
        """Returns a rect shifted by the camera offset."""
        return target_rect.move(-self.offset.x, -self.offset.y)

    def update(self, target: pygame.sprite.Sprite):
        """
        Center the camera on the target sprite.
        Clamps can be added so you don't scroll past the level edges.
        """
        # try to center target on screen
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2
        # optional: clamp so offset.x stays within world bounds
        # self.offset.x = max(0, min(self.offset.x, WORLD_WIDTH - self.width))
        # self.offset.y = max(0, min(self.offset.y, WORLD_HEIGHT - self.height))

    def smooth_update(self, target: pygame.sprite.Sprite, dt: float):
        """Smoothly move the camera towards the target sprite."""
        desired = pygame.Vector2(
            target.rect.centerx - self.width // 2,
            target.rect.centery - self.height // 2
        )
        alpha = min(1, dt * self.smooth_speed)
        self.offset = self.offset.lerp(desired, alpha)
