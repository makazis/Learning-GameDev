import pygame
from math import *
from random import *
class Card:
    def __init__(self): #Will be called when a new card is created
        self.sides={
            "Front":pygame.Surface((210,320)),
            "Back":pygame.Surface((210,320))
        } #2 sides for each card right now, maybe i'll add more later

        pygame.draw.rect(self.sides["Front"], (255, 255, 255), (0, 0, 210, 320), 0, 20) #RGB, Postiion, Border width, Border radius
        self.sides["Front"].set_colorkey((0,0,0)) #Removes black to transperent, Border/Rect

        pygame.draw.rect(self.sides["Back"], (55, 55, 55), (0, 0, 210, 320), 0, 20) #RGB, Postiion, Border width, Border radius
        self.sides["Back"].set_colorkey((0,0,0)) #Removes black to transperent, Border/Rect

        #MOdernise the back card with in loop rectengles

        self.sprite=pygame.Surface((210, 320))
        self.animations=[]
        self.front_visible=True #parbauda pusi, lai nevaretu apggriezt uz to pasu pusi
        
pygame.init()
win=pygame.display.set_mode((1200, 600)) #creates window
run=True

new_card = Card()

run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((0, 0, 0))

    win.blit(new_card.sides["Front"], (100, 100)) #draws surface on another surface

    win.blit(new_card.sides["Back"], (340, 100))

    pygame.display.update() #update the screen



pygame.quit()