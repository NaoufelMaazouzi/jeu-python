import pygame
import globalVariables


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player, direction, window):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/sprites/fireball.png").convert_alpha()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/5), int(self.size[1]/5)))
        self.rect = self.image.get_rect()
        self.velocity = 20
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 45
        self.rect.y = player.rect.y + 60
        self.player = player
        self.screen_width = window.get_width()
        self.direction = direction
    
    def remove(self):
        self.player.all_projectiles.remove(self)
    
    def move(self):
        if self.direction == "right":
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity

        for enemy in pygame.sprite.spritecollide(self, globalVariables.blob_group, False, pygame.sprite.collide_mask):
            self.remove()
            enemy.damage(self.player.attack)
        if self.rect.x > self.screen_width:
            self.remove()

