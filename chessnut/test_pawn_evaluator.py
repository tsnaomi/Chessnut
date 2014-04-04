import unittest
from chess import ChessnutGame, MoveNotLegalError


class TestPawnEvaluator(unittest.TestCase):
    """Test the pawn logic evaluator."""
    def setUp(self):
        self.c = ChessnutGame()
        self.c.board = [[(0, 0) for i in range(8)] for i in range(8)]
        self.c.board[1][1] = ('P', False)
        self.c.board[6][1] = ('P', True)
        self.groups = {
            'piece': 'P',
            'dest': None,
            'rank': None,
            'file': None,
            'capture': None,
            'check': None,
            'checkmate': None,
            'promotion': None,
        }

    def test_move_pawn_forward_one(self):
        """Move a pawn forward one space and assert that this move is
        determined legal.
        """
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_pawn_forward_two_from_start(self):
        """Move a pawn forward two spaces on its first move and assert
        that this move is determined legal.
        """
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b4'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.turn = False
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b5'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_move_pawn_forward_one_blocked(self):
        """Try to move a pawn forward when it is blocked and assert that
        this move is determined illegal.
        """
        self.c.board[5][1] = ('K', True)
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b3'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[2][1] = ('K', False)
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b6'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_forward_two_from_start_blocked_path(self):
        """Attempt to move a pawn forward two spaces on its first move
        when its path is blocked and assert that this move is determined
        illegal.
        """
        self.c.board[5][1] = ('K', True)
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b4'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[2][1] = ('K', False)
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b5'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_forward_two_from_start_blocked_space(self):
        """Attempt to move a pawn forward two spaces on its first move
        when the destination space is blocked and assert that this move
        is determined illegal.
        """
        self.c.board[4][1] = ('K', True)
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b4'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)
        self.c.turn = False
        self.c.board[3][1] = ('K', False)
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b5'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_move_pawn_illegally(self):
        """Try to move a pawn to every space on the board except those
        that are legal and assert that each operation is determined
        illegal.
        """
        dests = [col + row for col in 'abcdefgh' for row in '12345678']
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        for dest in dests:
            if dest in ['b3', 'b4']:
                continue
            self.groups['dest'] = dest
            self.assertRaises(
                MoveNotLegalError, self.c._pawn_evaluator, self.groups)

        self.c.turn = False
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        for dest in dests:
            if dest in ['b5', 'b6']:
                continue
            self.groups['dest'] = dest
            self.assertRaises(
                MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_capture_pawn(self):
        """Capture pieces with a pawn and assert that this move is
        determined legal.
        """
        self.groups['capture'] = 'x'

        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.c.board[5][2] = ('P', False)
        self.groups['dest'] = 'c3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))
        self.c.board[5][0] = ('P', False)
        self.groups['dest'] = 'a3'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (6, 1))

        self.c.turn = False
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.c.board[2][2] = ('P', True)
        self.groups['dest'] = 'c6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))
        self.c.board[2][0] = ('P', True)
        self.groups['dest'] = 'a6'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (1, 1))

    def test_capture_pawn_forward(self):
        """Attempt to capture a piece in front of a pawn and assert that
        this move is determined illegal.
        """
        self.groups['capture'] = 'x'

        self.c.board[5][1] = ('K', True)
        self.groups['rank'] = '2'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b3'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

        self.c.turn = False
        self.c.board[2][1] = ('K', False)
        self.groups['rank'] = '7'
        self.groups['file'] = 'b'
        self.groups['dest'] = 'b6'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_en_passant_capture(self):
        """Capture an enemy pawn en passant and assert that this move is
        determined legal.
        """
        self.groups['capture'] = 'x'

        self.c.board[4][2] = ('P', False)
        self.c.board[4][1] = ('P', True)
        self.c.board[3][4] = ('P', True)
        self.c.board[3][5] = ('P', False)

        self.c.en_passant[not self.c.turn].append((4, 2))
        self.groups['dest'] = 'c5'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (4, 1))

        self.c.turn = False
        self.c.en_passant[not self.c.turn].append((3, 4))
        self.groups['dest'] = 'e4'
        self.assertEqual(self.c._pawn_evaluator(self.groups), (3, 5))

    def test_en_passant_capture_expired(self):
        """Attempt an en passant capture after the option to capture en
        passant has expired and assert that this move is determined illegal.
        """
        self.c.board[4][2] = ('P', False)
        self.c.board[4][1] = ('P', True)
        self.c.board[3][4] = ('P', True)
        self.c.board[3][5] = ('P', False)

        self.groups['dest'] = 'c5'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

        self.c.turn = False
        self.groups['dest'] = 'e4'
        self.assertRaises(
            MoveNotLegalError, self.c._pawn_evaluator, self.groups)

    def test_promotion_logic_tracking(self):
        """Test whether the logic for pawn promotion tracking is correctly
        triggered.
        """
        self.c.board[6] = [('P', False) for i in range(8)]
        self.c.board[1] = [('P', True) for i in range(8)]
        self.groups['promotion'] = 'N'
        for dest in [rank + _file for rank in 'abcdefgh' for _file in '81']:
            self.groups['dest'] = dest
            self.c._pawn_evaluator(self.groups)
            self.assertTrue(self.c.pawn_promotion)
            self.c.pawn_promotion = False
            self.c.turn = not self.c.turn

    def test_promotion_logic_not_legal_promotion(self):
        """Assert that the pawn promotion logic is only triggered when pawns
        are able to be promoted.
        """
        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.groups['promotion'] = 'N'
        for row in range(7, 1, -1):
            drow = self.c._row_to_pgn_rank(row - 1)
            self.c.board[row] = [('P', True) for i in range(8)]
            for dest in [_file + rank for _file in 'abcdefgh' for rank in [drow]]:
                self.groups['dest'] = dest
                self.c._pawn_evaluator(self.groups)
                self.assertFalse(self.c.pawn_promotion)

        self.c.board = [[(0, 0) for i in range(8)] for j in range(8)]
        self.c.turn = False
        for row in range(6):
            drow = self.c._row_to_pgn_rank(row + 1)
            self.c.board[row] = [('P', False) for i in range(8)]
            for dest in [_file + rank for _file in 'abcdefgh' for rank in [drow]]:
                self.groups['dest'] = dest
                self.c._pawn_evaluator(self.groups)
                self.assertFalse(self.c.pawn_promotion)


if __name__ == '__main__':
    unittest.main()
