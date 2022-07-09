import pygame
import random
import math
from pygame import mixer


# initialize pygame
pygame.init()
# sets height and width and creates the screen
screen = pygame.display.set_mode((800, 600))

# background img
background = pygame.image.load("space.back.jpg")
#bullet = pygame.image.load("bullet.png")

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title/caption and icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load("spaceShuttle.png.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("space-invaders.png")
# x and y coordinates
playerX = 390
playerY = 560
playerXchange = 0
playerYchange = 0

# Enemy
enemyImg = []
# x and y coordinates
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("alien (1).png"))
    # x and y coordinates
    enemyX.append(random.randint(0, 760))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.5)
    enemyYchange.append(20)

# bullet
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 560
bulletXchange = 0
bulletYchange = 1
# you can't see bullet on screen and fire means it's moving
bullet_state = "ready"

#score text and font
score_val=0
font = pygame.font.Font("Pixel Craft.ttf",22)
textX=10
textY=10

#gameovertext
over_font = pygame.font.Font("Pixel Craft.ttf",70)

def show_score(x,y):
    score = font.render("Score: "+ str(score_val), True,(34,0,102) )
    screen.blit(score, (x, y))

def game_over_text(x,y):
    over_text = font.render("GAME OVER" , True, (34, 0, 102))
    screen.blit(over_text, (300, 250))

def player(x, y):
    # drawing image in the window with blit
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # drawing image in the window with blit
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 15, y + 10))

def collided(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# this is a game loop so the window stays open
running = True
while running:
    # rgb values! And always updating
    screen.fill((70, 101, 119))
    # adding background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke pressed, check if it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -0.5
            if event.key == pygame.K_RIGHT:
                playerXchange = 0.5
            if event.key == pygame.K_SPACE:
                #get current x value of bullet
                if bullet_state == "ready":
                 bullet_sound = mixer.Sound("laser.wav")
                 bullet_sound.play()
                 bulletX= playerX
                 fire_bullet(bulletX,bulletY)
        # keyup means a key is released or not being pressed anymore
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    playerX += playerXchange
    # setting boundries of screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    # enemy movement
    for i in range(numOfEnemies):

        #Game Over
        if enemyY[i] >430:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text(250,250)
            break

        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 0.3
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 760:
            enemyXchange[i] = -0.3
            enemyY[i] += enemyYchange[i]

            # collision
        collision = collided(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
             exp_sound = mixer.Sound("explosion.wav")
             exp_sound.play()
             bulletY = 560
             bullet_state = "ready"
             score_val += 1
             enemyX[i] = random.randint(0, 800)
             enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
   #bullet movement
    if bulletY <=0:
        bulletY = 510
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

    #collision was here

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
