import unittest
from ..utils.decorators import all_spaces, all_players
from itertools import combinations
from chessnut_game import ChessnutGame
from chessnut_game.pieces import Knight, Pawn


class TestKnight(unittest.TestCase):
    """Test the Knight class."""
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

    @all_spaces
    @all_players
    def test_generate_naive_cache(self, player=None, _file=None, rank=None):
        """Assert that the naive_moves cache is correctly generated from
        the given space."""
        self.knight.player = player
        self.knight.file = _file
        self.knight.rank = rank

        expected_spaces = set()
        for filemod, rankmod in self.knight_modifiers:
            if 0 <= self.knight.file + filemod <= 7 and \
                    0 <= self.knight.rank + rankmod <= 7:
                expected_spaces.add(
                    (self.knight.file + filemod, self.knight.rank + rankmod)
                )

        self.knight.generate_naive_cache()

        self.assertEqual(self.knight.naive_moves, expected_spaces)

    @all_spaces
    @all_players
    def test_generate_actual_cache_blockers(
        self,
        player=None,
        _file=None,
        rank=None
    ):
        """Assert that the actual_moves cache is correctly generated from
        the given space even when various naive_moves locations are blocked
        by friendly pieces.
        """
        self.knight.player = player
        self.knight.file = _file
        self.knight.rank = rank
        self.knight.generate_naive_cache()

        for i in range(len(self.knight.naive_moves)):
            for spaces in combinations(self.knight.naive_moves, i):
                game = ChessnutGame()
                for block_file, block_rank in spaces:
                    game._hard_place_piece(
                        Pawn(self.knight.player, block_file, block_rank)
                    )

                self.knight.generate_actual_cache(game)

                for space in self.knight.actual_moves:
                    self.assertIn(space, self.knight.naive_moves)
                    self.assertNotIn(space, spaces)

    @all_spaces
    @all_players
    def test_generate_actual_cache_enemies(
        self,
        player=None,
        _file=None,
        rank=None
    ):
        """Assert that the actual_moves cache is correctly generated from
        the given space even when various naive_moves locations are occupied
        by enemy pieces.
        """
        self.knight.player = player
        self.knight.file = _file
        self.knight.rank = rank
        self.knight.generate_naive_cache()

        for i in range(len(self.knight.naive_moves)):
            for spaces in combinations(self.knight.naive_moves, i):
                game = ChessnutGame()
                for block_file, block_rank in spaces:
                    game._hard_place_piece(
                        Pawn(not self.knight.player, block_file, block_rank)
                    )

                self.knight.generate_actual_cache(game)

                self.assertEqual(
                    self.knight.actual_moves,
                    self.knight.naive_moves
                )
