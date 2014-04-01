import unittest
from chess import ChessnutGame, MoveNotLegalError, NotationParseError


class TestPawnEvaluator(unittest.TestCase):
    """Test the pawn logic evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'P',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_pawn_forward_1(self):
        """Move a pawn forward one space and assert that this move is
        determined legal.
        """
        self.groups['dest'] = 'b3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_exact_pawn_forward_1(self):
        """Use SAN to specify a specific pawn be moved forward one space
        and assert that this move is determined legal.
        """
        self.groups['dest'] = 'b3'
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_rank_pawn_forward_1(self):
        """Use SAN to specify that a pawn from a certain rank should be
        moved forward and assert that this move is determined legal.
        """
        self.groups['dest'] = 'b3'
        self.groups['rank'] = '2'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.groups['rank'] = '7'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_file_pawn_forward_1(self):
        """Use SAN to specify that a pawn from a certain file should be
        moved forward and assert that this move is determined legal.
        """
        self.groups['dest'] = 'b3'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_pawn_forward_2_from_start(self):
        """Move a pawn forward two spaces on its first move and assert
        that this move is determined legal.
        """
        self.groups['dest'] = 'b4'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b5'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_exact_pawn_forward_2_from_start(self):
        """Use SAN to specify a specific pawn be moved forward two spaces
        from its starting position and assert that this move is determined
        legal.
        """
        self.groups['dest'] = 'b4'
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b5'
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_rank_pawn_forward_2_from_start(self):
        """Use SAN to specify that a pawn from a specific rank be moved
        forward two spaces from its starting position and assert that this
        move is determined legal.
        """
        self.groups['dest'] = 'b4'
        self.groups['rank'] = '2'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b5'
        self.groups['rank'] = '7'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_file_pawn_forward_2_from_start(self):
        """Use SAN to specify that a pawn from a specific file be moved
        forward two spaces from its starting position and assert that this
        move is determined legal.
        """
        self.groups['dest'] = 'b4'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['dest'] = 'b5'
        self.groups['file'] = 'b'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_pawn_forward_blocked(self):
        """Try to move a pawn forward when it is blocked and assert that
        this move is determined illegal.
        """
        self.c.board[5][1] = ('K', True)
        self.groups['dest'] = 'b3'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[2][1] = ('K', False)
        self.groups['dest'] = 'b6'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_diagonally_not_capture(self):
        """Try to move a pawn diagonally when not capturing and assert
        that this move is determined illegal.
        """
        self.groups['dest'] = 'b3'
        self.groups['rank'] = '2'
        self.groups['file'] = 'a'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.groups['rank'] = '7'
        self.groups['file'] = 'a'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_forward_2_not_start(self):
        """Try to move a pawn forward two spaces not from its starting
        position and assert that this move is determined illegal.
        """
        self.c.board[5][1] = ('P', True)
        self.groups['dest'] = 'b5'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[2][1] = ('P', False)
        self.groups['dest'] = 'b4'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_backward(self):
        """Try to move a pawn backwards and assert that this move is
        determined illegal.
        """
        self.c.board[0][1] = (0, 0)
        self.groups['dest'] = 'b1'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[7][1] = (0, 0)
        self.groups['dest'] = 'b8'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_sideways(self):
        """Try to move a pawn sideways and assert that this move is
        determined illegal.
        """
        self.c.board[6] = [(0, 0) for i in range(8)]
        self.c.board[6][1] = ('P', True)
        self.groups['dest'] = 'c2'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[1][1] = ('P', False)
        self.groups['dest'] = 'c7'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)


class TestRookEvaluator(unittest.TestCase):
    """Test the rook evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'R',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_rook_forward(self):
        """Move a rook forward several spaces and assert that this move
        is determined legal.
        """
        pass

    def test_move_rook_backward(self):
        """Move a rook backward several spaces and assert that this move
        is determined legal.
        """
        pass

    def test_move_rook_left(self):
        """Move a rook left several spaces and assert that this move is
        determined legal.
        """
        pass

    def test_move_rook_right(self):
        """Move a rook right several spaces and assert that this move is
        determined legal.
        """
        pass

    def test_move_rook_forward_blocked(self):
        """Try to move a rook forward to a space it is blocked from
        reaching and assert that this move is determined illegal.
        """
        pass

    def test_move_rook_backward_blocked(self):
        """Try to move a rook backward to a space it is blocked from
        reaching and assert that this move is determined illegal.
        """
        pass

    def test_move_rook_left_blocked(self):
        """Try to move a rook left to a space it is blocked from
        reaching and assert that this move is determined illegal.
        """
        pass

    def test_move_rook_right_blocked(self):
        """Try to move a rook right to a space it is blocked from
        reaching and assert that this move is determined illegal.
        """
        pass

    def test_capture_rook_forward(self):
        """Capture a piece in front of a rook and assert that this move
        is determined legal.
        """

    def test_capture_rook_backward(self):
        """Capture a piece behind a rook and assert that this move is
        determined legal.
        """

    def test_capture_rook_left(self):
        """Capture a piece to a rook's left and assert that this move is
        determined legal.
        """

    def test_capture_rook_right(self):
        """Capture a piece to a rook's right and assert that this move
        is determined legal.
        """


class TestKnightEvaluator(unittest.TestCase):
    """Test the knight evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'N',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_knight_forward(self):
        """Move a knight forward 2, then left or right 1, and assert that
        this move is determined legal.
        """

    def test_move_knight_backward(self):
        """Move a knight backward 2, then left or right 1, and assert
        that this move is determined legal.
        """

    def test_move_knight_left(self):
        """Move a knight left 2, then up or down 1, and assert that this
        move is determined legal.
        """

    def test_move_knight_right(self):
        """Move a knight right 2, then up or down 1, and assert that this
        move is determined legal.
        """

    def test_move_knight_forward_blocked(self):
        """Move a knight forward 2 then right 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """

    def test_move_knight_backward_blocked(self):
        """Move a knight backward 2 then right 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """

    def test_move_knight_left_blocked(self):
        """Move a knight left 2 then up 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """

    def test_move_knight_right_blocked(self):
        """Move a knight right 2 then up 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """

    def test_capture_knight_forward(self):
        """Capture with a knight by moving forward 2, then right or left
        1, and assert that these moves are determined legal.
        """

    def test_capture_knight_backward(self):
        """Capture with a knight by moving backward 2, then right or left
        1, and assert that these moves are determined legal.
        """

    def test_capture_knight_left(self):
        """Capture with a knight by moving left 2, then up or down 1,
        and assert that these moves are determined legal.
        """

    def test_capture_knight_right(self):
        """Capture with a knight by moving right 2, then up or down 1,
        and assert that these moves are determined legal.
        """


class TestBishopEvaluator(unittest.TestCase):
    """Test the bishop evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'B',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }


class TestQueenEvaluator(unittest.TestCase):
    """Test the queen evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'Q',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }


class TestKingEvaluator(unittest.TestCase):
    """Test the king evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'K',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }


if __name__ == '__main__':
    unittest.main()
