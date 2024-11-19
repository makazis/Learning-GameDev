import pygame
from math import *
from random import *
from card import *
pygame.init()
win=pygame.display.set_mode((1200,600))
run=True
cards=[Card() for i in range(5)]
#new_card=Card()
#new_card.side_from_surface(pygame.image.load("Resources/Sprites/Blue Eyes White Dragon.jpg"),"BEWD")

frame=0
clock=pygame.time.Clock()
while run:
    clock.tick(100)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((55,55,55)) #Deletes the screen, fills all with black
    for I,i in enumerate(cards):
        i.draw()
        if frame%200==I*20:
            i.flip(100)
        center(pygame.transform.rotate(i.sprite,(2-I)*10),win,200+I*130,300+abs(2-I)**2*20)
    frame+=1
    pygame.display.update() #Updates the screen
pygame.quit()