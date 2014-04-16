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
            '1': set(),
            '2': set(),
            '3': set(),
            '4': set(),
            '5': set(),
            '6': set(),
            '7': set(),
            '8': set(),
        }
        self.pieces_by_file = {
            'a': set(),
            'b': set(),
            'c': set(),
            'd': set(),
            'e': set(),
            'f': set(),
            'g': set(),
            'h': set(),
        }

        #Bucket pieces by the diagonal on which they lie. Diagonals
        #originate from the the left and/or bottom edges of the board.
        #For example, a8 is the forward diagonal starting from space a8
        #and extending up and to the right of a8 - where there are no spaces,
        #meaning that this diagonal contains only one space. a8 is also
        #the backward diagonal starting at space a8 and extending down
        #and to the left of a8 - all the way across the board to space h1.

        #Forward diagonal are from bottom left to top right, like a
        #forward slash '/'
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

        #Backward diagonal are from top left to bottom right, like a
        #backslash '\'
        self.pieces_by_backward_diagonal = {
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

    def reconstruct_from_pgn():
        pass

    def _initialize_board(self):
        """Initialize a game board."""
        for player in [White, Black]:
            homerank = '1' if player is White else '8'
            pawnrank = '2' if player is White else '7'

            for _file in 'abcdefgh':
                pawn = Pawn(player=player, rank=pawnrank, _file=_file)
                self.pieces_by_player[player].add(pawn)
                self.pieces_by_type['pawn'].add(pawn)
                self.pieces_by_rank[pawnrank].add(pawn)
                self.pieces_by_file[_file].add(pawn)

            rook = QueensideRook()

    def _san_to_forward_diagonal(self, san):
        pass

    def _san_to_backward_diagonal(self, san):
        pass
