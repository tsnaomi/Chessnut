import unittest
from game import ChessnutGame


class TestCoordinatesToDiagonals(unittest.TestCase):
    """Test the _coordinates_to_forward_diagonal and
    _coordinates_to_backward_diagonal methods.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def build_forward_diagonal(self, _file, rank):
        """Determine all the spaces in a forward diagonal beginning at
        the specified cell.
        """
        while 0 <= rank <= 7 and 0 <= _file <= 7:
            yield (_file, rank)
            _file += 1
            rank += 1

    def build_backward_diagonal(self, _file, rank):
        """Determine all the spaces in a backward diagonal beginning at
        the specified cell.
        """
        while 0 <= rank <= 7 and 0 <= _file <= 7:
            yield (_file, rank)
            _file -= 1
            rank += 1

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
            for difile, dirank in self.build_forward_diagonal(_file, rank):
                self.assertEqual(
                    (_file, rank),
                    self.c._coordinates_to_forward_diagonal(difile, dirank)
                )

    def test_san_to_backward_diagonal(self):
        """Assert that all spaces are assigned to their correct backward
        diagonal.
        """
        diagonals = [
            ('a', '1'),
            ('b', '1'),
            ('c', '1'),
            ('d', '1'),
            ('e', '1'),
            ('f', '1'),
            ('g', '1'),
            ('h', '1'),
            ('h', '2'),
            ('h', '3'),
            ('h', '4'),
            ('h', '5'),
            ('h', '6'),
            ('h', '7'),
            ('h', '8'),
        ]

        for _file, rank in diagonals:
            for difile, dirank in self.build_backward_diagonal(_file, rank):
                self.assertEqual(
                    (_file, rank),
                    self.c._coordinates_to_backward_diagonal(difile, dirank)
                )


if __name__ == '__main__':
    unittest.main()
