import pygame
from services.chess_service import ChessService


class GameLoop:
    def __init__(self, board, renderer, event_queue, clock, display):
        self._board = board
        self._renderer = renderer
        self._event_queue = event_queue
        self._clock = clock
        self._chess_service = ChessService(board)
        self._display = display
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
        self._board.initialize_board(self._display, self._board.empty_board)

        if self._game_over:
            self._chess_service.end_game(self._display)
        if self._chess_service.checkmate():
            self._game_over = True

        if self._selected_piece:
            self._options = self._chess_service.get_moves(self._selected_piece)
            self._board.draw_options(self._display, self._options)

        for event in self._event_queue.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                piece = self._chess_service.choose_piece(self._turn, x, y)
                if not self._game_over and piece:
                    self._selected_piece = piece
                if self._options:
                    if self._chess_service.check_options(
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
        self._renderer.render()
