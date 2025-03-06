import pygame
import sys


def select_character(screen):
    """
    Affiche l'interface de sélection de personnage sur la fenêtre existante (screen)
    sans modifier le fond déjà présent, et retourne le personnage sélectionné.
    """
    # Récupère la taille de la fenêtre et capture le fond déjà présent
    WIDTH, HEIGHT = screen.get_size()
    background = screen.copy()

    # Définition des couleurs
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (50, 100, 200)
    GREEN = (50, 200, 50)
    WHITE = (255, 255, 255)

    # Liste des personnages (vous pouvez remplacer ces chaînes par des images)
    characters = ["Guerrier", "Mage", "Archer", "Voleur"]
    selected_index = 0

    # Définition des zones (rectangles) pour les boutons
    left_button = pygame.Rect(50, HEIGHT // 2 - 25, 50, 50)
    right_button = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 25, 50, 50)
    confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)

    # Police pour l'affichage du texte
    font = pygame.font.Font(None, 36)

    selected_character = None
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Bouton gauche : précédent personnage
                if left_button.collidepoint(mouse_pos):
                    selected_index = (selected_index - 1) % len(characters)
                # Bouton droit : personnage suivant
                elif right_button.collidepoint(mouse_pos):
                    selected_index = (selected_index + 1) % len(characters)
                # Bouton valider : confirmer la sélection
                elif confirm_button.collidepoint(mouse_pos):
                    selected_character = characters[selected_index]
                    print("Personnage sélectionné :", selected_character)
                    running = False

        # Restaurer le fond déjà présent
        screen.blit(background, (0, 0))

        # Dessiner le cadre du personnage sélectionné
        character_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
        pygame.draw.rect(screen, GRAY, character_rect)
        character_text = font.render(characters[selected_index], True, BLACK)
        text_rect = character_text.get_rect(center=character_rect.center)
        screen.blit(character_text, text_rect)

        # Bouton gauche
        pygame.draw.rect(screen, BLUE, left_button)
        left_text = font.render("<", True, WHITE)
        left_text_rect = left_text.get_rect(center=left_button.center)
        screen.blit(left_text, left_text_rect)

        # Bouton droit
        pygame.draw.rect(screen, BLUE, right_button)
        right_text = font.render(">", True, WHITE)
        right_text_rect = right_text.get_rect(center=right_button.center)
        screen.blit(right_text, right_text_rect)

        # Bouton de validation
        pygame.draw.rect(screen, GREEN, confirm_button)
        confirm_text = font.render("Valider", True, WHITE)
        confirm_text_rect = confirm_text.get_rect(center=confirm_button.center)
        screen.blit(confirm_text, confirm_text_rect)

        pygame.display.flip()
        clock.tick(60)  # Limite à 60 FPS

    return selected_character


# Exemple d'utilisation
if __name__ == "__main__":
    pygame.init()
    # Création d'une fenêtre avec un fond existant (ici un simple fond coloré)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Jeu principal")
    # Simulation d'un fond déjà présent
    screen.fill((100, 100, 100))  # fond gris foncé
    pygame.display.flip()

    # Appel de la fonction de sélection qui s'affichera sur le fond existant
    chosen_character = select_character(screen)
    print("Personnage final :", chosen_character)

    # Boucle principale fictive pour le jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()