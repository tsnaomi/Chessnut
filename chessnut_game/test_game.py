import unittest
from game import ChessnutGame


class TestSANToDiagonals(unittest.TestCase):
    """Test the _san_to_forward_diagonal and _san_to_backward_diagonal
    methods.
    """
    def test_san_to_forward_diagonal(self):
        """Assert that all spaces are assigned to their correct forward
        diagonal.
        """

    def test_san_to_backward_diagonal(self):
        """Assert that all spaces are assigned to their correct backward
        diagonal.
        """


if __name__ == '__main__':
    unittest.main()
