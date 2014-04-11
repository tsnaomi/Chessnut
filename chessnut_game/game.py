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
        self.pieces_by_player = {
            White: set(),
            Black: set(),
        }
        self.pieces_by_type = {
            'pawn': set(),
            'rook': set(),
            'knight': set(),
            'bishop': set(),
            'queen': set(),
            'king': set(),
        }
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
