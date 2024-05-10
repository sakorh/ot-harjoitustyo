import unittest
from repositories.fen_repository import fen_repository


class TestFENRepository(unittest.TestCase):
    def setUp(self):
        fen_repository.delete_all()
        self.starting_position_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        self.reversed_starting_position = "RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr w"

    def test_save_board(self):
        fen_repository.save_fen(
            self.starting_position_fen, "Starting Position")
        fens = fen_repository.get_fens()

        self.assertEqual(len(fens), 1)
        saved_fen = fen_repository.select_fen("Starting Position")
        self.assertEqual(saved_fen, self.starting_position_fen)

    def test_save_board_same_name(self):
        fen_repository.save_fen(
            self.starting_position_fen, "Starting Position")
        fen_repository.save_fen(
            self.reversed_starting_position, "Starting Position")

        fens = fen_repository.get_fens()

        self.assertEqual(len(fens), 1)
        saved_fen = fen_repository.select_fen("Starting Position")
        self.assertEqual(saved_fen, self.starting_position_fen)

    def test_delete_fen(self):
        fen_repository.save_fen(
            self.starting_position_fen, "Starting Position")
        fen_repository.save_fen(
            self.reversed_starting_position, "Reversed Starting Position")

        fens = fen_repository.get_fens()
        self.assertEqual(len(fens), 2)

        fen_repository.delete_fen(fens[0])

        fens = fen_repository.get_fens()
        self.assertEqual(len(fens), 1)
        saved_fen = fen_repository.select_fen(fens[0])
        self.assertEqual(saved_fen, self.reversed_starting_position)
