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
            'pawn': set(),
            'rook': set(),
            'knight': set(),
            'bishop': set(),
            'queen': set(),
            'king': set(),
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
        self.pieces_by_forward_diagonal = {
            'a8': set(),
            'a7': set(),
            'a6': set(),
            'a5': set(),
            'a4': set(),
            'a3': set(),
            'a2': set(),
            'a1': set(),
            'b1': set(),
            'c1': set(),
            'd1': set(),
            'e1': set(),
            'f1': set(),
            'g1': set(),
            'h1': set(),
        }

        #Backward diagonals are from bottom right to top left, like a
        #backslash '\'. Backward diagonals originate from the bottom
        #and/or right edges of the board.
        self.pieces_by_backward_diagonal = {
            'a1': set(),
            'b1': set(),
            'c1': set(),
            'd1': set(),
            'e1': set(),
            'f1': set(),
            'g1': set(),
            'h1': set(),
            'h2': set(),
            'h3': set(),
            'h4': set(),
            'h5': set(),
            'h6': set(),
            'h7': set(),
            'h8': set(),
        }

    def reconstruct_from_pgn():
        pass

    def _initialize_board(self):
        """Initialize a game board."""
        pieces = [
            (QueensideRook, 0)
            (Knight, 1),
            (Bishop, 2),
            (Queen, 3),
            (King, 4),
            (Bishop, 5),
            (Knight, 6),
            (KingsideRook, 7),
        ]

        piecenames = {
            QueensideRook: 'rook',
            KingsideRook: 'rook',
            Knight: 'knight',
            Bishop: 'bishop',
            Queen: 'queen',
            King: 'king',
        }

        for player in [White, Black]:
            homerank = 0 if player is White else 7
            pawnrank = 1 if player is White else 6

            for _file in range(8):
                pawn = Pawn(player=player, rank=pawnrank, _file=_file)
                self.pieces_by_player[player].add(pawn)
                self.pieces_by_type['pawn'].add(pawn)
                self.pieces_by_rank[pawnrank].add(pawn)
                self.pieces_by_file[_file].add(pawn)
                self.pieces_by_backward_diagonal[
                    self._san_to_backward_diagonal(pawn.rank, pawn.file)
                ].add(pawn)
                self.pieces_by_forward_diagonal[
                    self._san_to_forward_diagonal(pawn.rank, pawn.file)
                ].add(pawn)

            for piecetype, _file in pieces:
                piece = piecetype(player=player, rank=homerank, _file=_file)
                self.pieces_by_player[player].add(piece)
                self.pieces_by_type[piecenames[piecetype]].add(piece)
                self.pieces_by_rank[homerank].add(piece)
                self.pieces_by_file[_file].add(piece)
                self.pieces_by_backward_diagonal[
                    self._san_to_backward_diagonal(piece.rank, piece.file)
                ].add(pawn)
                self.pieces_by_forward_diagonal[
                    self._san_to_forward_diagonal(piece.rank, piece.file)
                ].add(pawn)

    def _san_to_forward_diagonal(self, rank, _file):
        """Find out which forward diagonal the space belongs to.
        Accomplish this by determining how many spaces along the diagonal
        we must travel down and to the left before we butt up against the
        edge of the board, then subtracting this value from the rank and
        file given.
        """
        #49 is the ordinal value of the character '1'
        rankdiff = ord(rank) - 49

        #97 is the ordinal value of the character 'a'
        filediff = ord(_file) - 97

        return ''.join([
            chr(ord(_file) - min(filediff, rankdiff)),
            chr(ord(rank) - min(filediff, rankdiff)),
        ])

    def _san_to_backward_diagonal(self, rank, _file):
        """Find out which backward diagonal the space belongs to.
        Accomplish this by determining how many spaces along the diagonal
        we must travel down and to the right before we butt up against
        the edge of the board, then subtracting this value from the file
        and adding it to the rank given.
        """
        #49 is the ordinal value of the character '1'
        rankdiff = ord(rank) - 49

        #104 is the ordinal value of the character 'h'
        filediff = 104 - ord(_file)

        return ''.join([
            chr(ord(_file) + min(filediff, rankdiff)),
            chr(ord(rank) - min(filediff, rankdiff)),
        ])
