import pygame
from board import Board
from game_loop import GameLoop


EMPTY_BOARD = [[0,1,0,1,0,1,0,1],
             [1,0,1,0,1,0,1,0],
             [0,1,0,1,0,1,0,1],
             [1,0,1,0,1,0,1,0],
             [0,1,0,1,0,1,0,1],
             [1,0,1,0,1,0,1,0],
             [0,1,0,1,0,1,0,1],
             [1,0,1,0,1,0,1,0]]

PIECES = [[7,3,5,9,11,5,3,7],
         [1,1,1,1,1,1,1,1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1],
         [0,0,0,0,0,0,0,0],
         [6,2,4,8,10,4,2,6]]

SQUARE_SIZE = 80

def main():
    display_size = 8 * SQUARE_SIZE
    display = pygame.display.set_mode((display_size+2*SQUARE_SIZE, display_size))

    pygame.display.set_caption("Chess")

    board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)

    pygame.init()
    
    game_loop = GameLoop(board, SQUARE_SIZE, display)
    game_loop.start()


if __name__ == "__main__":
    main()