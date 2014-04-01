import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestBishopEvaluator(unittest.TestCase):
    """Test the bishop evaluator and the diagonal component of the queen
    evaluator (as they share the same logic).
    """
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': None,
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_diagonally_one_space(self):
        """Move a bishop (or queen) diagonally one space and assert that
        this move is determined legal.
        """
        for piece in [('B', True), ('B', False), ('Q', True), ('Q', False)]:
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))

    def test_move_diagonally_multiple_spaces(self):
        """Move a bishop (or queen) diagonally several spaces and assert
        that this move is determined legal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for piece in [('B', True), ('B', False), ('Q', True), ('Q', False)]:
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['c2', 'c6', 'g2', 'g6']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))

    def test_move_diagonally_blocked_space(self):
        """Attempt to move a bishop (or queen) diagonally to a space that
        is blocked and assert that the move is determined illegal.
        """
        for piece in [('B', True), ('B', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)

    def test_move_diagonally_blocked_path(self):
        """Attempt to move a bishop (or queen) diagonally to a space the
        path to which is blocked and assert that the move is determined
        illegal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for piece in [('B', True), ('B', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['c2', 'c6', 'g2', 'g6']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)

    def test_capture_diagonally(self):
        """Attempt to capture diagonally with a bishop (or queen) and
        assert that the move is determined legal.
        """
        self.groups['capture'] = 'x'
        for piece in [('B', True), ('B', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', not piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))


if __name__ == '__main__':
    unittest.main()
