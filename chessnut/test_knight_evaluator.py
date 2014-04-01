import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestKnightEvaluator(unittest.TestCase):
    """Test the knight evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'N',
            'dest': None,
            'rank': '4',
            'file': 'e',
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_knight_legally(self):
        """Move a knight in any of the eight legal configurations and
        assert that the moves are determined legal.
        """
        self.c.board[6] = [(0, 0) for i in range(8)]
        for piece in [('N', True), ('N', False)]:
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d6', 'f6', 'c5', 'g5', 'c3', 'g3', 'd2', 'f2']:
                self.groups['dest'] = dest
                self.assertEqual(self.c._knight_evaluator(self.groups), (4, 4))

    def test_move_knight_legally_blocked(self):
        """Move a knight in any of the eight legal configurations, but
        block its destination space. Assert that each move is determined
        illegal.
        """
        for piece in [('N', True), ('N', False)]:
            self.c.board = \
                [[('K', piece[1]) for i in range(8)] for i in range(8)]
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d6', 'f6', 'c5', 'g5', 'c3', 'g3', 'd2', 'f2']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._knight_evaluator, self.groups)

    # def test_move_knight_forward_blocked(self):
    #     """Move a knight forward 2 then right 1 when another piece blocks
    #     that location and assert that this move is determined illegal.
    #     """
    #     self.c.board[5][0] = ('P', True)
    #     self.groups['dest'] = 'a3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[5][2] = ('P', True)
    #     self.groups['dest'] = 'c3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.turn = False
    #     self.c.board[2][0] = ('P', False)
    #     self.groups['dest'] = 'a6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[2][2] = ('P', False)
    #     self.groups['dest'] = 'c6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)

    # def test_move_knight_backward_blocked(self):
    #     """Move a knight backward 2 then right 1 when another piece blocks
    #     that location and assert that this move is determined illegal.
    #     """
    #     self.c.board[3][1] = ('N', True)
    #     self.c.board[7][1] = (0, 0)
    #     self.c.board[5][0] = ('P', True)
    #     self.groups['dest'] = 'a3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[5][2] = ('P', True)
    #     self.groups['dest'] = 'c3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.turn = False
    #     self.c.board[4][1] = ('N', False)
    #     self.c.board[0][1] = (0, 0)
    #     self.c.board[2][0] = ('P', False)
    #     self.groups['dest'] = 'a6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[2][2] = ('P', False)
    #     self.groups['dest'] = 'c6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)

    # def test_move_knight_left_blocked(self):
    #     """Move a knight left 2 then up 1 when another piece blocks
    #     that location and assert that this move is determined illegal.
    #     """
    #     self.c.board[3][2] = ('N', True)
    #     self.c.board[7][1] = (0, 0)
    #     self.c.board[4][0] = ('P', True)
    #     self.groups['dest'] = 'a4'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[2][0] = ('P', True)
    #     self.groups['dest'] = 'a6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.turn = False
    #     self.c.board[4][2] = ('N', False)
    #     self.c.board[0][1] = (0, 0)
    #     self.c.board[5][0] = ('P', False)
    #     self.groups['dest'] = 'a3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[3][0] = ('P', False)
    #     self.groups['dest'] = 'a5'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)

    # def test_move_knight_right_blocked(self):
    #     """Move a knight right 2 then up 1 when another piece blocks
    #     that location and assert that this move is determined illegal.
    #     """
    #     self.c.board[3][2] = ('N', True)
    #     self.c.board[7][1] = (0, 0)
    #     self.c.board[4][4] = ('P', True)
    #     self.groups['dest'] = 'e4'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[2][4] = ('P', True)
    #     self.groups['dest'] = 'e6'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.turn = False
    #     self.c.board[4][2] = ('N', False)
    #     self.c.board[0][1] = (0, 0)
    #     self.c.board[5][4] = ('P', False)
    #     self.groups['dest'] = 'e3'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)
    #     self.c.board[3][4] = ('P', False)
    #     self.groups['dest'] = 'e5'
    #     self.assertRaises(
    #         MoveNotLegalError, self.c._knight_evaluator, self.groups)

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
