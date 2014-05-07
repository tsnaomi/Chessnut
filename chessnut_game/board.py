class BoardGroup(object):
    """Data type representing a general grouping of spaces on the board
    (either a rank or a file).
    """
    def __init__(self, value):
        #Value is stored internally as an integer. The Rank and File
        #subclasses handle correct conversion of this integer to a single-
        #character string.
        self.value = value

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass


class Rank(BoardGroup):
    """Data type representing a Rank on the chessboard. This is not a
    container class of any kind; simply a data type representing a rank
    as a string '1' through '8' and supporting comparision and basic
    arithmetic operations.
    """


class File(BoardGroup):
    """Data type representing a File on the chessboard. This is not a
    container class of any kind; simply a data type representing a file
    as a string 'a' through 'h' and supporting comparision and basic
    arithmetic operations.
    """
