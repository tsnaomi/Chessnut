import unittest
from game import ChessnutGame, Black, White
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessnut_exceptions import BoardIndexError


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


class TestFirstBlockedSpaceFrom(unittest.TestCase):
    """Test the first_blocked_move_from method of the game class."""
    mods = (
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
        (-1, 0),
        (-1, 1)
    )

    c = ChessnutGame()

    def setUp(self):
        self.circling_pawns = []

    def tearDown(self):
        for pawn in self.circling_pawns:
            self.c._hard_remove_piece(pawn)

        self.circling_pawns = []

    def surround_piece(self, _file, rank, radius):
        """Create a circle of Pawns around the the given file and rank.
        Return a list of spaces at which they are placed, in clockwise order.
        """
        placed = []
        for filemod, rankmod in self.mods:
            p = Pawn(White, _file + radius * filemod, rank + radius * rankmod)
            try:
                self.c._hard_place_piece(p)
                placed.append((p.file, p.rank))
                self.circling_pawns.append(p)

            except BoardIndexError:
                placed.append((None, None))

        return placed

    def circle_piece(self, _file, rank, radius):
        """Create a single Pawn that circles the given file and rank.
        Yield the coordinates of the Pawn as it circles.
        """
        p = Pawn(White, _file, rank)
        self.c._hard_place_piece(p)

        for filemod, rankmod in self.mods:
            try:
                self.c.move_piece(
                    p,
                    _file + radius * filemod,
                    rank + radius * rankmod
                )
                yield (p.file, p.rank)

            except BoardIndexError:
                yield (None, None)

    def test_empty_board(self):
        """Test an empty board."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for direction in range(8):
                self.assertEqual(
                    self.c.first_blocked_space_from(_file, rank, direction),
                    (None, None)
                )

    def test_all_pieces(self):
        """Assert that each type of piece in each color can block spaces."""
        for piece in (Pawn, Rook, Knight, Bishop, Queen, King):
            for color in (Black, White):
                p = piece(color, 4, 5)
                self.c._hard_place_piece(p)
                self.assertEqual(
                    self.c.first_blocked_space_from(4, 4, 0),
                    (4, 5)
                )
                self.c._hard_remove_piece(p)

    def test_all_directions_surrounded(self):
        """Test all directions when surrounded by pawns."""
        for _file, rank in ((f, r) for f in range(8) for r in range(8)):
            for radius in range(1, 8):
                expected = self.surround_piece(_file, rank, radius)
                for direction in range(8):
                    self.assertEqual(
                        self.c.first_blocked_space_from(
                            _file,
                            rank,
                            direction
                        ),
                        expected.pop(0)
                    )

    def test_all_directions_circling_piece(self):
        """Test all directions as one Pawn circles."""

    def test_all_directions_layered(self):
        """Test two layers of blocking pieces."""

    def test_all_directions_staggered(self):
        """Test two staggered circles of pieces."""


if __name__ == '__main__':
    unittest.main()
