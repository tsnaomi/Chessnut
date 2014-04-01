import unittest
from chess import ChessnutGame


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
        determined legal and is made.
        """
        self.groups['dest'] = 'b3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 6))
        self.c.turn = False
        self.groups['dest'] = 'b6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_exact_pawn_forward_1(self):
        """Use SAN to specify a specific pawn be moved forward one space
        and assert that this move is determined legal and is made.
        """

    def test_move_pawn_forward_2_from_start(self):
        """Move a pawn forward two spaces on its first move and assert
        that this move is determined legal and is made.
        """

    def test_move_exact_pawn_forward_2_from_start(self):
        """Use SAN to specify a specific pawn be moved forward two spaces
        from its starting position and assert that this move is determined
        legal and is made.
        """

    def test_move_pawn_forward_blocked(self):
        """Try to move a pawn forward when it is blocked and assert that
        this move is determined illegal and is not made.
        """

    def test_move_pawn_diagonally_not_capture(self):
        """Try to move a pawn diagonally when not capturing and assert
        that this move is determined illegal and is not made.
        """

    def test_move_pawn_forward_2_not_start(self):
        """Try to move a pawn forward two spaces not from its starting
        position and assert that this move is determined illegal and is
        not made.
        """

    def test_move_pawn_backward(self):
        """Try to move a pawn backwards and assert that this move is
        determined illegal and is not made.
        """

    def test_move_pawn_sideways(self):
        """Try to move a pawn sideways and assert that this move is
        determined illegal and is not made.
        """


if __name__ == '__main__':
    unittest.main()
