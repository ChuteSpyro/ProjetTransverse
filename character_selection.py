import pygame
import sys

# Initialisation de Pygame
pygame.init()



def select_character(screen):
    # Dimensions de la fenêtre
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
    left_button = pygame.Rect(50, HEIGHT // 2 +15, 50, 50)
    right_button = pygame.Rect(WIDTH - 100, HEIGHT // 2 +15, 50, 50)
    confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)

    weapon_left_button = pygame.Rect(50, HEIGHT // 2 + 15, 50, 50)
    weapon_right_button = pygame.Rect(WIDTH - 100, HEIGHT // 2 + 15, 50, 50)
    weapon_confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)

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

        screen.fill(WHITE)

        if not character_selected:
            character_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
            pygame.draw.rect(screen, GRAY, character_rect)
            character_text = font.render(characters[selected_index], True, BLACK)
            text_rect = character_text.get_rect(center=character_rect.center)
            screen.blit(character_text, text_rect)

            pygame.draw.rect(screen, BLUE, left_button)
            left_text = font.render("<", True, WHITE)
            left_text_rect = left_text.get_rect(center=left_button.center)
            screen.blit(left_text, left_text_rect)

            pygame.draw.rect(screen, BLUE, right_button)
            right_text = font.render(">", True, WHITE)
            right_text_rect = right_text.get_rect(center=right_button.center)
            screen.blit(right_text, right_text_rect)

            pygame.draw.rect(screen, GREEN, confirm_button)
            confirm_text = font.render("Valider", True, WHITE)
            confirm_text_rect = confirm_text.get_rect(center=confirm_button.center)
            screen.blit(confirm_text, confirm_text_rect)
        else:
            weapon_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
            pygame.draw.rect(screen, GRAY, weapon_rect)
            weapon_text = font.render(weapons[selected_weapon_index], True, BLACK)
            weapon_text_rect = weapon_text.get_rect(center=weapon_rect.center)
            screen.blit(weapon_text, weapon_text_rect)

            pygame.draw.rect(screen, BLUE, weapon_left_button)
            weapon_left_text = font.render("<", True, WHITE)
            weapon_left_text_rect = weapon_left_text.get_rect(center=weapon_left_button.center)
            screen.blit(weapon_left_text, weapon_left_text_rect)

            pygame.draw.rect(screen, BLUE, weapon_right_button)
            weapon_right_text = font.render(">", True, WHITE)
            weapon_right_text_rect = weapon_right_text.get_rect(center=weapon_right_button.center)
            screen.blit(weapon_right_text, weapon_right_text_rect)

            pygame.draw.rect(screen, GREEN, weapon_confirm_button)
            weapon_confirm_text = font.render("Valider", True, WHITE)
            weapon_confirm_text_rect = weapon_confirm_text.get_rect(center=weapon_confirm_button.center)
            screen.blit(weapon_confirm_text, weapon_confirm_text_rect)
        pygame.display.flip()


# Ici, vous pouvez poursuivre avec le reste de votre code de jeu en utilisant selected_character et selected_weapon.
