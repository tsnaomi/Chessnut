import re


class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        #False means black's turn, True means white's.
        self.turn = True
        self.pgn = game
        self.board = self._pgn_to_board(game)
        self.image_name = self._board_to_image()

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        pass

    def _pgn_to_board(self):
        """Converts PGN notation to a 2D array representing board state."""
        board = self._initialize_chessboard()
        moves = re.split(r'\s?\d+\.\s', self.pgn)

        move_count = 0
        for move in moves:
            move_count += 1
            half_moves = move.split()

            for half_move in half_moves:
                self._evaluate_move(half_move)

            if len(half_moves) == 1:
                self.turn = False

    def _board_to_image(self, pgn):
        """Converts the board state to an image filename."""
        pass

    def _evaluate_move(self, move):
        """Take in a move in PGN/SAN notation, evaluate it, and perform
        it, if legal.
        """
        #Attempt to parse the SAN notation.
        match = re.match(
            r'(?P<piece>[RNBKQP])?(?P<file>[a-z])?(?P<rank>\d)?(?P<capture>x)?(?P<dest>\w\d)(?P<check>+)?(?P<checkmate>#)?',
            move
        )

        if not match:
            raise NotationParseError

        groups = match.groupdict()
        groups.setdefault('piece', 'P')

        evaluator = self._get_evaluator(groups['piece'])

        #ox and oy are origin x and origin y, the x and y coordinates from
        #which the piece is moving.
        ox, oy = evaluator(groups)

        #dx and dy are destination x and destination y, the x and y
        #coordinates to which the piece is moving.
        dx, dy = self._pgn_move_to_coords(groups['dest'])

        self.board[ox][oy], self.board[dx][dy] = 0, self.board[ox][oy]

        #TO DO: castling, en passant capture, check and checkmate

    def _get_evaluator(self, piece):
        """Return the appropriate evaluator callable for the piece passed
        in.
        """
        if piece == 'P':
            return self._pawn_evaluator
        elif piece == 'R':
            return self._rook_evaluator
        elif piece == 'N':
            return self._knight_evaluator
        elif piece == 'B':
            return self._bishop_evaluator
        elif piece == 'K':
            return self._king_evaluator
        elif piece == 'Q':
            return self._queen_evaluator

        raise ValueError(
            "_get_evaluator recieved a letter not corresponding to an evaluator.")

    def _pawn_evaluator(self, groups):
        """Return the coordinates of the pawn that will be making the move
        specified.
        """
        dx, dy = self._pgn_move_to_coords(groups['dest'])
        ox = self._pgn_file_to_x(groups['file'])
        oy = self._pgn_rank_to_y(groups['rank'])

        #If both the rank and file of the pawn moving have been explicitly
        #given.
        if ox is not None and oy is not None:
            if self.turn:
                if not groups['capture']:
                    pass
                else:
                    pass
            else:
                if not groups['capture']:
                    pass
                else:
                    pass

        #If the file of the pawn moving has been explictly given.
        elif ox is not None:
            if self.turn:
                if not groups['capture']:
                    pass
                else:
                    pass
            else:
                if not groups['capture']:
                    pass
                else:
                    pass

        #If the rank of the pawn moving has been explicitly given.
        elif oy is not None:
            if self.turn:
                if not groups['capture']:
                    pass
                else:
                    pass
            else:
                if not groups['capture']:
                    pass
                else:
                    pass

        #If neither the rank nor the file of the pawn moving has been
        #explicitly given.
        else:
            if self.turn:
                if not groups['capture']:
                    pass
                else:
                    pass
            else:
                if not groups['capture']:
                    pass
                else:
                    pass

        if self.turn:
            if not groups['capture']:
                if self.board[dx][dy + 1][0] == 'P' and \
                        self.board[dx][dy + 1][1] == self.turn:
                    return dx, dy + 1
                elif dy == 4 and \
                        self.board[dx][dy + 2][0] == 'P' and \
                        self.board[dx][dy + 2][1] == self.turn and \
                        self.board[dx][dy + 1][0] == 0:
                    return dx, dy + 2
            else:
                pass


        else:
            if not groups['capture']:
                if self.board[dx][dy - 1][0] == 'P' and \
                        self.board[dx][dy - 1][1] == self.turn:
                    return dx, dy - 1
                elif dy == 3 and \
                        self.board[dx][dy - 2][0] == 'P' and \
                        self.board[dx][dy - 2][1] == self.turn and \
                        self.board[dx][dy - 1][0] == 0:
                    return dx, dy - 2
            else:
                pass

        raise MoveNotLegalError

    def _rook_evaluator(self, groups):
        """Return the coordinates of the rook that will be making the move
        specified.
        """
        pass

    def _knight_evaluator(self, groups):
        """Return the coordinates of the knight that will be making the
        move specified.
        """
        pass

    def _bishop_evaluator(self, groups):
        """Return the coordinates of the bishop that will be making the
        move specified.
        """
        pass

    def _king_evaluator(self, groups):
        """Return the coordinates of the king that will be making the
        move specified.
        """
        pass

    def _queen_evaluator(self, groups):
        """Return the coordinates of the queen that will be making the
        move specified.
        """
        pass

    def _pgn_move_to_coords(self, move):
        """Converts a single move in PGN notation to board-state array
        coordinates.
        """
        pass

    def _pgn_file_to_x(self, file):
        pass

    def _pgn_rank_to_y(self, rank):
        pass

    def _initialize_chessboard(self):
        """Creates a 2D array representing an initial chessboard."""
        board = []

        board.append([
            ('R', False),
            ('N', False),
            ('B', False),
            ('Q', False),
            ('K', False),
            ('B', False),
            ('N', False),
            ('R', False),
        ])
        board.append([('P', False) for i in range(8)])

        for i in range(4):
            board.append([(0, 0) for i in range(8)])

        board.append(('P', True) for i in range(8))
        board.append([
            ('R', True),
            ('N', True),
            ('B', True),
            ('Q', True),
            ('K', True),
            ('B', True),
            ('N', True),
            ('R', True),
        ])

        return board


class ChessnutError(BaseException):
    """Chessnut base exception."""
    pass


class MoveNotLegalError(ChessnutError):
    """Exception raised when a player attempts to make a move that is not
    legal.
    """
    pass


class NotationParseError(ChessnutError):
    """Exception raised when a player submits chess notation that the
    game logic can't parse.
    """
    pass
