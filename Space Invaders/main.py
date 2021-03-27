import random
import math
import pygame
from pygame import mixer



#Initialize the pygame
pygame.init()

#Create the Screen
screen = pygame.display.set_mode((800,600))

"""Anything inside the game window is called an event"""


#Title and Icon

pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Player

playerImg=pygame.image.load("player.png")
playerX=370
playerY=480
playerX_change=0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	
	enemyImg.append(pygame.image.load("enemy.png"))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(4)
	enemyY_change.append(40)

#Bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state = "ready"

#Ready = You can't see the bullet on the screen
#Fire = The fire is currently moving


#Background
background=pygame.image.load("background.png")

#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

#Game over text
over_font=pygame.font.Font('freesansbold.ttf',32)

def game_over_text():
	over_text=over_font.render("GAME OVER",True,(255,0,0))
	screen.blit(over_text,(200,250))

def show_score(x,y):
	score=font.render("Score:" + str(score_value),True,(255,255,255) )
	screen.blit(score,(x,y))

def player(x,y):
	screen.blit(playerImg,(x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
		global bullet_state
		bullet_state = "fire"
		screen.blit(bulletImg, (x + 16, y + 10))

""" Everything we want to see persistently whether an image or anything it has to go inside this running infinite while loop """

def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt( (math.pow(enemyX-bulletX,2) ) + (math.pow(enemyY-bulletY,2) ) )
	if distance<27:
		return True

#Game loop
running = True
while running:
	#adds color to the screen
	screen.fill((225,0,0))
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		#getting the key is pressed
		if event.type==pygame.KEYDOWN:
			#when left arrow is pressed it subtracts value
			if event.key==pygame.K_LEFT:
				playerX_change=-5
			#when right arrow is pressed it adds value	
			if event.key==pygame.K_RIGHT:
				playerX_change=5

			if event.key==pygame.K_SPACE:
				
				if bullet_state=="ready":
					bullet_Sound=mixer.Sound('laser.wav')
					bullet_Sound.play()
					#get the current x Cooridinate of the spaceship
					bulletX=playerX
					fire_bullet(bulletX,bulletY)

		#getting the key is released
		if event.type==pygame.KEYUP:
			playerX_change=0

		#quitting the game window without which it will be on an infinite loop
			
		if event.type == pygame.QUIT:
			running = False

	#Adding boundaries to the game 
	if playerX<=0:
		playerX=0
	elif playerX>=736:
		playerX=736

	#TO move the spaceship left and right by adding the playerX_change values when we get the values 
	playerX+=playerX_change

	#Enemy movement
	for i in range(num_of_enemies):

		#game over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j]=2000
			game_over_text()
			break


		enemyX[i]+=enemyX_change[i]

		if enemyX[i]<=0:
			enemyX_change[i]=4
			enemyY[i]+=enemyY_change[i]
		elif enemyX[i]>=736:
			enemyX_change[i]=-4
			enemyY[i]+=enemyY_change[i]

		#Collision

		collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosion_sound=mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY=480
			bullet_state="ready"
			score_value+=1
			
			enemyX[i]=random.randint(0,735)
			enemyY[i]=random.randint(50,150)	

		enemy(enemyX[i],enemyY[i],i)
	# Bullet Movement
	if bulletY<=0:
		bulletY=480
		bullet_state="ready"
		
	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change

	


	#Calling the player and enemy function
	player(playerX,playerY)
	
	show_score(textX,textY)

	#updates the screen to refresh what has happen
	pygame.display.update()

