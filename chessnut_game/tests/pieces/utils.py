"""Helper functions for Piece tests."""


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
