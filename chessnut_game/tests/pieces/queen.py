import unittest
from ..utils.decorators import all_players, all_spaces
from chessnut_game import ChessnutGame
from chessnut_game.pieces import Queen

queen = Queen()


class TestQueen(unittest.TestCase):
    """Test the Queen class."""
    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        pass

    @all_spaces(queen)
    @all_players(queen)
    def test_generate_actual_cache_empty_board(self, queen=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        queen.generate_naive_cache(),
        queen.generate_actual_cache(game)
        self.assertEqual(queen.naive_moves, queen.actual_moves)
