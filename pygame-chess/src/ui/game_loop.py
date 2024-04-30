import pygame
import pygame_gui
from services.chess_service import ChessService


class GameLoop:
    """Pelisilmukasta vastaava luokka, joka lukee pelaajien syötteitä ja kutsuu sovelluslogiikan 
    metodeja pelaajien valitsemien toimintojen mukaan.
    """
    def __init__(self, board, renderer, event_queue, clock, manager, fen_repository):
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._chess_service = ChessService(board)
        self._manager = manager
        self.x = 0
        self.y = 7*board.square_size
        self._gui_element_selected = False
        self._fen_repository = fen_repository

    def start(self):
        while True:
            if self._handle_events() is False:
                break
            self._render()
            self._manager.update(self._clock.get_ticks())
            self._clock.tick(60)

    def _handle_events(self):
        """Käy silmukassa läpi pelaajien antamia syötteitä sekä hiiren että näppäimistön kautta.
        Returns:
            True, jos tapahtuma on joko hiiren klikkaus tai syöte näppäimistöltä, 
            False jos pelaaja sulkee sovelluksen. 
        """
        for event in self._event_queue.get():
            self._manager.process_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click()
                return True

            if event.type in [pygame_gui.UI_BUTTON_PRESSED,
                              pygame_gui.UI_TEXT_ENTRY_FINISHED,
                              pygame_gui.UI_DROP_DOWN_MENU_CHANGED]:
                self._handle_GUI_events(event)
                return True

            if event.type == pygame.KEYDOWN and not self._gui_element_selected:
                self._handle_keyboard_input(event)
                return True

            if event.type == pygame.QUIT:
                return False
            
    def _handle_mouse_click(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self._board.begin and self._board.fen.collidepoint(self.x, self.y):
            self._board.load_fen = True
            self._gui_element_selected = True

        if self._chess_service.game_over or self._board.begin \
                    and self._board.new_game.collidepoint(self.x, self.y):
            self._chess_service.initialize_game()
            self.x = 0
            self.y = 7*self._board.square_size
        self.x = (self.x//self._board.square_size) * \
                self._board.square_size
        self.y = (self.y//self._board.square_size) * \
                self._board.square_size

        self._chess_service.choose_piece(self.x, self.y)

        if self._chess_service.selected_piece:
            self._chess_service.choose_option(self.x, self.y)

    def _handle_keyboard_input(self, event):
        if event.key == pygame.K_RETURN:
            self._chess_service.choose_piece(self.x, self.y)

            if self._chess_service.selected_piece:
                self._chess_service.choose_option(self.x, self.y)

        elif event.key == pygame.K_RIGHT:
            self.x += self._board.square_size
        elif event.key == pygame.K_LEFT:
            self.x -= self._board.square_size
        elif event.key == pygame.K_UP:
            self.y -= self._board.square_size
        elif event.key == pygame.K_DOWN:
            self.y += self._board.square_size

    def _handle_GUI_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self._board.gui_elements.save_board:
                self._board.gui_elements.fen_name.show()
                self._gui_element_selected = True
            if event.ui_element == self._board.gui_elements.new_board:
                self._chess_service.initialize_game()
                self.x = 0
                self.y = 7*self._board.square_size
                self._gui_element_selected = False
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
                and event.ui_element == self._board.gui_elements.fen_name:
            name = event.text
            turn = self._chess_service._turn
            fen = self._board.board_to_fen(turn, name)
            self._fen_repository.save_fen(fen, name)
            self._gui_element_selected = False
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
            and event.ui_element == self._board.gui_elements.input_fen:
            turn = self._board.draw_pieces_from_fen(event.text)
            self._chess_service._turn = turn
            self._gui_element_selected = False
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            fen = self._fen_repository.select_fen(event.text)
            self._board.draw_pieces_from_fen(fen)
            self._gui_element_selected = False

    def _render(self):
        self._renderer.render(self._chess_service.options,
                              self._chess_service.game_over, self.x, self.y)
