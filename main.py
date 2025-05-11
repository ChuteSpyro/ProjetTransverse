import pygame
from game import Game
from map import *
import math
from character_selection import character_and_weapon_select, map_selection
from camera import Camera
from accueil import afficher_accueil


pygame.init()

pygame.display.set_caption("Simple Game")

#MAP
WIDTH, HEIGHT = 4000, 720
TILE_SIZE = 100


SKY = (135, 206, 235)

pygame.mixer.music.load("assets/sounds/Musique_de_fond.mp3")
pygame.mixer.music.play(-1)  # -1 = boucle infinie


screen = pygame.display.set_mode((1080,720))
camera = Camera(*screen.get_size())
# Génération du sol

background, terrain_mask = generate_map(WIDTH, HEIGHT, TILE_SIZE, map_selection(screen))

#selected_character = select_character(screen)

banner = pygame.image.load("assets/banner/moon_bg.jpg")
banner = pygame.transform.scale(banner, (500,500))
banner_rect = banner.get_rect()
banner_rect.x = (screen.get_width() - banner.get_width()) // 2
banner_rect.y = (screen.get_height() - banner.get_height()) // 2 - 70

play_button = pygame.image.load("assets/buttons/play_button.png")
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 + 9
play_button_rect.y = (screen.get_height() - banner.get_height()) // 2 + 300


afficher_accueil(screen)  # Affiche le menu avant de démarrer le jeu
game = Game()
game.terrain_mask = terrain_mask



# Position characters high in the sky for drop effect
game.player.rect.y = -game.player.rect.height
game.master.rect.y = -game.master.rect.height

player_vy = 0.0
master_vy = 0.0
falling_player = True
falling_master = True
gravity = 981  # pixels per second squared

def get_ground_y(sprite):
    x_center = sprite.rect.x + sprite.rect.width // 2
    for y in range(HEIGHT):
        if terrain_mask.get_at((x_center, y)):
            return y
    return HEIGHT

ground_y_player = get_ground_y(game.player)
ground_y_master = get_ground_y(game.master)

# Variables pour le tir
dragging = False  # Indique si on est en train de viser
follow_projectile = False
follow_timer = 0.0
follow_target = None
intro = True
intro_timer = 0.0
intro_duration = 3.0  # seconds of wide shot at game start
start_zoom = 1.0
end_zoom = 1.5
zoom_current = start_zoom
zoom_smooth_speed = 2.0

running = True
playing = "player"

choix_joueurs = character_and_weapon_select(screen)
carte = map_selection(screen)
game.carte = carte
game.is_playing = True
intro = True
intro_timer = 0.0
clock = pygame.time.Clock()
pygame.mixer.music.stop()


