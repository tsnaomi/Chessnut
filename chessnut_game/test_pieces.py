import unittest
from game import Black, White
from pieces import Piece, Pawn, Rook, QueensideRook, KingsideRook, \
    Knight, Bishop, Queen, King


class TestPiece(unittest.TestCase):
    """Test the Piece class."""
    def setUp(self):
        self.pW = Piece(White, 'a', '1')
        self.pB = Piece(Black, 'a', '1')

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

    def test_move_to_off_board(self):
        """Attempt to move the Piece to a space off the board. Assert
        that no movement is made and the naive_moves cache is unmodified.
        """


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
