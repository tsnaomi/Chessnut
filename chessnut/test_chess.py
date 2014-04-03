import unittest
from chess import ChessnutGame, MoveNotLegalError, MoveAmbiguousError


class TestBoardToImageString(unittest.TestCase):
    """Test _board_to_image_string."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_empty_board_string(self):
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        string = self.c._board_to_image_string()
        self.assertEqual(len(string), 64)
        self.assertEqual(string, ''.join(['0' for i in range(64)]))

    def test_initial_board_string(self):
        string = self.c._board_to_image_string()
        self.assertEqual(len(string), 64)
        expected = \
            'rnbqkbnr' + \
            ''.join(['p' for i in range(8)]) + \
            ''.join(['0' for i in range(32)]) + \
            ''.join(['P' for i in range(8)]) + \
            'RNBQKBNR'
        self.assertEqual(string, expected)


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
            ('a1', (7, 0)),
            ('b4', (4, 1)),
            ('c7', (1, 2)),
            ('d3', (5, 3)),
            ('e2', (6, 4)),
            ('f6', (2, 5)),
            ('g5', (3, 6)),
            ('h8', (0, 7)),
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


class TestCoordsToMove(unittest.TestCase):
    """Test the _coords_to_pgn_move function."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_coords_to_move_all_moves_unique(self):
        """Assert that every valid pair of coordinates returns a unique move.
        """
        coords = [(a, b) for a in range(8) for b in range(8)]
        moves = set()
        for row, col in coords:
            moves.add(self.c._coords_to_pgn_move(row, col))

        self.assertEqual(len(moves), len(coords))

    def test_coords_to_move(self):
        """Test several coordinate pairs and assert that the correct moves
        are received.
        """
        conversions = [
            ('a1', (7, 0)),
            ('b4', (4, 1)),
            ('c7', (1, 2)),
            ('d3', (5, 3)),
            ('e2', (6, 4)),
            ('f6', (2, 5)),
            ('g5', (3, 6)),
            ('h8', (0, 7)),
        ]

        for expected, initial in conversions:
            self.assertEqual(self.c._coords_to_pgn_move(*initial), expected)


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
            MoveNotLegalError,
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
            MoveNotLegalError,
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
            MoveNotLegalError,
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
            MoveNotLegalError,
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
            MoveNotLegalError,
            self.c._evaluate_rank_and_file,
            pieces, 1, 3
        )
        self.assertRaises(
            MoveNotLegalError,
            self.c._evaluate_rank_and_file,
            pieces, 3, 1
        )
        self.assertRaises(
            MoveNotLegalError,
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
            MoveNotLegalError,
            self.c._evaluate_rank_and_file,
            pieces, 3, 3
        )


class TestCastlingEvaluators(unittest.TestCase):
    """Test the castling logic evaluators."""
    def setUp(self):
        self.c = ChessnutGame()
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        self.c.board[0][0] = ('R', False)
        self.c.board[0][7] = ('R', False)
        self.c.board[0][4] = ('K', False)
        self.c.board[7][0] = ('R', True)
        self.c.board[7][7] = ('R', True)
        self.c.board[7][4] = ('K', True)

    def _kingside_performed(self, turn):
        row = 7 if turn else 0
        self.assertEqual(self.c.board[row][6], ('K', turn))
        self.assertEqual(self.c.board[row][5], ('R', turn))
        self.assertEqual(self.c.board[row][4], (0, 0))
        self.assertEqual(self.c.board[row][7], (0, 0))
        self.assertFalse(self.c.white_kingside)
        self.assertFalse(self.c.white_queenside)

    def _queenside_performed(self, turn):
        row = 7 if turn else 0
        self.assertEqual(self.c.board[row][2], ('K', turn))
        self.assertEqual(self.c.board[row][3], ('R', turn))
        self.assertEqual(self.c.board[row][4], (0, 0))
        self.assertEqual(self.c.board[row][0], (0, 0))
        self.assertFalse(self.c.white_kingside)
        self.assertFalse(self.c.white_queenside)

    def test_perform_kingside_castling(self):
        """Perform a kingside castle and assert that the move succeeds
        and alters the board and game variables as expected.
        """
        self.c._kingside_evaluator()
        self._kingside_performed(True)

        self.c.board[7] = [(0, 0) for i in range(8)]
        self.c.turn = False
        self.c._kingside_evaluator()
        self._kingside_performed(False)

    def test_perform_queenside_castling(self):
        """Perform a queenside castle and assert that the move succeeds
        and alters the board and game variables as expected.
        """
        self.c._queenside_evaluator()
        self._queenside_performed(True)

        self.c.board[7] = [(0, 0) for i in range(8)]
        self.c.turn = False
        self.c._queenside_evaluator()
        self._queenside_performed(False)

    def test_kingside_castling_checked(self):
        """Attempt to perform kingside castling when the king is checked
        or would move into or through check and assert that the move is
        determined illegal.
        """
        for turn in [True, False]:
            self.c.turn = turn
            for col in [4, 5, 6]:
                self.c.board[1][col] = ('Q', not turn)
                self.assertRaises(
                    MoveNotLegalError, self.c._kingside_evaluator)
                self.c.board[1] = [(0, 0) for i in range(8)]

    def test_queenside_castling_checked(self):
        """Attempt to perform queenside castling when the king is checked
        or would move into or through check and assert that the move is
        determined illegal.
        """
        for turn in [True, False]:
            self.c.turn = turn
            for col in [2, 3, 4]:
                self.c.board[1][col] = ('Q', not turn)
                self.assertRaises(
                    MoveNotLegalError, self.c._queenside_evaluator)
                self.c.board[1] = [(0, 0) for i in range(8)]

    def test_kingside_castling_blocked(self):
        """Attempt to perform kingside castling when the path for the
        rook and/or king is blocked and assert that the operation is
        determined illegal.
        """
        for turn in [True, False]:
            self.c.turn = turn
            row = 7 if turn else 0
            for col in [5, 6]:
                self.c.board[row][col] = ('P', turn)
                self.assertRaises(
                    MoveNotLegalError, self.c._kingside_evaluator)
                self.c.board[row][col] = (0, 0)

    def test_queenside_castling_blocked(self):
        """Attempt to perform queenside castling when the path for the
        rook and/or king is blocked and assert that the operation is
        determined illegal.
        """
        for turn in [True, False]:
            self.c.turn = turn
            row = 7 if turn else 0
            for col in [2, 3, 4]:
                self.c.board[row][col] = ('P', turn)
                self.assertRaises(
                    MoveNotLegalError, self.c._queenside_evaluator)
                self.c.board[row][col] = (0, 0)

    def test_kingside_castling_no_longer_allowed(self):
        """Attempt to perform kingside castling when the rook and/or
        king have already moved and assert that the move is determined
        illegal.
        """
        self.c.white_kingside = False
        self.assertRaises(
            MoveNotLegalError, self.c._kingside_evaluator)
        self.c.turn = False
        self.c.black_kingside = False
        self.assertRaises(
            MoveNotLegalError, self.c._kingside_evaluator)

    def test_queenside_castling_no_longer_allowed(self):
        """Attempt to perform queenside castling when the rook and/or
        king have already moved and assert that the move is determined
        illegal.
        """
        self.c.white_queenside = False
        self.assertRaises(
            MoveNotLegalError, self.c._queenside_evaluator)
        self.c.turn = False
        self.c.black_queenside = False
        self.assertRaises(
            MoveNotLegalError, self.c._queenside_evaluator)


