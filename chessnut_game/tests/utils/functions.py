"""Helper functions for use in tests."""

from .constants import direction_modifiers
from chessnut_game import White
from chessnut_game.pieces import Pawn
from chessnut_game.exceptions import BoardIndexError


def surround_space(game, _file, rank, radius, piece=Pawn, player=White):
    """Create a circle of pieces around the the given file and rank at the
    given radius. Return a list of length 8 containing at each index a piece
    placed, or None if that piece would be off-board, in clockwise order.

    By default, the pieces created are White Pawns.
    """
    placed = []
    for filemod, rankmod in direction_modifiers:
        pc = piece(player, _file + radius * filemod, rank + radius * rankmod)
        try:
            game._hard_place_piece(pc)
            placed.append(pc)

        except BoardIndexError:
            placed.append(None)

    return placed


def circle_space(game, _file, rank, radius, piece=Pawn, player=White):
    """Create a single piece that circles the given file and rank at the
    given radius. Yield the piece as it circles, or None if it would go
    off-board.

    By default, the piece is a White Pawn.
    """
    pc = piece(player, _file, rank)
    game._hard_place_piece(pc)

    for filemod, rankmod in direction_modifiers:
        try:
            game._soft_remove_piece(pc)
        except BoardIndexError:
            pass

        pc.file = _file + radius * filemod
        pc.rank = rank + radius * rankmod

        try:
            game._soft_place_piece(pc)
            yield pc

        except BoardIndexError:
            yield


def block_non_cache_spaces(game, piece=None, blocker=Pawn, player=White):
    """Block all spaces in 'game' not in 'piece's naive_moves cache.

    Blocking pieces are White Pawns by default.
    """
    for _file, rank in ((f, r) for f in range(8) for r in range(8)):
        if (_file, rank) not in piece.naive_moves:
            game._hard_place_piece(Pawn(player, _file, rank))

    return game


def generate_diagonal_spaces(_file, rank):
    """Given a file and a rank, this function generates all of the spaces
    in the two diagonals that intersect at that space, minus the space
    itself.
    """
    for file_mod, rank_mod in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        new_file = _file + file_mod
        new_rank = rank + rank_mod
        while 0 <= new_file <= 7 and 0 <= new_rank <= 7:
            yield (new_file, new_rank)
            new_file += file_mod
            new_rank += rank_mod
