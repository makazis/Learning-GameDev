import pygame
from useful_things import *
from math import *
from random import *
import os
import json

draw_data=[
    {
        "Sides":3, #Pawn
        "Theta":0,
        "Inner Radius":0
    },
    {
        "Sides":4, #Rook
        "Theta":0,
        "Inner Radius":0
    },
    {
        "Sides":4, #Knight
        "Theta":pi/4,
        "Inner Radius":0
    },
    {
        "Sides":3, #Bishop
        "Theta":pi,
        "Inner Radius":30
    },
    {
        "Sides":6, #queen
        "Theta":0,
        "Inner Radius":0
    },
    {
        "Sides":6, #King
        "Theta":0,
        "Inner Radius":30 
    }
]
class Chess_Piece:
    def __init__(self,index,color=(255,255,255)):
        self.index=index
        self.sprite=pygame.Surface((210,210))
        self.sprite.fill(card_transparency_color)
        self.draw_data=draw_data[self.index]
        pygame.draw.polygon(self.sprite,(255,255,255),[
            (cos(tau/self.draw_data["Sides"]*i+self.draw_data["Theta"])*100,sin(tau/self.draw_data["Sides"]*i+self.draw_data["Theta"])*100)
            for i in range(self.draw_data["Sides"])
        ],self.draw_data["Inner Radius"])