import unittest
from itertools import combinations
from chessnut_game.game import Black, White, ChessnutGame
from chessnut_game.pieces import Pawn


class TestPawn(unittest.TestCase):
    """Test the Pawn class."""
    def setUp(self):
        self.pW = Pawn(White, 0, 1)
        self.pB = Pawn(Black, 0, 6)

    def test_cache_methods_rebound(self):
        """Assert the the can_capture_to and in_naive_captures names are
        correctly rebound by the Pawn constructor.
        """
        for pawn in (self.pW, self.pB):
            self.assertNotEqual(pawn.can_move_to, pawn.can_capture_to)
            self.assertNotEqual(pawn.in_naive_captures, pawn.in_naive_moves)

    def test_generate_naive_cache_naive_moves(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                for has_moved in (True, False):
                    pawn.file = _file
                    pawn.rank = rank
                    pawn.has_moved = has_moved

                    expected_spaces = set()
                    if pawn.player is White:
                        if pawn.rank < 7:
                            expected_spaces.add((_file, rank + 1))
                        if not pawn.has_moved and pawn.rank < 6:
                            expected_spaces.add((_file, rank + 2))
                    else:
                        if pawn.rank > 0:
                            expected_spaces.add((_file, rank - 1))
                        if not pawn.has_moved and pawn.rank > 1:
                            expected_spaces.add((_file, rank - 2))

                    pawn.generate_naive_cache()

                    self.assertEqual(pawn.naive_moves, expected_spaces)

    def test_generate_naive_cache_naive_captures(self):
        """Assert that the naive_captures cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                for has_moved in (True, False):
                    pawn.file = _file
                    pawn.rank = rank
                    pawn.has_moved = has_moved

                    expected_spaces = set()
                    if pawn.player is White:
                        if pawn.rank < 7:
                            if pawn.file > 0:
                                expected_spaces.add((_file - 1, rank + 1))
                            if pawn.file < 7:
                                expected_spaces.add((_file + 1, rank + 1))
                    else:
                        if pawn.rank > 0:
                            if pawn.file > 0:
                                expected_spaces.add((_file - 1, rank - 1))
                            if pawn.file < 7:
                                expected_spaces.add((_file + 1, rank - 1))

                    pawn.generate_naive_cache()

                    self.assertEqual(pawn.naive_captures, expected_spaces)

    def test_generate_actual_cache_actual_moves(self):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves locations are blocked by friendly and enemy
        pieces.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                for has_moved in (True, False):
                    pawn.file = _file
                    pawn.rank = rank
                    pawn.has_moved = has_moved

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

    def test_generate_actual_cache_actual_captures_blockers(self):
        """Assert that the actual_captures cache is correctly generated even
        when various naive_captures locations are blocked by friendly pieces.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                for has_moved in (True, False):
                    pawn.file = _file
                    pawn.rank = rank
                    pawn.has_moved = has_moved

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

    def test_generate_actual_cache_actual_captures_enemies(self):
        """Assert that the actual_captures cache is correctly generated even
        when various naive_captures locations are occupied by enemy pieces.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                for has_moved in (True, False):
                    pawn.file = _file
                    pawn.rank = rank
                    pawn.has_moved = has_moved

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
