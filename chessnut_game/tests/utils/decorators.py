"""Decorators for use in wrapping test methods."""

from chessnut_game import Black, White
from chessnut_game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


def all_spaces(test_method, piece=None):
    """Run a test method from every space on the board.

    Runs its wrapped test method 64 times, once for each space on the board.
    If 'piece' is none, then 'rank' and '_file' are passed as keyword arguments
    to the wrapped test method. If 'piece' is not none, then the rank and file
    are set on the piece, and the piece is passed as keyword argument 'piece'
    to the test method.
    """
    if piece is None:
        def wrapped_test_method(self, *args, **kwargs):
            for _file, rank in ((f, r) for f in range(8) for r in range(8)):
                test_method(self, *args, _file=_file, rank=rank, **kwargs)

    else:
        def wrapped_test_method(self, *args, **kwargs):
            for _file, rank in ((f, r) for f in range(8) for r in range(8)):
                piece.file = _file
                piece.rank = rank
                test_method(self, *args, piece=piece, **kwargs)

    return wrapped_test_method


def all_players(test_method, piece=None):
    """Run a test method from the perspective of each player.

    Runs its wrapped test method twice, once for each player. If 'piece' is
    none, then 'player' is passed as a keyword argument to the wrapped test
    method. If 'piece' is not none, then the rank and file are set on the
    piece, and the piece is passed as keyword argument 'piece' to the test
    method.
    """
    if piece is None:
        def wrapped_test_method(self, *args, **kwargs):
            for player in (Black, White):
                test_method(self, *args, player=player, **kwargs)

    else:
        def wrapped_test_method(self, *args, **kwargs):
            for player in (Black, White):
                piece.player = player
                test_method(self, *args, piece=piece, **kwargs)

    return wrapped_test_method


def all_piece_types(test_method):
    """Run a test method with every type of piece.

    Runs its wrapped method 7 times, once for each type of piece. Pieces are
    passed to the test method as a 'piece' keyword argument.
    """
    def wrapped_test_method(self, *args, **kwargs):
        for piece in (Pawn, Rook, Knight, Bishop, Queen, King):
            test_method(self, *args, piece=piece, **kwargs)

    return wrapped_test_method
