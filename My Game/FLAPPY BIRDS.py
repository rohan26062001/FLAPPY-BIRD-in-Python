##Importing Libraries

import random
import sys
import pygame
from pygame.locals import *


##Declaring Global Variables

FPS=40
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/bird.png'       #Path of the image of the player
BACKGROUND='C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/background.jpg'   #Path of the image of the background
PIPE='C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/pipe.png'         #Path of the image of the Pipe


##Opening Screen Function
def openGame():
    x_player=int(SCREENWIDTH/5)
    y_player=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    x_message=int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    y_message=int((SCREENWIDTH - 0.3*GAME_SPRITES['message'].get_height())/2)
    x_base=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(x_base,GROUNDY))
                SCREEN.blit(GAME_SPRITES['message'],(x_message,y_message))
                SCREEN.blit(GAME_SPRITES['player'],(x_player,y_player))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
    
##Main Game Function
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return     

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +5:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe
    
##Main Function
if __name__=="__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Rohan,Aritri,Hritika and Ishak')
    # Game sprites
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/0.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/1.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/2.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/3.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/4.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/5.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/6.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/7.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/8.png').convert_alpha(),
        pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/new.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('C:/Users/rohan/Desktop/Python Game/My Game/Images/Images/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180), 
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Game sounds
    GAME_SOUNDS['music'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/mainmusic.mp3')
    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('C:/Users/rohan/Desktop/Python Game/My Game/Audio/wing.wav')

    
    openGame()
    mainGame()
