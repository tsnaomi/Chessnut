class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move (regardless of the
    legality of that move), and knows to which player it belongs.
    """
    def __init__(self, player=None, _file=None, rank=None):
        """Initialize the attributes of this Piece."""
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

        #Bind can_capture_to to can_move_to. In most pieces, capture logic
        #and move logic is the same, so the same method should be called
        #to determine both.
        self.can_capture_to = self.can_move_to

        #Generate the initial naive_moves cache.
        self._generate_naive_cache()

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        if not isinstance(value, bool):
            raise TypeError("Attempting to set player to non-boolean value.")
        self._player = value

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        if not isinstance(value, str):
            raise TypeError("Attempting to set file to non-string value.")
        elif len(value) != 1 or value not in 'abcdefgh':
            raise ValueError(
                "Attempting to set file to value not in range a-h.")
        self._file = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if not isinstance(value, str):
            raise TypeError("Attempting to set rank to non-string value.")
        elif len(value) != 1 or value not in '12345678':
            raise ValueError(
                "Attempting to set rank to value not in range 1-8.")
        self._rank = value

    def can_move_to(self, rank=None, _file=None):
        """Refer to the actual_moves cache to determine whether this piece
        can reach the space in question.
        """
        return True if (_file, rank) in self.actual_moves else False

    def move_to(self, rank=None, _file=None):
        """Move this Piece to the rank and file provided. If neither is
        provided, no action is taken. If only one is provided, the other
        is unmodified. If either is provided, the naive_moves cache is
        regenerated.
        """
        if rank is None and _file is None:
            return

        if _file is not None:
            self.file = _file

        if rank is not None:
            self.rank = rank

        self._generate_naive_cache()

    def _generate_naive_cache(self):
        """Generate the naive moves cache. The Piece class is non-specific
        and has no move logic, so this method is empty. Pieces derived
        from this class must implement their own version based on their move
        logic. _generate_horizontal_moves and _generate_diagonal_moves are
        provided to assist with this task.
        """
        pass

    def _generate_horizontal_moves(self, backward=True, sideways=True, limit=7):
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

    def _generate_diagonal_moves(self, backward=True, limit=7):
        """Calculates the spaces to which this piece can move diagonally.
        Can be limited by disallowing movement backwards along diagonals
        and by limiting the number of spaces that are allowed to be moved.
        """
        move_modifiers = [(1, 1), (1, -1)]
        if backward:
            move_modifiers.extend([(-1, 1), (-1, -1)])

        for rankmod, filemod in move_modifiers:
            for i in range(limit):
                rank = self.rank + rankmod
                _file = chr(ord(self.file) + filemod)

                if rank > 8 or rank < 0 or _file > 'h' or _file < 'a':
                    break

                yield ''.join([_file, rank])


class Pawn(Piece):
    """A pawn. In addition to the functions of normal pieces, pawns track
    whether they are eligible to be en-passant captured. Pawns also track
    separately which spaces they can move to and which they can capture
    to (since their capture and move logic are different).
    """
    def __init__(self, player=None, rank=None, _file=None):
        super(Pawn, self).__init__(player, rank, _file)

        #Track whether or not this pawn is eligible to be en-passant
        #captured.
        self.en_passant = False

        #Store a separate move set for captures, as pawns have separate
        #capture and move logic.
        self.naive_captures = set()
        self.actual_captures = set()

        #Bind can_capture_to to _can_capture_to (note the leading under-
        #score). This mild name mangling is necessary because the name
        #can_capture_to is bound by the call (above) to Piece's __init__.
        #If Pawn's method were not prefixed with an underscore, it would
        #then be overwritten and lost.
        self.can_capture_to = self._can_capture_to

    def _can_capture_to(self, space):
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
