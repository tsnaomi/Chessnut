import unittest
from ..utils.functions import generate_diagonal_spaces
from ..utils.decorators import all_spaces, all_players
from chessnut_game.game import Black, White
from chessnut_game.pieces import Piece

piece = Piece()


class TestPiece(unittest.TestCase):
    """Test the Piece class."""

    @all_players(piece)
    def test_can_move_to_in_set(self, piece=None):
        """Assert that a Piece reports that it can move to a space that
        is in its actual_moves cache.
        """
        piece.actual_moves.clear()
        piece.actual_moves.add((1, 1))
        self.assertTrue(piece.can_move_to(1, 1))

    @all_players(piece)
    def test_can_move_to_not_in_set(self, piece=None):
        """Assert that a Piece reports that it can't move to a space that
        is not in its actual_moves cache.
        """
        piece.actual_moves.clear()
        piece.actual_moves.add((1, 2))
        self.assertFalse(piece.can_move_to(1, 1))

    @all_players(piece)
    def test_in_naive_moves_in_set(self, piece=None):
        """Assert that a Piece correctly reports membership in its
        naive_moves cache.
        """
        piece.naive_moves.clear()
        piece.naive_moves.add((1, 1))
        self.assertTrue(piece.in_naive_moves(1, 1))

    @all_players(piece)
    def test_in_naive_moves_not_in_set(self, piece=None):
        """Assert that a Piece correctly reports non-membership in its
        naive_moves cache.
        """
        piece.naive_moves.clear()
        piece.naive_moves.add((1, 2))
        self.assertFalse(piece.in_naive_moves(1, 1))

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_horizontal_moves_default(self, piece=None):
        """Test _generate_horizontal_moves with its default settings."""
        expected_spaces = set(
            (piece.file, r) for r in range(8) if r != piece.rank
        )
        expected_spaces.update(
            (f, piece.rank) for f in range(8) if f != piece.file
        )

        actual_spaces = set(piece._generate_horizontal_moves())

        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_horizontal_moves_forward_only(self, piece=None):
        """Test _generate_horizontal_moves when only forward movement is
        allowed.
        """
        if piece.player is White:
            expected_spaces = set(
                (piece.file, r) for r in range(piece.rank + 1, 8)
            )
        else:
            expected_spaces = set(
                (piece.file, r) for r in range(piece.rank)
            )

        actual_spaces = set(
            piece._generate_horizontal_moves(backward=False, sideways=False)
        )

        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_horizontal_moves_no_sideways(self, piece=None):
        """Test _generate_horizontal_moves when only sideways movement is
        disallowed.
        """
        expected_spaces = set(
            (piece.file, r) for r in range(8) if r != piece.rank
        )

        actual_spaces = set(piece._generate_horizontal_moves(sideways=False))

        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_horizontal_moves_no_backward(self, piece=None):
        """Test _generate_horizontal_moves when only backward movement is
        disallowed.
        """
        if piece.player is White:
            expected_spaces = set(
                (piece.file, r) for r in range(piece.rank + 1, 8)
            )
        else:
            expected_spaces = set(
                (piece.file, r) for r in range(piece.rank)
            )

        expected_spaces.update(
            (f, piece.rank) for f in range(8) if f != piece.file
        )

        actual_spaces = set(piece._generate_horizontal_moves(backward=False))

        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_horizontal_moves_with_limit(self, piece=None):
        """Test _generate_horizontal_moves when the number of spaces to
        be moved is limited.
        """
        for limit in range(1, 7):
            expected_spaces = set(
                (piece.file, r) for r in range(
                    piece.rank - limit, piece.rank + limit + 1
                ) if r != piece.rank and 0 <= r <= 7
            )
            expected_spaces.update(
                (f, piece.rank) for f in range(
                    piece.file - limit, piece.file + limit + 1
                ) if f != piece.file and 0 <= f <= 7
            )

            actual_spaces = set(piece._generate_horizontal_moves(limit=limit))

            self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_diagonal_moves_default(self, piece=None):
        """Test _generate_diagonal_moves with its default settings."""
        expected_spaces = set(generate_diagonal_spaces(piece.file, piece.rank))
        actual_spaces = set(piece._generate_diagonal_moves())
        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_diagonal_moves_forward_only(self, piece=None):
        """Test _generate_diagonal_moves when only forward movement is
        allowed.
        """
        if piece.player is White:
            expected_spaces = set(
                (f, r)
                for f, r in generate_diagonal_spaces(piece.file, piece.rank)
                if r > piece.rank
            )
        else:
            expected_spaces = set(
                (f, r)
                for f, r in generate_diagonal_spaces(piece.file, piece.rank)
                if r < piece.rank
            )

        actual_spaces = set(piece._generate_diagonal_moves(backward=False))

        self.assertEqual(actual_spaces, expected_spaces)

    @all_spaces(piece)
    @all_players(piece)
    def test_generate_diagonal_moves_with_limit(self, piece=None):
        """Test _generate_diagonal_moves when the number of spaces to be
        moved is limited.
        """
        for limit in range(1, 7):
            expected_spaces = set(
                (f, r)
                for f, r in generate_diagonal_spaces(piece.file, piece.rank)
                if f in range(piece.file - limit, piece.file + limit + 1)
            )

            actual_spaces = set(piece._generate_diagonal_moves(limit=limit))

            self.assertEqual(actual_spaces, expected_spaces)
