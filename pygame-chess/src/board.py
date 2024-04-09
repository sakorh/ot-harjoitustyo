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
        self.black_pieces = pygame.sprite.Group()
        self.white_pieces = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self._initialize_pieces()

    def move_piece(self, sprite, dx, dy):
        if not self._check_move(sprite, dx, dy):
            return False
        else:
            sprite.rect.move_ip(dx,dy)
            return True

    def _check_move(self, sprite, dx, dy):
        sprite.rect.move_ip(dx,dy)
        
        for piece in self.all_sprites:
            if piece != sprite:
                collide = pygame.sprite.collide_rect(sprite, piece)
                if collide:
                    break
        
        can_move = not collide

        sprite.rect.move_ip(-dx,-dy)

        return can_move

        
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
                    self.all_sprites.add(Rook("black", normalized_x, normalized_y))
                elif square == 6:
                    self.all_sprites.add(Rook("white", normalized_x, normalized_y))
                elif square == 3:
                    self.all_sprites.add(Knight("black", normalized_x, normalized_y))
                elif square == 2:
                    self.all_sprites.add(Knight("white", normalized_x, normalized_y))
                elif square == 5:
                    self.all_sprites.add(Bishop("black", normalized_x, normalized_y))
                elif square == 4:
                    self.all_sprites.add(Bishop("white", normalized_x, normalized_y))
                elif square == 9:
                    self.all_sprites.add(Queen("black", normalized_x, normalized_y))
                elif square == 11:
                    self.all_sprites.add(King("black", normalized_x, normalized_y))
                elif square == 8:
                    self.all_sprites.add(Queen("white", normalized_x, normalized_y))
                elif square == 10:
                    self.all_sprites.add(King("white", normalized_x, normalized_y))


    def draw_options(self, display, x=0, y=0):
        pygame.draw.circle(display, (0,255,0), (x+40, y+40), 5)

    def initialize_board(self, display, board):
        height = width = len(board)
        black = (100,100,100)
        white = (255,255,255)

        for y in range(height):
            for x in range(width):
                square = board[y][x]
                normalized_x = x*self.square_size
                normalized_y = y*self.square_size

                if square == 0:
                    pygame.draw.rect(display, white, (normalized_x, normalized_y, self.square_size, self.square_size))
                elif square == 1:
                    pygame.draw.rect(display, black, (normalized_x, normalized_y, self.square_size, self.square_size))

        