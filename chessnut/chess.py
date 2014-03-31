class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        self.pgn = game
        self.fen = self._pgn_to_fen(game)
        self.board = self._fen_to_board(game)

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        pass

    def _pgn_to_fen(board):
        """Converts PGN notation to FEN notation."""
        pass

    def _fen_to_board(self, pgn):
        """Converts PGN format to a 2D array representing board state."""
        pass

    def _initialize_chessboard(self):
        """Creates a 2D array representing an initial chessboard."""


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
