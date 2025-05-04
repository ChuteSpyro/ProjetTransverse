import pygame
import sys
import math

pygame.init()

# Écran
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bowmaster - 2 joueurs")

# Monde
world_width, world_height = 2000, 1000
background = pygame.Surface((world_width, world_height))

# Couleurs
RED = (200, 0, 0)
BLUE = (0, 0, 200)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)

# Joueurs
archer_pos = pygame.Vector2(100, world_height - 150)
target_pos = pygame.Vector2(1700, world_height - 150)
archer_hp, target_hp = 100, 100

# Flèche
angle, power, charging = -45, 0, False
max_power = 25
current_player = "archer"
slow_motion = False
slow_motion_timer = 0

class Arrow:
    def __init__(self, x, y, velocity):
        self.pos = pygame.Vector2(x, y)
        self.vel = velocity
        self.radius = 8
        self.active = True

    def update(self):
        if self.active:
            self.pos += self.vel
            self.vel.y += 0.4
            if self.pos.y >= world_height - 100:
                self.active = False
                self.vel = pygame.Vector2(0, 0)

    def draw(self, surface, offset):
        pygame.draw.circle(surface, RED, (int(self.pos.x - offset.x), int(self.pos.y - offset.y)), self.radius)

arrows = []
# Fonctions décor
def draw_decor(surface):
    for i in range(world_height):
        sky_color = (max(0, 135 - i // 20), max(0, 206 - i // 15), max(0, 235 - i // 10))
        pygame.draw.line(surface, sky_color, (0, i), (world_width, i))

    points = []
    for x in range(0, world_width + 100, 100):
        y = world_height - 100 - 40 * math.sin(x * 0.002)
        points.append((x, y))
    points.append((world_width, world_height))
    points.append((0, world_height))
    pygame.draw.polygon(surface, (50, 205, 50), points)

    for x in range(300, world_width, 500):
        pygame.draw.rect(surface, (139, 69, 19), (x, world_height - 180, 20, 80))
        pygame.draw.circle(surface, (34, 139, 34), (x + 10, world_height - 180), 30)
    for x in range(200, world_width, 700):
        pygame.draw.circle(surface, (100, 100, 100), (x, world_height - 105), 15)

def draw_health_bar(surface, x, y, hp):
    pygame.draw.rect(surface, RED, (x, y, 100, 10))
    pygame.draw.rect(surface, GREEN, (x, y, max(0, hp), 10))
    pygame.draw.rect(surface, BLACK, (x, y, 100, 10), 2)

def arrow_hits(arrow, rect):
    return rect.collidepoint(arrow.pos.x, arrow.pos.y)

def draw_character(surface, pos, facing_left, color, offset):
    x = pos.x - offset.x
    y = pos.y - offset.y
    direction = -1 if facing_left else 1
    pygame.draw.circle(surface, color, (int(x + 15), int(y - 20)), 10)
    pygame.draw.line(surface, color, (x + 15, y - 10), (x + 15, y + 30), 3)
    pygame.draw.line(surface, color, (x + 15, y + 30), (x + 5, y + 50), 3)
    pygame.draw.line(surface, color, (x + 15, y + 30), (x + 25, y + 50), 3)
    pygame.draw.line(surface, color, (x + 15, y), (x + 15 + 15 * direction, y - 10), 3)
    pygame.draw.arc(surface, BLACK, (x + 15 + 5 * direction, y - 15, 20 * direction, 30), math.radians(90), math.radians(270), 2)

def show_message(screen, message):
    font = pygame.font.SysFont(None, 80)
    text = font.render(message, True, BLACK)
    rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.delay(2500)

def show_menu():
    screen.fill(GREY)
    font = pygame.font.SysFont(None, 60)
    title = font.render("Bowmaster Duel", True, BLACK)
    press = pygame.font.SysFont(None, 40).render("Appuie sur ESPACE pour commencer", True, BLACK)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 200))
    screen.blit(press, (screen_width // 2 - press.get_width() // 2, 300))
    pygame.display.flip()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                waiting = False
# Initialisation du fond et du menu
draw_decor(background)
show_menu()

# Boucle principale
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
running = True
camera_focus = archer_pos

while running:
    dt = clock.tick(60 if not slow_motion else 20)  # Slow-mo = baisse FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not charging:
            charging = True
            power = 0

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and charging:
            charging = False
            direction = 1 if current_player == "archer" else -1
            rad_angle = math.radians(angle)
            velocity = pygame.Vector2(
                math.cos(rad_angle) * power * direction,
                -math.sin(rad_angle) * power
            )
            start_pos = archer_pos if current_player == "archer" else target_pos
            arrows.append(Arrow(start_pos.x + 15, start_pos.y, velocity))
            camera_focus = arrows[-1].pos

    # Contrôles angle et puissance
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        angle = min(angle + 1, 90)
    if keys[pygame.K_DOWN]:
        angle = max(angle - 1, -90)
    if charging:
        power = min(power + 0.3, max_power)

    # MAJ flèches
    for arrow in arrows:
        arrow.update()
        if arrow.active:
            camera_focus = arrow.pos

            # Collision
            target_rect = pygame.Rect(target_pos.x, target_pos.y, 30, 60)
            archer_rect = pygame.Rect(archer_pos.x, archer_pos.y, 30, 60)

            if arrow_hits(arrow, target_rect) and current_player == "archer":
                target_hp -= 25
                arrow.active = False
                slow_motion = True
                slow_motion_timer = pygame.time.get_ticks()

            elif arrow_hits(arrow, archer_rect) and current_player == "target":
                archer_hp -= 25
                arrow.active = False
                slow_motion = True
                slow_motion_timer = pygame.time.get_ticks()

        # Si flèche terminée, changer de tour
        if not arrow.active and len(arrows) > 0:
            if pygame.time.get_ticks() - slow_motion_timer > 500:
                slow_motion = False
                arrows.clear()

                if archer_hp <= 0 or target_hp <= 0:
                    winner = "Joueur 1" if target_hp <= 0 else "Joueur 2"
                    show_message(screen, f"{winner} GAGNE !")
                    pygame.quit()
                    sys.exit()

                current_player = "target" if current_player == "archer" else "archer"
                angle = -45 if current_player == "archer" else 135
                power = 0
                camera_focus = archer_pos if current_player == "archer" else target_pos

    # Caméra
    offset = pygame.Vector2(camera_focus.x - screen_width // 2, camera_focus.y - screen_height // 2)
    offset.x = max(0, min(offset.x, world_width - screen_width))
    offset.y = max(0, min(offset.y, world_height - screen_height))

    # Affichage
    screen.blit(background, (-offset.x, -offset.y))

    # Personnages + vie
    if archer_hp > 0:
        draw_character(screen, archer_pos, False, BROWN, offset)
        draw_health_bar(screen, archer_pos.x - offset.x - 10, archer_pos.y - offset.y - 40, archer_hp)
    if target_hp > 0:
        draw_character(screen, target_pos, True, BLUE, offset)
        draw_health_bar(screen, target_pos.x - offset.x - 10, target_pos.y - offset.y - 40, target_hp)

    # Visée et jauge de puissance
    if charging:
        pos = archer_pos if current_player == "archer" else target_pos
        direction = 1 if current_player == "archer" else -1
        end_x = pos.x + math.cos(math.radians(angle)) * 50 * direction
        end_y = pos.y - math.sin(math.radians(angle)) * 50
        pygame.draw.line(screen, WHITE, (pos.x - offset.x + 15, pos.y - offset.y), (end_x - offset.x, end_y - offset.y), 2)
        pygame.draw.rect(screen, RED, (20, 20, (power / max_power) * 100, 10))
        pygame.draw.rect(screen, WHITE, (20, 20, 100, 10), 2)

    # Tour affiché
    screen.blit(font.render(f"Tour de : {current_player.upper()}", True, BLACK), (20, 50))

    # Flèches
    for arrow in arrows:
        arrow.draw(screen, offset)

    pygame.display.flip()

pygame.quit()
sys.exit()
