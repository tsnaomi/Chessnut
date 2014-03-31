import re


class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        #False means black's turn, True means white's.
        self.turn = True
        self.pgn = game
        self.board = self._pgn_to_board(game)
        self.image_name = self._board_to_image()

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        pass

    def _pgn_to_board(self):
        """Converts PGN notation to a 2D array representing board state."""
        board = self._initialize_chessboard()
        moves = re.split(r'\s?\d+\.\s', self.pgn)

        move_count = 0
        for move in moves:
            move_count += 1
            half_moves = move.split()

            for half_move in half_moves:
                self._evaluate_move(half_move)

            if len(half_moves) == 1:
                self.turn = False

    def _board_to_image(self, pgn):
        """Converts the board state to an image filename."""
        pass

    def _pgn_move_to_coords(self, move):
        """Converts a single move in PGN notation to board-state array
        coordinates.
        """
        pass

    def _evaluate_move(self, move):
        """Take in a move in PGN notation, evaluate it, and perform it,
        if legal.
        """
        pass

    def _initialize_chessboard(self):
        """Creates a 2D array representing an initial chessboard."""
        board = []

        board.append([
            ('R', False),
            ('N', False),
            ('B', False),
            ('Q', False),
            ('K', False),
            ('B', False),
            ('N', False),
            ('R', False),
        ])
        board.append([('P', False) for i in range(8)])

        for i in range(4):
            board.append([0 for i in range(8)])

        board.append(('P', False) for i in range(8))
        board.append([
            ('R', False),
            ('N', False),
            ('B', False),
            ('K', False),
            ('Q', False),
            ('B', False),
            ('N', False),
            ('R', False),
        ])

        return board


class ChessnutError(BaseException):
    """Chessnut base exception."""
    pass


class MoveNotValidError(ChessnutError):
    """Exception raised when a player attempts to make a move that is not
    legal.
    """
    pass


class NotationParseError(ChessnutError):
    """Exception raised when a player submits chess notation that the
    game logic can't parse.
    """
    pass
