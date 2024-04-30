import pygame
import pygame_gui


class GUIElements:
    """pygame_gui moduulin elementtien luomisesta ja piirtämisestä vastaava luokka.
    """
    def __init__(self, square_size, manager, fen_repository):
        self.new_board = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((8.2*square_size, 20), (150, 50)),
                                                      text='Start New Game',
                                                      manager=manager, visible=0)
        self.input_fen = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((square_size, 4.5*square_size),
                                      (6*square_size, 50)),
            manager=manager)
        self.save_board = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((square_size*8.2, 100), (150, 50)),
                                                       text='Save Board',
                                                       manager=manager, visible=0)
        self.choose_fen = pygame_gui.elements.UIDropDownMenu(options_list=fen_repository.get_fens(), starting_option="Starting Position", relative_rect=pygame.Rect((8.2*square_size, 3.5*square_size), (150, 50)),
                                                             manager=manager, expand_on_option_click=False)
        self.fen_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((square_size*8.2, 155), (150, 50)),
                                                            manager=manager)

    def beginning_view(self):
        self.new_board.hide()
        self.save_board.hide()
        self.input_fen.hide()
        self.fen_name.hide()

    def load_fen_view(self):
        self.input_fen.show()

    def game_view(self):
        self.input_fen.clear()
        self.input_fen.hide()
        self.new_board.show()
        self.save_board.show()

    def game_over_view(self):
        self.new_board.hide()
        self.save_board.hide()

    def add_fen_to_options(self, name):
        self.choose_fen.add_options([name])

    
