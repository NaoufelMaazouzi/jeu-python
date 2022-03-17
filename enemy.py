import pygame
from enemyProjectile import EnemyProjectile
import globalVariables
import time

walkRight = [
    pygame.image.load('images/sprites/Enemy/Walk (1).png'),
    pygame.image.load('images/sprites/Enemy/Walk (2).png'),
    pygame.image.load('images/sprites/Enemy/Walk (3).png'),
    pygame.image.load('images/sprites/Enemy/Walk (4).png'),
    pygame.image.load('images/sprites/Enemy/Walk (5).png'),
    pygame.image.load('images/sprites/Enemy/Walk (6).png'),
    pygame.image.load('images/sprites/Enemy/Walk (7).png'),
    pygame.image.load('images/sprites/Enemy/Walk (8).png'),
    pygame.image.load('images/sprites/Enemy/Walk (9).png'),
    pygame.image.load('images/sprites/Enemy/Walk (10).png')
    ]
walkLeft = [
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (1).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (2).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (3).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (4).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (5).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (6).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (7).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (1).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (1).png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Enemy/Walk (1).png'), True, False)
    ]

walkRight = [pygame.transform.scale(image, (79.75, 121.5)) for image in walkRight]
walkLeft = [pygame.transform.scale(image, (79.75, 121.5)) for image in walkLeft]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.image = pygame.image.load("images/sprites/Enemy/Idle (1).png").convert_alpha()
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/4), int(self.size[1]/4)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.walkRight = walkRight
        self.walkLeft = walkLeft
        self.walkCount = 0
        self.health = 100
        self.maxHealth = 100
        self.all_bones = pygame.sprite.Group()
        # self.all_bones.add(EnemyProjectile(self.move_direction, self, self.window))
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
        if self.walkCount + 1 >= 24:
          self.walkCount = 0
        #   self.launch_projectile()
        if self.move_direction < 0: 
            self.window.blit(self.walkLeft[self.walkCount//3], (self.rect.x, self.rect.y))
            self.walkCount += 1                          
        elif self.move_direction > 0:
          self.window.blit(self.walkRight[self.walkCount//3], (self.rect.x, self.rect.y))
          self.walkCount += 1
        # pygame.draw.rect(self.window, (255, 255, 255), self.rect, 2)
    
    def update_health_bar(self, window):
        bar_color = (51, 183, 24)
        back_bar_color = (63, 68, 67)
        bar_position = [self.rect.x, self.rect.y, self.health, 5]
        back_bar_position = [self.rect.x, self.rect.y, self.maxHealth, 5]

        pygame.draw.rect(window, back_bar_color, back_bar_position)
        pygame.draw.rect(window, bar_color, bar_position)
    
    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            globalVariables.blob_group.remove(self)
    
    def launch_projectile(self):
        x = EnemyProjectile(self.move_direction, self, self.window)
        self.all_bones.add(x)


    
   