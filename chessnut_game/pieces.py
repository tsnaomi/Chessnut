# Module-level constants representing which player's turn it is.
White = True
Black = False


class Piece(object):
    """The base class. A chess piece knows where it is on the board, caches
    the spaces on the board to which it could move (regardless of the
    legality of that move), acts as a container for the spaces on the
    board to which it can actually move (set by the game object),
    and knows to which player it belongs.
    """
    def __init__(self, player=None, _file=None, rank=None):
        """Initialize the attributes of this Piece."""
        # Keep track of whose piece this is and where it is on the board.
        self.player = player
        self.file = _file
        self.rank = rank

        # Store a set containing all the spaces on the board to which this
        # piece could move - IF this piece were the only piece on the board.
        # This much, the piece can calculate on its own, because it knows
        # its own move logic.
        self.naive_moves = set()

        # Store a set containing all of the spaces on the board to which
        # this piece can ACTUALLY move, given the state of the board. This
        # attribute is set by the game object, as the piece does not know
        # about the positions of other pieces on its own.
        self.actual_moves = set()

        # Bind can_capture_to to can_move_to and in_naive_captures to
        # in_naive_moves. In most pieces, capture logic and move logic are
        # the same, so the same methods should be called to determine both.
        self.can_capture_to = self.can_move_to
        self.in_naive_captures = self.in_naive_moves

        # Generate the initial naive_moves cache.
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
        if not isinstance(value, int):
            raise TypeError(
                "Attempting to set file to non-int value.")
        elif value < 0 or value > 7:
            raise ValueError(
                "Attempting to set file to value not in range 0-7.")
        self._file = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "Attempting to set rank to non-int value.")
        elif value < 0 or value > 7:
            raise ValueError(
                "Attempting to set rank to value not in range 0-7.")
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
        forward = 1 if self.player is White else -1
        move_modifiers = [(1 * forward, 0)]
        if backward:
            move_modifiers.append((-1 * forward, 0))
        if sideways:
            move_modifiers.extend([(0, 1), (0, -1)])

        for rankmod, filemod in move_modifiers:
            _file = self.file
            rank = self.rank
            for i in range(limit):
                _file += filemod
                rank += rankmod

                if _file > 7 or _file < 0 or rank > 7 or rank < 0:
                    break

                yield (_file, rank)

    def _generate_diagonal_moves(self, backward=True, limit=7):
        """Calculates the spaces to which this piece can move diagonally.
        Can be limited by disallowing movement backwards along diagonals
        and by limiting the number of spaces that are allowed to be moved.
        """
        forward = 1 if self.player is White else -1
        move_modifiers = [(1 * forward, 1), (1 * forward, -1)]
        if backward:
            move_modifiers.extend([(-1 * forward, 1), (-1 * forward, -1)])

        for rankmod, filemod in move_modifiers:
            _file = self.file
            rank = self.rank
            for i in range(limit):
                _file += filemod
                rank += rankmod

                if _file > 7 or _file < 0 or rank > 7 or rank < 0:
                    break

                yield (_file, rank)


class Pawn(Piece):
    """A pawn. In addition to the functions of normal pieces, pawns track
    whether they are eligible to be en-passant captured. Pawns also track
    separately which spaces they can move to and which they can capture
    to (since their capture and move logic are different).
    """
    def __init__(self, player=None, _file=None, rank=None):
        # Store a separate move set for captures, as pawns have separate
        # capture and move logic. Because _generate_naive_cache is called
        # in the super call below, these attributes must be instantiated
        # first.
        self.naive_captures = set()
        self.actual_captures = set()

        super(Pawn, self).__init__(player, _file, rank)

        # Track whether or not this pawn is eligible to be en-passant
        # captured.
        self.en_passant = False

        # Bind can_capture_to to _can_capture_to and in_naive_captures to
        # _in_naive_captures (note the leading underscores). This mild name
        # mangling is necessary because the names are bound by the call
        # (above) to Piece's __init__. If Pawn's methods were not prefixed
        # with an underscore, they would be overwritten and lost.
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

    def _generate_naive_cache(self):
        """Generate the Pawn's naive caches. The pawn in unique in that it
        must generate two caches, rather than one, but the situations in
        which each cache must be regenerated are identical.
        """
        self.naive_moves.clear()
        if self.player is White and self.rank == 1 or\
                self.player is Black and self.rank == 6:
            self.naive_moves.update(
                self._generate_horizontal_moves(
                    backward=False, sideways=False, limit=2
                )
            )
        else:
            self.naive_moves.update(
                self._generate_horizontal_moves(
                    backward=False, sideways=False, limit=1
                )
            )

        self.naive_captures.clear()
        self.naive_captures.update(
            self._generate_diagonal_moves(
                backward=False, limit=1
            )
        )


