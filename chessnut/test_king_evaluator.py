import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestKingEvaluator(unittest.TestCase):
    """Test the king evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'K',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }

    def test_move_king_horizontally(self):
        """Move a king horizontally and assert that this move is
        determined legal.
        """

    def test_move_king_diagonally(self):
        """Move a king diagonally and assert that this move is determined
        legal.
        """

    def test_move_king_horizontally_multiple_spaces(self):
        """Move a king horizontally more than one space and assert that
        this move is determined illegal.
        """

    def test_move_king_diagonally_multiple_spaces(self):
        """Move a king diagonally more than one space and assert that
        this move is determined illegal.
        """

    def test_move_king_horizontally_blocked(self):
        """Move a king horizontally when it is blocked and assert that
        this move is determined illegal.
        """

    def test_move_king_diagonally_blocked(self):
        """Move a king diagonally when it is blocked and assert that
        this move is determined illegal.
        """

    def test_capture_king_horizontally(self):
        """Capture pieces that lie horizontally around a king and assert
        that this move is determined legal.
        """

    def test_capture_king_vertically(self):
        """Capture pieces that lie diagonally around a king and assert
        that this move is determined legal.
        """


if __name__ == '__main__':
    unittest.main()
