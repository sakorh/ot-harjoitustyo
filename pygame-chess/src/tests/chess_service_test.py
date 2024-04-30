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

SQUARE_SIZE = 90


class TestChessService(unittest.TestCase):
    def setUp(self):
        self.board = Board(EMPTY_BOARD, SQUARE_SIZE, PIECES)
        self.board._initialize_pieces()
        self.chess_service = ChessService(self.board)

    def assert_equal_position(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)

    def test_pawn_can_move(self):
        pawns = self.board.pawns
        x = 0

        for pawn in pawns:
            if pawn.color == "black" and x <= 560:
                self.assert_equal_position(pawn, x, SQUARE_SIZE)
                self.chess_service.move_piece(pawn, dx=0, dy=SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 2*SQUARE_SIZE)
            elif pawn.color == "white" and x <= 560:
                self.assert_equal_position(pawn, x, 6*SQUARE_SIZE)
                self.chess_service.move_piece(pawn, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(pawn, x, 5*SQUARE_SIZE)
            x += SQUARE_SIZE

    def test_pieces_cannot_overlap(self):
        pieces = self.board.all_sprites

        for piece in pieces:
            if piece.color == "white" and piece.rect.x == 160 and piece.rect.y == 480:
                self.chess_service.move_piece(piece, dx=0, dy=-SQUARE_SIZE)
                self.assert_equal_position(piece, 160, 5*SQUARE_SIZE)
            elif piece.color == "white" and piece.rect.x == 80 and piece.rect.y == 560:
                self.chess_service.move_piece(
                    piece, dx=SQUARE_SIZE, dy=-2*SQUARE_SIZE)
                self.assert_equal_position(piece, 80, 7*SQUARE_SIZE)

    def test_rook_cannot_move_through_other_pieces(self):
        pieces = self.board.all_sprites

        for piece in pieces:
            if piece.color == "white" and piece in self.board.rooks and piece.rect.x == 0:
                legal_squares = self.chess_service.get_moves(piece)
                self.assertEqual(legal_squares, [])

    def test_can_eat_enemy_pawn_updated(self):
        self.chess_service.choose_piece(0, 6*SQUARE_SIZE)
        self.chess_service.choose_option(0, 4*SQUARE_SIZE)

        self.chess_service.choose_piece(SQUARE_SIZE, SQUARE_SIZE)
        piece_to_eat = self.chess_service.selected_piece
        self.chess_service.choose_option(SQUARE_SIZE, 3*SQUARE_SIZE)

        self.chess_service.choose_piece(0, 4*SQUARE_SIZE)

        self.assertEqual(self.chess_service.options, [
                         (SQUARE_SIZE, 3*SQUARE_SIZE), (0, 3*SQUARE_SIZE)])
        self.chess_service.choose_option(SQUARE_SIZE, 3*SQUARE_SIZE)
        self.assertTrue(piece_to_eat not in self.board.all_sprites)

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
        board._initialize_pieces()
        chess_service = ChessService(board)

        kings = board.kings
        for king in kings:
            if king.color == "white":
                legal_squares = chess_service.get_moves(king)
                self.assertEqual(
                    legal_squares, [(4*SQUARE_SIZE, 6*SQUARE_SIZE)])

    def test_checkmate_ends_game(self):
        pieces_in_checkmate = [[7, 3, 5, -1, 11, 5, 3, 7],
                               [1, 1, 1, 1, -1, 1, 1, 1],
                               [-1, -1, -1, -1, -1, -1, -1, -1],
                               [-1, -1, -1, -1, 1, -1, -1, -1],
                               [-1, -1, -1, -1, -1, -1, 0, 9],
                               [-1, -1, -1, -1, -1, 0, -1, -1],
                               [0, 0, 0, 0, 0, -1, -1, 0],
                               [6, 2, 4, 8, 10, 4, 2, 6]]

        board = Board(EMPTY_BOARD, SQUARE_SIZE, pieces_in_checkmate)
        board._initialize_pieces()
        chess_service = ChessService(board)

        self.assertTrue(chess_service.game_over)

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
        board._initialize_pieces()
        chess_service = ChessService(board)

        self.assertTrue(chess_service.game_over)

    def test_piece_selection(self):
        self.assertEqual(self.chess_service.selected_piece, None)
        self.chess_service.choose_piece(4*SQUARE_SIZE, 6*SQUARE_SIZE)

        self.assertTrue(self.chess_service.selected_piece in self.board.pawns)
        self.assertTrue(self.chess_service.selected_piece.color == "white")

    def test_cannot_choose_black_piece_on_whites_turn(self):
        self.assertEqual(self.chess_service.options, [])
        self.chess_service.choose_piece(3*SQUARE_SIZE, SQUARE_SIZE)
        self.assertEqual(self.chess_service.options, [])

    def test_option_selection(self):
        self.assertEqual(self.chess_service.options, [])
        self.chess_service.choose_piece(3*SQUARE_SIZE, 6*SQUARE_SIZE)
        self.assertEqual(self.chess_service.options, [
                         (3*SQUARE_SIZE, 5*SQUARE_SIZE), (3*SQUARE_SIZE, 4*SQUARE_SIZE)])
        selected_piece = self.chess_service.selected_piece
        self.chess_service.choose_option(3*SQUARE_SIZE, 4*SQUARE_SIZE)
        self.assert_equal_position(
            selected_piece, 3*SQUARE_SIZE, 4*SQUARE_SIZE)

    def test_movement_rules_in_check(self):
        pieces_in_check = [[7, 3, 5, 9, 11, 5, 3, 7],
                           [1, 1, 1, -1, 1, 1, 1, 1],
                           [-1, -1, -1, -1, -1, -1, -1, -1],
                           [-1, -1, 1, -1, 1, -1, -1, -1],
                           [-1, -1, -1, -1, 0, -1, -1, -1],
                           [-1, -1, -1, -1, -1, -1, -1, -1],
                           [0, 0, 0, 0, -1, 0, 0, 0],
                           [6, 2, 4, 8, 10, 4, 2, 6]]

        board = Board(EMPTY_BOARD, SQUARE_SIZE, pieces_in_check)
        board._initialize_pieces()
        chess_service = ChessService(board)

        chess_service.choose_piece(5*SQUARE_SIZE, 7*SQUARE_SIZE)
        chess_service.choose_option(SQUARE_SIZE, 3*SQUARE_SIZE)
        chess_service.choose_piece(2*SQUARE_SIZE, 0)
        self.assertEqual(chess_service.options, [(3*SQUARE_SIZE, SQUARE_SIZE)])
