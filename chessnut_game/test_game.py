import unittest
from game import ChessnutGame
from pieces import Pawn, Rook, Knight, Bishop, Queen, King


def build_forward_diagonal(_file, rank):
    """Determine all the spaces in a forward diagonal beginning at
    the specified cell.
    """
    while 0 <= rank <= 7 and 0 <= _file <= 7:
        yield (_file, rank)
        _file += 1
        rank += 1


def build_backward_diagonal(_file, rank):
    """Determine all the spaces in a backward diagonal beginning at
    the specified cell.
    """
    while 0 <= rank <= 7 and 0 <= _file <= 7:
        yield (_file, rank)
        _file -= 1
        rank += 1


class TestCoordinatesToDiagonals(unittest.TestCase):
    """Test the _coordinates_to_forward_diagonal and
    _coordinates_to_backward_diagonal methods.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def test_coordinates_to_forward_diagonal(self):
        """Assert that all spaces are assigned to their correct forward
        diagonal.
        """
        diagonals = [
            (0, 7),
            (0, 6),
            (0, 5),
            (0, 4),
            (0, 3),
            (0, 2),
            (0, 1),
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
        ]

        for _file, rank in diagonals:
            for difile, dirank in build_forward_diagonal(_file, rank):
                self.assertEqual(
                    (_file, rank),
                    self.c._coordinates_to_forward_diagonal(difile, dirank)
                )

    def test_coordinates_to_backward_diagonal(self):
        """Assert that all spaces are assigned to their correct backward
        diagonal.
        """
        diagonals = [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (7, 1),
            (7, 2),
            (7, 3),
            (7, 4),
            (7, 5),
            (7, 6),
            (7, 7),
        ]

        for _file, rank in diagonals:
            for difile, dirank in build_backward_diagonal(_file, rank):
                self.assertEqual(
                    (_file, rank),
                    self.c._coordinates_to_backward_diagonal(difile, dirank)
                )


class TestGenerateDiagonals(unittest.TestCase):
    """Test the _generate_forward_diagonals and _generate_backward_diagonals
    methods.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def test_generate_forward_diagonal(self):
        """Test the _generate_forward_diagonal method."""

    def test_generate_backward_diagonal(self):
        """Test the _generate_backward_diagonal method."""


class TestFirstBlockedMoveFrom(unittest.TestCase):
    """Test the first_blocked_move_from method of the game class."""
    def setUp(self):
        self.c = ChessnutGame()
        self.circling_pawns = []

    def tearDown(self):
        for pawn in self.circling_pawns:
            self.c._hard_remove_piece(pawn)

        self.circling_pawns = []

    def surround_piece(_file, rank, radius):
        """Create a circle of Pawns around the the given file and rank.
        Return a list of spaces at which they are placed, in clockwise order.
        """

    def circle_piece(_file, rank, radius):
        """Create a single Pawn that circles the given file and rank.
        Yield the coordinates of the Pawn as it circles.
        """

    def test_empty_board(self):
        """Test an empty board."""

    def test_all_pieces(self):
        """Assert that each type of piece in each color can block spaces."""

    def test_all_directions_surrounded(self):
        """Test all directions when surrounded by pawns."""

    def test_all_directions_circling_piece(self):
        """Test all directions as one Pawn circles."""

    def test_all_directions_layered(self):
        """Test two layers of blocking pieces."""

    def test_all_directions_staggered(self):
        """Test two staggered circles of pieces."""


if __name__ == '__main__':
    unittest.main()
