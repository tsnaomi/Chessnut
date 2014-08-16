import unittest
from ..utils.decorators import all_players, all_spaces, all_move_states
from ..utils.functions import block_non_cache_spaces, surround_space
from chessnut_game import ChessnutGame, Black, White
from chessnut_game.pieces import Rook

rook = Rook()


class TestRook(unittest.TestCase):
    """Test the Rook class."""
    def test_has_moved(self):
        """Assert that the has_moved flag is set and unset as expected."""
        rook = Rook()
        self.assertFalse(rook.has_moved)
        rook.generate_naive_cache()
        self.assertTrue(rook.has_moved)

    @all_spaces(rook)
    @all_players(rook)
    @all_move_states(rook)
    def test_generate_naive_cache(self, rook=None):
        """Assert that the naive_moves cache is correctly generated from
        the given space for the given player.
        """
        rook.generate_naive_cache()

        expected_spaces = set(
            (rook.file, r) for r in range(8) if r != rook.rank)
        expected_spaces.update(
            (f, rook.rank) for f in range(8) if f != rook.file)

        self.assertEqual(rook.naive_moves, expected_spaces)

    @all_spaces(rook)
    @all_players(rook)
    @all_move_states(rook)
    def test_generate_actual_cache_empty_board(self, rook=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        rook.generate_naive_cache(),
        rook.generate_actual_cache(game)
        self.assertEqual(
            rook.naive_cache,
            rook.actual_cache
        )

    @all_spaces(rook)
    @all_players(rook)
    @all_move_states(rook)
    def test_generate_actual_cache_non_blockers(self, rook=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space for the given player when friendly and enemy pieces
        are present in non-naive_moves locations on the board.
        """
        rook.generate_naive_cache()
        for player in (Black, White):
            game = block_non_cache_spaces(ChessnutGame(), rook)
            rook.generate_actual_cache(game)
            self.assertEqual(rook.actual_moves, rook.naive_moves)

    @all_spaces(rook)
    @all_players(rook)
    @all_move_states(rook)
    def test_generate_actual_cache_blockers(self, rook=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space for the given player when various naive_moves
        paths are blocked by friendly pieces.
        """
        rook.generate_naive_cache()
        for radius in range(8):
            for player in (Black, White):
                game = ChessnutGame()
                circle = surround_space(game, rook.file, rook.rank, radius)
                expected = set()

                rook.generate_actual_cache()

                self.assertEqual(rook.actual_cache, )

    @all_spaces(rook)
    @all_players(rook)
    @all_move_states(rook)
    def test_generate_actual_cache_enemies(self, rook=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space for the given player when various naive_moves
        paths are blocked by enemy pieces.
        """


if __name__ == '__main__':
    unittest.main()
