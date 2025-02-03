import pygame
pygame.init()

class Player(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()

class Master(pygame.sprite.Sprite) :
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.image = pygame.image.load('assets/mummy.png')
        self.rect = self.image.get_rect()


pygame.display.set_caption("Simple Game")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("assets/bg.jpg")

player = Player()

runnig = True
while runnig:

    screen.blit(background, (0, -200))

    screen.blit(player, (0, -200))

    pygame.display.flip()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            runnig = False
            pygame.quit()
            print("fermeture du jeu")