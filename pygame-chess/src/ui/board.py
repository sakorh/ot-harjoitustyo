import pygame
from sprites.pawn import Pawn
from sprites.rook import Rook
from sprites.knight import Knight
from sprites.bishop import Bishop
from sprites.king import King
from sprites.queen import Queen


class Board:
    def __init__(self, empty_board, square_size, pieces):
        self.empty_board = empty_board
        self.square_size = square_size
        self._pieces = pieces
        self.pawns = pygame.sprite.Group()
        self.bishops = pygame.sprite.Group()
        self.rooks = pygame.sprite.Group()
        self.queens = pygame.sprite.Group()
        self.kings = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self._initialize_pieces()

    def _initialize_pieces(self):
        for y in range(len(self.empty_board)):
            for x in range(len(self.empty_board)):
                square = self._pieces[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 1:
                    pawn = Pawn("black", normalized_x, normalized_y)
                    self.all_sprites.add(pawn)
                    self.pawns.add(pawn)
                elif square == 0:
                    pawn = Pawn("white", normalized_x, normalized_y)
                    self.all_sprites.add(pawn)
                    self.pawns.add(pawn)
                elif square == 7:
                    rook = Rook("black", normalized_x, normalized_y)
                    self.all_sprites.add(rook)
                    self.rooks.add(rook)
                elif square == 6:
                    rook = Rook("white", normalized_x, normalized_y)
                    self.all_sprites.add(rook)
                    self.rooks.add(rook)
                elif square == 3:
                    self.all_sprites.add(
                        Knight("black", normalized_x, normalized_y))
                elif square == 2:
                    self.all_sprites.add(
                        Knight("white", normalized_x, normalized_y))
                elif square == 5:
                    bishop = Bishop("black", normalized_x, normalized_y)
                    self.all_sprites.add(bishop)
                    self.bishops.add(bishop)
                elif square == 4:
                    bishop = Bishop("white", normalized_x, normalized_y)
                    self.all_sprites.add(bishop)
                    self.bishops.add(bishop)
                elif square == 9:
                    queen = Queen("black", normalized_x, normalized_y)
                    self.all_sprites.add(queen)
                    self.queens.add(queen)
                elif square == 11:
                    king = King("black", normalized_x, normalized_y)
                    self.all_sprites.add(king)
                    self.kings.add(king)
                elif square == 8:
                    queen = Queen("white", normalized_x, normalized_y)
                    self.all_sprites.add(queen)
                    self.queens.add(queen)
                elif square == 10:
                    king = King("white", normalized_x, normalized_y)
                    self.all_sprites.add(king)
                    self.kings.add(king)

    def draw_options(self, display, options):
        for option in options:
            pygame.draw.circle(display, (0, 255, 0),
                               (option[0]+40, option[1]+40), 5)

    def initialize_board(self, display, board):
        height = width = len(board)
        black = (100, 100, 100)
        white = (255, 255, 255)

        for y in range(height):
            for x in range(width):
                square = board[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 0:
                    pygame.draw.rect(
                        display, white, (normalized_x, normalized_y,
                                         self.square_size, self.square_size))
                elif square == 1:
                    pygame.draw.rect(
                        display, black, (normalized_x, normalized_y,
                                         self.square_size, self.square_size))
