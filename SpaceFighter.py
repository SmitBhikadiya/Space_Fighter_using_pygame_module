import pygame
import random
import math
import time
from pygame import mixer

# intialize the pygame
pygame.init()

# create the screen (width, height)
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('spacebg.jpg')

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# change the theme of windows
pygame.display.set_caption("Space Fighter (Smit Bhikadiya)")
icon = pygame.image.load('space-invaders-mini.png')
pygame.display.set_icon(icon)

# score
score_value = 0
flag = 1
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game_over
font_over = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, [0, 0, 255])
    screen.blit(score, (x, y))


# for player
playerLogo = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# for enemy
enemyLogo = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyLogo.append(pygame.image.load('pacman.png'))
	enemyX.append(random.randint(0, 735))
	enemyY.append(random.randint(30, 100))
	enemyX_change.append(3)
	enemyY_change.append(10)
	for i in range(9000):
		print(i)
	
# for bullet
# ready - you cant see the bullet on the screen
# fire - the bullet is currently moving
bulletLogo = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"


def player(x, y):
    screen.blit(playerLogo, (x, y))


def enemy(x, y, i):
    screen.blit(enemyLogo[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletLogo, (x + 16, y + 10))


def isCollision(X1, Y1, X2, Y2):
    distance = math.sqrt(math.fabs(math.pow(X2 - X1, 2) + math.pow(Y2 - Y1, 2)))
    if distance < 40:
        return True
    else:
        return False


def game_over(score_value):
    gover = font_over.render("GAME OVER", True, [255, 0, 0])
    score = font.render("Score :" + str(score_value), True, [0, 0, 0])
    screen.blit(score, (265, 320))
    screen.blit(gover, (200, 250))

# Game Loop
running = True
while running:

    # RGB color fill
    screen.fill((0, 0, 0))
    # set background
    screen.blit(background, (0, 30))
    # event for handling exit things when we hit cross button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # this for stop the loop when we press close button
            running = False
        # if keystroke is press check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('left arrow is pressed')
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                # print('right arrow is pressed')
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            # print('key has been release')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # checking for boundaries of spaceship so it dosen't go out of bound

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            flag = 0
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over(score_value)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision between enemy and bullet
        Wcollision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if Wcollision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 100)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if flag == 1:
        show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
