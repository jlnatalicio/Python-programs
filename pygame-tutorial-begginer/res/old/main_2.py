import pygame
from pygame import mixer
import random
import math

# initialize pygame module
pygame.init()

# create screen (height x width)
screen = pygame.display.set_mode((640, 480))

# Title and Icon of window
# "Icon made by Smashicons from www.flaticon.com"
pygame.display.set_caption("Space Invaders PyClone")
icon = pygame.image.load('res/img/space-invaders.png')
pygame.display.set_icon(icon)

# Create Background
# ("Sound made by VABsounds from www.freesound.org")
background_img = pygame.image.load('res/img/background.png')
mixer.music.load('res/sounds/background.wav')
mixer.music.play(-1)

# Create Player
player_img = pygame.image.load('res/img/player.png')
# player initial position
player_x = 304
player_y = 420
player_x_change = 0.0

# Score ("Font made by Geronimo Font Studios from www.dafont.com")
score = 0
font = pygame.font.Font('res/fonts/Gameplay.ttf', 16)
text_x = 10
text_y = 10
game_over_font = pygame.font.Font('res/fonts/Gameplay.ttf', 64)

# Create Bullet
# ("Sounds made by TheDweebMan and kutejnikov from www.freesound.org")
bullet_img = pygame.image.load('res/img/bullet.png')
bullet_x = 0
bullet_y = player_y
bullet_y_change = 0.3
bullet_state = "ready"                                                           

# Create Enemy
# "Icon made by Freepik from www.flaticon.com"
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for i in range(num_enemies):
      enemy_img.append(pygame.image.load('res/img/alien1.png')) 
      enemy_x.append( float(random.randint(0, 608)) )
      enemy_y.append( float(random.randint(50, 100)) ) 
      enemy_x_change.append(0.18)
      enemy_y_change.append(32.0)

def drawGameOverScreen():
      game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
      screen.blit(game_over_text, (128, 128))

def drawScore(x, y):
      score_value = font.render("Hi-Score: " + str(score), True, (255,255,255))
      screen.blit(score_value, (x, y))

def drawPlayer(pos_x, pos_y):
      screen.blit(player_img, (pos_x, pos_y)) # draw player on screen

def drawEnemy(pos_x, pos_y, i):
      screen.blit(enemy_img[i], (pos_x, pos_y))  # draw enemy on screen

def fireBullet(x, y):
      global bullet_state # you can access this variable in the function using global
      bullet_state = "fire"
      screen.blit(bullet_img, (x, y))

def checkCollision(x1, y1, x2, y2):
      x_coordinate_sqr = (x1 - x2) ** 2
      y_coordinate_sqr = (y1 - y2) ** 2
      distance = math.sqrt(x_coordinate_sqr + y_coordinate_sqr)

      if distance < 16.0:
            return True
      else:
            return False

game_is_running = True
while game_is_running:                        # sets game loop
      
      # paint screen R  G  B
      screen.fill((0, 0, 0))

      #draw background
      screen.blit(background_img, (0, 0))
      
      for event in pygame.event.get():
            if (event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE):
                  game_is_running = False

            # if keystroke is pressed, check whether its right or left
            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_LEFT:
                        player_x_change = -0.2
                  if event.key == pygame.K_RIGHT:
                        player_x_change = 0.2
                  if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                              bullet_sound = mixer.Sound('res/sounds/laser.wav')
                              bullet_sound.play()
                              # get current x coordinate of spaceship
                              bullet_x = player_x
                              fireBullet(bullet_x, bullet_y)
                  if event.key == pygame.K_ESCAPE:
                        game_is_running = False

            # if keystroke is released, check whether its right or left            
            if event.type == pygame.KEYUP:
                  if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player_x_change = 0.0

      # update player movement and keeping the player on the boundaries of screen
      player_x += player_x_change           
      if player_x < 0:           
            player_x = 0                    
      elif player_x > 604:                  
            player_x = 604

      # update enemy movement and keeping the enemy on the boundaries of screen
      for i in range(num_enemies):
            # Game Over
            if enemy_y[i] > player_y:
                  for j in range(num_enemies):
                        enemy_y[j] = 2000
                  drawGameOverScreen()
                  break
            
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0.0:           
                  enemy_x_change[i] = 0.18           
                  enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] > 604.0:                   
                  enemy_x_change[i] = -0.18
                  enemy_y[i] += enemy_y_change[i]

            bullet_hit = checkCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if bullet_hit:
                  bullet_y = player_y
                  bullet_state = "ready"
                  score += 1
                  enemy_x[i] = float(random.randint(0, 608))
                  enemy_y[i] = float(random.randint(50, 100))

            drawEnemy(enemy_x[i], enemy_y[i], i)

      # update bullet movement
      if bullet_y <= 0:              # when bullet hits the top of the screen...         
            bullet_y = player_y      # teleport to player's position
            bullet_state = "ready"   # and prepare it to be fired again
      
      if bullet_state == "fire":
            fireBullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

      # collision
      bullet_hit = checkCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
      if bullet_hit:
            explosion_sound = mixer.Sound('res/sounds/explosion.wav')
            explosion_sound.play()
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy_x = random.randint(0, 608)
            enemy_y = random.randint(50, 100)
      
      drawPlayer(player_x, player_y)
      drawScore(text_x, text_y)
      pygame.display.update()               # we need to update the screen to see changes

pygame.font.quit()
pygame.mixer.quit()
pygame.display.quit()                       # unitialize module and close window
