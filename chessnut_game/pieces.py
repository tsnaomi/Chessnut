class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move (regardless of the
    legality of that move), and knows to which player it belongs.
    """
    def __init__(self, player=None, rank=None, _file=None):
        """Initialize the attributes of this Piece, then bind can_capture_to
        to can_move_to. In most pieces, capture logic is the same as move
        logic, so this alias is desired. The only exception is in Pawns.
        """
        self._initialize_piece(player, rank, _file)
        self.can_capture_to = self.can_move_to

    def _initialize_piece(self, player, rank, _file):
        """This method is responsible for setting all attributes on Pieces.
        It should also be called in the __init__ of any class that subclasses
        Piece without calling Piece.__init__, if those objects are to correctly
        'inherit' these attributes. This encapsulation is necessary because
        Piece's __init__ binds the name 'can_capture_to' to the method
        'can_move_to', which is a behavior that is usually desired, but
        not ALWAYS desired. In Pawns, these names need to be bound to
        methods with different behaviors. However, if Pawn were to call
        Piece.__init__(), then this re-binding of names would become
        impossible.
        """
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
    def __init__(self, player=None, rank=None, _file=None):
        self._initialize_piece(player, rank, _file)

        #Track whether or not this pawn is eligible to be en-passant
        #captured.
        self.en_passant = False

        #Store a separate move set for captures, as pawns have separate
        #capture and move logic.
        self.naive_captures = set()
        self.actual_captures = set()


class Rook(Piece):
    """A rook."""
    pass


class QueensideRook(Rook):
    """A queenside rook. In addition to the functions of a normal rook,
    the queenside rook tracks whether it has moved (so that the legality
    of queenside castling can be determined).
    """
    def __init__(self, player=None, rank=None, _file=None):
        super(QueensideRook, self).__init__(player, rank, _file)

        #Track whether or not this rook has moved (so that the legality
        #of queenside castling can be determined).
        self.has_moved = False


class KingsideRook(Rook):
    """A kingside rook. In addition to the functions of a normal rook,
    the kingside rook tracks whether it has moved (so that the legality
    of kingside castling can be determined).
    """
    def __init__(self, player=None, rank=None, _file=None):
        super(KingsideRook, self).__init__(player, rank, _file)

        #Track whether or not this rook has moved (so that the legality
        #of kingside castling can be determined).
        self.has_moved = False


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
    def __init__(self, player=None, rank=None, _file=None):
        super(King, self).__init__(player, rank, _file)

        #Track whether or not this king has moved (so that the legality
        #of castling can be determined).
        self.has_moved = False
