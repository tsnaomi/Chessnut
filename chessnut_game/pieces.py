class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move (regardless of the
    legality of that move), and knows to which player it belongs.
    """
    def __init__(self, player=None, rank=None, _file=None):
        #Keep track of whose piece this is and where it is on the board.
        self.player = player
        self.rank = rank
        self.file = _file

        #Store a set containing all the spaces on the board to which this
        #piece could move - IF this piece were the only piece on the board.
        #This much, the piece can calculate on its own, because it knows
        #its own move logic.
        self.naive_moves = set()

        #Store a set containing all of the spaces on the board to which
        #this piece can ACTUALLY move, given the state of the board. This
        #attribute is set by the game object, as the piece does not know
        #about the positions of other pieces on its own.
        self.actual_moves = set()

        #Store a set containing all the spaces on the board to which this
        #piece could capture - IF this piece were the only piece on the
        #board, save for a single enemy piece at the space being captured
        #to. The piece can calculate this on its own because it is familiar
        #with its own move logic. For all pieces save the pawn, this set
        #will be identical to the naive_moves set.
        self.naive_captures = self.naive_moves

        #Store a set containing all of the spaces on the board to which
        #this piece can ACTUALLY capture. This attribute is set by the
        #game object, as it knows about the state of the board, while the
        #piece does not. For all pieces save the pawn, this set will be
        #identical to the actual_moves set.
        self.actual_captures = self.actual_moves


class Pawn(Piece):
    """A pawn. In addition to the functions of normal pieces, pawns track
    whether they are eligible to be en-passant captured. Pawns also track
    separately which spaces they can move to and which they can capture
    to (since their capture and move logic are different).
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