while running:

    dt = clock.tick(60) / 1000.0
    # Handle falling characters
    if falling_player:
        player_vy += gravity * dt
        game.player.rect.y += player_vy * dt
        if game.player.rect.bottom >= ground_y_player:
            game.player.rect.bottom = ground_y_player
            falling_player = False
            player_vy = 0.0
    if falling_master:
        master_vy += gravity * dt
        game.master.rect.y += master_vy * dt
        if game.master.rect.bottom >= ground_y_master:
            game.master.rect.bottom = ground_y_master
            falling_master = False
            master_vy = 0.0
    # Camera logic runs only when the game has started
    if game.is_playing:
        # Intro wide shot before gameplay zoom and follow
        if intro:
            intro_timer += dt
            if game.player is not None and game.master is not None:
                mid_x = (game.player.rect.centerx + game.master.rect.centerx) / 2
                # Horizontal centering between characters
                camera.offset.x = mid_x - screen.get_width() / 2
                # Vertical alignment based on lowest final ground position
                final_ground_y = max(ground_y_player, ground_y_master)
                camera.offset.y = final_ground_y - screen.get_height() + 50
                # Clamp only the upper bound so camera doesn't scroll past bottom of map
                max_offset_y = HEIGHT - screen.get_height()
                if camera.offset.y > max_offset_y:
                    camera.offset.y = max_offset_y
            if intro_timer >= intro_duration:
                intro = False
        # Follow projectile immediately after firing
        elif follow_projectile and follow_target is not None:
            follow_timer += dt
            camera.smooth_update(follow_target, dt)
            if follow_timer >= 2.0:
                follow_projectile = False
        # Regular smooth follow of active character after intro
        else:
            if playing == "player" and game.player is not None:
                camera.smooth_update(game.player, dt)
            elif playing == "master" and game.master is not None:
                camera.smooth_update(game.master, dt)

    if game.is_playing:
        # Create a viewport surface to draw everything non-zoomed
        viewport = pygame.Surface(screen.get_size())
        viewport.fill((180, 230, 255))

        # Draw background at camera offset
        bg_rect = background.get_rect()
        bg_rect.topleft = -camera.offset
        viewport.blit(background, bg_rect)

        # Draw game objects into viewport
        game.update(viewport, camera)

            # Trajectory debug draw if dragging
        # Trajectory preview
        if dragging:
            if playing == "player" and game.player is not None:
                origin_x, origin_y = game.player.rect.center
            elif playing == "master" and game.master is not None:
                origin_x, origin_y = game.master.rect.center
            else:
                origin_x, origin_y = 0, 0  # fallback

            # Convert mouse pos to world coordinates
            mouse_x = pygame.mouse.get_pos()[0] + camera.offset.x
            mouse_y = pygame.mouse.get_pos()[1] + camera.offset.y

            dx = origin_x - mouse_x
            dy = origin_y - mouse_y
            distance = math.hypot(dx, dy)
            power_ratio = min(distance / 300, 1.0)
            angle = math.atan2(-dy, dx)
            speed = power_ratio * 90
            gravity = 9.81

            # Draw
            for i in range(60):
                t = i * 0.1
                x = origin_x + speed * math.cos(angle) * t
                y = origin_y - (speed * math.sin(angle) * t - 0.5 * gravity * t ** 2)
                if i % 2 == 0:
                    pos = (int(x - camera.offset.x), int(y - camera.offset.y))
                    pygame.draw.circle(viewport, (255, 255, 255), pos, 3)

        # Zoom transition only after gameplay begins
        if not game.is_playing:
            zoom = start_zoom
        else:
            # First, hold start_zoom for intro duration
            if intro:
                zoom = start_zoom
            else:
                # interpolate zoom_current toward end_zoom
                zoom_current += (end_zoom - zoom_current) * dt * zoom_smooth_speed
                zoom = zoom_current
        sw, sh = screen.get_size()
        scaled = pygame.transform.scale(viewport, (int(sw * zoom), int(sh * zoom)))
        screen.fill((0, 0, 0))
        screen.blit(
            scaled,
            (-(scaled.get_width()  - sw)//2,
             -(scaled.get_height() - sh)//2)
        )
    else:
        # Main menu without zoom
        screen.fill((0, 0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(banner,      banner_rect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu mouahaha, looser !")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_RETURN and not intro:
                  # Garder cette ligne si tu veux un autre mode de tir
                if playing == "player" and game.player is not None:
                    game.player.launch_player_projectile(45)
                    playing = "master"
                    break

                if playing == "master" and game.master is not None:
                    game.master.launch_master_projectile(-45)
                    playing = "player"
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.is_playing = True
            elif not intro:
                # Début du tir
                dragging = True
                launch_pos = event.pos  # Enregistre la position de départ

        elif event.type == pygame.MOUSEBUTTONUP and dragging and not intro:
            dragging = False
            release_pos = event.pos

            if playing == "player" and game.player is not None:
                p_origin_x, p_origin_y = game.player.rect.center

                # Calculer la direction et la force du tir
                world_x = release_pos[0] + camera.offset.x
                world_y = release_pos[1] + camera.offset.y
                dx = p_origin_x - world_x
                dy = p_origin_y - world_y
                angle = math.atan2(-dy, dx)

                # Appliquer la vitesse au projectile du joueur
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.player.launch_player_projectile(angle, speed)
                playing = "master"  # Switch to master for the next round
                if playing == "master":
                    proj = game.player.all_projectiles.sprites()[-1]
                else:
                    proj = game.master.all_projectiles.sprites()[-1]
                follow_target = proj
                follow_projectile = True
                follow_timer = 0.0

            elif playing == "master" and game.master is not None:
                m_origin_x, m_origin_y = game.master.rect.center

                # Calculer la direction et la force du tir
                world_x = release_pos[0] + camera.offset.x
                world_y = release_pos[1] + camera.offset.y
                dx = m_origin_x - world_x
                dy = m_origin_y - world_y
                angle = math.atan2(-dy, dx)

                # Appliquer la vitesse au projectile du master
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.master.launch_master_projectile(angle, speed)
                playing = "player"  # Switch to player for the next round
                if playing == "master":
                    proj = game.player.all_projectiles.sprites()[-1]
                else:
                    proj = game.master.all_projectiles.sprites()[-1]
                follow_target = proj
                follow_projectile = True
                follow_timer = 0.0
