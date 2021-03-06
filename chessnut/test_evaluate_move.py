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

    def _make_test_move(self, move=None):
        """Make a test move in the test board array and then return the
        entire array as an image string for comparison.
        """
        if move:
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
        test_moves = ['Nb1d2', 'c7c7', 'd2c4', 'Qd8a5', 'Rh1h4', 'Bc8a6']
        for move in test_moves:
            self.assertRaises(MoveNotLegalError, self.c, move)
            self.assertEqual(
                self.original_board, self.c._board_to_image_string())
            self.c.turn = not self.c.turn

    def test_evaluate_moves_not_relieving_check(self):
        """Evaluate a some moves that should be illegal because they
        don't remove the king from check and assert that they are
        correctly determined illegal.
        """
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]

        self.c.board[0][4] = ('K', False)
        self.c.board[7][4] = ('K', True)
        self.c.board[3][4] = ('Q', True)
        self.c.board[4][4] = ('Q', False)
        self.c.board[1][0] = ('P', False)
        self.c.board[6][0] = ('P', True)

        #import pdb; pdb.set_trace()
        self.assertRaises(MoveNotLegalError, self.c, 'a2a3')
        self.c.turn = False
        self.assertRaises(MoveNotLegalError, self.c, 'a7a6')

    def test_castling_logic_tracking(self):
        """Evaluate a variety of moves that should disallow future
        castling and assert that the castling tracking is correctly
        updated.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]

        for turn in [True, False]:
            self.c.turn = turn
            self.c('Ra1a2' if turn else 'Ra8a7')
            self.assertFalse(
                self.c.white_queenside if turn else self.c.black_queenside)
            self.c('Rh1h2' if turn else 'Rh8h7')
            self.assertFalse(
                self.c.white_kingside if turn else self.c.black_kingside)

        self.c.black_kingside = True
        self.c.black_queenside = True
        self.c.white_kingside = True
        self.c.white_queenside = True

        for turn in [True, False]:
            self.c.turn = turn
            self.c('Ke2' if turn else 'Ke7')
            self.assertFalse(
                self.c.white_queenside if turn else self.c.black_queenside)
            self.assertFalse(
                self.c.white_kingside if turn else self.c.black_kingside)

    def test_king_tracking(self):
        """Move kings around and assert that the game correctly keeps
        track of their position.
        """
        self.c.board[1] = [(0, 0) for i in range(8)]
        self.c.board[6] = [(0, 0) for i in range(8)]

        for turn in [True, False]:
            self.c.turn = turn
            self.c('Ke2' if turn else 'Ke7')
            self.assertEqual(
                self.c.white_king if turn else self.c.black_king,
                (6, 4) if turn else (1, 4)
            )

    def test_end_game_on_checkmate(self):
        """Set up several checkmates and assert that they end the game
        with the correct player being declared winner.
        """
        for turn in [True, False]:
            self.c = ChessnutGame()
            self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
            self.c.black_king = (0, 0)
            self.c.white_king = (0, 0)
            self.c.board[0][0] = ('K', not turn)
            self.c.board[1][0] = ('P', not turn)
            self.c.board[0][1] = ('B', not turn)
            self.c.board[3][1] = ('B', turn)

            self.c.turn = turn

            self.c('Bb5c6')
            self.assertTrue(self.c.is_over)
            self.assertTrue(self.c.winner if turn else not self.c.winner)

    def test_end_game_on_forfeit(self):
        """End the game on a forfeit and assert that the game ends with
        the correct player as winner.
        """

    def test_en_passant_tracking(self):
        """Check whether the game is correctly tracking when pawns are
        eligible to be captured en passant.
        """
        last_black, last_white = [], []
        for move in [rank + _file for rank in 'abcdefgh' for _file in '45']:
            drow, dcol = self.c._pgn_move_to_coords(move)
            self.c(move)
            self.assertEqual([(drow, dcol)], self.c.en_passant[self.c.turn])
            if self.c.turn:
                last_white = [(drow, dcol)]
                self.assertEqual(last_black, self.c.en_passant[False])
            else:
                last_black = [(drow, dcol)]
                self.assertEqual(last_white, self.c.en_passant[True])
            self.c.turn = not self.c.turn

    def test_en_passant_capture(self):
        """Perform several en passant captures and assert that the board
        and game variables are being modified in the correct ways.
        """
        self.c.board[4][2] = ('P', False)
        self.c.board[6][1] = ('P', True)
        self.c.board[3][4] = ('P', True)
        self.c.board[1][5] = ('P', False)

        self.c('b4')
        self.c.turn = False
        self.c('xb3')
        self.assertEqual(self.c.board[4][1], (0, 0))
        self.assertEqual(self.c.board[5][1], ('P', False))

        self.c('f5')
        self.c.turn = True
        self.c('xf6')
        self.assertEqual(self.c.board[3][5], (0, 0))
        self.assertEqual(self.c.board[2][5], ('P', True))

    def test_pawn_promotion(self):
        """Perform all possible pawn promotions and assert that they are
        performed as expected.
        """
        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.c.white_king = (4, 0)
        self.c.black_king = (4, 7)
        self.c.board[5] = [('P', False) for i in range(8)]
        self.c.board[3] = [('P', True) for i in range(8)]
        for piece in ['R', 'B', 'N', 'Q']:
            for join in ['', '=']:
                self.c.board[7] = [(0, 0) for i in range(8)]
                self.c.board[0] = [(0, 0) for i in range(8)]
                self.c.board[6] = [('P', False) for i in range(8)]
                self.c.board[1] = [('P', True) for i in range(8)]
                for dest in [rank + _file for rank in 'abcdefgh' for _file in '81']:
                    drow, dcol = self.c._pgn_move_to_coords(dest)
                    self.c("P%s%s%s" % (dest, join, piece))
                    self.assertEqual(self.c.board[drow][dcol], (piece, self.c.turn))
                    self.c.turn = not self.c.turn

    def test_pawn_promotion_blocked(self):
        """Attempt to perform pawn promotions when the destination cell
        is blocked and assert that the promotions fail.
        """
        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.c.white_king = (4, 0)
        self.c.black_king = (4, 7)
        self.c.board[0] = [('P', False) for i in range(8)]
        self.c.board[7] = [('P', True) for i in range(8)]
        self.c.board[6] = [('P', False) for i in range(8)]
        self.c.board[1] = [('P', True) for i in range(8)]
        for piece in ['R', 'B', 'N', 'Q']:
            for join in ['', '=']:
                for dest in [rank + _file for rank in 'abcdefgh' for _file in '81']:
                    drow, dcol = self.c._pgn_move_to_coords(dest)
                    self.assertRaises(
                        MoveNotLegalError,
                        self.c,
                        "P%s%s%s" % (dest, join, piece)
                    )
                    self.assertEqual(
                        self.c.board[drow][dcol], ('P', not self.c.turn))
                    self.c.turn = not self.c.turn

    def test_pawn_promotion_to_pawn_or_king(self):
        """Attempt to promote a pawn to a king or a pawn and assert that
        these moves are determined illegal.
        """
        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.c.white_king = (4, 0)
        self.c.black_king = (4, 7)
        self.c.board[6] = [('P', False) for i in range(8)]
        self.c.board[1] = [('P', True) for i in range(8)]
        for piece in ['K', 'P']:
            for join in ['', '=']:
                for dest in [rank + _file for rank in 'abcdefgh' for _file in '81']:
                    drow, dcol = self.c._pgn_move_to_coords(dest)
                    self.assertRaises(
                        MoveNotLegalError,
                        self.c,
                        "P%s%s%s" % (dest, join, piece)
                    )
                    self.assertEqual(
                        self.c.board[drow][dcol], (0, 0))
                    self.c.turn = not self.c.turn

    def test_pawn_promotion_not_pawns(self):
        """Try to promote pieces that aren't pawns and assert that these
        moves are determined illegal.
        """
        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.c.white_king = (5, 0)
        self.c.black_king = (4, 7)
        self.c.board[5] = [('P', False) for i in range(8)]
        self.c.board[2] = [('P', True) for i in range(8)]
        self.c.board[6] = [('R', False) for i in range(8)]
        self.c.board[1] = [('R', True) for i in range(8)]
        for piece in ['R', 'B', 'N', 'Q']:
            for join in ['', '=']:
                for dest in [rank + _file for rank in 'abcdefgh' for _file in '81']:
                    drow, dcol = self.c._pgn_move_to_coords(dest)
                    self.assertRaises(
                        MoveNotLegalError,
                        self.c,
                        "R%s%s%s" % (dest, join, piece)
                    )
                    self.assertEqual(
                        self.c.board[drow][dcol], (0, 0))
                    self.c.turn = not self.c.turn


if __name__ == '__main__':
    unittest.main()
