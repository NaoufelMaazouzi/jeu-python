import pygame
import globalVariables

class Meteorite(pygame.sprite.Sprite):
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/meteorite.png").convert_alpha()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/5), int(self.size[1]/5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.velocity = 10
        self.screen_width = window.get_width()
        self.screen_height = window.get_height()
        self.attack = 100
    
    def remove(self):
        globalVariables.meteorites.remove(self)
    
    def move(self, player):
        self.rect.y += self.velocity
        if(pygame.sprite.collide_rect(self, player)):
            self.remove()
            player.damage(self.attack)
        if self.rect.y > self.screen_height:
            self.remove()

