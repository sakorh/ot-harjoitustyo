import unittest
from ui.board import Board
from services.chess_service import ChessService

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

SQUARE_SIZE = 80


class PiecesTest(unittest.TestCase):
    def setUp(self):
        self.board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)
        self.chess_service = ChessService(self.board)

    def assert_equal_position(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)

    def test_pawn_can_move(self):
        pawns = self.board.pawns
        x = 0

        for pawn in pawns:
            if pawn.color == "black" and x <= 7*SQUARE_SIZE:
                self.assert_equal_position(pawn, x, SQUARE_SIZE)
                self.chess_service.move_piece(pawn, dx=0, dy=SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 2*SQUARE_SIZE)
            elif pawn.color == "white" and x <= 7*SQUARE_SIZE:
                self.assert_equal_position(pawn, x, 6*SQUARE_SIZE)
                self.chess_service.move_piece(pawn, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 5*SQUARE_SIZE)
            x += SQUARE_SIZE

    def test_pieces_cannot_overlap(self):
        pieces = self.board.all_sprites
        pawns = self.board.pawns

        for pawn in pawns:
            if pawn.color == "white" and pawn.rect.x == 2*SQUARE_SIZE and pawn.rect.y == 6*SQUARE_SIZE:
                self.chess_service.move_piece(pawn, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(pawn, 2*SQUARE_SIZE, 5*SQUARE_SIZE)
        for piece in pieces:
            if piece.color == "white" and piece.rect.x == SQUARE_SIZE and piece.rect.y == 7*SQUARE_SIZE:
                options = self.chess_service.get_moves(piece)
                self.assertEqual(options, [(0, 5*SQUARE_SIZE)])

    def test_rook_cannot_move_through_other_pieces(self):
        pieces = self.board.all_sprites

        for piece in pieces:
            if piece.color == "white" and piece in self.board.rooks and piece.rect.x == 0:
                legal_squares = self.chess_service.get_moves(piece)
                self.assertEqual(legal_squares, [])

    def test_can_eat_enemy_piece(self):
        pawns = self.board.pawns

        for pawn in pawns:
            if pawn.color == "white" and pawn.rect.x == 0:
                self.chess_service.move_piece(pawn, dx=0, dy=2*-SQUARE_SIZE)
        for pawn in pawns:
            if pawn.color == "black" and pawn.rect.x == SQUARE_SIZE:
                self.chess_service.move_piece(pawn, dx=0, dy=2*SQUARE_SIZE)
                can_move, can_eat = self.chess_service._check_move(
                    pawn, dx=-SQUARE_SIZE, dy=SQUARE_SIZE)

        self.assertTrue(can_eat)

    def test_king_legal_squares_in_check(self):

        pieces_in_check = [[7, 3, 5, -1, 11, 5, 3, 7],
                           [1, 1, 1, 1, -1, 1, 1, 1],
                           [-1, -1, -1, -1, -1, -1, -1, -1],
                           [-1, -1, -1, -1, 1, -1, -1, -1],
                           [-1, -1, -1, -1, -1, 0, -1, 9],
                           [-1, -1, -1, -1, 0, -1, -1, -1],
                           [0, 0, 0, 0, -1, -1, 0, 0],
                           [6, 2, 4, 8, 10, 4, 2, 6]]

        board = Board(EMPTY_BOARD, SQUARE_SIZE, pieces_in_check)
        chess_service = ChessService(board)

        kings = board.kings
        for king in kings:
            if king.color == "white":
                legal_squares = chess_service.get_moves(king)
                self.assertEqual(
                    legal_squares, [(4*SQUARE_SIZE, 6*SQUARE_SIZE)])

    def test_checkmate_ends_game(self):
        pieces_in_checkmate = [[7, 3, 5, -1, 11, 5, 3, 7],
                               [1, 1, 1, -1, 1, 1, 1, 1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, 9, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, 2, -1, -1, -1, -1, -1],
                               [0, 0, 0, 0, -1, 0, 0, 0],
                               [6, -1, 4, 8, 10, 4, 2, 6]]

        board = Board(EMPTY_BOARD, SQUARE_SIZE, pieces_in_checkmate)
        chess_service = ChessService(board)

        self.assertTrue(chess_service.game_over())

    def test_stalemate_ends_game(self):

        pieces_in_stalemate = [[11, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, 9, -1, -1],
                               [-1, -1, -1, -1, -1, -1, -1, 10]]

        board = Board(EMPTY_BOARD, SQUARE_SIZE, pieces_in_stalemate)
        chess_service = ChessService(board)

        self.assertTrue(chess_service.game_over())
