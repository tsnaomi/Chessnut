import unittest
from ..utils.decorators import all_players, all_spaces
from itertools import combinations
from chessnut_game import ChessnutGame
from chessnut_game.pieces import Rook, Pawn

rook = Rook()


class TestRook(unittest.TestCase):
    """Test the Rook class."""
    @all_spaces(rook)
    @all_players(rook)
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
        print rook.player, rook.file, rook.rank

    @all_spaces(rook)
    @all_players(rook)
    def test_generate_actual_cache_empty_board(self, rook=None):
        """Assert that the actual_moves cache is identical to the naive_moves
        cache in the case of an empty board.
        """
        game = ChessnutGame()
        self.assertEqual(
            rook.generate_naive_cache(),
            rook.generate_actual_cache(game)
        )

    # @all_spaces
    # @all_players
    # def test_generate_actual_cache_blockers(
    #     self,
    #     player=None,
    #     _file=None,
    #     rank=None
    # ):
    #     """Assert that the actual_moves cache is correctly generated from
    #     the given space for the given player even when various naive_moves
    #     paths are blocked by friendly pieces.
    #     """
    #     piece.file = _file
    #     piece.rank = rank
    #     piece.generate_naive_cache()

    #     for i in range(len(piece.naive_moves)):
    #         for spaces in combinations(piece.naive_moves, i):
    #             game = ChessnutGame()
    #             for block_file, block_rank in spaces:
    #                 blocking_piece = Pawn(
    #                     piece.player,
    #                     block_file,
    #                     block_rank,
    #                 )
    #                 game._hard_place_piece(blocking_piece)

    #             piece.generate_actual_cache(game)

    #             blocker_0 = game.first_blocking_piece(_file, rank, 0)
    #             blocker_2 = game.first_blocking_piece(_file, rank, 2)
    #             blocker_4 = game.first_blocking_piece(_file, rank, 4)
    #             blocker_6 = game.first_blocking_piece(_file, rank, 6)

    #             for space in piece.actual_moves:
    #                 self.assertIn(space, piece.naive_moves)
    #                 to_file, to_rank = space
    #                 self.assertTrue(
    #                     (to_file == piece.file) !=
    #                     (to_rank == piece.rank)
    #                 )
    #                 if to_file == piece.file:
    #                     self.assertTrue(
    #                         -1 if blocker_4 is None else blocker_4.rank
    #                         < to_rank <
    #                         8 if blocker_0 is None else blocker_0.rank
    #                     )
    #                 elif to_rank == piece.rank:
    #                     self.assertTrue(
    #                         -1 if blocker_6 is None else blocker_6.file
    #                         < to_file <
    #                         8 if blocker_2 is None else blocker_2.file
    #                     )

    # def test_generate_actual_cache_enemies(self):
    #     """Assert that the actual_moves cache is correctly generated even
    #     when various naive_moves paths are occupied by enemy pieces.
    #     """

if __name__ == '__main__':
    unittest.main()
