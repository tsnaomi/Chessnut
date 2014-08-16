"""Constants for use in tests."""

# Modifiers for movement in directions 0 through 7, in order.
direction_modifiers = (
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1)
)

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
