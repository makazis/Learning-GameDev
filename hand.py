from card import *
class Card_Space:
    def __init__(self):
        self.card=None
        self.sprite=pygame.Surface((210,320))
        self.sprite.set_colorkey(card_transparency_color)
    def draw(self):
        if self.card==None:
            self.sprite.fill(card_transparency_color)
            pygame.draw.rect(self.sprite,(155,255,255),(0,0,210,320),10,15)
        else:
            center(self.card.sprite,self.sprite,0,0)
class Board:
    def __init__(self):
        self.locations={  #Contains all the data about where cards can exist
            "Board":[]
        }
        self.camera_x=0
        self.camera_y=0
    def add_space_to_board(self,x_offset=0,y_offset=0):
        self.locations["Board"].append({
            "Space":Card_Space(),
            "X Offset":x_offset,
            "Y Offset":y_offset
            })