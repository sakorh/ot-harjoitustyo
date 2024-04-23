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
        self.new_game = None
        self._initialize_pieces()

    def end_game(self, display):
        for sprite in self.all_sprites:
            sprite.kill()
        green = (0, 255, 0)
        black = (0, 0, 0)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Game Over', True, green, black)
        text_rect = text.get_rect()
        x = y = 8*self.square_size
        text_rect.center = (x // 2, y // 2)
        display.blit(text, text_rect)
        new_game_text = font.render("Start New Game", True, green, black)
        self.new_game = new_game_text.get_rect()
        self.new_game.center = (x // 2, (y//2)+64)
        display.blit(new_game_text, self.new_game)

    def start_game(self):
        self._initialize_pieces()

    def _initialize_pieces(self):
        for y in range(len(self.empty_board)):
            for x in range(len(self.empty_board)):
                square = self._pieces[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 1:
                    self.pawns.add(Pawn("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 0:
                    self.pawns.add(Pawn("white", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 7:
                    self.rooks.add(Rook("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 6:
                    self.rooks.add(Rook("white", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 3:
                    self.all_sprites.add(
                        Knight("black", self.square_size, normalized_x, normalized_y))
                elif square == 2:
                    self.all_sprites.add(
                        Knight("white", self.square_size, normalized_x, normalized_y))
                elif square == 5:
                    self.bishops.add(Bishop("black", self.square_size,
                                            normalized_x, normalized_y))
                elif square == 4:
                    self.bishops.add(Bishop("white", self.square_size,
                                            normalized_x, normalized_y))
                elif square == 9:
                    self.queens.add(Queen("black", self.square_size,
                                          normalized_x, normalized_y))
                elif square == 11:
                    self.kings.add(King("black", self.square_size,
                                        normalized_x, normalized_y))
                elif square == 8:
                    self.queens.add(Queen("white", self.square_size,
                                          normalized_x, normalized_y))
                elif square == 10:
                    self.kings.add(King("white", self.square_size,
                                        normalized_x, normalized_y))
        self.all_sprites.add(self.pawns, self.rooks,
                             self.bishops, self.queens, self.kings)

    def draw_options(self, display, options):
        for option in options:
            pygame.draw.circle(display, (0, 255, 0),
                               (option[0]+self.square_size//2, option[1]+self.square_size//2), 5)

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
