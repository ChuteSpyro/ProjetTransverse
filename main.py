import pygame
from game import Game
from map import *
import math
import sys
from character_selection import character_and_weapon_select, map_selection, weapons
from camera import Camera
from accueil import afficher_accueil


def main():
    pygame.init()

    # Initialize Pygame modules
    pygame.display.set_caption("Simple Game")

    # Map configuration constants
    WIDTH, HEIGHT = 6000, 720
    TILE_SIZE = 100

    pygame.mixer.music.load("assets/sounds/Musique_de_fond.mp3")
    pygame.mixer.music.play(-1)  # -1 = infinite loop playback

    screen = pygame.display.set_mode((1080,720))
    camera = Camera(1728,1152)


    play_button = pygame.image.load("assets/buttons/play_button.png")
    play_button = pygame.transform.scale(play_button, (400,150))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 + 9
    play_button_rect.y = (screen.get_height() - play_button.get_height()) // 2 + 300

    afficher_accueil(screen)  # Display the main menu before starting the game
    selection = character_and_weapon_select(screen)
    game = Game(selection)

    # Position characters high in the sky for drop effect
    game.player.rect.y = -game.player.rect.height
    game.master.rect.y = -game.master.rect.height

    player_vy = 0.0
    master_vy = 0.0
    falling_player = True
    falling_master = True
    gravity = 981  # pixels per second squared

    # Variables for aiming and shooting
    dragging = False  # Indicates if the player is currently aiming
    follow_projectile = False
    follow_timer = 0.0
    follow_target = None
    intro = True
    intro_timer = 0.0
    intro_duration = 3.0  # seconds of wide shot at game start
    start_zoom = 1.0
    end_zoom = 2.2
    zoom_current = start_zoom
    zoom_smooth_speed = 2.0

    running = True
    playing = "player"

    carte = map_selection(screen)
    game.carte = carte
    game.is_playing = True
    intro = True
    intro_timer = 0.0
    clock = pygame.time.Clock()

    # Generate terrain map and collision mask
    background, terrain_mask = generate_map(WIDTH, HEIGHT, TILE_SIZE, carte)
    game.terrain_mask = terrain_mask

    def get_ground_y(sprite):
        x_center = sprite.rect.x + sprite.rect.width // 2
        for y in range(HEIGHT):
            if terrain_mask.get_at((x_center, y)):
                return y
        return HEIGHT

    ground_y_player = get_ground_y(game.player)
    ground_y_master = get_ground_y(game.master)

    pygame.mixer.music.set_volume(0.2)

    # Preload game over and buttons for access in event loop
    game_over = pygame.image.load("assets/buttons/game_over.png")
    replay_button = pygame.image.load("assets/buttons/button_replay.png")
    leave_button = pygame.image.load("assets/buttons/button_leave.png")

    # Load hover images for replay and leave buttons
    replay_button_hover = pygame.image.load("assets/buttons/button_replay_hover.png")
    leave_button_hover = pygame.image.load("assets/buttons/button_leave_hover.png")


    replay_button.set_colorkey((0, 0, 0))
    leave_button.set_colorkey((0, 0, 0))
    replay_button_hover.set_colorkey((0, 0, 0))
    leave_button_hover.set_colorkey((0, 0, 0))

    replay_button = pygame.transform.scale(replay_button, (150, 60))
    leave_button = pygame.transform.scale(leave_button, (150, 60))

    replay_button_hover = pygame.transform.scale(replay_button_hover, (150, 60))
    leave_button_hover = pygame.transform.scale(leave_button_hover, (150, 60))

    game_over_rect = game_over.get_rect(center=(540, 200))
    replay_rect = replay_button.get_rect(center=(370, 400))
    leave_rect = leave_button.get_rect(center=(710, 400))

    # Main game loop
    while running:
        dt = clock.tick(60) / 1000.0
        # Update character falling physics
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
                if game.master.health <= 0:
                    game.player = None
                    game.master = None
        # Camera logic runs only when the game has started and game is not over
        if game.is_playing and not game.game_over:
            # Intro wide shot before gameplay zoom and follow
            if intro:
                # Compute current viewport size based on active zoom
                current_zoom = start_zoom if intro else zoom_current
                vw = 1728
                vh = 1152
                intro_timer += dt
                if game.player is not None and game.master is not None:
                    mid_x = (game.player.rect.centerx + game.master.rect.centerx) / 2
                    # Horizontal centering between characters
                    camera.offset.x = mid_x - vw / 2
                    # Vertical alignment based on lowest final ground position
                    final_ground_y = max(ground_y_player, ground_y_master)
                    camera.offset.y = final_ground_y - vh + 250
                    max_offset_y = HEIGHT - vh
                    if camera.offset.y > max_offset_y:
                        camera.offset.y = max_offset_y
                if intro_timer >= intro_duration:
                    intro = False
            # Follow projectile immediately after firing
            elif follow_projectile and follow_target is not None:
                follow_timer += dt
                camera.smooth_update(follow_target, dt)
                if follow_timer >= 3.0:
                    follow_projectile = False
            # Regular smooth follow of active character after intro
            else:
                if playing == "player" and game.player is not None:
                    camera.smooth_update(game.player, dt)
                elif playing == "master" and game.master is not None:
                    camera.smooth_update(game.master, dt)

        if game.is_playing:
            # Create a viewport surface to draw everything non-zoomed
            viewport = pygame.Surface((vw, vh))
            if carte == "Earth":
                viewport.fill((155, 230, 255))
            if carte == "Moon":
                viewport.fill((0, 0, 0))
            if carte == "Mars":
                viewport.fill((250, 200, 129))

            # Draw background at camera offset
            bg_rect = background.get_rect()
            bg_rect.topleft = -camera.offset
            viewport.blit(background, bg_rect)

            # Draw game objects into viewport only if game is not over
            if not game.game_over:
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
                speed= speed * 1.5
                if carte == "Earth" :
                    gravity = 9.81
                if carte == "Moon" :
                    gravity = 1.72
                if carte == "Mars" :
                    gravity = 3.73

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
        elif game.game_over:
            end_bg = pygame.image.load("assets/backgrounds/bg.png")
            end_bg = pygame.transform.scale(end_bg,(screen.get_width(),screen.get_height()))
            screen.blit(end_bg, (0, 0))
            screen.blit(game_over, game_over_rect)
            # Hover effect for replay and leave buttons
            if replay_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(replay_button_hover, replay_rect)
            else:
                screen.blit(replay_button, replay_rect)
            if leave_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(leave_button_hover, leave_rect)
            else:
                screen.blit(leave_button, leave_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

                print("fermeture du jeu mouahaha, looser !")

            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True

                if event.key == pygame.K_RETURN and not intro:
                    if playing == "player" and game.player is not None:
                        game.player.launch_player_projectile(45,selection['player1']['weapon'])
                        playing = "master"
                        break

                    if playing == "master" and game.master is not None:
                        game.master.launch_master_projectile(-45,selection['player2']['weapon'])
                        playing = "player"
                        break

            elif event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                if replay_rect.collidepoint(event.pos):
                    main()
                elif leave_rect.collidepoint(event.pos):
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game.is_playing = True
                elif not intro:
                    # Begin aiming on mouse button down
                    dragging = True
                    launch_pos = event.pos  # Record the starting position of the drag

            elif event.type == pygame.MOUSEBUTTONUP and dragging and not intro:
                dragging = False
                release_pos = event.pos

                if playing == "player" and game.player is not None:
                    p_origin_x, p_origin_y = game.player.rect.center

                    # Calculate direction and power of the shot
                    world_x = release_pos[0] + camera.offset.x
                    world_y = release_pos[1] + camera.offset.y
                    dx = p_origin_x - world_x
                    dy = p_origin_y - world_y
                    angle = math.atan2(-dy, dx)

                    # Apply speed to player's projectile
                    distance = math.hypot(dx, dy)
                    power_ratio = min(distance / 300, 1.0)
                    speed = power_ratio * 90
                    speed = speed * 1.5
                    game.player.launch_player_projectile(angle,selection['player1']['weapon'] ,speed)
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

                    # Calculate direction and power of the shot
                    world_x = release_pos[0] + camera.offset.x
                    world_y = release_pos[1] + camera.offset.y
                    dx = m_origin_x - world_x
                    dy = m_origin_y - world_y
                    angle = math.atan2(-dy, dx)

                    # Apply speed to master's projectile
                    distance = math.hypot(dx, dy)
                    power_ratio = min(distance / 300, 1.0)
                    speed = power_ratio * 90
                    speed = speed * 1.5
                    game.master.launch_master_projectile(angle,selection['player2']['weapon'],speed)
                    playing = "player"  # Switch to player for the next round
                    if playing == "master":
                        proj = game.player.all_projectiles.sprites()[-1]
                    else:
                        proj = game.master.all_projectiles.sprites()[-1]
                    follow_target = proj
                    follow_projectile = True
                    follow_timer = 0.0


if __name__ == "__main__":
    main()
