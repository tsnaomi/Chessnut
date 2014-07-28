class ChessnutBaseException(BaseException):
    """Base exception class for Chessnut."""
    pass


class BoardIndexError(ChessnutBaseException):
    """Exception raised when attempting to access a space outside the
    coordinates of the board.
    """
    pass
