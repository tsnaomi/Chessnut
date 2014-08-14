"""Decorators for use in wrapping test methods."""

from chessnut_game import Black, White
from chessnut_game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


def all_spaces(test_method):
    """Run a test method from every space on the board.

    For use on test methods which take 'rank' and '_file' as keyword arguments.
    """
    def wrapped_test_method(self, *args, **kwargs):
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            test_method(self, *args, _file=_file, rank=rank, **kwargs)

    return wrapped_test_method


def all_piece_types(test_method):
    """Run a test method with every type of piece.

    For use on test methods which take 'piece' as a keyword argument.
    """
    def wrapped_test_method(self, *args, **kwargs):
        for piece in (Pawn, Rook, Knight, Bishop, Queen, King):
            test_method(self, *args, piece=piece, **kwargs)

    return wrapped_test_method


def all_players(test_method):
    """Run a test method from the perspective of each player.

    For use on test methods which take 'player' as a keyword argument.
    """
    def wrapped_test_method(self, *args, **kwargs):
        for player in (Black, White):
            test_method(self, *args, player=player, **kwargs)

    return wrapped_test_method
