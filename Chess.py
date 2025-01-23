from board import *
from Chess_Piece import *
def draw(self):
    self.sprite.fill(card_transparency_color)
    if "Color" in self.tags:
        pygame.draw.rect(self.sprite,self.tags["Color"],(0,0,210,210),0,10)
    else:
        pygame.draw.rect(self.sprite,(255,255,255),(0,0,210,210),0,10)
    if self.card!=None:
        self.card.draw()
        center(self.card.sprite,self.sprite,105,105)
Card_Space.draw=draw
pygame.init()
win=pygame.display.set_mode((0,0)) #Sets the screen to fullscreen mode
run=True
board=Board(win.get_size())
for i in range(8):
    for ii in range(8):
        board.add_space_to_board(i*220,ii*220,required_type="Piece",tags={"Interactable":{},"Color":[((i+ii)%2==0)*255 for iii in range(3)]})
        if ii==1:
            new_piece=Chess_Piece(0,(255,255,255))
            new_card=Card()
            #board.locations["Board"][-1]["Space"].card=
clock=pygame.time.Clock()
Pieces=[]
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    clock.tick(100)
    keys=pygame.key.get_pressed()
    if keys[27]: run=False  
    win.fill((55,55,55)) #Deletes the screen, fills all with black
    board.draw()
    board.update()
    win.blit(pygame.transform.scale(board.surface,win.get_size()),(0,0))
    #win.blit(render_text(board.mouse_pos),(0,0))
    #frame+=1
    pygame.display.update()
pygame.quit()