class Rook(Piece):
    """A rook. In addition to the functions of usual pieces, rooks track
    whether they have moved (so that the legality of castling can be
    determined)."""
    def __init__(self, *args, **kwargs):
        super(Rook, self).__init__(*args, **kwargs)
        self.has_moved = False

    def _generate_naive_cache(self):
        """Generate the Rook's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves())

    def move_to(self, _file, rank):
        """Move this rook to the file and rank provided, regenerate its
        naive_moves cache, and set its has_moved to True.
        """
        super(Rook, self).move_to(_file, rank)
        self.has_moved = True


# class QueensideRook(Rook):
#     """A queenside rook. In addition to the functions of a normal rook,
#     the queenside rook tracks whether it has moved (so that the legality
#     of queenside castling can be determined).
#     """
#     def __init__(self, player=None, _file=None, rank=None):
#         super(QueensideRook, self).__init__(player, _file, rank)

#         # Track whether or not this rook has moved (so that the legality
#         # of queenside castling can be determined).
#         self.has_moved = False

#     def move_to(self, _file, rank):
#         """Move this rook to the file and rank provided, regenerate its
#         naive_moves cache, and set its has_moved to True.
#         """
#         super(QueensideRook, self).move_to(_file, rank)
#         self.has_moved = True


# class KingsideRook(Rook):
#     """A kingside rook. In addition to the functions of a normal rook,
#     the kingside rook tracks whether it has moved (so that the legality
#     of kingside castling can be determined).
#     """
#     def __init__(self, player=None, _file=None, rank=None):
#         super(KingsideRook, self).__init__(player, _file, rank)

#         # Track whether or not this rook has moved (so that the legality
#         # of kingside castling can be determined).
#         self.has_moved = False

#     def move_to(self, _file, rank):
#         """Move this rook to the file and rank provided, regenerate its
#         naive_moves cache, and set its has_moved to True.
#         """
#         super(KingsideRook, self).move_to(_file, rank)
#         self.has_moved = True


class Knight(Piece):
    """A knight."""
    def _generate_naive_cache(self):
        """Generate the Knight's naive_moves cache."""
        self.naive_moves.clear()
        for filemod, rankmod in (
            (f, r) for f in (-2, -1, 1, 2) for r in (-2, -1, 1, 2)
            if abs(f) != abs(r)
        ):
            if 0 <= self._file + filemod <= 7 and \
                    0 <= self._rank + rankmod <= 7:
                self.naive_moves.add(
                    (self._file + filemod, self.rank + rankmod)
                )


class Bishop(Piece):
    """A bishop."""
    def _generate_naive_cache(self):
        """Generate the Bishop's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_diagonal_moves())


class Queen(Piece):
    """A queen."""
    def _generate_naive_cache(self):
        """Generate the Queen's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves())
        self.naive_moves.update(self._generate_diagonal_moves())


class King(Piece):
    """A king. In addition to the functions of normal pieces, the king
    tracks whether it has moved (so that the legality of castling can be
    determined).
    """
    def __init__(self, *args, **kwargs):
        super(King, self).__init__(*args, **kwargs)

        # Track whether or not this king has moved (so that the legality
        # of castling can be determined).
        self.has_moved = False

    def move_to(self, _file, rank):
        """Move this King to the file and rank provided, regenerate its
        naive_moves cache, and set its has_moved to True.
        """
        super(King, self).move_to(_file, rank)
        self.has_moved = True

    def _generate_naive_cache(self):
        """Generate the King's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves(limit=1))
        self.naive_moves.update(self._generate_diagonal_moves(limit=1))
