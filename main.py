import pygame
from game import Game
from character_selection import select_character


pygame.init()

pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("assets/bg.jpg")

selected_character = select_character(screen)

game = Game()


running = True
while running:

    screen.blit(background, (0, -200))

    screen.blit(game.player.image, game.player.rect)
    screen.blit(game.master.image, game.master.rect)

    for projectile in game.player.all_projectiles:
        projectile.move()

    game.master.update_health_bar(screen)

    game.player.all_projectiles.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("fermeture du jeu mouahaha, looser !")
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True


            if event.key == pygame.K_RETURN:
                game.player.launch_projectile()

