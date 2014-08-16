import unittest
from ..utils.decorators import all_spaces, all_players
from itertools import combinations
from chessnut_game import ChessnutGame
from chessnut_game.pieces import Knight, Pawn

knight = Knight()
knight_modifiers = (
    (1, 2),
    (1, -2),
    (2, 1),
    (2, -1),
    (-1, 2),
    (-1, -2),
    (-2, 1),
    (-2, -1),
)


class TestKnight(unittest.TestCase):
    """Test the Knight class."""
    @all_spaces(knight)
    @all_players(knight)
    def test_generate_naive_cache(self, knight=None):
        """Assert that the naive_moves cache is correctly generated from
        the given space."""
        expected_spaces = set()
        for filemod, rankmod in knight_modifiers:
            if 0 <= knight.file + filemod <= 7 and \
                    0 <= knight.rank + rankmod <= 7:
                expected_spaces.add(
                    (knight.file + filemod, knight.rank + rankmod)
                )

        knight.generate_naive_cache()

        self.assertEqual(knight.naive_moves, expected_spaces)

    @all_spaces(knight)
    @all_players(knight)
    def test_generate_actual_cache_empty_board(self, knight=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        knight.generate_naive_cache(),
        knight.generate_actual_cache(game)
        self.assertEqual(knight.naive_moves, knight.actual_moves)

    @all_spaces(knight)
    @all_players(knight)
    def test_generate_actual_cache_blockers(self, knight=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space even when various naive_moves locations are blocked
        by friendly pieces.
        """
        knight.generate_naive_cache()

        for i in range(len(knight.naive_moves)):
            for spaces in combinations(knight.naive_moves, i):
                game = ChessnutGame()
                for block_file, block_rank in spaces:
                    game._hard_place_piece(
                        Pawn(knight.player, block_file, block_rank)
                    )

                knight.generate_actual_cache(game)

                for space in knight.actual_moves:
                    self.assertIn(space, knight.naive_moves)
                    self.assertNotIn(space, spaces)

    @all_spaces(knight)
    @all_players(knight)
    def test_generate_actual_cache_enemies(self, knight=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space even when various naive_moves locations are occupied
        by enemy pieces.
        """
        knight.generate_naive_cache()

        for i in range(len(knight.naive_moves)):
            for spaces in combinations(knight.naive_moves, i):
                game = ChessnutGame()
                for block_file, block_rank in spaces:
                    game._hard_place_piece(
                        Pawn(not knight.player, block_file, block_rank)
                    )

                knight.generate_actual_cache(game)

                self.assertEqual(
                    knight.actual_moves,
                    knight.naive_moves
                )
