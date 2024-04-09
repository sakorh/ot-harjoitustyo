import unittest
from board import Board

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

class PiecesTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)

    def assert_equal_position(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)

    def test_pawn_can_move(self):
        pawns = self.board.pawns
        x = 0

        for pawn in pawns:
            if pawn.color == "black" and x <= 560:
                self.assert_equal_position(pawn, x, SQUARE_SIZE)
                self.board.move_piece(pawn, dx=0, dy=SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 2*SQUARE_SIZE)
            elif pawn.color == "white" and x <= 560:
                self.assert_equal_position(pawn, x, 6*SQUARE_SIZE)
                self.board.move_piece(pawn, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 5*SQUARE_SIZE)
            x += SQUARE_SIZE
            

    def test_pieces_cannot_overlap(self):
        pieces = self.board.all_sprites

        for piece in pieces:
            if piece.color == "white" and piece.rect.x == 160 and piece.rect.y == 480:
                self.board.move_piece(piece, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(piece, 160, 5*SQUARE_SIZE)
            elif piece.color == "white" and piece.rect.x == 80 and piece.rect.y == 560:
                self.board.move_piece(piece, dx=SQUARE_SIZE,dy=-2*SQUARE_SIZE)
                self.assert_equal_position(piece, 80, 7*SQUARE_SIZE)






    



