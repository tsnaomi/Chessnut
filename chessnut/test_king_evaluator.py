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


if __name__ == '__main__':
    unittest.main()
