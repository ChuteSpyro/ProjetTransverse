
import pygame
import sys

# init pygame
pygame.init()

# taille écran
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sélection des persos et map")

# police
font = pygame.font.Font(None, 48)

# images de fond et boutons
background = pygame.image.load("assets/backgrounds/bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

left_img = pygame.image.load("assets/buttons/left_button.png")
right_img = pygame.image.load("assets/buttons/right_button.png")
confirm_img = pygame.image.load("assets/buttons/confirm_button.png")

# on les rend plus petits
left_img = pygame.transform.scale(left_img, (50, 50))
right_img = pygame.transform.scale(right_img, (50, 50))
confirm_img = pygame.transform.scale(confirm_img, (150, 60))

# persos et armes
character_images = {
    "fleur": pygame.image.load("assets/characters/fleur.png"),
    "ghost": pygame.image.load("assets/characters/ghost.png"),
}
weapon_images = {
    "Axe": pygame.image.load("assets/weapons/Axe.png"),
    "dagger": pygame.image.load("assets/weapons/dagger.png"),
}

characters = ["fleur", "ghost"]
weapons = ["Axe", "dagger"]

# === Fonction sélection persos + armes ===
def character_and_weapon_select(screen):
    p1_char, p1_weapon = 0, 0
    p2_char, p2_weapon = 0, 0
    p1_ready, p2_ready = False, False

    running = True
    while running:
        screen.blit(background, (0, 0))

        x1 = WIDTH * 0.1
        x2 = WIDTH * 0.65
        y_char = HEIGHT * 0.2
        y_weapon = HEIGHT * 0.55

        # Boutons J1
        left1_char = left_img.get_rect(topleft=(x1, y_char + 50))
        right1_char = right_img.get_rect(topleft=(x1 + 250, y_char + 50))
        confirm1 = confirm_img.get_rect(topleft=(x1 + 100, y_weapon + 220))
        left1_weapon = left_img.get_rect(topleft=(x1, y_weapon + 50))
        right1_weapon = right_img.get_rect(topleft=(x1 + 250, y_weapon + 50))

        # Boutons J2
        left2_char = left_img.get_rect(topleft=(x2, y_char + 50))
        right2_char = right_img.get_rect(topleft=(x2 + 250, y_char + 50))
        confirm2 = confirm_img.get_rect(topleft=(x2 + 100, y_weapon + 220))
        left2_weapon = left_img.get_rect(topleft=(x2, y_weapon + 50))
        right2_weapon = right_img.get_rect(topleft=(x2 + 250, y_weapon + 50))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if not p1_ready:
                    if left1_char.collidepoint((mx, my)):
                        p1_char = (p1_char - 1) % len(characters)
                    elif right1_char.collidepoint((mx, my)):
                        p1_char = (p1_char + 1) % len(characters)
                    elif left1_weapon.collidepoint((mx, my)):
                        p1_weapon = (p1_weapon - 1) % len(weapons)
                    elif right1_weapon.collidepoint((mx, my)):
                        p1_weapon = (p1_weapon + 1) % len(weapons)
                    elif confirm1.collidepoint((mx, my)):
                        p1_ready = True

                if not p2_ready:
                    if left2_char.collidepoint((mx, my)):
                        p2_char = (p2_char - 1) % len(characters)
                    elif right2_char.collidepoint((mx, my)):
                        p2_char = (p2_char + 1) % len(characters)
                    elif left2_weapon.collidepoint((mx, my)):
                        p2_weapon = (p2_weapon - 1) % len(weapons)
                    elif right2_weapon.collidepoint((mx, my)):
                        p2_weapon = (p2_weapon + 1) % len(weapons)
                    elif confirm2.collidepoint((mx, my)):
                        p2_ready = True

        # affichage J1
        text1 = font.render("Player 1", True, (255, 255, 255))
        screen.blit(text1, (x1 + 100, y_char - 60))
        screen.blit(pygame.transform.scale(character_images[characters[p1_char]], (200, 200)), (x1 + 50, y_char))
        screen.blit(left_img, left1_char.topleft)
        screen.blit(right_img, right1_char.topleft)

        screen.blit(pygame.transform.scale(weapon_images[weapons[p1_weapon]], (200, 200)), (x1 + 50, y_weapon + 10))
        screen.blit(left_img, left1_weapon.topleft)
        screen.blit(right_img, right1_weapon.topleft)
        screen.blit(confirm_img, confirm1.topleft)

        if p1_ready:
            ready_text = font.render("READY", True, (0, 255, 0))
            screen.blit(ready_text, (x1 + 120, y_weapon + 280))

        # affichage J2
        text2 = font.render("Player 2", True, (255, 255, 255))
        screen.blit(text2, (x2 + 100, y_char - 60))
        screen.blit(pygame.transform.scale(character_images[characters[p2_char]], (200, 200)), (x2 + 50, y_char  ))
        screen.blit(left_img, left2_char.topleft)
        screen.blit(right_img, right2_char.topleft)


        screen.blit(pygame.transform.scale(weapon_images[weapons[p2_weapon]], (200, 200)), (x2 + 50, y_weapon + 10))
        screen.blit(left_img, left2_weapon.topleft)
        screen.blit(right_img, right2_weapon.topleft)
        screen.blit(confirm_img, confirm2.topleft)

        if p2_ready:
            ready_text = font.render("READY", True, (0, 255, 0))
            screen.blit(ready_text, (x2 + 120, y_weapon + 280))

        pygame.display.flip()

        if p1_ready and p2_ready:
            pygame.time.delay(1000)
            return {
                "player1": {"character": characters[p1_char], "weapon": weapons[p1_weapon]},
                "player2": {"character": characters[p2_char], "weapon": weapons[p2_weapon]}
            }

# === Fonction sélection de la map avec boutons image ===
def map_selection(screen):
    pygame.display.set_caption("Choix de la map")

    bg = pygame.image.load("assets/backgrounds/bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    earth_img = pygame.image.load("assets/buttons/button_earth.png")
    moon_img = pygame.image.load("assets/buttons/button_moon.png")
    mars_img = pygame.image.load("assets/buttons/button_mars.png")

    earth_rect = earth_img.get_rect(center=(WIDTH // 2, 250))
    moon_rect = moon_img.get_rect(center=(WIDTH // 2, 370))
    mars_rect = mars_img.get_rect(center=(WIDTH // 2, 490))

    en_cours = True
    while en_cours:
        screen.blit(bg, (0, 0))
        screen.blit(earth_img, earth_rect)
        screen.blit(moon_img, moon_rect)
        screen.blit(mars_img, mars_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if earth_rect.collidepoint(pos):
                    return "Earth"
                if moon_rect.collidepoint(pos):
                    return "Moon"
                if mars_rect.collidepoint(pos):
                    return "Mars"

        pygame.display.flip()

# === Lancement ===
if __name__ == "__main__":
    selections = character_and_weapon_select(screen)
    print("Sélections faites :", selections)

    chosen_map = map_selection(screen)
    print("Map choisie :", chosen_map)
