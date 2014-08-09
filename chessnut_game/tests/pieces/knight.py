import unittest
from itertools import combinations
from chessnut_game.game import Black, White, ChessnutGame
from chessnut_game.pieces import Knight, Pawn


class TestKnight(unittest.TestCase):
    """Test the Knight class."""
    def setUp(self):
        self.pW = Knight(White, 0, 0)
        self.pB = Knight(Black, 0, 7)

    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set()
                for filemod, rankmod in (
                        (1, 2), (1, -2), (2, 1), (2, -1),
                        (-1, 2), (-1, -2), (-2, 1), (-2, -1)):
                    if 0 <= piece.file + filemod <= 7 and \
                            0 <= piece.rank + rankmod <= 7:
                        expected_spaces.add(
                            (piece.file + filemod, piece.rank + rankmod)
                        )

                piece.generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)

    def test_generate_actual_cache_blockers(self):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves locations are blocked by friendly pieces.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                piece.generate_naive_cache()

                for i in range(len(piece.naive_moves)):
                    for spaces in combinations(piece.naive_moves, i):
                        game = ChessnutGame()
                        for _file, rank in spaces:
                            blocking_piece = Pawn(
                                piece.player,
                                _file,
                                rank,
                            )
                            game._hard_place_piece(blocking_piece)

                        piece.generate_actual_cache(game)

                        for space in piece.actual_moves:
                            self.assertIn(space, piece.naive_moves)
                            self.assertNotIn(space, spaces)

    def test_generate_actual_cache_enemies(self):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves locations are occupied by enemy pieces.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                piece.generate_naive_cache()

                for i in range(len(piece.naive_moves)):
                    for spaces in combinations(piece.naive_moves, i):
                        game = ChessnutGame()
                        for _file, rank in spaces:
                            blocking_piece = Pawn(
                                not piece.player,
                                _file,
                                rank,
                            )
                            game._hard_place_piece(blocking_piece)

                        piece.generate_actual_cache(game)

                        self.assertEqual(piece.naive_moves, piece.actual_moves)
