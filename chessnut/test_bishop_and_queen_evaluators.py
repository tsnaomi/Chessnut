import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestBishopEvaluator(unittest.TestCase):
    """Test the bishop evaluator and the diagonal component of the queen
    evaluator.
    """
    def setUp(self):
        self.c = ChessnutGame()
        self.groups = {
            'piece': 'B',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
        }


if __name__ == '__main__':
    unittest.main()
