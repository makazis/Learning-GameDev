import pygame
from math import *
from random import *
from card import Card
pygame.init()
win=pygame.display.set_mode((1200,600))
run=True
new_card=Card()
new_card.side_from_surface(pygame.image.load("Resources/Sprites/Blue Eyes White Dragon.jpg"),"BEWD")

frame=0
while run:
    frame+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((55,55,55)) #Deletes the screen, fills all with black
    new_card.draw()
    if new_card.data["Side On Top"]=="Back" and randint(1,10)==1:
        new_card.flip(1000,"BEWD")
    else:
        if new_card.data["Side On Top"]=="BEWD":
            new_card.flip(1000,"Back")
        else:
            new_card.flip(1000)
    win.blit(new_card.sprite,(100,100))
    pygame.display.update() #Updates the screen
pygame.quit()