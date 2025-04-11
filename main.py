import pygame
from game import Game
import math
from character_selection import select_character


pygame.init()

pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("assets/bg.jpg")

selected_character = select_character(screen)

banner = pygame.image.load("assets/banner.png")
banner = pygame.transform.scale(banner, (500,500))
banner_rect = banner.get_rect()
banner_rect.x = (screen.get_width() - banner.get_width()) // 2
banner_rect.y = (screen.get_height() - banner.get_height()) // 2 - 70

play_button = pygame.image.load("assets/play_button.png")
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 + 9
play_button_rect.y = (screen.get_height() - banner.get_height()) // 2 + 300



game = Game()
clock = pygame.time.Clock()

# Variables pour le tir
dragging = False  # Indique si on est en train de viser

running = True
playing = "player"
while running:


    dt = clock.tick(60) / 1000.0
    screen.blit(background, (0, -200))

    if game.is_playing :
        game.update(screen)

    else :
        screen.blit(play_button, (play_button_rect.x, play_button_rect.y))

        screen.blit(banner, (banner_rect.x, banner_rect.y))

    if game.is_playing and dragging:
        if playing == "player" and game.player is not None:
            p_origin_x, p_origin_y = game.player.rect.center  # Récupérer la position du joueur
            #pygame.draw.line(screen, (0, 0, 255), (p_origin_x, p_origin_y), pygame.mouse.get_pos(), 3)

            # Affichage de la trajectoire en pointillés blancs
            dx = p_origin_x - pygame.mouse.get_pos()[0]
            dy = p_origin_y - pygame.mouse.get_pos()[1]
            distance = math.hypot(dx, dy)
            power_ratio = min(distance / 300, 1.0)
            angle = math.atan2(-dy, dx)
            speed = power_ratio * 90  # même vitesse que pour le projectile
            start_x, start_y = game.player.rect.center
            start_x += 50
            start_y += 10
            gravity = 9.81


        if playing == "master" and game.master is not None:
            m_origin_x, m_origin_y = game.master.rect.center  # Récupérer la position du master
            #pygame.draw.line(screen, (0, 0, 255), (m_origin_x, m_origin_y), pygame.mouse.get_pos(), 3)

            # Affichage de la trajectoire en pointillés blancs
            dx = m_origin_x - pygame.mouse.get_pos()[0]
            dy = m_origin_y - pygame.mouse.get_pos()[1]
            distance = math.hypot(dx, dy)
            power_ratio = min(distance / 300, 1.0)
            angle = math.atan2(-dy, dx)
            speed = power_ratio * 90  # même vitesse que pour le projectile
            start_x, start_y = game.master.rect.center
            start_x -= 50
            start_y -= 10
            gravity = 9.81


        for i in range(40):  # 40 points max
            t = i * 0.1
            x = start_x + speed * math.cos(angle) * t
            y = start_y - (speed * math.sin(angle) * t - 0.5 * gravity * t**2)
            if i % 2 == 0:
                pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), 3)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu mouahaha, looser !")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_RETURN:
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
            else:
                # Début du tir
                dragging = True
                launch_pos = event.pos  # Enregistre la position de départ

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            release_pos = event.pos

            if playing == "player" and game.player is not None:
                p_origin_x, p_origin_y = game.player.rect.center

                # Calculer la direction et la force du tir
                dx = p_origin_x - release_pos[0]
                dy = p_origin_y - release_pos[1]
                angle = math.atan2(-dy, dx)

                # Appliquer la vitesse au projectile du joueur
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.player.launch_player_projectile(angle, speed)
                playing = "master"  # Switch to master for the next round

            elif playing == "master" and game.master is not None:
                m_origin_x, m_origin_y = game.master.rect.center

                # Calculer la direction et la force du tir
                dx = m_origin_x - release_pos[0]
                dy = m_origin_y - release_pos[1]
                angle = math.atan2(-dy, dx)
                
                # Appliquer la vitesse au projectile du master
                distance = math.hypot(dx, dy)
                power_ratio = min(distance / 300, 1.0)
                speed = power_ratio * 90
                game.master.launch_master_projectile(angle, speed)
                playing = "player"  # Switch to player for the next round