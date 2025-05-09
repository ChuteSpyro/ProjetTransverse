import pygame
import sys

# Initialisation de pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = 1080, 720  # Définition d'une taille de fenêtre plus petite
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Suppression de pygame.FULLSCREEN
pygame.display.set_caption("Sélection des personnages et armes")

# Chargement des images
background = pygame.image.load("assets/bg.png")
left_img = pygame.image.load("assets/left_button.png")
right_img = pygame.image.load("assets/right_button.png")
confirm_img = pygame.image.load("assets/confirm_button.png")

# Redimensionnement dynamique des images
def resize_image(img, scale):
    return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

left_img = resize_image(left_img, 0.1)
right_img = resize_image(right_img, 0.1)
confirm_img = resize_image(confirm_img, 0.5)

character_images = {
    "fleur": pygame.image.load("assets/fleur.png"),
    "ghost": pygame.image.load("assets/ghost.png"),
}

weapon_images = {
    "Axe": pygame.image.load("assets/Axe.png"),
    "dagger": pygame.image.load("assets/dagger.png"),
}

characters = ["fleur", "ghost"]
weapons = ["Axe", "dagger"]
font = pygame.font.Font(None, 48)

def draw_selection(screen, x, y, label, name, left_button, right_button, confirm_button, is_character=True):
    text = font.render(label, True, (255, 255, 255))
    screen.blit(text, (x, y))

    if is_character:
        image = pygame.transform.scale(character_images[name], (200, 200))
    else:
        image = pygame.transform.scale(weapon_images[name], (200, 200))

    screen.blit(image, (x + 100, y + 40))
    screen.blit(left_img, left_button.topleft)
    screen.blit(right_img, right_button.topleft)
    screen.blit(confirm_img, confirm_button.topleft)

def character_and_weapon_select(screen):
    p1 = {"char": 0, "weapon": 0, "ready": False}
    p2 = {"char": 0, "weapon": 0, "ready": False}

    while True:
        screen.blit(pygame.transform.scale(background, (WIDTH, HEIGHT)), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if not p1["ready"]:
                    if left1_char.collidepoint((mx, my)):
                        p1["char"] = (p1["char"] - 1) % len(characters)
                    elif right1_char.collidepoint((mx, my)):
                        p1["char"] = (p1["char"] + 1) % len(characters)
                    elif left1_weapon.collidepoint((mx, my)):
                        p1["weapon"] = (p1["weapon"] - 1) % len(weapons)
                    elif right1_weapon.collidepoint((mx, my)):
                        p1["weapon"] = (p1["weapon"] + 1) % len(weapons)
                    elif confirm1.collidepoint((mx, my)):
                        p1["ready"] = True
                if not p2["ready"]:
                    if left2_char.collidepoint((mx, my)):
                        p2["char"] = (p2["char"] - 1) % len(characters)
                    elif right2_char.collidepoint((mx, my)):
                        p2["char"] = (p2["char"] + 1) % len(characters)
                    elif left2_weapon.collidepoint((mx, my)):
                        p2["weapon"] = (p2["weapon"] - 1) % len(weapons)
                    elif right2_weapon.collidepoint((mx, my)):
                        p2["weapon"] = (p2["weapon"] + 1) % len(weapons)
                    elif confirm2.collidepoint((mx, my)):
                        p2["ready"] = True

        # Placement dynamique des éléments sur l'écran
        x1 = WIDTH * 0.1
        x2 = WIDTH * 0.65
        y_char = HEIGHT * 0.2
        y_weapon = HEIGHT * 0.55

        left1_char = left_img.get_rect(topleft=(x1, y_char + 50))
        right1_char = right_img.get_rect(topleft=(x1 + 250, y_char + 50))
        confirm1 = confirm_img.get_rect(topleft=(x1 + 100, y_weapon + 220))
        left1_weapon = left_img.get_rect(topleft=(x1, y_weapon + 50))
        right1_weapon = right_img.get_rect(topleft=(x1 + 250, y_weapon + 50))

        left2_char = left_img.get_rect(topleft=(x2, y_char + 50))
        right2_char = right_img.get_rect(topleft=(x2 + 250, y_char + 50))
        confirm2 = confirm_img.get_rect(topleft=(x2 + 100, y_weapon + 220))
        left2_weapon = left_img.get_rect(topleft=(x2, y_weapon + 50))
        right2_weapon = right_img.get_rect(topleft=(x2 + 250, y_weapon + 50))

        draw_selection(screen, x1, y_char, "Perso J1", characters[p1["char"]], left1_char, right1_char, confirm1, True)
        draw_selection(screen, x1, y_weapon, "Arme J1", weapons[p1["weapon"]], left1_weapon, right1_weapon, confirm1, False)
        draw_selection(screen, x2, y_char, "Perso J2", characters[p2["char"]], left2_char, right2_char, confirm2, True)
        draw_selection(screen, x2, y_weapon, "Arme J2", weapons[p2["weapon"]], left2_weapon, right2_weapon, confirm2, False)

        if p1["ready"]:
            screen.blit(font.render("READY", True, (0, 255, 0)), (x1 + 120, y_weapon + 280))
        if p2["ready"]:
            screen.blit(font.render("READY", True, (0, 255, 0)), (x2 + 120, y_weapon + 280))

        pygame.display.flip()

        if p1["ready"] and p2["ready"]:
            pygame.time.delay(1000)
            return {
                "joueur1": {"personnage": characters[p1["char"]], "arme": weapons[p1["weapon"]]},
                "joueur2": {"personnage": characters[p2["char"]], "arme": weapons[p2["weapon"]]},
            }

if __name__ == "__main__":
    choix = character_and_weapon_select(screen)
    print("Sélections faites :")
    print(choix)

def map_selection(screen):
    pygame.display.set_caption("Sélection de la carte")
    font = pygame.font.Font(None, 36)

    maps = ["Forêt", "Désert", "Lave"]
    selected = 0

    running = True
    while running:
        screen.fill((50, 50, 50))
        title = font.render("Choisissez la carte", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, name in enumerate(maps):
            color = (0, 200, 0) if i == selected else (200, 200, 200)
            pygame.draw.rect(screen, color, (WIDTH // 2 - 100, 150 + i * 80, 200, 60))
            text = font.render(name, True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 165 + i * 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(maps)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(maps)
                elif event.key == pygame.K_RETURN:
                    return maps[selected]

        pygame.display.flip()

def map_selection(screen):
    pygame.display.set_caption("Sélection de la carte")
    font = pygame.font.Font(None, 36)

    maps = ["Forêt", "Désert", "Lave"]
    selected = 0

    running = True
    while running:
        screen.fill((50, 50, 50))
        title = font.render("Choisissez la carte", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, name in enumerate(maps):
            color = (0, 200, 0) if i == selected else (200, 200, 200)
            pygame.draw.rect(screen, color, (WIDTH // 2 - 100, 150 + i * 80, 200, 60))
            text = font.render(name, True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 165 + i * 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(maps)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(maps)
                elif event.key == pygame.K_RETURN:
                    return maps[selected]

        pygame.display.flip()

