import pygame
import globalVariables
from player import Player
from world import World
from player import Player
from enemy import Enemy
from button import Button
from threading import Timer
import time

module_charge = pygame.init()
window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width = window.get_width()
screen_height = window.get_height()
pygame.display.set_caption('Jeu Naoufel')

clock = pygame.time.Clock()
background = pygame.image.load("images/background.png").convert()
startBtn = pygame.image.load("images/startBTN.png").convert_alpha()
exitBtn = pygame.image.load("images/exitBTN.png").convert_alpha()
restartBtn = pygame.image.load("images/restartBTN.png").convert_alpha()
globalVariables.init()
world = World(window)
player = Player(0, 700, world)
start_button = Button(screen_width // 2.7 - 350, screen_height // 2.5, startBtn, window)
exit_button = Button(screen_width // 2.4 + 150, screen_height // 2.68, exitBtn, window)
restart_button = Button(screen_width // 3, screen_height // 2.8, restartBtn, window)
enemy = Enemy(0, 900, window)
pygame.mixer.music.load("music/music.mp3")

class MainRun(object):
    def __init__(self):
        self.Main()

    def Main(self):
        global right, left, walkCount, isJump, jumpCount
        pygame.mixer.music.play()

        running = True
        main_menu = True
        t = Timer(10.0, world.launch_meteorites)
        t.start()
        projectile_count = 0

        while running:
          clock.tick(27)
          window.blit(background, (0,0))

          if main_menu == True:
            if exit_button.draw():
              running = False
            if start_button.draw():
              main_menu = False

          else:
            world.draw()

            if globalVariables.game_over == 0:
              globalVariables.blob_group.update()
              for meteorite in globalVariables.meteorites:
                meteorite.move(player)
              globalVariables.meteorites.draw(window)

              for blob in globalVariables.blob_group:
                blob.update_health_bar(window)
                if(projectile_count == 30):
                  blob.launch_projectile()  
                  projectile_count = 0
                projectile_count +=1
                for projectile in blob.all_bones:
                  projectile.move(blob, player)
                blob.all_bones.draw(window)

              player.update(window)

              for projectile in player.all_projectiles:
                projectile.move()
              player.all_projectiles.draw(window)
            
            if globalVariables.game_over == -1:
              if restart_button.draw():
                player.reset(100, screen_height - 130, world)
                globalVariables.game_over = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
              pygame.quit()
              running = False

          pygame.display.update()

          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False

        pygame.quit()

if __name__ == "__main__":
    MainRun()