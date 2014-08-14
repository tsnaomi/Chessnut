print __name__

import unittest
from ..utils.functions import circle_space, surround_space
from ..utils.decorators import all_players, all_spaces, all_piece_types
from chessnut_game import ChessnutGame, Black, White
from chessnut_game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chessnut_game.exceptions import BoardIndexError


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


class TestFirstBlockingPiece(unittest.TestCase):
    """Test the first_blocking_piece method of the game class."""
    game = ChessnutGame()

    @all_spaces
    def test_empty_board(self, _file=None, rank=None):
        """Test an empty board from the given space."""
        for direction in range(8):
            self.assertIsNone(
                self.game.first_blocking_piece(_file, rank, direction)
            )

    @all_players
    @all_piece_types
    def test_all_pieces(self, piece=None, player=None):
        """Assert that each type of piece in each color can block spaces."""
        pc = piece(player, 4, 5)
        game = ChessnutGame()
        game._hard_place_piece(pc)
        self.assertIs(
            game.first_blocking_piece(4, 4, 0),
            pc
        )

    @all_spaces
    def test_all_directions_circling_piece(self, _file=None, rank=None):
        """Test all directions as one Pawn circles the given space."""
        for radius in range(1, 8):
            game = ChessnutGame()
            for direction, expected in enumerate(
                circle_space(game, _file, rank, radius)
            ):
                self.assertIs(
                    game.first_blocking_piece(_file, rank, direction),
                    expected
                )

    @all_spaces
    def test_all_directions_surrounded(self, _file=None, rank=None):
        """Test all directions when the given space is surrounded by Pawns."""
        for radius in range(1, 8):
            game = ChessnutGame()
            expected = surround_space(game, _file, rank, radius)
            for direction in range(8):
                self.assertIs(
                    game.first_blocking_piece(_file, rank, direction),
                    expected.pop(0)
                )

    @all_spaces
    def test_all_directions_layered(self, _file=None, rank=None):
        """Test two layers of blocking Pawns from the given space."""
        game = ChessnutGame()
        surround_space(game, _file, rank, 2)
        expected = surround_space(game, _file, rank, 1)
        for direction in range(8):
            self.assertIs(
                game.first_blocking_piece(_file, rank, direction),
                expected.pop(0)
            )

    @all_spaces
    def test_all_directions_staggered(self, _file=None, rank=None):
        """Test two staggered circles of pieces."""
        game = ChessnutGame()
        surround_space(game, _file, rank, 3)
        expected = surround_space(game, _file, rank, 1)
        for direction in range(8):
            self.assertIs(
                game.first_blocking_piece(_file, rank, direction),
                expected.pop(0)
            )


if __name__ == '__main__':
    unittest.main()
