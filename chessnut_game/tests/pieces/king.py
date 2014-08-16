import unittest
from ..utils.decorators import all_players, all_spaces
from chessnut_game import ChessnutGame
from chessnut_game.pieces import King

king = King()


class TestKing(unittest.TestCase):
    """Test the King class."""
    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        pass

    @all_spaces(king)
    @all_players(king)
    def test_generate_actual_cache_empty_board(self, king=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        king.generate_naive_cache(),
        king.generate_actual_cache(game)
        self.assertEqual(king.naive_moves, king.actual_moves)
