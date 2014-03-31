import unittest
from chess import ChessnutGame


class TestPawnEvaluator(unittest.TestCase):
    """Test the pawn logic evaluator."""
    def setUp(self):
        self.c = ChessnutGame()

    def move_pawn_forward_1(self):
        pass

    def move_pawn_forward_2_from_start(self):
        pass

    def move_pawn_diagonally_not_capture(self):
        pass

    def move_pawn_forward_2_not_start(self):
        pass

    def move_pawn_backward(self):
        pass

    def move_pawn_sideways(self):
        pass


if __name__ == '__main__':
    unittest.main()
