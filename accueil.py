import pygame

def afficher_accueil(screen):
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

        screen.fill((0, 0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
        pygame.display.flip()
        clock.tick(60)
