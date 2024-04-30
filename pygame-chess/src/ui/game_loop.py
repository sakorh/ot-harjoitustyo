import pygame
from services.chess_service import ChessService


class GameLoop:
    """Pelisilmukasta vastaava luokka, joka lukee pelaajien syötteitä ja kutsuu sovelluslogiikan 
    metodeja pelaajien valitsemien toimintojen mukaan.
    """

    def __init__(self, board, renderer, event_queue, clock, fen_repository):
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._chess_service = ChessService(board)
        self.x = 0
        self.y = 7*board.square_size
        self._fen_repository = fen_repository

    def start(self):
        while True:
            if self._handle_events() is False:
                break
            self._render()
            self._clock.tick(60)

    def _handle_events(self):
        """Käy silmukassa läpi pelaajien antamia syötteitä sekä hiiren että näppäimistön kautta.
        Returns:
            True, jos tapahtuma on joko hiiren klikkaus tai syöte näppäimistöltä, 
            False jos pelaaja sulkee sovelluksen. 
        """
        for event in self._event_queue.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click()
                return True

            if event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event)
                return True

            if event.type == pygame.QUIT:
                return False

    def _handle_mouse_click(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self._board.begin and self._board.fen.collidepoint(self.x, self.y):
            self._board.begin = False
            self._board.input_fen = True

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
        if self._board.input_fen and event.key == pygame.K_BACKSPACE:
            self._board.user_text = self._board.user_text[:-1]

        elif self._board.input_fen and event.key == pygame.K_RETURN:
            turn = self._board.draw_pieces_from_fen()
            self._chess_service._turn = turn
            self.x = 0
            self.y = 7*self._board.square_size

        elif self._board.input_fen:
            self._board.user_text += event.unicode

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

    def _render(self):
        self._renderer.render(self._chess_service.options,
                              self._chess_service.game_over, self.x, self.y)
