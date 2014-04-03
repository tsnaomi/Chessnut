import unittest
from chess import ChessnutGame, GameOverError, MoveNotLegalError, \
    MoveAmbiguousError, NotationParseError


class TestEvaluateMove(unittest.TestCase):
    """Test the evaluate_move function for a variety of different
    functionalities.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def test_evaluate_legal_moves(self):
        """Evaluate a variety of legal moves and assert that they change
        the board in expected ways.
        """

    def test_evaluate_illegal_moves(self):
        """Evaluate a variety of illegal moves and assert that they don't
        change the board.
        """

    def test_evaluate_moves_not_relieving_check(self):
        """Evaluate a variety of moves that should be illegal because
        they don't remove the king from check and assert that they are
        correctly determined illegal.
        """

    def test_castling_logic_tracking(self):
        """Evaluate a variety of moves that should disallow future
        castling and assert that the castling tracking is correctly
        updated.
        """

    def test_king_tracking(self):
        """Moves kings around and assert that the game correctly keeps
        track of their position.
        """

    def test_end_game_on_checkmate(self):
        """Set up several checkmates and assert that they end the game
        with the correct player being declared winner.
        """

    def test_end_game_on_forfeit(self):
        """