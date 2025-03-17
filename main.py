import pygame
from game import Game
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

play_button = pygame.image.load("assets/button.png")
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 + 9
play_button_rect.y = (screen.get_height() - banner.get_height()) // 2 - 70

game = Game()
clock = pygame.time.Clock()

running = True
while running:

    dt = clock.tick(60) / 1000.0
    screen.blit(background, (0, -200))

    if game.is_playing :
        game.update(screen)

    else :
        screen.blit(play_button, (play_button_rect.x, play_button_rect.y))

        screen.blit(banner, (banner_rect.x, banner_rect.y))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu mouahaha, looser !")

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True


            if event.key == pygame.K_RETURN:
                game.player.launch_projectile()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.is_playing = True
