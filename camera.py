import pygame

class Camera:
    def __init__(self, width, height):
        # Initialize viewport size and offset for world coordinates
        self.width = width
        self.height = height
        # Set offset vector for the top-left corner of the viewport
        self.offset = pygame.Vector2(0, 0)
        # Speed factor for smooth camera interpolation
        self.smooth_speed = 3.0

    def apply(self, target_rect: pygame.Rect) -> pygame.Rect:
        # Apply the current camera offset to a rectangle, returning its screen position.
        return target_rect.move(-self.offset.x, -self.offset.y)

    def update(self, target: pygame.sprite.Sprite):
        # Instantly recenter the camera on the target sprite by adjusting the offset.
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2

    def smooth_update(self, target: pygame.sprite.Sprite, dt: float):
        # Smoothly interpolate the camera offset toward the target sprite based on delta time.
        desired = pygame.Vector2(
            target.rect.centerx - self.width // 2,
            target.rect.centery - self.height // 2
        )
        alpha = min(1, dt * self.smooth_speed)
        self.offset = self.offset.lerp(desired, alpha)
