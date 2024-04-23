import pygame
from ui.board import Board
from ui.game_loop import GameLoop
from clock import Clock
from event_queue import EventQueue
from renderer import Renderer


EMPTY_BOARD = [[0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0],
               [0, 1, 0, 1, 0, 1, 0, 1],
               [1, 0, 1, 0, 1, 0, 1, 0]]

PIECES = [[7, 3, 5, 9, 11, 5, 3, 7],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [-1, -1, -1, -1, -1, -1, -1, -1],
          [-1, -1, -1, -1, -1, -1, -1, -1],
          [-1, -1, -1, -1, -1, -1, -1, -1],
          [-1, -1, -1, -1, -1, -1, -1, -1],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [6, 2, 4, 8, 10, 4, 2, 6]]


SQUARE_SIZE = 90


def main():
    display_size = 8 * SQUARE_SIZE
    display = pygame.display.set_mode(
        (display_size+2*SQUARE_SIZE, display_size))

    pygame.display.set_caption("Chess")

    board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)

    pygame.init()

    game_loop = GameLoop(board, Renderer(display, board),
                         EventQueue(), Clock())
    game_loop.start()


if __name__ == "__main__":
    main()
