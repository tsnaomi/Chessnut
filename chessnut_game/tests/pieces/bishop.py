import unittest
from ..utils.functions import generate_diagonal_spaces
from ..utils.decorators import all_players, all_spaces
from chessnut_game import ChessnutGame
from chessnut_game.pieces import Bishop

bishop = Bishop()


class TestBishop(unittest.TestCase):
    """Test the Bishop class."""
    @all_spaces(bishop)
    @all_players(bishop)
    def test_generate_naive_cache(self, bishop=None):
        """Assert that the naive_moves cache is correctly generated."""
        expected_spaces = set(
            (f, r)
            for f, r in generate_diagonal_spaces(bishop.file, bishop.rank)
        )

        bishop.generate_naive_cache()

        self.assertEqual(bishop.naive_moves, expected_spaces)

    @all_spaces(bishop)
    @all_players(bishop)
    def test_generate_actual_cache_empty_board(self, bishop=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        self.assertEqual(
            bishop.generate_naive_cache(),
            bishop.generate_actual_cache(game)
        )
