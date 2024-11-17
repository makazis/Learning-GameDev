import pygame
from math import *
from random import *

pygame.init()
win=pygame.display.set_mode((1200,600))
run=True
new_card=Card()
#new_card.flip(1000)
frame=0
while run:
    frame+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((0,0,0)) #Deletes the screen, fills all with black
    win.blit(new_card.sprite,(100,100))

    #win.blit(new_card.sides["Back"],(340,100))

    pygame.display.update() #Updates the screen
pygame.quit()
#print(new_card.sides["Front"])
#print("HIIIi")
