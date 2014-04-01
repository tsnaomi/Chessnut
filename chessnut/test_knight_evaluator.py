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


if __name__ == '__main__':
    unittest.main()
