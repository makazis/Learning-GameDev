import pygame
from math import *
from random import *
class Card:
    def __init__(self): #Will be called when a new card is created
        self.sides={
            "Front":pygame.Surface((210,320)),
            "Back":pygame.Surface((210,320))
        } #2 sides for each card right now, maybe i'll add more later
        pygame.draw.rect(self.sides["Front"],(255,255,255),(0,0,210,320),0,15)
        self.sides["Front"].set_colorkey((0,0,0)) #Turns the black color invisible

        pygame.draw.rect(self.sides["Back"],(55,55,55),(0,0,210,320),0,15) #Creates the card back
        for i in range(2):
            i+=1
            pygame.draw.rect(self.sides["Back"],(255,255,55),(i*5,i*5,210-i*10,320-i*10),3-i,15-i)
        self.sides["Back"].set_colorkey((0,0,0)) #Turns the black color invisible

        self.sprite=pygame.Surface((210,320))
        self.animations=[]
        self.front_visible=True
    def flip(self):
        self.animations.append({
            "Type":"Flipping",
            "Frames Left":10
        })
    def draw(self):
        self.sprite.fill((0,0,0))
        self.default_draw=True
        for i in self.animations:
            if i["Type"]=="Flipping":
                self.default_draw=False
                
        if self.default_draw:
            self.sprite.blit(self.sides["Front"],(0,0))
pygame.init()
win=pygame.display.set_mode((1200,600))
run=True
new_card=Card()
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((0,0,0)) #Deletes the screen, fills all with black
    
    win.blit(new_card.sides["Front"],(100,100))

    win.blit(new_card.sides["Back"],(340,100))

    pygame.display.update() #Updates the screen
pygame.quit()
#print(new_card.sides["Front"])
#print("HIIIi")
