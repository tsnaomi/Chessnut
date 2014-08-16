import unittest
from mock import patch
from chessnut_game.game import Black, White
from chessnut_game.pieces import Piece
from ..utils.functions import generate_diagonal_spaces


class TestPiece(unittest.TestCase):
    """Test the Piece class."""
    def setUp(self):
        self.pW = Piece(White, 0, 0)
        self.pB = Piece(Black, 0, 0)

    def test_pieces_on_all_legal_spaces(self):
        """Create Pieces with all possible legal combinations of ranks
        and files and assert that they are determined legal.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for player in (Black, White):
                p = Piece(player, _file, rank)
                self.assertIs(p.player, player)
                self.assertEqual(p.file, _file)
                self.assertEqual(p.rank, rank)

    def test_can_move_to_in_set(self):
        """Assert that a Piece reports that it can move to a space that
        is in its actual_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 0, 0)
            p.actual_moves.add((1, 1))
            self.assertTrue(p.can_move_to(1, 1))

    def test_can_move_to_not_in_set(self):
        """Assert that a Piece reports that it can't move to a space that
        is not in its actual_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 0, 0)
            p.actual_moves.add((1, 2))
            self.assertFalse(p.can_move_to(1, 1))

    def test_in_naive_moves_in_set(self):
        """Assert that a Piece correctly reports membership in its
        naive_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 0, 0)
            p.naive_moves.add((1, 1))
            self.assertTrue(p.in_naive_moves(1, 1))

    def test_in_naive_moves_not_in_set(self):
        """Assert that a Piece correctly reports non-membership in its
        naive_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 0, 0)
            p.naive_moves.add((1, 2))
            self.assertFalse(p.in_naive_moves(1, 1))

    def test_move_to(self):
        """Assert that the move_to method changes the location of the
        Piece and regenerates its naive moves cache.
        """
        dest_file = 1
        dest_rank = 1
        for piece in (self.pW, self.pB):
            with patch.object(Piece, 'generate_naive_cache') as mock_method:
                mock_method.return_value = None
                piece.move_to(dest_file, dest_rank)

            mock_method.assert_called_once_with()
            self.assertEqual(piece.file, dest_file)
            self.assertEqual(piece.rank, dest_rank)

    # def test_move_to_off_board(self):
    #     """Attempt to move the Piece to a space off the board. Assert
    #     that no movement is made and the naive_moves cache is unmodified.
    #     """
    #     dest_file = 9
    #     dest_rank = 1
    #     for piece in (self.pW, self.pB):
    #         with patch.object(Piece, '_generate_naive_cache') as mock_method:
    #             mock_method.return_value = None
    #             try:
    #                 piece.move_to(dest_file, dest_rank)
    #             except ValueError:
    #                 pass

    #         self.assertFalse(mock_method.called)
    #         self.assertEqual(piece.file, 0)
    #         self.assertEqual(piece.rank, 0)

    def test_generate_horizontal_moves_default(self):
        """Test _generate_horizontal_moves with its default settings."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in range(8) if r != rank)
                expected_spaces.update(
                    (f, rank) for f in range(8) if f != _file)

                actual_spaces = set(piece._generate_horizontal_moves())

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_horizontal_moves_forward_only(self):
        """Test _generate_horizontal_moves when only forward movement is
        allowed.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (_file, r) for r in range(8) if r > rank)
                else:
                    expected_spaces = set(
                        (_file, r) for r in range(8) if r < rank)

                actual_spaces = set(
                    piece._generate_horizontal_moves(
                        backward=False, sideways=False
                    )
                )

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_horizontal_moves_no_sideways(self):
        """Test _generate_horizontal_moves when only sideways movement is
        disallowed.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in range(8) if r != rank)

                actual_spaces = set(
                    piece._generate_horizontal_moves(
                        sideways=False
                    )
                )

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_horizontal_moves_no_backward(self):
        """Test _generate_horizontal_moves when only backward movement is
        disallowed.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (_file, r) for r in range(8) if r > rank)
                else:
                    expected_spaces = set(
                        (_file, r) for r in range(8) if r < rank)
                expected_spaces.update(
                    (f, rank) for f in range(8) if f != _file)

                actual_spaces = set(
                    piece._generate_horizontal_moves(
                        backward=False
                    )
                )

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_horizontal_moves_with_limit(self):
        """Test _generate_horizontal_moves when the number of spaces to
        be moved is limited.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                for limit in range(1, 7):
                    expected_spaces = set(
                        (_file, r) for r in range(
                            rank - limit, rank + limit + 1
                            )
                        if r != rank and 0 <= r <= 7
                    )
                    expected_spaces.update(
                        (f, rank) for f in range(
                            _file - limit, _file + limit + 1
                            )
                        if f != _file and 0 <= f <= 7
                    )

                    actual_spaces = set(
                        piece._generate_horizontal_moves(
                            limit=limit
                        )
                    )

                    self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_diagonal_moves_default(self):
        """Test _generate_diagonal_moves with its default settings."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (f, r)
                    for f, r in generate_diagonal_spaces(_file, rank)
                )

                actual_spaces = set(piece._generate_diagonal_moves())

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_diagonal_moves_forward_only(self):
        """Test _generate_diagonal_moves when only forward movement is
        allowed.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (f, r)
                        for f, r in generate_diagonal_spaces(_file, rank)
                        if r > rank
                    )
                else:
                    expected_spaces = set(
                        (f, r)
                        for f, r in generate_diagonal_spaces(_file, rank)
                        if r < rank
                    )

                actual_spaces = set(
                    piece._generate_diagonal_moves(backward=False)
                )

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_diagonal_moves_with_limit(self):
        """Test _generate_diagonal_moves when the number of spaces to be
        moved is limited.
        """
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                for limit in range(1, 7):
                    expected_spaces = set(
                        (f, r)
                        for f, r in generate_diagonal_spaces(_file, rank)
                        if f in range(_file - limit, _file + limit + 1)
                    )

                    actual_spaces = set(
                        piece._generate_diagonal_moves(limit=limit)
                    )

                    self.assertEqual(actual_spaces, expected_spaces)
