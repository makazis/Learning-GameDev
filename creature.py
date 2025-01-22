import pygame
from useful_things import *
from math import *
from random import *
import os
import json

default_creature_image_path="Library/Creatures/Test Alpha/Sprites/Warrior.png"
default_creature_image=pygame.transform.scale(pygame.image.load(default_creature_image_path),(190,130))
##Imports all creature data in json objects listed in the Library/Creatures as a single large json object, where the name of each creature is its 
creature_data={}
for root,dirs,files in os.walk(r"Library/Creatures"): #Looks at every single folder within Library/Creatures
    for file in files: #Looks at every single file
        if file.endswith(".json"): #If the file ends with .json
            with open(os.path.join(root,file)) as f: #opens the file in the reading mode
                creature_data[file[:-5]]=json.loads(f.read()) #sets the files contents as a json object at a key that is the name of the file 
#This is a creature class, i am inspiring from the hearthstone ruleset, as it is a very flexible one.
class Creature:
    def __init__(self,name):
        self.name=name # The Name of the creature, and how it is reffered to in the Creature Library
        self.data=creature_data[self.name].copy() # The data of the creature imported

        self.attributes=self.data["Attributes"]

        self.cost=self.data["Cost"]
        self.sprite=pygame.Surface((210,320))
        self.type="Creature" #Used in identifying card types down the road
        #Thanks past me for creating this

        #Adds all the optional data in the creature type file
        if "Image Path" in self.data:       self.image=pygame.transform.scale(pygame.image.load(self.data["Image Path"]),(190,130))
        else:                               self.image=default_creature_image
        if "Display Name" in self.data:     self.display_name=self.data["Display Name"]
        else:                               self.display_name="???"

        #Adds all the attributes
        #Note that attack and health should be in the file, otherwise the creature won't be able to function correctly
        if "Health" in self.attributes:     self.health=self.attributes["Health"]
        else:                               self.health=1
        if "Attack" in self.attributes:     self.attack=self.attributes["Attack"]
        else:                               self.attack=1
        #self.card.sides["Front"]
    def update(self):
        pass
    def draw(self):
        self.sprite.fill((120,0,0))
        center(self.image,self.sprite,105,95)
        #Renders the name of the creature
        pygame.draw.rect(self.sprite,(255,255,255),(3,3,194,24),0,7)
        pygame.draw.rect(self.sprite,(0,0,0),(3,3,194,24),2,7)
        center(render_text(self.display_name,17,(0,0,0)),self.sprite,98,15)
        #Renders the mana cost of the creature
        if "Mana" in self.cost:
            pygame.draw.circle(self.sprite,(255,255,255),(195,15),15)
            pygame.draw.circle(self.sprite,(0,0,0),(195,15),15,3)
            center(render_text(self.cost["Mana"],15,(0,0,0)),self.sprite,195,15)
        
        temp_x=20 #Renders the attack value on the card
        temp_y=300
        pygame.draw.circle(self.sprite,(125,205,255),(temp_x,temp_y),20)
        pygame.draw.circle(self.sprite,(0,0,0),(temp_x,temp_y),20,2)
        center(render_text(self.attack,17,(0,0,0)),self.sprite,temp_x,temp_y)

        temp_x=190 #Renders the health value on the card
        temp_y=300
        pygame.draw.circle(self.sprite,(255,205,125),(temp_x,temp_y),20)
        pygame.draw.circle(self.sprite,(0,0,0),(temp_x,temp_y),20,2)
        center(render_text(self.health,17,(0,0,0)),self.sprite,temp_x,temp_y)

        #Adds the new sprite to the front of the card this creature is locked in
        self.card.sides["Front"].blit(self.sprite,(0,0))
        self.card.sides["Front"].blit(card_transparency_overlay,(0,0)) #Ran at the end, in case the overlay is missing