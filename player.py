from random import *
from math import *
import pygame
class Player:
    def __init__(self):
        self.health=100
        self.max_health=100
        self.resources={
            "Mana":0 # Max mana increases by 1 every turn up to 6. It can be increased by other things such as creatures or spells, or relics later (spooked)
        }