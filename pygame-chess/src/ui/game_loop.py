import pygame
from services.chess_service import ChessService


class GameLoop:
    """Pelisilmukasta vastaava luokka, joka lukee pelaajien syötteitä ja kutsuu sovelluslogiikan 
    metodeja pelaajien valitsemien toimintojen mukaan.
    """

    def __init__(self, board, renderer, event_queue, clock, fen_repository):
        """Konstruktori pelisilmukasta vastaavalle luokalle.

        Args:
            board: Board-luokan instanssi.
            renderer: Renderer-luokan instanssi.
            event_queue: EventQueue-luokan instanssi.
            clock: Clock-luokan instanssi.
            fen_repository: FENRepository-luokan instanssi.
        """
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._chess_service = ChessService(board)
        self.x = 0
        self.y = 7*board.square_size
        self._fen_repository = fen_repository

    def start(self):
        """Käynnistää pelisilmukan.
        """
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

        return True

    def _handle_mouse_click(self):
        """Kutsuu sovelluslogiikan metodeja ja päivittää pelilaudan/sovelluksen näkymää pelaajan hiiren
        klikkausten perusteella.
        """
        self.x, self.y = pygame.mouse.get_pos()
        if self._board.begin and self._board.fen.collidepoint(self.x, self.y):
            self._board.begin = False
            self._board.input_fen = True

        if self._board.begin and self._board.new_game.collidepoint(self.x, self.y):
            self._chess_service.initialize_game()
            self.x = 0
            self.y = 7*self._board.square_size
        elif self._board.new_game.collidepoint(self.x, self.y):
            self._board.begin = True
            self._board.fens.clear()

        if self._board.input_name and self._board.save_board.collidepoint(self.x, self.y):
            self._board.input_name = False
            self._board.error_message = ""
        elif not self._board.input_name and self._board.save_board and self._board.save_board.collidepoint(self.x, self.y):
            self._board.input_name = True

        if (self._board.begin or self._chess_service.game_over) \
                and self._board.choose_fen and self._board.choose_fen.collidepoint(self.x, self.y):
            self._board.fens = self._fen_repository.get_fens()
            if not self._board.fens:
                self._board.error_message = "You have no FENs saved."

        if self._board.fen_options:
            for option, name, delete in self._board.fen_options:
                if option.collidepoint(self.x, self.y):
                    fen = self._fen_repository.select_fen(name)
                    turn = self._board.draw_pieces_from_fen(fen)
                    self._chess_service.initialize_game(turn)
                    self.x = 0
                    self.y = 7*self._board.square_size
                if delete.collidepoint(self.x, self.y):
                    self._fen_repository.delete_fen(name)
                    if self._board.fens_page > 0:
                        self._board.fens_page -= 1
                    self._board.fens = self._fen_repository.get_fens()
            if self._board.load_more and self._board.load_more.collidepoint(self.x, self.y):
                self._board.fens_page += 1
            if self._board.previous and self._board.previous.collidepoint(self.x, self.y):
                self._board.fens_page -= 1

        self.x = (self.x//self._board.square_size) * \
            self._board.square_size
        self.y = (self.y//self._board.square_size) * \
            self._board.square_size

        self._chess_service.choose_piece(self.x, self.y)

        if self._chess_service.selected_piece:
            self._chess_service.choose_option(self.x, self.y)

    def _handle_keyboard_input(self, event):
        """Kutsuu sovelluslogiikan metodeja ja päivittää pelilaudan/sovelluksen näkymää pelaajan näppäinpainallusten 
        perusteella.

        Args:
            event: käyttäjän syötteen tuottama tapahtuma.
        """
        if (self._board.input_fen or self._board.input_name) and event.key == pygame.K_BACKSPACE:
            self._board.user_text = self._board.user_text[:-1]

        elif self._board.input_fen and event.key == pygame.K_RETURN:
            turn = self._board.draw_pieces_from_fen()
            if turn:
                self._chess_service.initialize_game(turn)
                self.x = 0
                self.y = 7*self._board.square_size

        elif self._board.input_name and event.key == pygame.K_RETURN:
            if self._board.user_text == "":
                self._board.error_message = "Name for FEN is required."
                return True
            turn = self._chess_service.turn
            fen = self._board.board_to_fen(turn)
            error = self._fen_repository.save_fen(fen, self._board.user_text)
            self._board.user_text = ""
            if error:
                self._board.error_message = error
                return True
            self._board.input_name = False

        elif self._board.input_fen and len(self._board.user_text) < 75 \
                or self._board.input_name and len(self._board.user_text) < 50:
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

        return True

    def _render(self):
        """Kutsuu pelinäkymän päivittämisestä vastaavan Renderer-luokan metodia.
        """
        self._renderer.render(self._chess_service.options,
                              self._chess_service.game_over, self.x, self.y)
