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


if __name__ == '__main__':
    unittest.main()
