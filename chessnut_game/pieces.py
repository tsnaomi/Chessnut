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

    def can_move_to(self, space):
        """Refer to the actual_moves cache to determine whether this piece
        can reach the space in question.
        """
        return True if space in self.actual_moves else False

    def _cache_horizontal_moves(self, backward=True, sideways=True, limit=7):
        """Calculates the spaces to which this piece can move horizontally.
        Can be limited by disallowing backward and/or side-to-side movement
        and by limiting the number of spaces that are allowed to be moved.
        """
        move_modifiers = [(1, 0)]
        if backward:
            move_modifiers.append((-1, 0))
        if sideways:
            move_modifiers.extend([(0, 1), (0, -1)])

        for rankmod, filemod in move_modifiers:
            for i in range(limit):
                rank = self.rank + rankmod
                _file = chr(ord(self.file) + filemod)

                if rank > 8 or rank < 0 or _file > 'h' or _file < 'a':
                    break

                yield ''.join([_file, rank])

    def _cache_diagonal_moves(self, backward=True, limit=7):
        """Calculates the spaces to which this piece can move diagonally.
        Can be limited by disallowing movement backwards along diagonals
        and by limiting the number of spaces that are allowed to be moved.
        """
        pass


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

    def can_capture_to(self, space):
        """Pawns are a special case piece: their move logic and capture logic
        differ. They must therefore have separate behavior for can_capture_to
        (in other pieces, this function is an alias for can_move_to).
        """
        return True if space in self.actual_captures else False


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
