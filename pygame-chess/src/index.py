import pygame
from ui.board import Board
from ui.game_loop import GameLoop
from ui.clock import Clock
from ui.event_queue import EventQueue
from ui.renderer import Renderer
from repositories.fen_repository import FENRepository


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
        (display_size+2*SQUARE_SIZE, display_size), pygame.RESIZABLE)

    pygame.display.set_caption("Chess")
    pygame.init()

    fen_repository = FENRepository()
    board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)

    game_loop = GameLoop(board, Renderer(display, board),
                         EventQueue(), Clock(), fen_repository)
    game_loop.start()


if __name__ == "__main__":
    main()
