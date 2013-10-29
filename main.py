import pygame
import math
import random
import os

from pygame.locals import *

pygame.init()
width, height = 620, 480
screen = pygame.display.set_mode((width,height))
badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue= 260
accuracy = [0,0]
cannonBalls=[]

# ^^setting some local vars to be used later

current_directory = os.getcwd()

player = pygame.image.load(os.path.join(current_directory, "cannon1small.png"))
background = pygame.image.load(os.path.join(current_directory, "background.png"))
tower = pygame.image.load(os.path.join(current_directory, "towersized.png"))
cannonBall= pygame.image.load(os.path.join(current_directory, "cannonBall.png"))
badGuyImg1 = pygame.image.load(os.path.join(current_directory, "badguy.png"))
badGuyImg = badGuyImg1
healthBar = pygame.image.load(os.path.join(current_directory, "healthbarred.png"))
health = pygame.image.load(os.path.join(current_directory, "healthbargreen.png"))
gameOver = pygame.image.load(os.path.join(current_directory, "gameover.png"))

#^^setting the image for everything on screen

running = 1
while running: #while the end game requirements have not been met
    badtimer= badtimer - 1
    screen.fill(0)
    screen.blit(background,(0,0))
    screen.blit(tower,(0,50))
    playerPos = [160,155]
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]- (playerPos[1]),position[0] -(playerPos[0]))
    playerRot = pygame.transform.rotate(player, 360-angle*57.29)#turns the player according to mouse position
    playerPos1 = (playerPos[0]-playerRot.get_rect().width/2, playerPos[1]-playerRot.get_rect().height/2) 
    screen.blit(playerRot, playerPos1)
    for bullet in cannonBalls:
        index=0
        velx=math.cos(bullet[0])*8 #determines how fast the canonballs are going based on their position
        vely=math.sin(bullet[0])*8
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            cannonBalls.pop(index) #gets rid of the cannonball if it goes off screen
        index+=1
        for projectile in cannonBalls:
            screen.blit(cannonBall, (projectile[1], projectile[2])) 
    if badtimer==0: #Creates new Bad Guy after a set amount of time
        badguys.append([640, random.randint(50,430)]) #places the bad guy at a random place between (640,50)and*640,430)
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index=0
    for badguy in badguys:
        if badguy[0]<-90: #Removes bad guy if they go off screen
            badguys.pop(index)
        badguy[0]-=10 #speed of bad guy movement
        badrect=pygame.Rect(badGuyImg.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<90: #checks if bad guy hits the tower
            healthvalue -= random.randint(10,30) #removes a random amount of health between 10 and 30
            badguys.pop(index) #removes bad guy
        index1=0
        for bullet in cannonBalls:
            bullrect=pygame.Rect(cannonBall.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect): #checks if cannonball hits bad guy
                accuracy[0]+=1 #increases accuracy
                badguys.pop(index) #removes bad guy
                cannonBalls.pop(index1)#removes cannon ball
            index1+=1

        index+=1
    for badguy in badguys: #make all bad guys appear
            screen.blit(badGuyImg, badguy)

    font = pygame.font.Font(None,40)
    text= font.render(str(pygame.time.get_ticks()/60000)+":"+str(pygame.time.get_ticks()/1000%60).zfill(2),True,(0,0,0))
    textRect=text.get_rect() #makes a timer
    textRect.topright=[600,5]
    screen.blit(text,textRect)
    
    screen.blit(healthBar, (8,8))
    for health1 in range (healthvalue-10): #displays healthbar
        screen.blit(health,(health1+8,8))#draws the smaller green healthbar image as many times as needed to fill up the red background
                      
    pygame.display.flip() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=pygame.mouse.get_pos()#creates a cannonball at the mouse position and adds 1 to the number of shots fired
            accuracy[1]+=1 
            cannonBalls.append([math.atan2(position[1]-(playerPos1[1]+32),position[0]-(playerPos1[0]+26)),playerPos1[0]+32, playerPos1[1]+32])  
        if healthvalue <= 0:
            running = 0
        if accuracy[1]!=0:
            accuracyScore = round(accuracy[0]*1.0/accuracy[1]*100,1) #calculates accuracy to the nearest decimal point
        else:
            accuracyScore = 0
pygame.font.init()
font = pygame.font.Font(None,40)
text = font.render("Accuracy: "+str(accuracyScore)+"%",True,(0,0,0)) #(0,0,0) sets the RGB
timeText= font.render("You survived "+str(pygame.time.get_ticks()/60000)+" minutes and "+str(pygame.time.get_ticks()/1000%60)+" seconds.",True,(0,0,0))
textRect = text.get_rect() 
timeTextRect= timeText.get_rect()
timeTextRect.centerx = screen.get_rect().centerx
timeTextRect.centery = screen.get_rect().centery+80
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery+40
screen.blit(gameOver,(0,0)) #displays the game over image,accuracy,and time survived
screen.blit(text,textRect)
screen.blit(timeText,timeTextRect)
while 1: #exits the game if the x button is pressed on the pygame window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
