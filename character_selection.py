import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Choose character")

# Couleurs utilisées
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
GREEN = (50, 200, 50)

# Liste des personnages (vous pouvez remplacer ces noms par des images ou d'autres ressources)
characters = ["Guerrier", "Mage", "Archer", "Voleur"]

# Indice du personnage actuellement sélectionné
selected_index = 0

# Définition des zones (rectangles) pour les boutons
left_button = pygame.Rect(50, HEIGHT // 2 - 25, 50, 50)
right_button = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 25, 50, 50)
confirm_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)

# Police pour l'affichage du texte
font = pygame.font.Font(None, 36)

# Variable qui contiendra le personnage validé
selected_character = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Bouton gauche : changer le personnage sélectionné vers la gauche
            if left_button.collidepoint(mouse_pos):
                selected_index = (selected_index - 1) % len(characters)

            # Bouton droit : changer le personnage sélectionné vers la droite
            elif right_button.collidepoint(mouse_pos):
                selected_index = (selected_index + 1) % len(characters)

            # Bouton valider : confirmer la sélection
            elif confirm_button.collidepoint(mouse_pos):
                selected_character = characters[selected_index]
                print("Personnage sélectionné :", selected_character)
                # Ici, vous pouvez transmettre la variable selected_character au reste du jeu
                running = False

    # Rafraîchissement de l'affichage
    screen.fill(WHITE)

    # Affichage du personnage sélectionné (représenté ici par un rectangle et le nom)
    character_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150)
    pygame.draw.rect(screen, GRAY, character_rect)
    character_text = font.render(characters[selected_index], True, BLACK)
    text_rect = character_text.get_rect(center=character_rect.center)
    screen.blit(character_text, text_rect)

    # Affichage du bouton gauche
    pygame.draw.rect(screen, BLUE, left_button)
    left_text = font.render("<", True, WHITE)
    left_text_rect = left_text.get_rect(center=left_button.center)
    screen.blit(left_text, left_text_rect)

    # Affichage du bouton droit
    pygame.draw.rect(screen, BLUE, right_button)
    right_text = font.render(">", True, WHITE)
    right_text_rect = right_text.get_rect(center=right_button.center)
    screen.blit(right_text, right_text_rect)

    # Affichage du bouton de validation
    pygame.draw.rect(screen, GREEN, confirm_button)
    confirm_text = font.render("Valider", True, WHITE)
    confirm_text_rect = confirm_text.get_rect(center=confirm_button.center)
    screen.blit(confirm_text, confirm_text_rect)

    pygame.display.flip()

# Après la boucle, la variable selected_character contient le personnage validé
print("Personnage final :", selected_character)

# Ici, vous pouvez poursuivre avec le reste de votre code de jeu en utilisant la variable selected_character.