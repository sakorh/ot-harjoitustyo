import pygame


class Renderer:
    def __init__(self, display, board):
        self._display = display
        self._board = board

    def render(self, options, game_over):
        self._board.initialize_board(self._display, self._board.empty_board)
        self._board.all_sprites.draw(self._display)
        if options:
            self._board.draw_options(self._display, options)

        if game_over:
            self._board.end_game(self._display)

        pygame.display.update()
