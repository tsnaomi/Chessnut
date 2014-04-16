import unittest
from game import ChessnutGame


class TestSANToDiagonals(unittest.TestCase):
    """Test the _san_to_forward_diagonal and _san_to_backward_diagonal
    methods.
    """
    def setUp(self):
        self.c = ChessnutGame()

    def build_forward_diagonal(self, rank, _file):
        """Determine all the spaces in a forward diagonal beginning at
        the specified cell.
        """
        diagonals = []
        rankord = ord(rank)
        fileord = ord(_file)
        while rankord <= 56 and fileord <= 104:
            diagonals.append((chr(rankord), chr(fileord)))
            rankord += 1
            fileord += 1

        return diagonals

    def build_backward_diagonal(self, rank, _file):
        """Determine all the spaces in a backward diagonal beginning at
        the specified cell.
        """
        diagonals = []
        rankord = ord(rank)
        fileord = ord(_file)
        while rankord <= 56 and fileord >= 97:
            diagonals.append((chr(rankord), chr(fileord)))
            rankord += 1
            fileord -= 1

        return diagonals

    def test_san_to_forward_diagonal(self):
        """Assert that all spaces are assigned to their correct forward
        diagonal.
        """
        diagonals = [
            ('a', '8'),
            ('a', '7'),
            ('a', '6'),
            ('a', '5'),
            ('a', '4'),
            ('a', '3'),
            ('a', '2'),
            ('a', '1'),
            ('b', '1'),
            ('c', '1'),
            ('d', '1'),
            ('e', '1'),
            ('f', '1'),
            ('g', '1'),
            ('h', '1'),
        ]

        for _file, rank in diagonals:
            expected = ''.join([_file, rank])
            for dirank, difile in self.build_forward_diagonal(rank, _file):
                self.assertEqual(
                    expected, self.c._san_to_forward_diagonal(dirank, difile))

    def test_san_to_backward_diagonal(self):
        """Assert that all spaces are assigned to their correct backward
        diagonal.
        """


if __name__ == '__main__':
    unittest.main()
