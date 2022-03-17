import pygame
import globalVariables

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, direction, enemy, window):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/sprites/bone.png").convert_alpha()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/5), int(self.size[1]/5)))
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x + 45
        self.rect.y = enemy.rect.y + 60
        self.velocity = 10
        self.screen_width = window.get_width()
        self.screen_height = window.get_height()
        self.attack = 100
        self.direction = direction
    
    def remove(self):
        globalVariables.meteorites.remove(self)
    
    def move(self, enemy, player):
        if(self.direction > 0):
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity
        if(pygame.sprite.collide_rect(self, player)):
            self.remove()
            player.damage(self.attack)
        # if self.rect.y > self.screen_height:
        #     self.remove()

