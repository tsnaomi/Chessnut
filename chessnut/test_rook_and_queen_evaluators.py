import unittest
from chess import ChessnutGame, MoveNotLegalError


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


if __name__ == '__main__':
    unittest.main()
