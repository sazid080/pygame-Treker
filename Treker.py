import pygame
import random
import math

#initialize the pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800, 600))

#background image
background = pygame.image.load('background.jpg')

#title and icon
pygame.display.set_caption("Trekers")
icon = pygame.image.load('startrek.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('shooter.png')
playerX = 360
playerY = 450
playerX_change = 0
playerY_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,699))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.7)
    enemyY_change.append(40)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf',64)

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 50, y + 10))

#collision algo
def iscollision(enemyX, enemyY, bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + (math.pow(enemyY-bulletY,2)))
    if distance < 35:
        return True
    else:
        return False

#show score
def show_score(x, y):
    score = font.render("Score: " + str(score_value),True, (0,150,140))
    screen.blit(score, (x, y))

#game over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200,250))
    

#Game Loop
running = True
while running:
 
    #screen color
    screen.fill((0, 0, 0))

    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        
        #if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_UP:
                playerY_change = -1   
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_DOWN:
                playerY_change = 1
            if event.key == pygame.K_RCTRL:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0  

    #player movement
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= -100:
        playerX = 780
    elif playerX >= 800:
        playerX = -90
    if playerY <= -100:
        playerY = 580
    elif playerY >= 600:
        playerY = -90   

    #enemy movement
    for i in range(number_of_enemies):

        #game over
        if enemyY[i] > 450:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -40:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 700:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]

        #collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,699)
            enemyY[i]= random.randint(50,150)  

        enemy(enemyX[i], enemyY[i], i)          

    #bullet movement
    if bulletY <= -40:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()     