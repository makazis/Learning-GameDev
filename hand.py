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
            self.card.draw()
            center(self.card.sprite,self.sprite,105,160)
class Board:
    def __init__(self):
        self.locations={  #Contains all the data about where cards can exist
            "Board":[]
        }
        self.surface=pygame.Surface((1920,1080))
        self.camera_x=-1920/2 
        self.camera_y=-1080/2 #Aligns the center to the center
    def add_space_to_board(self,x_offset=0,y_offset=0): #Adds a card spot to the board
        self.locations["Board"].append({
            "Space":Card_Space(),
            "X Offset":x_offset,
            "Y Offset":y_offset
            })
    def setup_hand(self,max_cards=10):
        self.locations["Hand"]={
            "Position":(0,1000), #Can be changed later if needed
            "Max Cards":max_cards,
            "Cards":[],
            "Curvature Settings":{ #Defines some stuff about how cards are held in hand, It's best not to think about this that much right now
                "Alpha":10, #How much the cards are bent
                "Beta":1.4, #Exponential of how far down the cards go, it's best to be kept small at larger number of cards
                "Gamma":5 #Card Descent Multiplier in pixels
            }
        }
    def draw(self):
        self.surface.fill((5,5,45)) #Fills the board with a nice color to draw on
        #Draws the board at the very bottom
        for I in self.locations["Board"]:
            #I=self.locations["Board"][i]
            I["Space"].draw()
            center(I["Space"].sprite,self.surface,I["X Offset"]-self.camera_x,I["Y Offset"]-self.camera_y)
        if "Hand" in self.locations:
            self.cards_in_hand=len(self.locations["Hand"]["Cards"])
            curvature_settings=self.locations["Hand"]["Curvature Settings"]
            for I,iterated_card in enumerate(self.locations["Hand"]["Cards"]):
                central_offset=-(self.cards_in_hand-1)/2+I
                iterated_card.draw()
                current_x=self.locations["Hand"]["Position"][0]-((self.cards_in_hand-1)/2-I)*170 #Determines card position in hand
                current_y=self.locations["Hand"]["Position"][1]+curvature_settings["Beta"]
                rotation=curvature_settings["Alpha"]*(self.locations["Hand"]["Position"][0]+(self.cards_in_hand-1)/2-I)/((self.locations["Hand"]["Max Cards"]-1)/2)
                center(pygame.transform.rotate(iterated_card.sprite,rotation),self.surface,current_x-self.camera_x,current_y-self.camera_y)
    def update(self): #Updates the board so that 
        self.mouse_rel=pygame.mouse.get_rel()
        self.mouse_down=pygame.mouse.get_pressed()
        if self.mouse_down[0]:
            self.camera_x-=self.mouse_rel[0]
            self.camera_y-=self.mouse_rel[1]
            