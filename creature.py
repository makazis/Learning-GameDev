from card import *
import os
import json

##Imports all creature data in json objects listed in the Library/Creatures as a single large json object, where the name of each creature is its 
creature_data={}
for root,dirs,files in os.walk(r"Library/Creatures"): #Looks at every single folder within Library/Creatures
    for file in files: #Looks at every single file
        if file.endwith(".json"): #If the file ends with .json
            with open(os.path.join(root,file)) as f: #opens the file in the reading mode
                creature_data[file[:-5]]=json.loads(f.read()) #sets the files contents as a json object at a key that is the name of the file 
#This is a creature class, i am inspiring from the hearthstone ruleset, as it is a very flexible one.
class Creature:
    def __init__(self,name):
        self.name=name # The Name of the creature, and how it is reffered to in the Creature Library
        self.data=creature_data[self.name] # The data of the creature imported
        self.card=Card()
        self.card.contains=self
        self.cost=self.data["Cost"]
        #self.card.sides["Front"]
    def update(self):
        pass
    def update_card(self):
        self.card.sides["Front"].blit(card_transparency_overlay,(0,0)) #Ran at the end, in case the overlay is missing