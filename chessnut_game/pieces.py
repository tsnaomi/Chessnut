class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move (regardless of the
    legality of that move), acts as a container for the spaces on the
    board to which it can actually move (set by the game object),
    and knows to which player it belongs.
    """
    def __init__(self, player=None, _file=None, rank=None):
        """Initialize the attributes of this Piece."""
        #Keep track of whose piece this is and where it is on the board.
        self.player = player
        self.file = _file
        self.rank = rank

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

        #Bind can_capture_to to can_move_to and in_naive_captures to
        #in_naive_moves. In most pieces, capture logic and move logic are
        #the same, so the same methods should be called to determine both.
        self.can_capture_to = self.can_move_to
        self.in_naive_captures = self.in_naive_moves

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
            raise TypeError(
                "Attempting to set file to non-string value.")
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
            raise TypeError(
                "Attempting to set rank to non-string value.")
        elif len(value) != 1 or value not in '12345678':
            raise ValueError(
                "Attempting to set rank to value not in range 1-8.")
        self._rank = value

    def can_move_to(self, _file, rank):
        """Refer to the actual_moves cache to determine whether this piece
        can reach the space in question.
        """
        return True if (_file, rank) in self.actual_moves else False

    def in_naive_moves(self, _file, rank):
        """Determine membership in the naive_moves cache."""
        return True if (_file, rank) in self.naive_moves else False

    def move_to(self, _file, rank):
        """Move this Piece to the file and rank provided, then regenerate
        the naive_moves cache.
        """
        self.file = _file
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
            _file = ord(self._file)
            rank = ord(self.rank)
            for i in range(limit):
                _file += filemod
                rank += rankmod

                #97 is the ordinal value of 'a'
                #104 is the ordinal value of 'h'
                #49 is the ordinal value of '1'
                #56 is the ordinal value of '8'
                if _file > 104 or _file < 97 or rank > 56 or rank < 49:
                    break

                yield (chr(_file), chr(rank))

    def _generate_diagonal_moves(self, backward=True, limit=7):
        """Calculates the spaces to which this piece can move diagonally.
        Can be limited by disallowing movement backwards along diagonals
        and by limiting the number of spaces that are allowed to be moved.
        """
        move_modifiers = [(1, 1), (1, -1)]
        if backward:
            move_modifiers.extend([(-1, 1), (-1, -1)])

        for rankmod, filemod in move_modifiers:
            _file = ord(self._file)
            rank = ord(self.rank)
            for i in range(limit):
                _file += filemod
                rank += rankmod

                #97 is the ordinal value of 'a'
                #104 is the ordinal value of 'h'
                #49 is the ordinal value of '1'
                #56 is the ordinal value of '8'
                if _file > 104 or _file < 97 or rank > 56 or rank < 49:
                    break

                yield (chr(_file), chr(rank))


class Pawn(Piece):
    """A pawn. In addition to the functions of normal pieces, pawns track
    whether they are eligible to be en-passant captured. Pawns also track
    separately which spaces they can move to and which they can capture
    to (since their capture and move logic are different).
    """
    def __init__(self, player=None, _file=None, rank=None):
        super(Pawn, self).__init__(player, _file, rank)

        #Track whether or not this pawn is eligible to be en-passant
        #captured.
        self.en_passant = False

        #Store a separate move set for captures, as pawns have separate
        #capture and move logic.
        self.naive_captures = set()
        self.actual_captures = set()

        #Bind can_capture_to to _can_capture_to and in_naive_captures to
        #_in_naive_captures (note the leading underscores). This mild name
        #mangling is necessary because the names are bound by the call
        #(above) to Piece's __init__. If Pawn's methods were not prefixed
        #with an underscore, they would be overwritten and lost.
        self.can_capture_to = self._can_capture_to
        self.in_naive_captures = self._in_naive_captures

    def _can_capture_to(self, _file, rank):
        """Pawns are a special case piece: their move logic and capture logic
        differ. They must therefore have separate behavior for can_capture_to
        (in other pieces, this function is an alias for can_move_to).
        """
        return True if (_file, rank) in self.actual_captures else False

    def _in_naive_captures(self, _file, rank):
        """Pawns are a special case piece: their move logic and capture logic
        differ. They must therefore have separate behavior for
        in_naive_captures (in other pieces, this function is an alias for
        in_naive_moves).
        """
        return True if (_file, rank) in self.naive_captures else False


class Rook(Piece):
    """A rook."""
    pass


class QueensideRook(Rook):
    """A queenside rook. In addition to the functions of a normal rook,
    the queenside rook tracks whether it has moved (so that the legality
    of queenside castling can be determined).
    """
    def __init__(self, player=None, _file=None, rank=None):
        super(QueensideRook, self).__init__(player, _file, rank)

        #Track whether or not this rook has moved (so that the legality
        #of queenside castling can be determined).
        self.has_moved = False


class KingsideRook(Rook):
    """A kingside rook. In addition to the functions of a normal rook,
    the kingside rook tracks whether it has moved (so that the legality
    of kingside castling can be determined).
    """
    def __init__(self, player=None, _file=None, rank=None):
        super(KingsideRook, self).__init__(player, _file, rank)

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
    def __init__(self, player=None, _file=None, rank=None):
        super(King, self).__init__(player, _file, rank)

        #Track whether or not this king has moved (so that the legality
        #of castling can be determined).
        self.has_moved = False
