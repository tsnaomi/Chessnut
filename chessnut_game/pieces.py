from abc import abstractmethod

# Module-level constants representing which player's turn it is.
White = True
Black = False


class Piece(object):
    """The piece base class.

    A chess piece knows where it is on the board, knows to which player it
    belongs, caches the spaces on the board to which it could move
    (regardless of the legality of that move), and is consulted by the game
    to cache the spaces on the board to which it can actually move.
    """
    def __init__(self, player=None, _file=None, rank=None, same_logic=True):
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
        if same_logic:
            self.can_capture_to = self.can_move_to
            self.in_naive_captures = self.in_naive_moves

        # Generate the initial naive_moves cache.
        self.generate_naive_cache()

    def can_move_to(self, _file, rank):
        """Determine whether this piece can move to the space in question.
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
        self.generate_naive_cache()

    @abstractmethod
    def generate_naive_cache(self):
        """Generate the naive moves cache.

        The Piece class is non-specific and has no move logic, so this method
        is empty. Pieces derived from this class must implement their own
        version based on their move logic. _generate_horizontal_moves and
        _generate_diagonal_moves are provided to assist with this task.
        """
        pass

    @abstractmethod
    def generate_actual_cache(self, game):
        """Generate the actual_moves_cache.

        The Piece class is non-specific and has no move logic, so this method
        is empty. Pieces derived from this class must implement their own
        version based on their move logic.
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
            _file, rank = self.file, self.rank
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
            _file, rank = self.file, self.rank
            for i in range(limit):
                _file += filemod
                rank += rankmod

                if _file > 7 or _file < 0 or rank > 7 or rank < 0:
                    break

                yield (_file, rank)


class Pawn(Piece):
    """A pawn.

    In addition to the functions of normal pieces, pawns track whether they
    are eligible to be en-passant captured, track separately which spaces
    they can move to and which they can capture to (since their capture
    and move logic are different), and track whether they have moved, to
    determine whether they're allowed to move two spaces.
    """
    def __init__(self, player=None, _file=None, rank=None):
        # Store a separate move set for captures, as pawns have separate
        # capture and move logic. Because generate_naive_cache is called
        # in the super call below, these attributes must be instantiated
        # first.
        self.naive_captures = set()
        self.actual_captures = set()

        # Track whether or not this pawn is eligible to be en-passant
        # captured.
        self.en_passant = False

        # Track whether this pawn has moved, so we can figure out whether a
        # move two spaces forward is legal.
        self.has_moved = False

        super(Pawn, self).__init__(player, _file, rank, same_logic=False)

    def move_to(self, _file, rank):
        """In addition to moving the Pawn, set has_moved to True."""
        super(Pawn, self).move_to(_file, rank)
        self.has_moved = True

    def can_capture_to(self, _file, rank):
        """Determine whether this Pawn can capture to the space in question.

        Pawns are a special case piece: their move logic and capture logic
        differ. They must therefore have separate behavior for can_capture_to
        (in other pieces, this method is an alias for can_move_to).
        """
        return True if (_file, rank) in self.actual_captures else False

    def in_naive_captures(self, _file, rank):
        """Determine membership in the naive_captures cache.

        Pawns are a special case piece: their move logic and capture logic
        differ. They must therefore have separate behavior for
        in_naive_captures (in other pieces, this method is an alias for
        in_naive_moves).
        """
        return True if (_file, rank) in self.naive_captures else False

    def generate_naive_cache(self):
        """Generate the Pawn's naive caches.

        The pawn in unique in that it must generate two caches, rather than
        one, but the situations in which each cache must be regenerated are
        identical.
        """
        self.naive_moves.clear()
        self.naive_moves.update(
            self._generate_horizontal_moves(
                backward=False,
                sideways=False,
                limit=1 if self.has_moved else 2
            )
        )

        self.naive_captures.clear()
        self.naive_captures.update(
            self._generate_diagonal_moves(backward=False, limit=1)
        )

    def generate_actual_cache(self, game):
        """Generate the Pawn's actual caches.

        The pawn in unique in that it must generate two caches, rather than
        one, but the situations in which each cache must be regenerated are
        identical.
        """
        self.actual_moves.clear()
        for _file, rank in self.naive_moves:
            if not (
                game.pieces_by_file[_file] &
                game.pieces_by_rank[rank]
            ):
                self.actual_moves.add((_file, rank))

        self.actual_captures.clear()
        for _file, rank in self.naive_captures:
            if (
                game.pieces_by_file[_file] &
                game.pieces_by_rank[rank] &
                game.pieces_by_player[not self.player]
            ):
                self.actual_captures.add((_file, rank))

            else:
                try:
                    en_passant_piece = (
                        game.pieces_by_file[_file] &
                        game.pieces_by_rank[self.rank] &
                        game.pieces_by_player[not self.player]
                    ).pop()

                    if en_passant_piece.en_passant:
                        self.actual_captures.add((_file, rank))

                except (KeyError, AttributeError):
                    pass


class Rook(Piece):
    """A rook.

    In addition to the functions of usual pieces, rooks track whether
    they have moved (so that the legality of castling can be determined).
    """
    def __init__(self, *args, **kwargs):
        super(Rook, self).__init__(*args, **kwargs)
        self.has_moved = False

    def generate_naive_cache(self):
        """Generate the Rook's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves())

    def move_to(self, _file, rank):
        """Move this rook to the file and rank provided, regenerate its
        naive_moves cache, and set its has_moved to True.
        """
        super(Rook, self).move_to(_file, rank)
        self.has_moved = True


class Knight(Piece):
    """A knight."""
    def generate_naive_cache(self):
        """Generate the Knight's naive_moves cache."""
        self.naive_moves.clear()
        for filemod, rankmod in (
            (f, r) for f in (-2, -1, 1, 2) for r in (-2, -1, 1, 2)
            if abs(f) != abs(r)
        ):
            if 0 <= self.file + filemod <= 7 and \
                    0 <= self.rank + rankmod <= 7:
                self.naive_moves.add(
                    (self.file + filemod, self.rank + rankmod)
                )

    def generate_actual_cache(self, game):
        """Generate the Knight's actual_moves cache."""
        self.actual_moves.clear()
        for _file, rank in self.naive_moves:
            if not (
                game.pieces_by_file[_file] &
                game.pieces_by_rank[rank] &
                game.pieces_by_player[self.player]
            ):
                self.actual_moves.add((_file, rank))


class Bishop(Piece):
    """A bishop."""
    def generate_naive_cache(self):
        """Generate the Bishop's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_diagonal_moves())


class Queen(Piece):
    """A queen."""
    def generate_naive_cache(self):
        """Generate the Queen's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves())
        self.naive_moves.update(self._generate_diagonal_moves())


class King(Piece):
    """A king.

    In addition to the functions of normal pieces, the king tracks whether
    it has moved (so that the legality of castling can be determined).
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

    def generate_naive_cache(self):
        """Generate the King's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves(limit=1))
        self.naive_moves.update(self._generate_diagonal_moves(limit=1))
