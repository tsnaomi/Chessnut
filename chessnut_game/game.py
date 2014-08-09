from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessnut_exceptions import BoardIndexError

# Module-level constants representing which player's turn it is.
White = True
Black = False


class ChessnutGame(object):
    """A game of chess."""
    def __init__(self, pgn=None):
        # Track whose turn it is.
        self.turn = White

        # Bucket the pieces on the board by several criteria.

        # Bucket by the owner of the piece.
        self.pieces_by_player = {
            White: set(),
            Black: set(),
        }

        # Bucket by the type of piece.
        self.pieces_by_type = {
            Pawn: set(),
            Rook: set(),
            Knight: set(),
            Bishop: set(),
            Queen: set(),
            King: set(),
        }

        # Bucket by rank and by file.
        self.pieces_by_rank = {
            0: set(),
            1: set(),
            2: set(),
            3: set(),
            4: set(),
            5: set(),
            6: set(),
            7: set(),
        }
        self.pieces_by_file = {
            0: set(),
            1: set(),
            2: set(),
            3: set(),
            4: set(),
            5: set(),
            6: set(),
            7: set(),
        }

        # Bucket pieces by the diagonal on which they lie.

        # Forward diagonals are from bottom left to top right, like a
        # forward slash '/'. Forward diagonals originate from the bottom
        # and/or left edges of the board.

        # Begin by adding buckets for the coordinate pairs that define
        # the forward diagonals.
        self.pieces_by_forward_diagonal = {
            (0, 7): set(),
            (0, 6): set(),
            (0, 5): set(),
            (0, 4): set(),
            (0, 3): set(),
            (0, 2): set(),
            (0, 1): set(),
            (0, 0): set(),
            (1, 0): set(),
            (2, 0): set(),
            (3, 0): set(),
            (4, 0): set(),
            (5, 0): set(),
            (6, 0): set(),
            (7, 0): set(),
        }
        # Next, add keys for every coordinate pair on the board, pointing
        # those coordinates back to the bucket representing the forward
        # diagonal they lie on.
        for _file, rank in self.pieces_by_forward_diagonal.keys():
            for difile, dirank in self._generate_forward_diagonal(_file, rank):
                self.pieces_by_forward_diagonal[(difile, dirank)] = \
                    self.pieces_by_forward_diagonal[(_file, rank)]

        # Backward diagonals are from bottom right to top left, like a
        # backslash '\'. Backward diagonals originate from the bottom
        # and/or right edges of the board.

        # Begin by adding buckets for the coordinate pairs that define
        # the backward diagonals.
        self.pieces_by_backward_diagonal = {
            (0, 0): set(),
            (1, 0): set(),
            (2, 0): set(),
            (3, 0): set(),
            (4, 0): set(),
            (5, 0): set(),
            (6, 0): set(),
            (7, 0): set(),
            (7, 1): set(),
            (7, 2): set(),
            (7, 3): set(),
            (7, 4): set(),
            (7, 5): set(),
            (7, 6): set(),
            (7, 7): set(),
        }
        # Next, add keys for every coordinate pair on the board, pointing
        # those coordinates back to the bucket representing the backward
        # diagonal they lie on.
        for _file, rank in self.pieces_by_backward_diagonal.keys():
            for difile, dirank in self._generate_backward_diagonal(_file, rank):
                self.pieces_by_backward_diagonal[(difile, dirank)] = \
                    self.pieces_by_backward_diagonal[(_file, rank)]

    def reconstruct_from_pgn():
        pass

    def move_piece(self, piece, _file, rank):
        """Move the given piece to the specified space."""
        old_file = piece.file
        old_rank = piece.rank
        self._soft_remove_piece(piece)
        piece.file = _file
        piece.rank = rank

        try:
            self._soft_place_piece(piece)
        except BoardIndexError:
            piece.file = old_file
            piece.rank = old_rank
            self._soft_place_piece(piece)
            raise

    def first_blocked_space_from(self, _file, rank, direction):
        """Find the first space from the space at (_file, rank) blocked by
        another piece in the given direction and return as (_file, rank).
        Returns (None, None) if no space is blocked.

        Directions start at 0 for up/North, and proceed clockwise through 7
        for diagonally up and left/Northwest.
        """
        if direction not in range(8):
            raise ValueError(
                "ChessnutGame.first_blocked_space_from got value not"
                " between 0 and 7, inclusive, for direction. Value received"
                " was %s." % direction
            )

        filemod = 0 if not direction % 4 else (1 if direction < 4 else -1)
        rankmod = 0 if not direction % 2 and direction % 4 else \
            (-1 if 2 < direction < 6 else 1)

        blocked_file = _file + filemod
        blocked_rank = rank + rankmod

        while 0 <= blocked_file <= 7 and 0 <= blocked_rank <= 7:
            if (
                self.pieces_by_file[blocked_file] &
                self.pieces_by_rank[blocked_rank]
            ):
                return (blocked_file, blocked_rank)

            blocked_file += filemod
            blocked_rank += rankmod

        return (None, None)

    def _set_actual_moves_cache(self, piece):
        """Set the actual_moves cache of the given piece."""
        piece.generate_actual_cache(self)

    def _initialize_board(self):
        """Initialize a game board."""
        pieces = [
            (Rook, 0)
            (Knight, 1),
            (Bishop, 2),
            (Queen, 3),
            (King, 4),
            (Bishop, 5),
            (Knight, 6),
            (Rook, 7),
        ]

        for player in [White, Black]:
            homerank = 0 if player is White else 7
            pawnrank = 1 if player is White else 6

            for _file in range(8):
                self._hard_place_piece(
                    Pawn(player=player, _file=_file, rank=pawnrank)
                )

            for piecetype, _file in pieces:
                self._hard_place_piece(
                    piecetype(player=player, _file=_file, rank=homerank)
                )

    def _soft_place_piece(self, piece):
        """Place a piece already existent (in piece and player caches) at the
        location specified by its current rank and file.
        """
        if not 0 <= piece.file <= 7 or not 0 <= piece.rank <= 7:
            raise BoardIndexError(
                "Attempting to place piece at board indices (%s, %s)." % (
                    piece.file,
                    piece.rank
                )
            )
        self.pieces_by_file[piece.file].add(piece)
        self.pieces_by_rank[piece.rank].add(piece)
        self.pieces_by_forward_diagonal[(piece.file, piece.rank)].add(piece)
        self.pieces_by_backward_diagonal[(piece.file, piece.rank)].add(piece)

    def _hard_place_piece(self, piece):
        """Add the given piece to all caches, placing it on the board."""
        self._soft_place_piece(piece)
        self.pieces_by_player[piece.player].add(piece)
        self.pieces_by_type[piece.__class__].add(piece)

    def _soft_remove_piece(self, piece):
        """Remove the given piece from its current location, leaving it in the
        player and piece caches.
        """
        if not 0 <= piece.file <= 7 or not 0 <= piece.rank <= 7:
            raise BoardIndexError(
                "Attempting to remove piece at board indices (%s, %s)." % (
                    piece.file,
                    piece.rank
                )
            )
        self.pieces_by_file[piece.file].remove(piece)
        self.pieces_by_rank[piece.rank].remove(piece)
        self.pieces_by_forward_diagonal[(piece.file, piece.rank)].remove(piece)
        self.pieces_by_backward_diagonal[(piece.file, piece.rank)].remove(piece)

    def _hard_remove_piece(self, piece):
        """Remove the given piece from all caches, removing it from the board.
        """
        self._soft_remove_piece(piece)
        self.pieces_by_player[piece.player].remove(piece)
        self.pieces_by_type[piece.__class__].remove(piece)

    def _coordinates_to_forward_diagonal(self, _file, rank):
        """Find out which forward diagonal the given space belongs to."""
        # Determine how many spaces along the diagonal we must travel down
        # and to the left before we butt up against the edge of the board,
        # then subtract that value from the file and rank given.
        return (_file - min(_file, rank), rank - min(_file, rank))

    def _coordinates_to_backward_diagonal(self, rank, _file):
        """Find out which backward diagonal the given space belongs to."""
        # Determine how many spaces along the diagonal we must travel down
        # and to the right before we butt up against the edge of the board,
        # then add this value from the file and subtract it to the rank given.
        return (_file + min(7 - _file, rank), rank - min(7 - _file, rank))

    def _generate_forward_diagonal(self, _file, rank):
        """Determine all the spaces in a forward diagonal containing the
        specified space.
        """
        _file, rank = self._coordinates_to_forward_diagonal(_file, rank)
        while 0 <= rank <= 7 and 0 <= _file <= 7:
            yield (_file, rank)
            _file += 1
            rank += 1

    def _generate_backward_diagonal(self, _file, rank):
        """Determine all the spaces in a backward diagonal containing
        the specified space.
        """
        _file, rank = self._coordinates_to_backward_diagonal(_file, rank)
        while 0 <= rank <= 7 and 0 <= _file <= 7:
            yield (_file, rank)
            _file -= 1
            rank += 1
