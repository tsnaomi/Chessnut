import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestKingEvaluator(unittest.TestCase):
    """Test the king evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        self.groups = {
            'piece': 'K',
            'dest': None,
            'rank': '4',
            'file': 'e',
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_king_horizontally(self):
        """Move a king horizontally and assert that this move is
        determined legal.
        """
        for king in [('K', True), ('K', False)]:
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['e3', 'e5', 'd4', 'f4']:
                self.groups['dest'] = dest
                self.assertEqual(self.c._king_evaluator(self.groups), (4, 4))

    def test_move_king_diagonally(self):
        """Move a king diagonally and assert that this move is determined
        legal.
        """
        for king in [('K', True), ('K', False)]:
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertEqual(self.c._king_evaluator(self.groups), (4, 4))

    def test_move_king_horizontally_multiple_spaces(self):
        """Move a king horizontally more than one space and assert that
        this move is determined illegal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for king in [('K', True), ('K', False)]:
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['e2', 'e6', 'c4', 'g4']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._king_evaluator, self.groups)

    def test_move_king_diagonally_multiple_spaces(self):
        """Move a king diagonally more than one space and assert that
        this move is determined illegal.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]
        for king in [('K', True), ('K', False)]:
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['c2', 'c6', 'g2', 'g6']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._king_evaluator, self.groups)

    def test_move_king_horizontally_blocked(self):
        """Move a king horizontally when it is blocked and assert that
        this move is determined illegal.
        """
        for king in [('K', True), ('K', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', king[1])
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['e3', 'e5', 'd4', 'f4']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._king_evaluator, self.groups)

    def test_move_king_diagonally_blocked(self):
        """Move a king diagonally when it is blocked and assert that
        this move is determined illegal.
        """
        for king in [('K', True), ('K', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', king[1])
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._king_evaluator, self.groups)

    def test_move_king_to_checked_position(self):
        """Try to move a king to a space that is under check and assert
        that this move is determined illegal.
        """
        for king in [('K', True), ('K', False)]:
            self.c.board[4][4] = king
            self.c.board[3][0] = ('Q', not king[1])
            self.c.turn = king[1]
            for dest in ['d5', 'e5', 'f5']:
                self.groups['dest'] = dest
                self.assertRaises(
                    MoveNotLegalError, self.c._king_evaluator, self.groups)

    def test_capture_king_horizontally(self):
        """Capture pieces that lie horizontally around a king and assert
        that this move is determined legal.
        """
        self.groups['capture'] = 'x'
        for king in [('K', True), ('K', False)]:
            self.c.turn = king[1]
            for dest in ['e3', 'e5', 'd4', 'f4']:
                for i in [3, 4, 5]:
                    for j in [3, 4, 5]:
                        self.c.board[i][j] = (0, 0)
                self.c.board[4][4] = king
                row, col = self.c._pgn_move_to_coords(dest)
                self.c.board[row][col] = ('P', not king[1])
                self.groups['dest'] = dest
                self.assertEqual(self.c._king_evaluator(self.groups), (4, 4))

    def test_capture_king_vertically(self):
        """Capture pieces that lie diagonally around a king and assert
        that this move is determined legal.
        """
        self.groups['capture'] = 'x'
        for king in [('K', True), ('K', False)]:
            for i in [3, 4, 5]:
                for j in [3, 4, 5]:
                    self.c.board[i][j] = ('P', not king[1])
            self.c.turn = king[1]
            self.c.board[4][4] = king
            for dest in ['d3', 'd5', 'f3', 'f5']:
                self.groups['dest'] = dest
                self.assertEqual(self.c._king_evaluator(self.groups), (4, 4))


if __name__ == '__main__':
    unittest.main()
