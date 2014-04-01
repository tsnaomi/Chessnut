import unittest
from chess import ChessnutGame, MoveNotLegalError, MoveAmbiguousError


class TestPGNToCoords(unittest.TestCase):
    """Test _pgn_move_to_coords."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_move_to_coords_all_moves_unique(self):
        """Assert that every valid move returns a unique pair of coordinates.
        """
        moves = [a + b for a in 'abcdefgh' for b in '12345678']
        coords = set()
        for move in moves:
            coords.add(self.c._pgn_move_to_coords(move))

        self.assertEqual(len(moves), len(coords))

    def test_move_to_coords(self):
        """Test several moves and assert that the correct coordinates are
        received.
        """
        conversions = [
            ('a1', (0, 7)),
            ('b4', (1, 4)),
            ('c7', (2, 1)),
            ('d3', (3, 5)),
            ('e2', (4, 6)),
            ('f6', (5, 2)),
            ('g5', (6, 3)),
            ('h8', (7, 0)),
        ]

        for initial, expected in conversions:
            self.assertEqual(self.c._pgn_move_to_coords(initial), expected)

    def test_move_to_coords_invalid_move(self):
        """Try to convert a one-character move to a pair of coordinates
        and assert that an exception is raised.
        """
        self.assertRaises(ValueError, self.c._pgn_move_to_coords, 'a')

    def test_move_to_coords_file_out_of_range(self):
        """Try to convert a move in which the file is out of range and
        assert that an exception is raised.
        """
        self.assertRaises(ValueError, self.c._pgn_move_to_coords, 'j2')

    def test_move_to_coords_rank_out_of_range(self):
        """Try to convert a move in which the rank is out of range and
        assert that an exception is raised.
        """
        self.assertRaises(ValueError, self.c._pgn_move_to_coords, 'a9')


class TestFileToX(unittest.TestCase):
    """Test _pgn_file_to_col."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_file_to_x(self):
        """Assert that every file is correctly converted."""
        conversions = [
            ('a', 0),
            ('b', 1),
            ('c', 2),
            ('d', 3),
            ('e', 4),
            ('f', 5),
            ('g', 6),
            ('h', 7),
        ]

        for initial, expected in conversions:
            self.assertEqual(self.c._pgn_file_to_col(initial), expected)

    def test_invalid_file(self):
        """Try to get x coordinate of an invalid file and assert that an
        exception is raised.
        """
        self.assertRaises(ValueError, self.c._pgn_file_to_col, 'i')


class TestRankToY(unittest.TestCase):
    """Test _pgn_rank_to_row."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_rank_to_y(self):
        """Assert that every rank is correctly converted."""
        conversions = [
            ('8', 0),
            ('7', 1),
            ('6', 2),
            ('5', 3),
            ('4', 4),
            ('3', 5),
            ('2', 6),
            ('1', 7),
        ]

        for initial, expected in conversions:
            self.assertEqual(self.c._pgn_rank_to_row(initial), expected)

    def test_invalid_rank(self):
        """Try to get y coordinate of an invalid rank and assert that an
        exception is raised.
        """
        self.assertRaises(ValueError, self.c._pgn_rank_to_row, '9')


class TestEvaluateRankAndFile(unittest.TestCase):
    """Test the _evaluate_rank_and_file function, a helper function to
    the evaluator functions.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def test_no_restrictions_one_piece(self):
        """When one piece could make a move, and rank or file have not
        been given, assert that that single piece is returned.
        """
        pieces = [(1, 1)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, None, None), pieces[0])

    def test_no_restrictions_multiple_pieces(self):
        """When more than one piece could make a move, and rank or file
        have not been given, assert that an exception is raised.
        """
        pieces = [(1, 1), (1, 2)]
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, None, None
        )

    def test_rank_restriction_one_piece(self):
        """When one piece could make a move, and the rank of the piece to
        move has been specified, assert that we see the appropriate
        behavior.
        """
        pieces = [(1, 1)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, 1, None), pieces[0])
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 3, None
        )

    def test_rank_restriction_multiple_pieces(self):
        """When more than one piece could make a move, and the rank of
        the piece to move has been specified, assert that we see the
        appropriate behavior.
        """
        pieces = [(1, 1), (2, 1)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, 1, None), pieces[0])
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 3, None
        )
        pieces.append((1, 2))
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 1, None
        )

    def test_file_restriction_one_piece(self):
        """When one piece could make a move, and the file of the piece to
        move has been specified, assert that we see the appropriate
        behavior.
        """
        pieces = [(1, 1)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, None, 1), pieces[0])
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, None, 3
        )

    def test_file_restriction_multiple_pieces(self):
        """When more than one piece could make a move, and the file of
        the piece to move has been specified, assert that we see the
        appropriate behavior.
        """
        pieces = [(1, 1), (1, 2)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, None, 1), pieces[0])
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, None, 3
        )
        pieces.append((2, 1))
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, None, 1
        )

    def test_rank_and_file_restriction_one_piece(self):
        """When one piece could make a move, and the rank and file of the
        piece to move have both been specified, assert that we see the
        appropriate behavior.
        """
        pieces = [(1, 1)]
        self.assertEqual(
            self.c._evaluate_rank_and_file(pieces, 1, 1), pieces[0])
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 1, 3
        )
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 3, 1
        )
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 3, 3
        )

    def test_rank_and_file_restriction_multiple_pieces(self):
        """When more than one piece could make a move, and the rank and
        file of the piece to move have both been specified, assert that
        we see the appropriate behavior.
        """
        pieces = [(1, 1), (1, 2), (2, 1)]
        for row, col in pieces:
            self.assertEqual(
                (row, col),
                self.c._evaluate_rank_and_file(pieces, row, col)
        )
        self.assertRaises(
            MoveAmbiguousError,
            self.c._evaluate_rank_and_file,
            pieces, 3, 3
        )


if __name__ == '__main__':
    unittest.main()
