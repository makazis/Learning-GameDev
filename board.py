from card import *
class Card_Space:
    def __init__(self):
        self.card=None
        self.sprite=pygame.Surface((210,320))
        self.sprite.set_colorkey(card_transparency_color)
        self.almost_selected=False
    def draw(self):
        if self.card==None:
            self.sprite.fill(card_transparency_color)
            if self.almost_selected:
                pygame.draw.rect(self.sprite,(255,255,155),(0,0,210,320),10,15)
                self.almost_selected=False
            else:
                pygame.draw.rect(self.sprite,(155,255,255),(0,0,210,320),10,15)
        else:
            self.card.draw()
            center(self.card.sprite,self.sprite,105,160)
class Board:
    def __init__(self,inherited_screen_size=(1920,1080)):
        self.locations={  #Contains all the data about where cards can exist
            "Board":[]
        }
        self.card_piles=[]
        self.surface=pygame.Surface((1920,1080))
        self.camera_x=-1920/2 
        self.camera_y=-1080/2 #Aligns the center to the center

        self.mouse_pos=[0,0] #Set to this for now, as it causes a crash if unset
        self.r_mouse_pos=[0,0]
        self.mouse_pos_multiplier=[[1920,1080][i]/inherited_screen_size[i] for i in range(2)] #Adjusts the mouse correctly
        self.drag_screen_allowed=True #Sets whether or not if you drag something, it will be dragged across the screen
        self.mouse_down=[False for i in range(3)]
        self.ctimer=[0,0,0]
        self.click=[False,False,False] #Can accurately detect the first frame when the mouse button is clicked

        self.open_GUIs={}
    def add_space_to_board(self,x_offset=0,y_offset=0,required_type=None,tags={}): #Adds a card spot to the board
        self.locations["Board"].append({
            "Space":Card_Space(),
            "X Offset":x_offset,
            "Y Offset":y_offset,
            "Type Needed":required_type,
            "Tags":tags
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
    def setup_card_pile(self,card_pile_name="Deck",pos=(900,0)):
        self.locations[card_pile_name]={
            "Position":pos,
            "Cards":[]
        }
        self.card_piles.append(card_pile_name)
    def draw(self):
        self.drag_screen_allowed=True
        self.surface.fill((5,5,45)) #Fills the board with a nice color to draw on
        #Draws the board at the very bottom
        for I in self.locations["Board"]:
            #I=self.locations["Board"][i]
            I["Space"].draw()
            if I["Space"].card!=None:
                I["Space"].card.vector_space_element.x=I["X Offset"]
                I["Space"].card.vector_space_element.y=I["Y Offset"]
            center(I["Space"].sprite,self.surface,I["X Offset"]-self.camera_x,I["Y Offset"]-self.camera_y)
        for iterated_card_pile in self.card_piles: #Draws the top card of every card pile
            selected_card_pile=self.locations[iterated_card_pile]
            cards_in_pile=len(selected_card_pile["Cards"])
            if cards_in_pile>0:
                selected_card_pile["Cards"][0].draw()
                center(selected_card_pile["Cards"][0].sprite,self.surface,selected_card_pile["Position"][0]-self.camera_x,selected_card_pile["Position"][1]-self.camera_y)                
        if "Hand" in self.locations:
            self.locations["Hand"]["Position"]=[self.camera_x+960,self.camera_y+540+500]
            self.cards_in_hand=len(self.locations["Hand"]["Cards"])
            if self.cards_in_hand>0:
                curvature_settings=self.locations["Hand"]["Curvature Settings"]
                card_distance_from_mouse={}
                for I,iterated_card in enumerate(self.locations["Hand"]["Cards"]):
                    if not iterated_card in [self.locations["Hand"]["Selected Card"],self.locations["Hand"]["Card Rendered On Top"]]:
                        central_offset=-(self.cards_in_hand-1)/2+I #Used to calculate rotation
                        iterated_card.draw()
                        destination_x=self.locations["Hand"]["Position"][0]-((self.cards_in_hand-1)/2-I)*170 #Determines card position in hand
                        destination_y=self.locations["Hand"]["Position"][1]+abs(central_offset)**curvature_settings["Beta"]*curvature_settings["Gamma"] #This is where the schizophrenia starts. I'll forget how this works once i look away, so i must not look away.
                        rotation=curvature_settings["Alpha"]*((self.cards_in_hand-1)/2-I)/((self.locations["Hand"]["Max Cards"]-1)/2)
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
                    I=saved_I
                    iterated_card=self.locations["Hand"]["Card Rendered On Top"]
                    central_offset=-(self.cards_in_hand-1)/2+I
                    iterated_card.draw()
                    destination_x=self.locations["Hand"]["Position"][0]-((self.cards_in_hand-1)/2-I)*170 #Determines card position in hand
                    destination_y=self.locations["Hand"]["Position"][1]+abs(central_offset)**curvature_settings["Beta"]*curvature_settings["Gamma"] #This is where the schizophrenia starts. I'll forget how this works once i look away, so i must not look away.
                    rotation=curvature_settings["Alpha"]*((self.cards_in_hand-1)/2-I)/((self.locations["Hand"]["Max Cards"]-1)/2)
                    
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
                if len(self.open_GUIs)==0: #If there are any other GUIs, cards cannot be interacted with
                    if self.locations["Hand"]["Selected Card"]!=None:
                        self.selected_card=self.locations["Hand"]["Selected Card"]
                        self.selected_card.vector_space_element.move_with_easing_motion_to(self.mouse_pos[0],self.mouse_pos[1],4,0)
                        if not self.mouse_down[0]:
                            self.locations["Hand"]["Selected Card"]=None
                            self.locations["Hand"]["Card Rendered On Top"]=None
                            for iterated_card_space in self.locations["Board"]:
                                distance_from_that_center=dist((iterated_card_space["X Offset"],iterated_card_space["Y Offset"]),
                                                        (self.selected_card.vector_space_element.x,self.selected_card.vector_space_element.y))
                                if distance_from_that_center<45:
                                    if iterated_card_space["Type Needed"]==self.selected_card.parent.type:
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
        for iterated_card_space in self.locations["Board"]: #Made just now just to remember how stuff works, and to handle attacking.
            if not "Interacting With Card On Field" in self.open_GUIs: #Can't open more than 1 GUI at the same time.
                if "Interactable" in iterated_card_space["Tags"]:  #Checks if the card in this zone can attack
                    if abs(iterated_card_space["X Offset"]-self.mouse_pos[0])<105 and abs(iterated_card_space["Y Offset"]-self.mouse_pos[1])<160: #Detects if the mouse is currently on the current card
                        if iterated_card_space["Space"].card!=None: #Checks if a card exists in that space
                            if self.click[0]:
                                self.open_GUIs["Interacting With Card On Field"]={
                                    "Selected Card":iterated_card_space["Space"].card
                                }
        if "Interacting With Card On Field" in self.open_GUIs:
            interacted_card=self.open_GUIs["Interacting With Card On Field"]["Selected Card"]
            if interacted_card.parent.type=="Creature":
                possible_actions=["Close"]
                #A Nice little block checking all the cases for actions that a creature can do. 
                if interacted_card.parent.attack>0:             possible_actions.append("Attack")
                for I,i in enumerate(possible_actions):
                    action_center_x=960-((len(possible_actions)-1)/2-I)*200
                    pygame.draw.rect(self.surface,(15,15,15),(action_center_x-80,820,160,60),0,10)
                    center(render_text(i,20,(255,255,255)),self.surface,action_center_x,850)
                    if not (abs(self.r_mouse_pos[0]-action_center_x)<80 and abs(self.r_mouse_pos[1]-835)<30): #If The mouse hovers over this button
                        pygame.draw.rect(self.surface,(125,125,125),(action_center_x-80,820,160,60),5,10)
                    else:
                        pygame.draw.rect(self.surface,(175,175,125),(action_center_x-80,820,160,60),5,10) #It Gets a different color
                        if self.click[0]:
                            if i=="Close":
                                del self.open_GUIs["Interacting With Card On Field"]
    def update(self): #Updates the board so that 
        self.mouse_rel=pygame.mouse.get_rel()
        self.mouse_down=pygame.mouse.get_pressed()
        self.mouse_pos=pygame.mouse.get_pos()
        self.r_mouse_pos=[self.mouse_pos[i]*self.mouse_pos_multiplier[i] for i in range(2)] #adjusts to the change in resolution
        self.mouse_pos=[self.r_mouse_pos[0]+self.camera_x,self.r_mouse_pos[1]+self.camera_y] #adds the position of camera to the mouse, allowing simple access. 
        if self.mouse_down[0] and self.drag_screen_allowed:
            self.camera_x-=self.mouse_rel[0]
            self.camera_y-=self.mouse_rel[1]
        self.ctimer=[(self.ctimer[i]+1)*self.mouse_down[i] for i in range(3)]
        self.click=[self.ctimer[i]==1 for i in range(3)]
    def add_plain_card_to_game(self,plain_card,plain_card_type="Creature"): #Adds a new card to the game, returns the created card
        new_card=Card() 
        if plain_card_type=="Creature":
            new_object_manager=Creature(plain_card)
            new_object_manager.card=new_card
            new_object_manager.draw() #Draws the new card at the start, so it is visible at all
            new_card.parent=new_object_manager #Also attributes the parent to whatever is locked inside the card
            return new_object_manager.card
    def draw_a_card(self,from_pile="Deck"): #Takes a card from a deck, adds it to the hand, the animation engine itself figures out how to animate that
        if len(self.locations[from_pile]["Cards"])>0:
            drawn_card=self.locations[from_pile]["Cards"][0]
            self.locations[from_pile]["Cards"].pop(0)
            if len(self.locations["Hand"]["Cards"])<self.locations["Hand"]["Max Cards"]:
                self.locations["Hand"]["Cards"].append(drawn_card)
                drawn_card.vector_space_element=Vector_Element()
                drawn_card.vector_space_element.setup(self.locations[from_pile]["Position"][0],self.locations[from_pile]["Position"][1])
                drawn_card.flip(40)
            else:
                return "Full Hand"
        else:
            return "Empty Pile"
    def import_deck(self,json_deck_list=[],to_card_pile="Deck"): #Imports deck from a decklist
        # Ideal decklist should be a list consisting of cards in the following format
        # {"Name":"CARD NAME","Type":"CARD TYPE"}
        # This doesn't shuffle the deck, so it has to be done manually
        self.setup_card_pile(to_card_pile)
        for iterated_card_packed in json_deck_list:
            new_card=self.add_plain_card_to_game(iterated_card_packed["Name"],iterated_card_packed["Type"])
            new_card.flip()
            self.locations[to_card_pile]["Cards"].append(new_card)
    def shuffle_card_pile(self,card_pile="Deck"):
        shuffle(self.locations[card_pile]["Cards"])
    def check_for_target(self,locations=[]):
        possible_cards=[]
        #First finds all the cards, then removes all the ones that don't count. 
        for i in self.locations:
            if not i in ["Board"]: #Custom Card Location
                if len(locations)>0:
                    if i in locations:
                        #print(i,locations)
                        for card in self.locations[i]["Cards"]:
                            possible_cards.append(card)
                    else:
                        continue
                else:
                    for card in i["Cards"]:
                        possible_cards.append(card)
            else:
                if len(locations)>0:
                    if "Board" in locations:
                        for space in self.locations[i]:
                            if space["Space"].card!=None:
                                possible_cards.append(space["Space"].card)

        #print(possible_cards)
        return possible_cards