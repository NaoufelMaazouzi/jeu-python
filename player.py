import pygame
import globalVariables
from projectile import Projectile

walkRight = [
    pygame.image.load('images/sprites/Player/Run__000.png'),
    pygame.image.load('images/sprites/Player/Run__001.png'),
    pygame.image.load('images/sprites/Player/Run__002.png'),
    pygame.image.load('images/sprites/Player/Run__003.png'),
    pygame.image.load('images/sprites/Player/Run__004.png'),
    pygame.image.load('images/sprites/Player/Run__005.png'),
    pygame.image.load('images/sprites/Player/Run__006.png'),
    pygame.image.load('images/sprites/Player/Run__007.png'),
    pygame.image.load('images/sprites/Player/Run__008.png'),
    pygame.image.load('images/sprites/Player/Run__009.png')
    ]
walkLeft = [
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__000.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__001.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__002.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__003.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__004.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__005.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__006.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__007.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__008.png'), True, False),
    pygame.transform.flip(pygame.image.load('images/sprites/Player/Run__009.png'), True, False)
    ]
jumpRight = [
    pygame.image.load('images/sprites/Player/Jump__000.png'),
    pygame.image.load('images/sprites/Player/Jump__001.png'),
    pygame.image.load('images/sprites/Player/Jump__002.png'),
    pygame.image.load('images/sprites/Player/Jump__003.png'),
    pygame.image.load('images/sprites/Player/Jump__004.png'),
    pygame.image.load('images/sprites/Player/Jump__005.png'),
    pygame.image.load('images/sprites/Player/Jump__006.png'),
    pygame.image.load('images/sprites/Player/Jump__007.png'),
    pygame.image.load('images/sprites/Player/Jump__008.png'),
    pygame.image.load('images/sprites/Player/Jump__009.png')
    ]

walkRight = [pygame.transform.scale(image, (79.75, 121.5)) for image in walkRight]
walkLeft = [pygame.transform.scale(image, (79.75, 121.5)) for image in walkLeft]
jumpRight = [pygame.transform.scale(image, (79.75, 121.5)) for image in jumpRight]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y, world)
        
        
    def update(self, window):
        dx = 0
        dy = 0
        if globalVariables.game_over == 0:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.launch_projectile(window)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.rect.x > self.vel:
                dx = -self.vel
                self.left = True
                self.right = False
                self.image = self.idleLeft
                self.direction = "left"
            elif keys[pygame.K_RIGHT] and self.rect.x < 1460 - self.vel:
                dx = self.vel
                self.right = True
                self.left = False
                sizeImg = self.idleRight.get_size()
                self.image = pygame.transform.scale(self.idleRight, (int(sizeImg[0]/4), int(sizeImg[1]/4)))
                self.direction = "right"
            else: 
                self.left = False
                self.right = False
                self.walkCount = 0
            if keys[pygame.K_SPACE] and self.jumped == False and self.vel_y == 0:
                self.vel_y = -15
                self.jumped = True
                self.left = False
                self.right = False
                self.walkCount = 0
            if keys[pygame.K_SPACE] == False:
                self.jumped = False
        

            #add gravity
            self.vel_y += 1.5
            if self.vel_y > 10:
                self.vel_y = 10
            if self.y == 0:
                self.jumped = False
            dy += self.vel_y

            for tile in self.world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and tile[2] == 'exit':
                    globalVariables.game_over = -1
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            if pygame.sprite.spritecollide(self, globalVariables.blob_group, False):
                globalVariables.game_over = -1

            self.rect.x += dx
            self.rect.y += dy

            if self.walkCount + 1 >= 24:
                self.walkCount = 0
            if self.left:
                window.blit(self.walkLeft[self.walkCount//3], (self.rect.x, self.rect.y))
                self.walkCount += 1                          
            elif self.right:
                window.blit(self.walkRight[self.walkCount//3], (self.rect.x, self.rect.y))
                self.walkCount += 1
            elif self.jumped:
                window.blit(self.jumpRight[self.walkCount//3], (self.rect.x, self.rect.y))
                self.walkCount += 1
            else:
                window.blit(self.image, (self.rect.x, self.rect.y))
                self.walkCount = 0
        
        elif globalVariables.game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5
            # globalVariables.displayExit = True
            
    def launch_projectile(self, window):
        self.all_projectiles.add(Projectile(self, self.direction, window))
    
    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            globalVariables.game_over = -1

    def reset(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.idleRight = pygame.image.load("images/sprites/Player/Idle__006.png").convert_alpha()
        self.idleLeft = pygame.transform.flip(self.idleRight, True, False)
        self.sizeIdleLeft = self.idleLeft.get_size()
        self.idleLeft = pygame.transform.scale(self.idleLeft, (int(self.sizeIdleLeft[0]/4), int(self.sizeIdleLeft[1]/4)))
        self.image = self.idleRight
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/4), int(self.size[1]/4)))
        self.dead_image = pygame.transform.scale(pygame.image.load('images/sprites/ghost.png').convert_alpha(), (100, 70))
        self.velocity = 5
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.walkRight = walkRight
        self.walkLeft = walkLeft
        self.jumpRight = jumpRight
        self.vel_y = 0
        self.vel = 7
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumped = False
        self.attack = 25
        self.all_projectiles = pygame.sprite.Group()
        self.direction = "right"
        self.health = 100
        
