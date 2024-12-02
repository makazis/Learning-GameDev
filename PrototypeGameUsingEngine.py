from board import *
class Game:
    def __init__(self):
        pygame.init()
        self.win=pygame.display.set_mode((0,0)) #Sets the screen to fullscreen mode
        self.run=True
        self.clock=pygame.time.Clock()
        self.board=Board(self.win.get_size())
        for i in range(5):
            i-=2
            for ii in range(2):
                self.board.add_space_to_board(i*220,(ii-0.5)*330,required_type="Creature",)
        self.board.setup_hand()
        #blow_up_board=False
        test_deck=[
            {
                "Name":choice(["john","wario"]),
                "Type":"Creature"
            } for i in range(30)
        ]
        self.board.import_deck(test_deck)
        self.board.shuffle_card_pile()
        self.board.draw() #This is required to update the card states in deck, otherwise, they don't flip correctly
        for i in range(5):
            self.board.draw_a_card()
            self.board.draw()
    def fight_loop(self):
        in_fight_loop=True
        while self.run and in_fight_loop:
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.run=False
            self.board.draw()
            self.board.update()
            self.win.blit(pygame.transform.scale(self.board.surface,self.win.get_size()),(0,0))
            self.win.blit(render_text(self.board.mouse_pos),(0,0))
            pygame.display.update() #Updates the screen
b=Game()
b.fight_loop()
pygame.quit()