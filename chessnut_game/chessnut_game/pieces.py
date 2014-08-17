from chessnut_game.constants import White
from chessnut_game.signals import SignalCollector


class Piece(object):
    """The piece base class.

    A chess piece knows where it is on the board, knows to which player it
    belongs, caches the spaces on the board to which it can move, and keeps
    track of a set of spaces it needs to watch in order to determine when
    its available moves have changed.
    """
    def __init__(self, player=White, _file=0, rank=0):
        """Initialize the attributes of this Piece."""
        # Keep track of whose piece this is and where it is on the board.
        self.player = player
        self.file = _file
        self.rank = rank

        # Store a set containing all the spaces on the board to which this
        # piece can move.
        self.moves = set()

        # In most pieces, capture logic and move logic are the same.
        self.captures = self.moves

        # A dictionary in which signals are accumulated as they're generated.
        self.signals = {}

        # Generate the initial moves.
        self.generate_moves()

    def generate_moves(self, game):
        """Generate the moves cache. Return a dict containing signals for the
        game to register.

        The Piece class is non-specific and has no move logic, so this method
        is empty. Pieces derived from this class must implement their own
        version based on their move logic. _generate_horizontal_moves and
        _generate_diagonal_moves are provided to assist with this task.
        """
        raise NotImplementedError(
            "%s has not implemented generate_moves." % self.__class__
        )

    def update_moves(self, game, code):
        """Update the moves cache. In addition to a game, take a code
        dictating piece-specific update logic. Return a dict containing
        signals for the game to register.

        The Piece class is non-specific and has no move logic, so this method
        is empty. Pieces derived from this class must implement their own
        version based on their move logic.
        """
        raise NotImplementedError(
            "%s has not implemented update_moves." % self.__class__
        )

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

    Pawns track separately which spaces they can move to and which they
    can capture to (since their capture and move logic are different),
    whether they are eligible to be en-passant captured, and whether they
    have moved (to determine whether they're allowed to move two spaces).
    """
    def __init__(self, player=White, _file=0, rank=0):
        super(Pawn, self).__init__(player, _file, rank)

        # Store a separate move set for captures, as pawns have separate
        # capture and move logic.
        self.captures = set()

        # Track whether this pawn is eligible to be en-passant captured.
        self.en_passant = False

        # Track whether this pawn has moved, so we can figure out whether a
        # move two spaces forward is legal.
        self.has_moved = False

    def generate_moves_cache(self, game):
        """Generate the Pawn's caches.

        The pawn must generate two caches, rather than one, but the caches
        are regenerated under the same conditions.
        """
        signals = {
            'piece_moved': {},
            'space_moved_from': {},
            'space_moved_to': {},
        }
        if not self.has_moved:
            signals['piece_moved'].setdefault(self, [])
            signals['piece_moved'][self].append((self.set_has_moved))

        self.moves.clear()
        for _file, rank in self._generate_horizontal_moves(
            backward=False,
            sideways=False,
            limit=1 if self.has_moved else 2
        ):
            if not (game.pieces_by_file[_file] & game.pieces_by_rank[rank]):
                self.moves.add((_file, rank))
            else:
                self.move_sentinels[(_file, rank)] = 0
                break

        self.captures.clear()
        for _file, rank in self._generate_diagonal_moves(
            backward=False,
            limit=1
        ):
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

        return signals

    def update_moves_cache(self, game, space):
        """Update the Pawn's caches."""
        pass

    def generate_actual_cache(self, game):
        """Generate the Pawn's actual caches.

        The pawn is unique in that it must generate two caches, rather than
        one, but the situations in which each cache must be regenerated are
        identical.
        """
        self.actual_moves.clear()
        for _file, rank in sorted(self.naive_moves, reverse=not self.player):
            if not (
                game.pieces_by_file[_file] &
                game.pieces_by_rank[rank]
            ):
                self.actual_moves.add((_file, rank))
            else:
                break

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

    def generate_moves(self):
        """Generate the Rook's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves())

        # The naive cache is only regenerated when this piece moves.
        self.has_moved = True

    def generate_actual_cache(self, game):
        """Generate the Rook's actual_moves cache."""
        self.actual_moves.clear()
        for direction in range(0, 8, 2):
            blocker = game.first_blocking_piece(
                self.file,
                self.rank,
                direction
            )

            if direction == 0:
                self.actual_moves.update(
                    (self.file, rank) for rank in range(
                        self.rank + 1,
                        8 if blocker is None else (
                            blocker.rank if blocker.player is self.player else
                            blocker.rank + 1
                        )
                    )
                )

            elif direction == 2:
                self.actual_moves.update(
                    (_file, self.rank) for _file in range(
                        self.file + 1,
                        8 if blocker is None else (
                            blocker.file if blocker.player is self.player else
                            blocker.file + 1
                        )
                    )
                )

            elif direction == 4:
                self.actual_moves.update(
                    (self.file, rank) for rank in range(
                        self.rank - 1,
                        -1 if blocker is None else (
                            blocker.rank if blocker.player is self.player else
                            blocker.rank - 1
                        ),
                        -1
                    )
                )

            elif direction == 6:
                self.actual_moves.update(
                    (_file, self.rank) for _file in range(
                        self.file - 1,
                        -1 if blocker is None else (
                            blocker.file if blocker.player is self.player else
                            blocker.file - 1
                        ),
                        -1
                    )
                )

    def move_to(self, _file, rank):
        """Move this rook to the file and rank provided, regenerate its
        naive_moves cache, and set its has_moved to True.
        """
        super(Rook, self).move_to(_file, rank)
        self.has_moved = True


class Knight(Piece):
    """A knight."""
    def generate_moves(self):
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
    def generate_moves(self):
        """Generate the Bishop's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_diagonal_moves())


class Queen(Piece):
    """A queen."""
    def generate_moves(self):
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

    def generate_moves(self):
        """Generate the King's naive_moves cache."""
        self.naive_moves.clear()
        self.naive_moves.update(self._generate_horizontal_moves(limit=1))
        self.naive_moves.update(self._generate_diagonal_moves(limit=1))

        # The naive cache is only regenerated when this piece moves.
        self.has_moved = True
