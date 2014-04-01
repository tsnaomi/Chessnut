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

    def test_capture_knight_legally(self):
        """Capture with a knight in any of the eight legal configurations
        and assert that each move is determined legal.
        """
        self.groups['capture'] = 'x'
        for piece in [('N', True), ('N', False)]:
            self.c.board = \
                [[('K', not piece[1]) for i in range(8)] for i in range(8)]
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d6', 'f6', 'c5', 'g5', 'c3', 'g3', 'd2', 'f2']:
                self.groups['dest'] = dest
                self.assertEqual(self.c._knight_evaluator(self.groups), (4, 4))


if __name__ == '__main__':
    unittest.main()
