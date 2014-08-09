import unittest
from chessnut_game.game import Black, White
from chessnut_game.pieces import Bishop
from .utils import generate_diagonal_spaces


class TestBishop(unittest.TestCase):
    """Test the Bishop class."""
    def setUp(self):
        self.pW = Bishop(White, 0, 0)
        self.pB = Bishop(Black, 0, 7)

    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (f, r)
                    for f, r in generate_diagonal_spaces(_file, rank)
                )

                piece.generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)
