import pygame
import sys

# Initialisation de Pygame
pygame.init()
background = pygame.image.load("assets/bg.jpg")
left_img = pygame.image.load("assets/left_button.png")
right_img = pygame.image.load("assets/right_button.png")
confirm_img = pygame.image.load("assets/confirm_button.png")

def select_character(screen):
    # Dimensions de la fenêtre
    screen.blit(background, (0, -200))
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Choose character and weapon")

    # Couleurs utilisées
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (50, 100, 200)
    GREEN = (50, 200, 50)

    # Liste des personnages
    characters = ["Guerrier", "Mage", "Archer", "Voleur"]
    selected_index = 0

    # Liste des armes
    weapons = ["Épée", "Bâton magique", "Arc", "Dagues"]
    selected_weapon_index = 0

    # Définition des zones (rectangles) pour les boutons
    left_button = left_img.get_rect(topleft=(50, HEIGHT // 2 + 15))
    right_button = right_img.get_rect(topleft=(WIDTH - 100, HEIGHT // 2 + 15))
    confirm_button = confirm_img.get_rect(center=(WIDTH // 2, HEIGHT - 75))

    weapon_left_button = left_img.get_rect(topleft=(50, HEIGHT // 2 + 15))
    weapon_right_button = right_img.get_rect(topleft=(WIDTH - 100, HEIGHT // 2 + 15))
    weapon_confirm_button = confirm_img.get_rect(center=(WIDTH // 2, HEIGHT - 75))

    # Police pour l'affichage du texte
    font = pygame.font.Font(None, 36)

    # Variables de sélection
    selected_character = None
    selected_weapon = None
    character_selected = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if not character_selected:
                    if left_button.collidepoint(mouse_pos):
                        selected_index = (selected_index - 1) % len(characters)
                    elif right_button.collidepoint(mouse_pos):
                        selected_index = (selected_index + 1) % len(characters)
                    elif confirm_button.collidepoint(mouse_pos):
                        selected_character = characters[selected_index]
                        character_selected = True
                else:
                    if weapon_left_button.collidepoint(mouse_pos):
                        selected_weapon_index = (selected_weapon_index - 1) % len(weapons)
                    elif weapon_right_button.collidepoint(mouse_pos):
                        selected_weapon_index = (selected_weapon_index + 1) % len(weapons)
                    elif weapon_confirm_button.collidepoint(mouse_pos):
                        selected_weapon = weapons[selected_weapon_index]
                        running = False

        if not character_selected:
            character_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
            pygame.draw.rect(screen, GRAY, character_rect)
            character_text = font.render(characters[selected_index], True, BLACK)
            text_rect = character_text.get_rect(center=character_rect.center)
            screen.blit(character_text, text_rect)

            screen.blit(left_img, left_button.topleft)
            screen.blit(right_img, right_button.topleft)
            screen.blit(confirm_img, confirm_button.topleft)
        else:
            weapon_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
            pygame.draw.rect(screen, GRAY, weapon_rect)
            weapon_text = font.render(weapons[selected_weapon_index], True, BLACK)
            weapon_text_rect = weapon_text.get_rect(center=weapon_rect.center)
            screen.blit(weapon_text, weapon_text_rect)

            screen.blit(left_img, weapon_left_button.topleft)
            screen.blit(right_img, weapon_right_button.topleft)
            screen.blit(confirm_img, weapon_confirm_button.topleft)
        pygame.display.flip()
