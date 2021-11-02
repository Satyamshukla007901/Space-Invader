import pygame
import random
import math

from pygame import mixer
#Hndling Music
pygame.init()
#Background Music
mixer.music.load("Programming\python\Space-Invader\mbackground.wav")
mixer.music.play(-1)


# initialise the pygame


# create the screen # Width,Height
screen = pygame.display.set_mode((800, 600))
# Screen will display till the the final termination of the program
# If we set an infinite loop then the screen will be avaible always to us but in a hang mode as it is in a inifnite loop

# so we add an event that when the red Cross is pressed so the quit event make the running to false forcing the termination of the pro gram to stop

# Background
background = pygame.image.load(
    'Programming\python\Space-Invader\gbackground.png')
#Title and Icon
pygame.display.set_caption("Space-Invaders")
icon = pygame.image.load('Programming\python\Space-Invader\ship.png')
pygame.display.set_icon(icon)

# Adding a Player image
playerimg = pygame.image.load(
    'Programming\python\Space-Invader\playership.png')
playerX = 380
playerY = 480
playerXchange = 0

# Score
score_value = 0
font = pygame.font.Font('Programming\python\Space-Invader\ScarletJosephine.ttf', 50)

textX = 10
textY = 10

#Game Over text
over_font = pygame.font.Font('Programming\python\Space-Invader\ScarletJosephine.ttf',80)


def show_score(x, y):
    score = font.render("Score : "+str(score_value), True, (255, 50, 50))
    screen.blit(score,(x,y))

#game over
def game_over_text():
    over_text = over_font.render("GAME OVER!!",True,(255,50,50))
    screen.blit(over_text,(200,260))


# function to create a player


def player(x, y):
    screen.blit(playerimg, (x, y))


# Adding an Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num_of_enemies = 7
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load(
        'Programming\python\Space-Invader\space-invaders.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(4)
    enemyYchange.append(40)

# Adding an Bullet
# Ready - You Cant see the bullet on the Screen
# Fire - The Bullet Is Currently Moving
bulletimg = pygame.image.load('Programming\python\Space-Invader\gbullets.png')
bulletX = 0
bulletY = 480
bulletXchange = 0
bulletYchange = 10
bullet_state = "ready"


# function to create a enemy
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# function of firing bullet


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))

# Collision function


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # Background color
    # RGB = Red , Green, Blue
    screen.fill((255, 0, 150))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard Input Event and Press Events
    # if keystroke is pressed check whther its is right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -5
            if event.key == pygame.K_RIGHT:
                playerXchange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('Programming\python\Space-Invader\laser.wav')
                    bullet_sound.play()
                    # get the current X coordinate of the space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0

    # player should be drawn after the background fill as the image of player should appear over the background
    # Checing for the boundaries of spaceship so it doesnt go out of bounds
    playerX += playerXchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[i] = 2000
            game_over_text()
            break


        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 4
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 736:
            enemyXchange[i] = -4
            enemyY[i] += enemyYchange[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exp_sound = mixer.Sound('Programming\python\Space-Invader\explosion.wav')
            exp_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # to update the screen
