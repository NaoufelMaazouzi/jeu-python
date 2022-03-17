import pygame

def init():
    global game_over, blob_group, meteorites, displayExit
    blob_group = pygame.sprite.Group()
    meteorites = pygame.sprite.Group()
    game_over = 0
    displayExit = False