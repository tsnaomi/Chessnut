import unittest
from chess import ChessnutGame, GameOverError, MoveNotLegalError, \
    MoveAmbiguousError, NotationParseError


class TestEvaluateMove(unittest.TestCase):
    """Test the evaluate_move function for a variety of different
    functionalities.
    """
    def setUp(self):
        self.c = ChessnutGame()
        self.board_array = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p' for i in range(8)],
            ['0' for i in range(8)],
            ['0' for i in range(8)],
            ['0' for i in range(8)],
            ['0' for i in range(8)],
            ['P' for i in range(8)],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ]
        self.original_board = \
            ''.join([''.join(row) for row in self.board_array])

    def _make_test_move(self, move):
        """Make a test move in the test board array and then return the
        entire array as an image string for comparison.
        """
        if len(move) == 5:
            move = move[1:]
        orow, ocol = self.c._pgn_move_to_coords(move[:2])
        drow, dcol = self.c._pgn_move_to_coords(move[2:])

        self.board_array[drow][dcol], self.board_array[orow][ocol] = \
            self.board_array[orow][ocol], '0'

        return ''.join([''.join(row) for row in self.board_array])

    def test_evaluate_legal_moves(self):
        """Evaluate some legal moves and assert that they change the
        the board in expected ways.
        """
        test_moves = ['Nb1c3', 'c7c5', 'd2d4', 'Qd8a5', 'h2h4', 'Qa5a3']
        for move in test_moves:
            self.c(move)
            self.assertEqual(
                self._make_test_move(move), self.c._board_to_image_string())
            self.c.turn = not self.c.turn

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
        """End the game on a forfeit and assert that the game ends with
        the correct player as winner.
        """