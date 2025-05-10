
import pygame

def afficher_accueil(screen):
    WIDTH, HEIGHT = 1080, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # images de fond
    background = pygame.image.load("assets/backgrounds/mpbg.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    play_button = pygame.image.load("assets/buttons/play_button.png")
    play_button = pygame.transform.scale(play_button, (400,150))
    play_button_rect = play_button.get_rect()
    play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 +9 # changes the pos in x coordinates
    play_button_rect.y = 400  # changes the pos in y coordinates
    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return  # L'utilisateur a cliqué sur "Play"

        screen.blit(background, (0, 0))  # <- Affiche le fond
        screen.blit(play_button, play_button_rect)
        pygame.display.flip()
        clock.tick(60)
