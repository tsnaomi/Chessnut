import unittest
from itertools import combinations
from chessnut_game.game import Black, White, ChessnutGame
from chessnut_game.pieces import Rook, Pawn


class TestRook(unittest.TestCase):
    """Test the Rook class."""
    def setUp(self):
        self.pW = Rook(White, 0, 0)
        self.pB = Rook(Black, 0, 7)

    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in range(8) if r != rank)
                expected_spaces.update(
                    (f, rank) for f in range(8) if f != _file)

                piece.generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)

    def test_move_to(self):
        """Assert that move_to marks these pieces as having moved."""
        for piece in (self.pW, self.pB):
            self.assertFalse(piece.has_moved)
            piece.move_to(0, 1)
            self.assertTrue(piece.has_moved)
            self.assertEqual(piece.file, 0)
            self.assertEqual(piece.rank, 1)

    def test_generate_actual_cache_blockers(self):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves paths are blocked by friendly pieces.
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

                        blocker_0 = game.first_blocking_piece(_file, rank, 0)
                        blocker_2 = game.first_blocking_piece(_file, rank, 2)
                        blocker_4 = game.first_blocking_piece(_file, rank, 4)
                        blocker_6 = game.first_blocking_piece(_file, rank, 6)

                        for space in piece.actual_moves:
                            self.assertIn(space, piece.naive_moves)
                            to_file, to_rank = space
                            if to_file == piece.file:
                                self.assertTrue(
                                    8 if blocker_0 is None else blocker_0.rank
                                    < to_rank <
                                    -1 if blocker_4 is None else blocker_4.rank
                                )
                            elif to_rank == piece.rank:
                                self.assertTrue(
                                    blocker_6.file < to_file < blocker_2.file
                                )

    def test_generate_actual_cache_enemies(self):
        """Assert that the actual_moves cache is correctly generated even
        when various naive_moves paths are occupied by enemy pieces.
        """

if __name__ == '__main__':
    unittest.main()
