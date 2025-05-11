import pygame

def afficher_accueil(screen):
    WIDTH, HEIGHT = 1080, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # background images
    background = pygame.image.load("assets/backgrounds/mpbg.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT)) #set up the window size

    # Load play button images
    play_button = pygame.image.load("assets/buttons/play_button.png")
    play_button_hover = pygame.image.load("assets/buttons/button_play_hover.png")

    #dimension of the buttons
    play_button = pygame.transform.scale(play_button, (400,150))
    play_button_hover = pygame.transform.scale(play_button_hover, (400,150))

    # Get button position and center it horizontally
    play_button_rect = play_button.get_rect()
    play_button_rect.x = (screen.get_width() - play_button.get_width()) // 2 +9 # changes the pos in x coordinates
    play_button_rect.y = 400  # changes the pos in y coordinates

    waiting = True
    clock = pygame.time.Clock() # control the frame rate

    while waiting:

        mx, my = pygame.mouse.get_pos()

        #events control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # If the user clicks on the play button, exit the menu
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return  # Exit the loop and return to the main program because the user clicked on play

        # Draw the background
        screen.blit(background, (0, 0))

        # Display hover effect if the mouse is over the button
        # Show normal or hover button depending on the cursor position
        if play_button_rect.collidepoint((mx, my)):
            screen.blit(play_button_hover, play_button_rect)
        else:
            screen.blit(play_button, play_button_rect)

        pygame.display.flip()# Update the display
        clock.tick(60)# Limit the loop to 60 frames per second