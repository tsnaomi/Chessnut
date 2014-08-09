import unittest
from chessnut_game.game import Black, White
from chessnut_game.pieces import Rook


class TestRook(unittest.TestCase):
    """Test the Rook class."""
    def setUp(self):
        self.pW = Rook(White, 0, 0)
        self.pB = Rook(Black, 0, 7)

    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in range(8) if r != rank)
                expected_spaces.update(
                    (f, rank) for f in range(8) if f != _file)

                piece.generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)

    def test_move_to(self):
        """Assert that move_to marks these pieces as having moved."""
        for piece in (self.pW, self.pB):
            self.assertFalse(piece.has_moved)
            piece.move_to(0, 1)
            self.assertTrue(piece.has_moved)
            self.assertEqual(piece.file, 0)
            self.assertEqual(piece.rank, 1)
