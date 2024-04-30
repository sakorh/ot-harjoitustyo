import pygame


class Renderer:
    def __init__(self, display, board):
        self._display = display
        self._board = board

    def render(self):
        self._board.all_sprites.draw(self._display)
        pygame.display.flip()
        pygame.display.update()

