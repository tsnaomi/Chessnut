import unittest
from mock import patch
from game import Black, White
from pieces import Piece, Pawn, Rook, QueensideRook, KingsideRook, \
    Knight, Bishop, Queen, King


class TestPiece(unittest.TestCase):
    """Test the Piece class."""
    def setUp(self):
        self.pW = Piece(White, 'a', '1')
        self.pB = Piece(Black, 'a', '1')

    def generate_diagonal_spaces(self, _file, rank):
        """Given a file and a rank, this function generates all of the
        spaces in the two diagonals that intersect at that space, minus
        the space itself.
        """
        for file_mod, rank_mod in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_file = ord(_file) + file_mod
            new_rank = ord(rank) + rank_mod
            while 97 <= new_file <= 104 and 49 <= new_rank <= 56:
                yield (chr(new_file), chr(new_rank))
                new_file += file_mod
                new_rank += rank_mod

    def test_pieces_on_all_legal_spaces(self):
        """Create Pieces with all possible legal combinations of ranks
        and files and assert that they are determined legal.
        """
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for player in (Black, White):
                p = Piece(player, _file, rank)
                self.assertIs(p.player, player)
                self.assertEqual(p.file, _file)
                self.assertEqual(p.rank, rank)

    def test_rank_setter_not_string(self):
        """Attempt to set the rank to a non-string value. Assert that a
        TypeError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.rank = 1

    def test_rank_setter_out_of_range(self):
        """Attempt to create a piece with a rank not in 1-8.
        Assert that this operation fails.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(ValueError):
                piece.rank = '0'

    def test_file_setter_not_string(self):
        """Attempt to create a piece with a non-string _file argument.
        Assert that this operation fails.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.file = 1

    def test_file_setter_out_of_range(self):
        """Attempt to create a piece with a _file not in a-h.
        Assert that this operation fails.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(ValueError):
                piece.file = 'j'

    def test_player_setter_not_bool(self):
        """Attempt to create a piece with a non-boolean player.
        Assert that this operation fails.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.player = 'player'

    def test_can_move_to_in_set(self):
        """Assert that a Piece reports that it can move to a space that
        is in its actual_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 'a', '1')
            p.actual_moves.add(('b', '2'))
            self.assertTrue(p.can_move_to('b', '2'))

    def test_can_move_to_not_in_set(self):
        """Assert that a Piece reports that it can't move to a space that
        is not in its actual_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 'a', '1')
            p.actual_moves.add(('b', '3'))
            self.assertFalse(p.can_move_to('b', '2'))

    def test_in_naive_moves_in_set(self):
        """Assert that a Piece correctly reports membership in its
        naive_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 'a', '1')
            p.naive_moves.add(('b', '2'))
            self.assertTrue(p.in_naive_moves('b', '2'))

    def test_in_naive_moves_not_in_set(self):
        """Assert that a Piece correctly reports non-membership in its
        naive_moves cache.
        """
        for player in (Black, White):
            p = Piece(player, 'a', '1')
            p.naive_moves.add(('b', '3'))
            self.assertFalse(p.in_naive_moves('b', '2'))

    def test_move_to(self):
        """Assert that the move_to method changes the location of the
        Piece and regenerates its naive moves cache.
        """
        dest_file = 'b'
        dest_rank = '2'
        for piece in (self.pW, self.pB):
            with patch.object(Piece, '_generate_naive_cache') as mock_method:
                mock_method.return_value = None
                piece.move_to(dest_file, dest_rank)

            mock_method.assert_called_once_with()
            self.assertEqual(piece.file, dest_file)
            self.assertEqual(piece.rank, dest_rank)

    def test_move_to_off_board(self):
        """Attempt to move the Piece to a space off the board. Assert
        that no movement is made and the naive_moves cache is unmodified.
        """
        dest_file = 'j'
        dest_rank = '2'
        for piece in (self.pW, self.pB):
            with patch.object(Piece, '_generate_naive_cache') as mock_method:
                mock_method.return_value = None
                try:
                    piece.move_to(dest_file, dest_rank)
                except ValueError:
                    pass

            self.assertFalse(mock_method.called)
            self.assertEqual(piece.file, 'a')
            self.assertEqual(piece.rank, '1')

    def test_generate_horizontal_moves_default(self):
        """Test _generate_horizontal_moves with its default settings."""
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in '12345678' if r != rank)
                expected_spaces.update(
                    (f, rank) for f in 'abcdefgh' if f != _file)

                actual_spaces = set(piece._generate_horizontal_moves())

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_horizontal_moves_forward_only(self):
        """Test _generate_horizontal_moves when only forward movement is
        allowed.
        """
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (_file, r) for r in '12345678' if r > rank)
                else:
                    expected_spaces = set(
                        (_file, r) for r in '12345678' if r < rank)

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
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (_file, r) for r in '12345678' if r != rank)

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
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (_file, r) for r in '12345678' if r > rank)
                else:
                    expected_spaces = set(
                        (_file, r) for r in '12345678' if r < rank)
                expected_spaces.update(
                    (f, rank) for f in 'abcdefgh' if f != _file)

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
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                for limit in range(1, 7):
                    expected_spaces = set(
                        (_file, chr(r)) for r in range(
                            ord(rank) - limit, ord(rank) + limit + 1
                            )
                        if r != ord(rank) and 49 <= r <= 56
                    )
                    expected_spaces.update(
                        (chr(f), rank) for f in range(
                            ord(_file) - limit, ord(_file) + limit + 1
                            )
                        if f != ord(_file) and 97 <= f <= 104
                    )

                    actual_spaces = set(
                        piece._generate_horizontal_moves(
                            limit=limit
                        )
                    )

                    self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_diagonal_moves_default(self):
        """Test _generate_diagonal_moves with its default settings."""
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (f, r)
                    for f, r in self.generate_diagonal_spaces(_file, rank)
                )

                actual_spaces = set(piece._generate_diagonal_moves())

                self.assertEqual(actual_spaces, expected_spaces)

    def test_generate_diagonal_moves_forward_only(self):
        """Test _generate_diagonal_moves when only forward movement is
        allowed.
        """
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                if piece.player is White:
                    expected_spaces = set(
                        (f, r)
                        for f, r in self.generate_diagonal_spaces(_file, rank)
                        if r > rank
                    )
                else:
                    expected_spaces = set(
                        (f, r)
                        for f, r in self.generate_diagonal_spaces(_file, rank)
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
        for _file, rank in ((f, r) for f in 'abcdefgh' for r in '12345678'):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank
                for limit in range(1, 7):
                    expected_spaces = set(
                        (f, r)
                        for f, r in self.generate_diagonal_spaces(_file, rank)
                        if ord(f) in range(
                            ord(_file) - limit, ord(_file) + limit + 1)
                    )

                    actual_spaces = set(
                        piece._generate_diagonal_moves(limit=limit)
                    )

                    self.assertEqual(actual_spaces, expected_spaces)


class TestPawn(unittest.TestCase):
    """Test the Pawn class."""


class TestRook(unittest.TestCase):
    """Test the Rook class."""


class TestQueensideRook(unittest.TestCase):
    """Test the QueensideRook class."""


class TestKingsideRook(unittest.TestCase):
    """Test the KingsideRook class."""


class TestKnight(unittest.TestCase):
    """Test the Knight class."""


class TestBishop(unittest.TestCase):
    """Test the Bishop class."""


class TestQueen(unittest.TestCase):
    """Test the Queen class."""


class TestKing(unittest.TestCase):
    """Test the King class."""


if __name__ == '__main__':
    unittest.main()
