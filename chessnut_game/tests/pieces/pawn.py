import unittest
from itertools import combinations
from ..utils.decorators import all_players, all_spaces, all_move_states
from ..utils.functions import block_non_cache_spaces
from chessnut_game import Black, White, ChessnutGame
from chessnut_game.pieces import Pawn

pawn = Pawn()


class TestPawn(unittest.TestCase):
    """Test the Pawn class."""
    def test_cache_methods_rebound(self):
        """Assert the the can_capture_to and in_naive_captures names are
        correctly rebound by the Pawn constructor.
        """
        self.assertNotEqual(pawn.can_move_to, pawn.can_capture_to)
        self.assertNotEqual(pawn.in_naive_captures, pawn.in_naive_moves)

    def test_has_moved(self):
        """Assert that the has_moved flag is set and unset as expected."""
        pawn = Pawn()
        self.assertFalse(pawn.has_moved)
        pawn.generate_naive_cache()
        self.assertTrue(pawn.has_moved)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_naive_cache_naive_moves(self, pawn=None):
        """Assert that the naive_moves cache is correctly generated."""
        expected_spaces = set()
        if pawn.player is White:
            if pawn.rank < 7:
                expected_spaces.add((pawn.file, pawn.rank + 1))
            if not pawn.has_moved and pawn.rank < 6:
                expected_spaces.add((pawn.file, pawn.rank + 2))
        else:
            if pawn.rank > 0:
                expected_spaces.add((pawn.file, pawn.rank - 1))
            if not pawn.has_moved and pawn.rank > 1:
                expected_spaces.add((pawn.file, pawn.rank - 2))

        pawn.generate_naive_cache()

        self.assertEqual(pawn.naive_moves, expected_spaces)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_actual_cache_empty_board(self, pawn=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        pawn.generate_naive_cache(),
        pawn.generate_actual_cache(game)
        self.assertEqual(pawn.naive_moves, pawn.actual_moves)
        self.assertEqual(pawn.naive_captures, pawn.actual_captures)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_actual_cache_non_blockers(self, pawn=None):
        """Assert that the actual_moves cache is correctly generated from
        the given space for the given player when friendly and enemy pieces
        are present in non-naive_moves locations on the board.
        """
        pawn.generate_naive_cache()
        for player in (Black, White):
            game = block_non_cache_spaces(ChessnutGame(), pawn)
            pawn.generate_actual_cache(game)
            self.assertEqual(pawn.actual_moves, pawn.naive_moves)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_naive_cache_naive_captures(self, pawn=None):
        """Assert that the naive_captures cache is correctly generated."""
        expected_spaces = set()
        if pawn.player is White:
            if pawn.rank < 7:
                if pawn.file > 0:
                    expected_spaces.add((pawn.file - 1, pawn.rank + 1))
                if pawn.file < 7:
                    expected_spaces.add((pawn.file + 1, pawn.rank + 1))
        else:
            if pawn.rank > 0:
                if pawn.file > 0:
                    expected_spaces.add((pawn.file - 1, pawn.rank - 1))
                if pawn.file < 7:
                    expected_spaces.add((pawn.file + 1, pawn.rank - 1))

        pawn.generate_naive_cache()

        self.assertEqual(pawn.naive_captures, expected_spaces)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_actual_cache_actual_moves(self, pawn=None):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves locations are blocked by friendly and enemy
        pieces.
        """
        pawn.generate_naive_cache()

        for i in range(len(pawn.naive_moves)):
            for spaces in combinations(pawn.naive_moves, i):
                for player in (Black, White):
                    game = ChessnutGame()
                    for _file, rank in spaces:
                        blocking_piece = Pawn(
                            player,
                            _file,
                            rank,
                        )
                        game._hard_place_piece(blocking_piece)

                    pawn.generate_actual_cache(game)

                    for space in pawn.actual_moves:
                        self.assertIn(space, pawn.naive_moves)
                        self.assertNotIn(space, spaces)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_actual_cache_actual_captures_blockers(self, pawn=None):
        """Assert that the actual_captures cache is correctly generated even
        when various naive_captures locations are blocked by friendly pieces.
        """
        pawn.generate_naive_cache()

        for i in range(len(pawn.naive_captures)):
            for spaces in combinations(pawn.naive_captures, i):
                game = ChessnutGame()
                for _file, rank in spaces:
                    blocking_piece = Pawn(
                        pawn.player,
                        _file,
                        rank,
                    )
                    game._hard_place_piece(blocking_piece)

                pawn.generate_actual_cache(game)

                self.assertEqual(set(), pawn.actual_captures)

    @all_spaces(pawn)
    @all_players(pawn)
    @all_move_states(pawn)
    def test_generate_actual_cache_actual_captures_enemies(self, pawn=None):
        """Assert that the actual_captures cache is correctly generated even
        when various naive_captures locations are occupied by enemy pieces.
        """
        pawn.generate_naive_cache()

        for i in range(len(pawn.naive_captures)):
            for spaces in combinations(pawn.naive_captures, i):
                game = ChessnutGame()
                for _file, rank in spaces:
                    blocking_piece = Pawn(
                        not pawn.player,
                        _file,
                        rank,
                    )
                    game._hard_place_piece(blocking_piece)

                pawn.generate_actual_cache(game)

                for space in pawn.actual_captures:
                    self.assertIn(space, pawn.naive_captures)
                    self.assertIn(space, spaces)
