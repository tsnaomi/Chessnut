import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestRookEvaluator(unittest.TestCase):
    """Test the rook evaluator and the horizontal component of the queen
    evaluator (as they share the same logic)."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': None,
            'dest': None,
            'rank': '4',
            'file': 'e',
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_horizontally_one_space(self):
        """Move a rook (or queen) horizontally one space and assert that
        this move is determined legal.
        """
        for piece in [('R', True), ('R', False), ('Q', True), ('Q', False)]:
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['e3', 'e5', 'd4', 'f4']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))

    def test_move_horizontally_several_spaces(self):
        """Move a rook (or queen) horizontally several spaces and assert
        that this move is determined legal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for piece in [('R', True), ('R', False), ('Q', True), ('Q', False)]:
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['e2', 'e6', 'c4', 'g4']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))

    def test_move_horizontally_blocked_space(self):
        """Attempt to move a rook (or queen) horizontally to a space
        that is blocked and assert that the move is determined illegal.
        """
        for piece in [('R', True), ('R', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['e3', 'e5', 'd4', 'f4']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)

    def test_move_horizontally_blocked_path(self):
        """Attempt to move a rook (or queen) horizontally to a space the
        path to which is blocked and assert that the move is determined
        illegal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for piece in [('R', True), ('R', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['e2', 'e6', 'c4', 'g4']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)

    def test_capture_horizontally(self):
        """Attempt to capture horizontally with a rook (or queen) and
        assert that the move is determined legal.
        """
        self.groups['capture'] = 'x'
        for piece in [('R', True), ('R', False), ('Q', True), ('Q', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', not piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['e3', 'e5', 'd4', 'f4']:
                self.groups['dest'] = dest
                self.assertEqual(evaluator(self.groups), (4, 4))

    def test_move_rook_diagonally(self):
        """Try to move a rook diagonally and assert that move is determined
        illegal.
        """
        for piece in [('R', True), ('R', False)]:
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)

    def test_capture_rook_diagonally(self):
        """Attempt to capture diagonally with a rook and assert that the
        move is determined illegal.
        """
        self.groups['capture'] = 'x'
        for piece in [('R', True), ('R', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', not piece[1])
            self.groups['piece'] = piece[0]
            evaluator = self.c._get_evaluator(piece[0])
            self.c.turn = piece[1]
            self.c.board[4][4] = piece
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertRaises(MoveNotLegalError, evaluator, self.groups)


if __name__ == '__main__':
    unittest.main()
