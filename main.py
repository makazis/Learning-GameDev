import pygame
from math import *
from random import *
from card import *
from board import *
pygame.init()
win=pygame.display.set_mode((0,0)) #Sets the screen to fullscreen mode
run=True
#cards=[Card() for i in range(5)]
#new_card=Card()
#new_card.side_from_surface(pygame.image.load("Resources/Sprites/Blue Eyes White Dragon.jpg"),"BEWD")
board=Board(win.get_size())
for i in range(7):
    i-=3
    board.add_space_to_board(i*220,100,required_type="Creature",tags={"Interactable":{}})
board.setup_hand()
#for i in range(10):
#    board.locations["Hand"]["Cards"].append(Card())
frame=0
clock=pygame.time.Clock()
#blow_up_board=False
test_deck=[
    {
        "Name":choice(["john","wario"]),
        "Type":"Creature"
    } for i in range(30)
]
board.import_deck(test_deck)
board.shuffle_card_pile()
while run:
    if frame<50 and frame%10==1:
        board.draw_a_card()
        
        #print(board.locations["Hand"]["Cards"][-1].data)
    clock.tick(100)
    cards_in_hand=board.check_for_target(["Hand"])
    cards_on_board=board.check_for_target(["Board"])

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((55,55,55)) #Deletes the screen, fills all with black
    board.draw()
    board.update()
    keys=pygame.key.get_pressed()
    if keys[27]: run=False  
    #for I,i in enumerate(cards):
    #    i.draw()
    #    if frame%200==I*20:
    #        i.flip(100)
    #    center(pygame.transform.rotate(i.sprite,(2-I)*10),win,200+I*130,300+abs(2-I)**2*20)
    #for i in cards_in_hand:
    #    pygame.draw.circle(board.surface,(255,255,255),(i.x-board.camera_x,i.vector_space_element.y-board.camera_y),200,10)
    #for i in cards_on_board:
    #    pygame.draw.circle(board.surface,(0,255,255),
    #                       (i.vector_space_element.x-board.camera_x,i.vector_space_element.y-board.camera_y),
    #                       200,10)
    win.blit(pygame.transform.scale(board.surface,win.get_size()),(0,0))
    win.blit(render_text(board.mouse_pos),(0,0))
    frame+=1
    pygame.display.update() #Updates the screen
pygame.quit()