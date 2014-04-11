class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move, and knows to which
    player it belongs.
    """
    def __init__(self):
        pass


class Pawn(Piece):
    """A pawn. In addition to the functions of normal pieces, pawns track
    whether they are eligible to be en-passant captured.
    """
    pass


class Rook(Piece):
    """A rook."""
    pass


class QueensideRook(Rook):
    """A queenside rook. In addition to the functions of a normal rook,
    the queenside rook tracks whether it has moved (so that the legality
    of queenside castling can be determined).
    """
    pass


class KingsideRook(Rook):
    """A kingside rook. In addition to the functions of a normal rook,
    the kingside rook tracks whether it has moved (so that the legality
    of kingside castling can be determined).
    """
    pass


class Knight(Piece):
    """A knight."""
    pass


class Bishop(Piece):
    """A bishop."""
    pass


class Queen(Piece):
    """A queen."""
    pass


class King(Piece):
    """A king. In addition to the functions of normal pieces, the king
    tracks whether it has moved (so that the legality of castling can be
    determined).
    """
    pass
