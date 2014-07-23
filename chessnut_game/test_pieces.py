import unittest
from mock import patch
from game import Black, White
from pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from game import ChessnutGame

# Create a module-level game instance that we can use to test move cache
# generation.
game = ChessnutGame()


def generate_diagonal_spaces(_file, rank):
    """Given a file and a rank, this function generates all of the spaces
    in the two diagonals that intersect at that space, minus the space
    itself.
    """
    for file_mod, rank_mod in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        new_file = _file + file_mod
        new_rank = rank + rank_mod
        while 0 <= new_file <= 7 and 0 <= new_rank <= 7:
            yield (new_file, new_rank)
            new_file += file_mod
            new_rank += rank_mod


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

    def test_rank_setter_not_int(self):
        """Attempt to set the rank to a non-int value. Assert that a
        TypeError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.rank = '1'

    def test_rank_setter_out_of_range(self):
        """Attempt to create a piece with a rank not in 0-7.
        Assert that a ValueError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(ValueError):
                piece.rank = 8

    def test_file_setter_not_string(self):
        """Attempt to set the _file to a non-int value. Assert that a
        TypeError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.file = '1'

    def test_file_setter_out_of_range(self):
        """Attempt to create a piece with a file not in 0-7.
        Assert that a ValueError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(ValueError):
                piece.file = 8

    def test_player_setter_not_bool(self):
        """Attempt to set the player to a non-boolean value.
        Assert that a TypeError is raised.
        """
        for piece in (self.pW, self.pB):
            with self.assertRaises(TypeError):
                piece.player = 'player'

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
        dest_file = 9
        dest_rank = 1
        for piece in (self.pW, self.pB):
            with patch.object(Piece, '_generate_naive_cache') as mock_method:
                mock_method.return_value = None
                try:
                    piece.move_to(dest_file, dest_rank)
                except ValueError:
                    pass

            self.assertFalse(mock_method.called)
            self.assertEqual(piece.file, 0)
            self.assertEqual(piece.rank, 0)

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
            self.assertEqual(pawn.can_capture_to, pawn._can_capture_to)
            self.assertEqual(pawn.in_naive_captures, pawn._in_naive_captures)
            self.assertNotEqual(pawn.can_move_to, pawn.can_capture_to)
            self.assertNotEqual(pawn.in_naive_captures, pawn.in_naive_moves)

    def test_generate_naive_cache_naive_moves(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                pawn.file = _file
                pawn.rank = rank
                expected_spaces = set()
                if pawn.player is White:
                    if pawn.rank < 7:
                        expected_spaces.add((_file, rank + 1))
                    if pawn.rank == 1:
                        expected_spaces.add((_file, 3))
                else:
                    if pawn.rank > 0:
                        expected_spaces.add((_file, rank - 1))
                    if pawn.rank == 6:
                        expected_spaces.add((_file, 4))

                pawn._generate_naive_cache()

                self.assertEqual(pawn.naive_moves, expected_spaces)

    def test_generate_naive_cache_naive_captures(self):
        """Assert that the naive_captures cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for pawn in (self.pW, self.pB):
                pawn.file = _file
                pawn.rank = rank
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

                pawn._generate_naive_cache()

                self.assertEqual(pawn.naive_captures, expected_spaces)


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

                piece._generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)

    def test_move_to(self):
        """Assert that move_to marks these pieces as having moved."""
        for piece in (self.pW, self.pB):
            self.assertFalse(piece.has_moved)
            piece.move_to(0, 1)
            self.assertTrue(piece.has_moved)
            self.assertEqual(piece.file, 0)
            self.assertEqual(piece.rank, 1)


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

                piece._generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)


class TestBishop(unittest.TestCase):
    """Test the Bishop class."""
    def setUp(self):
        self.pW = Bishop(White, 0, 0)
        self.pB = Bishop(Black, 0, 7)

    def test_generate_naive_cache(self):
        """Assert that the naive_moves cache is correctly generated."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for piece in (self.pW, self.pB):
                piece.file = _file
                piece.rank = rank

                expected_spaces = set(
                    (f, r)
                    for f, r in generate_diagonal_spaces(_file, rank)
                )

                piece._generate_naive_cache()

                self.assertEqual(piece.naive_moves, expected_spaces)


class TestQueen(unittest.TestCase):
    """Test the Queen class."""


class TestKing(unittest.TestCase):
    """Test the King class."""


if __name__ == '__main__':
    unittest.main()
