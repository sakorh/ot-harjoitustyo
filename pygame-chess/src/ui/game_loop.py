import pygame
from services.chess_service import ChessService


class GameLoop:
    def __init__(self, board, renderer, event_queue, clock):
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._chess_service = ChessService(board)
        self._selected_piece = None
        self._options = []
        self._turn = "white"
        self._game_over = False

    def start(self):
        while True:
            if self._handle_events() is False:
                break
            self._render()
            self._clock.tick(60)

    def _handle_events(self):

        if self._chess_service.game_over():
            self._game_over = True

        if self._selected_piece:
            self._options = self._chess_service.get_moves(self._selected_piece)

        for event in self._event_queue.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self._game_over:
                    if self._board.new_game.collidepoint(x, y):
                        self._chess_service.king_in_check = False
                        self._game_over = False
                        self._board.start_game()
                        self._turn = "white"

                piece = self._chess_service.choose_piece(self._turn, x, y)
                if not self._game_over and piece:
                    self._selected_piece = piece

                if self._options:
                    if self._chess_service.choose_option(
                            self._selected_piece, self._options, self._turn, x, y):
                        self._options.clear()
                        if self._selected_piece.color == "white":
                            self._turn = "black"
                            self._selected_piece = None
                        else:
                            self._turn = "white"
                            self._selected_piece = None

                return True

            if event.type == pygame.QUIT:
                return False

    def _render(self):
        self._renderer.render(self._options, self._game_over)
