from pieces import Pawn, Rook, QueensideRook, KingsideRook, \
    Knight, Bishop, Queen, King

#Module-level constants representing which player's turn it is.
White = True
Black = False


class ChessnutGame(object):
    """A game of chess.
    """
    def __init__(self, pgn=None):
        #Track whose turn it is.
        self.turn = White

        #Bucket the pieces on the board by several criteria.

        #Bucket by the owner of the piece.
        self.pieces_by_player = {
            White: set(),
            Black: set(),
        }

        #Bucket by the type of piece.
        self.pieces_by_type = {
            Pawn: set(),
            Rook: set(),
            Knight: set(),
            Bishop: set(),
            Queen: set(),
            King: set(),
        }

        #Bucket by rank and by file.
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

        #Bucket pieces by the diagonal on which they lie.

        #Forward diagonals are from bottom left to top right, like a
        #forward slash '/'. Forward diagonals originate from the bottom
        #and/or left edges of the board.

        #Begin by adding buckets for the coordinate pairs that define
        #the forward diagonals.
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
        #Next, add keys for every coordinate pair on the board, pointing
        #those coordinates back to the bucket representing the forward
        #diagonal they lie on.
        for _file, rank in self.pieces_by_forward_diagonal.keys():
            for difile, dirank in self._generate_forward_diagonal(_file, rank):
                self.pieces_by_forward_diagonal[(difile, dirank)] = \
                    self.pieces_by_forward_diagonal[(_file, rank)]

        #Backward diagonals are from bottom right to top left, like a
        #backslash '\'. Backward diagonals originate from the bottom
        #and/or right edges of the board.

        #Begin by adding buckets for the coordinate pairs that define
        #the backward diagonals.
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
        #Next, add keys for every coordinate pair on the board, pointing
        #those coordinates back to the bucket representing the backward
        #diagonal they lie on.
        for _file, rank in self.pieces_by_backward_diagonal.keys():
            for difile, dirank in self._generate_forward_diagonal(_file, rank):
                self.pieces_by_forward_diagonal[(difile, dirank)] = \
                    self.pieces_by_forward_diagonal[(_file, rank)]

    def reconstruct_from_pgn():
        pass

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
                pawn = Pawn(player=player, _file=_file, rank=pawnrank)
                self.pieces_by_player[player].add(pawn)
                self.pieces_by_type[Pawn].add(pawn)
                self.pieces_by_rank[pawnrank].add(pawn)
                self.pieces_by_file[_file].add(pawn)
                self.pieces_by_forward_diagonal[
                    (pawn.file, pawn.rank)].add(pawn)
                self.pieces_by_backward_diagonal[
                    (pawn.file, pawn.rank)].add(pawn)

            for piecetype, _file in pieces:
                piece = piecetype(player=player, _file=_file, rank=homerank)
                self.pieces_by_player[player].add(piece)
                self.pieces_by_type[piecetype].add(piece)
                self.pieces_by_rank[homerank].add(piece)
                self.pieces_by_file[_file].add(piece)
                self.pieces_by_forward_diagonal[
                    (piece.file, piece.rank)].add(pawn)
                self.pieces_by_backward_diagonal[
                    (piece.file, piece.rank)].add(pawn)

    def _coordinates_to_forward_diagonal(self, _file, rank):
        """Find out which forward diagonal the given space belongs to."""
        #Determine how many spaces along the diagonal we must travel down
        #and to the left before we butt up against the edge of the board,
        #then subtract that value from the file and rank given.
        return (_file - min(_file, rank), rank - min(_file, rank))

    def _coordinates_to_backward_diagonal(self, rank, _file):
        """Find out which backward diagonal the given space belongs to."""
        #Determine how many spaces along the diagonal we must travel down
        #and to the right before we butt up against the edge of the board,
        #then add this value from the file and subtract it to the rank given.
        return (_file + min(_file, rank), rank - min(_file, rank))

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