class TestIsCheck(unittest.TestCase):
    """Test the _is_check function of the game."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_is_check_empty_board(self):
        """Completely empty the board and assert that no space registers
        as checked for either player.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                self.assertFalse(self.c._is_check(i, j))

    def test_is_check_all_threatened(self):
        """Place a row of enemy queens along one side of the board and
        verify that every space registers as checked for the relevant
        player.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        for turn in [True, False]:
            self.c.board[0] = [('Q', not turn) for i in range(8)]
            self.c.turn = turn
            for i in range(8):
                for j in range(8):
                    self.assertTrue(self.c._is_check(i, j))

    def test_is_check_each_piece(self):
        """Select a single spot on the board and check it with each of
        the different pieces, asserting that it registers as checked each
        time.
        """
        pieces = [
            ('R', 4, 0),
            ('B', 0, 0),
            ('N', 2, 3),
            ('Q', 4, 0),
            ('K', 3, 3),
            ()
        ]
        for turn in [True, False]:
            pieces[5] = ('P', 3 if turn else 5, 3)
            self.c.turn = turn
            for piece, row, col in pieces:
                self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
                self.c.board[row][col] = (piece, not turn)
                self.assertTrue(self.c._is_check(4, 4))

    def test_is_check_not_each_piece(self):
        """Select a single spot on the board and place one of each of the
        different pieces at a space around it that doesn't check it, and
        assert that it never registers as checked.
        """
        pieces = [
            ('R', 3, 0),
            ('B', 0, 1),
            ('N', 2, 2),
            ('Q', 3, 0),
            ('K', 2, 2),
            ()
        ]
        for turn in [True, False]:
            pieces[5] = ('P', 3 if turn else 5, 1)
            self.c.turn = turn
            for piece, row, col in pieces:
                self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
                self.c.board[row][col] = (piece, not turn)
                self.assertFalse(self.c._is_check(4, 4))


class TestIsCheckmate(unittest.TestCase):
    """Test the _is_checkmate function."""
    def setUp(self):
        self.c = ChessnutGame()

    def test_is_checkmate_empty_board(self):
        """Completely empty the board and assert that no space registers
        as checkmate.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(8):
                self.assertFalse(self.c._is_checkmate(i, j))

    def test_is_checkmate_all_threatened(self):
        """Place a row of enemy queens along one side of the board and
        verify that every space registers as checkmated for the relevant
        player.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        for turn in [True, False]:
            self.c.board[0] = [('Q', not turn) for i in range(8)]
            self.c.turn = turn
            for i in range(8):
                for j in range(8):
                    self.assertTrue(self.c._is_checkmate(i, j))

    def test_stalemate_is_not_checkmate(self):
        """Create a stalemate and assert that it does not register as a
        checkmate.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        for turn in [True, False]:
            self.c.turn = turn
            self.c.board[0][0] = ('K', turn)
            self.c.board[2][1] = ('Q', not turn)
            self.assertFalse(self.c._is_checkmate(0, 0))


if __name__ == '__main__':
    unittest.main()
