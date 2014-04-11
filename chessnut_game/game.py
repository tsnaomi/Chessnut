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
        self.pieces_by_player = {}
        self.pieces_by_type = {}
        self.pieces_by_rank = {}
        self.pieces_by_file = {}

    def reconstruct_from_pgn():
        pass
