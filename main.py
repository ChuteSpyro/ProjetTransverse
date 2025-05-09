import pygame
from game import Game
from map import *
import math
from character_selection import character_and_weapon_select, map_selection
from camera import Camera
from accueil import afficher_accueil

# Initialisation Pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Simple Game")

# Constantes
WIDTH, HEIGHT = 4000, 720
TILE_SIZE = 100
SKY = (135, 206, 235)

# Music
pygame.mixer.music.load("assets/sounds/Musique_de_fond.mp3")
pygame.mixer.music.play(-1)  # -1 = boucle infinie

# Génération du fond et du masque terrain
background, terrain_mask = generate_map(WIDTH, HEIGHT, TILE_SIZE)

# Écran et caméra
screen = pygame.display.set_mode((1080, 720))
camera = Camera(*screen.get_size())

# Éléments du menu
banner = pygame.image.load("assets/banner.png")
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = (screen.get_width() - banner.get_width()) // 2
banner_rect.y = (screen.get_height() - banner.get_height()) // 2 - 70

play_button = pygame.image.load("assets/play_button.png")
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 + 9
play_button_rect.y = (screen.get_height() - banner.get_height()) // 2 + 300

# Initialisation du jeu
game = Game()
game.terrain_mask = terrain_mask
clock = pygame.time.Clock()

# Variables de gameplay
dragging = False
follow_projectile = False
follow_timer = 0.0
follow_target = None
intro = True
intro_timer = 0.0
intro_duration = 3.0
start_zoom = 1.0
end_zoom = 1.5
zoom_current = start_zoom
zoom_smooth_speed = 2.0
running = True
playing = "player"

# Boucle principale
while running:

    dt = clock.tick(60) / 1000.0


    # Logique de caméra si le jeu est actif
    if game.is_playing:
        if intro:
            intro_timer += dt
            if game.player and game.master:
                mid_x = (game.player.rect.centerx + game.master.rect.centerx) / 2
                mid_y = (game.player.rect.centery + game.master.rect.centery) / 2
                camera.offset.x = mid_x - screen.get_width() / 2
                camera.offset.y = mid_y - screen.get_height() / 2
            if intro_timer >= intro_duration:
                intro = False
        elif follow_projectile and follow_target:
            follow_timer += dt
            camera.smooth_update(follow_target, dt)
            if follow_timer >= 2.0:
                follow_projectile = False
        else:
            if playing == "player" and game.player:
                camera.smooth_update(game.player, dt)
            elif playing == "master" and game.master:
                camera.smooth_update(game.master, dt)

    # Rendu du jeu
    if game.is_playing:
        viewport = pygame.Surface(screen.get_size())
        viewport.fill(SKY)
        bg_rect = background.get_rect()
        bg_rect.topleft = -camera.offset
        viewport.blit(background, bg_rect)

        game.update(viewport, camera)

        # Affichage trajectoire
        if dragging:
            if playing == "player" and game.player:
                origin_x, origin_y = game.player.rect.center
            elif playing == "master" and game.master:
                origin_x, origin_y = game.master.rect.center
            else:
                origin_x, origin_y = 0, 0

            mouse_x = pygame.mouse.get_pos()[0] + camera.offset.x
            mouse_y = pygame.mouse.get_pos()[1] + camera.offset.y

            dx = origin_x - mouse_x
            dy = origin_y - mouse_y
            distance = math.hypot(dx, dy)
            power_ratio = min(distance / 300, 1.0)
            angle = math.atan2(-dy, dx)
            speed = power_ratio * 90
            gravity = 9.81

            for i in range(60):
                t = i * 0.1
                x = origin_x + speed * math.cos(angle) * t
                y = origin_y - (speed * math.sin(angle) * t - 0.5 * gravity * t ** 2)
                if i % 2 == 0:
                    pos = (int(x - camera.offset.x), int(y - camera.offset.y))
                    pygame.draw.circle(viewport, (255, 255, 255), pos, 3)

        # Zoom dynamique
        if intro:
            zoom = start_zoom
        else:
            zoom_current += (end_zoom - zoom_current) * dt * zoom_smooth_speed
            zoom = zoom_current

        sw, sh = screen.get_size()
        scaled = pygame.transform.scale(viewport, (int(sw * zoom), int(sh * zoom)))
        screen.fill((0, 0, 0))
        screen.blit(
            scaled,
            (-(scaled.get_width() - sw) // 2,
             -(scaled.get_height() - sh) // 2)
        )
    else:
        # Menu principal
        screen.fill((0, 0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    pygame.display.update()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu mouahaha, looser !")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.is_playing = True
            else:
                dragging = True
                launch_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            release_pos = event.pos

            # Joueur
            if playing == "player" and game.player:
                p_origin_x, p_origin_y = game.player.rect.center
                world_x = release_pos[0] + camera.offset.x
                world_y = release_pos[1] + camera.offset.y
                dx = p_origin_x - world_x
                dy = p_origin_y - world_y
                angle = math.atan2(-dy, dx)
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.player.launch_player_projectile(angle, speed)
                playing = "master"

                proj = game.player.all_projectiles.sprites()[-1]
                follow_target = proj
                follow_projectile = True
                follow_timer = 0.0

            # Maître
            elif playing == "master" and game.master:
                m_origin_x, m_origin_y = game.master.rect.center
                world_x = release_pos[0] + camera.offset.x
                world_y = release_pos[1] + camera.offset.y
                dx = m_origin_x - world_x
                dy = m_origin_y - world_y
                angle = math.atan2(-dy, dx)
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.master.launch_master_projectile(angle, speed)
                playing = "player"

                proj = game.master.all_projectiles.sprites()[-1]
                follow_target = proj
                follow_projectile = True
                follow_timer = 0.0