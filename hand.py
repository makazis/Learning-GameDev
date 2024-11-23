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
    def __init__(self,inherited_screen_size=(1920,1080)):
        self.locations={  #Contains all the data about where cards can exist
            "Board":[]
        }
        self.surface=pygame.Surface((1920,1080))
        self.camera_x=-1920/2 
        self.camera_y=-1080/2 #Aligns the center to the center

        self.mouse_pos=[0,0] #Set to this for now, as it causes a crash if unset
        self.mouse_pos_multiplier=[[1920,1080][i]/inherited_screen_size[i] for i in range(2)] #Adjusts the mouse correctly
        self.drag_screen_allowed=True #Sets whether or not if you drag something, it will be dragged across the screen
        self.mouse_down=[False for i in range(3)]
        self.ctimer=[0,0,0]
        self.click=[False,False,False] #Can accurately detect the first frame when the mouse button is clicked
    def add_space_to_board(self,x_offset=0,y_offset=0,is_locked=False): #Adds a card spot to the board
        self.locations["Board"].append({
            "Space":Card_Space(),
            "X Offset":x_offset,
            "Y Offset":y_offset,
            "Locked":is_locked,
            })
    def setup_hand(self,max_cards=10):
        self.locations["Hand"]={
            "Position":(0,500), #Can be changed later if needed
            "Max Cards":max_cards,
            "Cards":[],
            "Curvature Settings":{ #Defines some stuff about how cards are held in hand, It's best not to think about this that much right now
                "Alpha":10, #How much the cards are bent
                "Beta":1.5, #Exponential of how far down the cards go, it's best to be kept small at larger number of cards
                "Gamma":10 #Card Descent Multiplier in pixels
            },
            "Card Rendered On Top":None,
            "Selected Card":None
        }
    def draw(self):
        self.drag_screen_allowed=True
        self.surface.fill((5,5,45)) #Fills the board with a nice color to draw on
        #Draws the board at the very bottom
        for I in self.locations["Board"]:
            #I=self.locations["Board"][i]
            I["Space"].draw()
            center(I["Space"].sprite,self.surface,I["X Offset"]-self.camera_x,I["Y Offset"]-self.camera_y)
        if "Hand" in self.locations:
            self.cards_in_hand=len(self.locations["Hand"]["Cards"])
            if self.cards_in_hand>0:
                curvature_settings=self.locations["Hand"]["Curvature Settings"]
                card_distance_from_mouse={}
                for I,iterated_card in enumerate(self.locations["Hand"]["Cards"]):
                    if not iterated_card in [self.locations["Hand"]["Selected Card"],self.locations["Hand"]["Card Rendered On Top"]]:
                        central_offset=-(self.cards_in_hand-1)/2+I
                        iterated_card.draw()
                        destination_x=self.locations["Hand"]["Position"][0]-((self.cards_in_hand-1)/2-I)*170 #Determines card position in hand
                        destination_y=self.locations["Hand"]["Position"][1]+abs(central_offset)**curvature_settings["Beta"]*curvature_settings["Gamma"] #This is where the schizophrenia starts. I'll forget how this works once i look away, so i must not look away.
                        rotation=curvature_settings["Alpha"]*(self.locations["Hand"]["Position"][0]+(self.cards_in_hand-1)/2-I)/((self.locations["Hand"]["Max Cards"]-1)/2)
                        if not iterated_card.vector_space_element.set_up:
                            iterated_card.vector_space_element.setup(destination_x,destination_y)
                        iterated_card.vector_space_element.move_with_easing_motion_to(destination_x,destination_y,20,rotation)
                        center(pygame.transform.rotate(iterated_card.sprite,iterated_card.vector_space_element.rotation),
                            self.surface,iterated_card.vector_space_element.x-self.camera_x,
                            iterated_card.vector_space_element.y-self.camera_y)
                        #center(render_text((round(iterated_card.vector_space_element.x),round(iterated_card.vector_space_element.y)),30,(255,0,0)),self.surface,iterated_card.vector_space_element.x-self.camera_x,iterated_card.vector_space_element.y-self.camera_y)
                        #The line above is used in debug to determine card positions
                    elif iterated_card==self.locations["Hand"]["Card Rendered On Top"]:
                        saved_I=I
                    
                    dist_from_mouse=dist((iterated_card.vector_space_element.x,iterated_card.vector_space_element.y),self.mouse_pos)
                    while dist_from_mouse in card_distance_from_mouse: #Ensures all the elements are of unique distance to the mouse position
                        dist_from_mouse+=0.000001
                    card_distance_from_mouse[dist_from_mouse]=iterated_card #Sets up detection of which card is selected
                    #if dist_from_mouse<192: #If is within a circle of the mouse cursor
                    #    self.drag_screen_allowed=False #You can't drag the screen
                if self.locations["Hand"]["Card Rendered On Top"]!=None: #Brings the topmost rendered card to the very end of the loop, ensuring it is rendered last
                    try:
                        I=saved_I
                    except:
                        print(self.locations["Hand"]["Cards"].index(self.locations["Hand"]["Card Rendered On Top"]))
                    iterated_card=self.locations["Hand"]["Card Rendered On Top"]
                    central_offset=-(self.cards_in_hand-1)/2+I
                    iterated_card.draw()
                    destination_x=self.locations["Hand"]["Position"][0]-((self.cards_in_hand-1)/2-I)*170 #Determines card position in hand
                    destination_y=self.locations["Hand"]["Position"][1]+abs(central_offset)**curvature_settings["Beta"]*curvature_settings["Gamma"] #This is where the schizophrenia starts. I'll forget how this works once i look away, so i must not look away.
                    rotation=curvature_settings["Alpha"]*(self.locations["Hand"]["Position"][0]+(self.cards_in_hand-1)/2-I)/((self.locations["Hand"]["Max Cards"]-1)/2)
                    
                    if not iterated_card.vector_space_element.set_up:
                        iterated_card.vector_space_element.setup(destination_x,destination_y)
                    if iterated_card!=self.locations["Hand"]["Selected Card"]:
                        iterated_card.vector_space_element.move_with_easing_motion_to(destination_x,destination_y,20,rotation)
                    center(pygame.transform.rotate(iterated_card.sprite,iterated_card.vector_space_element.rotation),
                        self.surface,iterated_card.vector_space_element.x-self.camera_x,
                        iterated_card.vector_space_element.y-self.camera_y)
                    #center(render_text((round(iterated_card.vector_space_element.x),round(iterated_card.vector_space_element.y)),30,(255,0,0)),self.surface,iterated_card.vector_space_element.x-self.camera_x,iterated_card.vector_space_element.y-self.camera_y)
                    #The line above is used in debug to determine card positions
                    
                    if self.mouse_down[0]:
                        self.locations["Hand"]["Selected Card"]=iterated_card
                if self.locations["Hand"]["Selected Card"]!=None:
                    self.selected_card=self.locations["Hand"]["Selected Card"]
                    self.selected_card.vector_space_element.move_with_easing_motion_to(self.mouse_pos[0],self.mouse_pos[1],4,0)
                    if not self.mouse_down[0]:
                        self.locations["Hand"]["Selected Card"]=None
                        self.locations["Hand"]["Card Rendered On Top"]=None
                        for iterated_card_space in self.locations["Board"]:
                            distance_from_that_center=dist((iterated_card_space["X Offset"],iterated_card_space["Y Offset"]),
                                                    (self.selected_card.vector_space_element.x,self.selected_card.vector_space_element.y))
                            if distance_from_that_center<45 and not iterated_card_space["Locked"]:
                                self.locations["Hand"]["Cards"].remove(self.selected_card)
                                iterated_card_space["Space"].card=self.selected_card
                                
                    else:
                        self.drag_screen_allowed=False
                else:
                    closest_card_to_mouse_distance=sorted(list(card_distance_from_mouse.keys()))[0]
                    if closest_card_to_mouse_distance<192 or self.locations["Hand"]["Selected Card"]!=None:
                        #self.surface.blit(render_text(closest_card_to_mouse_distance,30,(255,0,0)),(200,0))
                        self.locations["Hand"]["Card Rendered On Top"]=card_distance_from_mouse[closest_card_to_mouse_distance]
                        self.drag_screen_allowed=False
                    else:
                        self.locations["Hand"]["Card Rendered On Top"]=None
    def update(self): #Updates the board so that 
        self.mouse_rel=pygame.mouse.get_rel()
        self.mouse_down=pygame.mouse.get_pressed()
        self.mouse_pos=pygame.mouse.get_pos()
        self.mouse_pos=[self.mouse_pos[i]*self.mouse_pos_multiplier[i] for i in range(2)] #adjusts to the change in resolution
        self.mouse_pos=[self.mouse_pos[0]+self.camera_x,self.mouse_pos[1]+self.camera_y]
        if self.mouse_down[0] and self.drag_screen_allowed:
            self.camera_x-=self.mouse_rel[0]
            self.camera_y-=self.mouse_rel[1]
        self.ctimer=[(self.ctimer[i]+1)*self.mouse_down[i] for i in range(3)]
            