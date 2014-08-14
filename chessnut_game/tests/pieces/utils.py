"""Helper functions and constants for Piece tests."""

# Some tests become too complex if every space on the board is tested.
# Test only a collection of interesting spaces, instead.
test_spaces = (
    # Test the spaces in the corners of the board.
    (0, 0),
    (0, 7),
    (7, 0),
    (7, 7),
    # Test a space along each side of the board.
    (0, 4),
    (4, 0),
    (7, 4),
    (4, 7),
    # Test a space in the middle of the board.
    (4, 4),
)


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
