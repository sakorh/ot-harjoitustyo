import pygame


class Renderer:
    """Pelinäkymän piirtämisestä vastaava luokka.
    """
    def __init__(self, display, board, manager):
        self._display = display
        self._board = board
        self._manager = manager

    def render(self, options, game_over, x, y):
        self._board.initialize_board(self._display, self._board.empty_board)
        self._board.all_sprites.draw(self._display)
        self._manager.draw_ui(self._display)
        if self._board.begin:
            self._board.begin_view(self._display)
        elif game_over:
            self._board.end_game(self._display)
        elif x < 8*self._board.square_size and y < 8*self._board.square_size:
            self._board.draw_current_square(self._display, x, y)
        if options:
            self._board.draw_options(self._display, options)

        pygame.display.update()
