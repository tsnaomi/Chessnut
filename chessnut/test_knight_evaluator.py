import unittest
from chess import ChessnutGame, MoveNotLegalError


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
        self.groups['dest'] = 'a3'
        self.assertEqual(self.c._knight_evaluator(self.groups), (7, 1))
        self.groups['dest'] = 'c3'
        self.assertEqual(self.c._knight_evaluator(self.groups), (7, 1))
        self.c.turn = False
        self.groups['dest'] = 'a6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (0, 1))
        self.groups['dest'] = 'c6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (0, 1))

    def test_move_knight_backward(self):
        """Move a knight backward 2, then left or right 1, and assert
        that this move is determined legal.
        """
        self.c.board[3][1] = ('N', True)
        self.c.board[7][1] = (0, 0)
        self.groups['dest'] = 'a3'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 1))
        self.groups['dest'] = 'c3'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 1))
        self.c.turn = False
        self.c.board[4][1] = ('N', False)
        self.c.board[0][1] = (0, 0)
        self.groups['dest'] = 'a6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 1))
        self.groups['dest'] = 'c6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 1))

    def test_move_knight_left(self):
        """Move a knight left 2, then up or down 1, and assert that this
        move is determined legal.
        """
        self.c.board[3][2] = ('N', True)
        self.c.board[7][1] = (0, 0)
        self.groups['dest'] = 'a4'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 2))
        self.groups['dest'] = 'a6'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 2))
        self.c.turn = False
        self.c.board[4][2] = ('N', False)
        self.c.board[0][1] = (0, 0)
        self.groups['dest'] = 'a3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 2))
        self.groups['dest'] = 'a5'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 2))

    def test_move_knight_right(self):
        """Move a knight right 2, then up or down 1, and assert that this
        move is determined legal.
        """
        self.c.board[3][2] = ('N', True)
        self.c.board[7][1] = (0, 0)
        self.groups['dest'] = 'e4'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 2))
        self.groups['dest'] = 'e6'
        self.assertEqual(self.c._knight_evaluator(self.groups), (3, 2))
        self.c.turn = False
        self.c.board[4][2] = ('N', False)
        self.c.board[0][1] = (0, 0)
        self.groups['dest'] = 'e3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 2))
        self.groups['dest'] = 'e5'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 2))

    def test_move_knight_forward_blocked(self):
        """Move a knight forward 2 then right 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """
        self.c.board[5][0] = ('P', True)
        self.groups['dest'] = 'a3'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[5][2] = ('P', True)
        self.groups['dest'] = 'c3'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.turn = False
        self.c.board[2][0] = ('P', False)
        self.groups['dest'] = 'a6'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[2][2] = ('P', False)
        self.groups['dest'] = 'c6'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)

    def test_move_knight_backward_blocked(self):
        """Move a knight backward 2 then right 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """
        self.c.board[3][1] = ('N', True)
        self.c.board[7][1] = (0, 0)
        self.c.board[5][0] = ('P', True)
        self.groups['dest'] = 'a3'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[5][2] = ('P', True)
        self.groups['dest'] = 'c3'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.turn = False
        self.c.board[4][1] = ('N', False)
        self.c.board[0][1] = (0, 0)
        self.c.board[2][0] = ('P', False)
        self.groups['dest'] = 'a6'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[2][2] = ('P', False)
        self.groups['dest'] = 'c6'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)

    def test_move_knight_left_blocked(self):
        """Move a knight left 2 then up 1 when another piece blocks
        that location and assert that this move is determined illegal.
        """
        self.c.board[3][2] = ('N', True)
        self.c.board[7][1] = (0, 0)
        self.c.board[4][0] = ('P', True)
        self.groups['dest'] = 'a4'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[2][0] = ('P', True)
        self.groups['dest'] = 'a6'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.turn = False
        self.c.board[4][2] = ('N', False)
        self.c.board[0][1] = (0, 0)
        self.c.board[5][0] = ('P', False)
        self.groups['dest'] = 'a3'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)
        self.c.board[3][0] = ('P', False)
        self.groups['dest'] = 'a5'
        self.assertRaises(
            MoveNotLegalError, self.c._knight_evaluator, self.groups)

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


if __name__ == '__main__':
    unittest.main()
