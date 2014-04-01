import re


class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game=None):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        #False means black's turn, True means white's.
        self.turn = True
        if game is not None:
            self.pgn = game
            self.board = self._pgn_to_board(game)
            self.image_name = self._board_to_image()
        else:
            self.pgn = None
            self.board = self._initialize_chessboard()
            self.image_name = None

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        pass

    def _pgn_to_board(self, game):
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

        #orow and ocol are origin x and origin y, the x and y coordinates from
        #which the piece is moving.
        orow, ocol = evaluator(groups)

        #drow and dcol are destination x and destination y, the x and y
        #coordinates to which the piece is moving.
        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        self.board[orow][ocol], self.board[drow][dcol] = 0, self.board[orow][ocol]

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
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of pawns that could make the given move.
        pieces = []
        if self.turn:
            if not groups['capture']:
                if self.board[drow + 1][dcol] == ('P', self.turn) and \
                        self.board[drow][dcol] == (0, 0):
                    pieces.append((drow + 1, dcol))
                elif drow == 4 and \
                        self.board[drow + 2][dcol] == ('P', self.turn) and \
                        self.board[drow + 1][dcol] == (0, 0) and \
                        self.board[drow][dcol] == (0, 0):
                    pieces.append((drow + 2, dcol))
            else:
                pass

        else:
            if not groups['capture']:
                if self.board[drow - 1][dcol] == ('P', self.turn) and \
                        self.board[drow][dcol] == (0, 0):
                    pieces.append((drow - 1, dcol))
                elif drow == 3 and \
                        self.board[drow - 2][dcol] == ('P', self.turn) and \
                        self.board[drow - 1][dcol] == (0, 0) and \
                        self.board[drow][dcol] == (0, 0):
                    pieces.append((drow - 2, dcol))
            else:
                pass

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _rook_evaluator(self, groups):
        """Return the coordinates of the rook that will be making the move
        specified.
        """
        raise MoveNotLegalError

    def _knight_evaluator(self, groups):
        """Return the coordinates of the knight that will be making the
        move specified.
        """
        raise MoveNotLegalError

    def _bishop_evaluator(self, groups):
        """Return the coordinates of the bishop that will be making the
        move specified.
        """
        raise MoveNotLegalError

    def _king_evaluator(self, groups):
        """Return the coordinates of the king that will be making the
        move specified.
        """
        raise MoveNotLegalError

    def _queen_evaluator(self, groups):
        """Return the coordinates of the queen that will be making the
        move specified.
        """
        raise MoveNotLegalError

    def _evaluate_rank_and_file(self, pieces, orow, ocol):
        """Given a list of pieces that could potentially make any given
        move, and the rank and/or file from which the move has specifcally
        been requested made (if any), determine whether there is exactly
        one piece that can make the given move and return it, if so.
        """
        #If both the rank and file of the piece moving have been explicitly
        #given.
        if orow is not None and ocol is not None:
            for row, col in pieces:
                if row == orow and col == ocol:
                    return row, col

        #If the rank of the piece moving has been explicitly given.
        elif orow is not None:
            rowmatch = []
            for row, col in pieces:
                if row == orow:
                    rowmatch.append((row, col))

            if len(rowmatch) == 1:
                return rowmatch[0]

        #If the file of the piece moving has been explicitly given.
        elif ocol is not None:
            colmatch = []
            for row, col in pieces:
                if col == ocol:
                    colmatch.append((row, col))

            if len(colmatch) == 1:
                return colmatch[0]

        #If neither the rank nor the file of the piece moving have been
        #explicitly given.
        elif len(pieces) == 1:
            return pieces[0]

        raise MoveNotLegalError

    def _pgn_move_to_coords(self, move):
        """Converts a single move in PGN notation to board-state array
        coordinates.
        """
        move = list(move)
        if len(move) != 2:
            raise ValueError("_pgn_move_to_coords got input of length != 2")

        return self._pgn_file_to_col(move[0]), self._pgn_rank_to_row(move[1])

    def _pgn_file_to_col(self, _file):
        """Convert a lettered file to its column in the 2D board array."""
        if _file not in 'abcdefgh':
            raise ValueError(
                "_pgn_file_to_col got %s (not a valid file)" % _file
            )
        return ord(_file) - 97

    def _pgn_rank_to_row(self, rank):
        """Convert a numbered rank to its row in the 2D board array."""
        if rank not in '12345678':
            raise ValueError(
                "_pgn_rank_to_row got %s (not a valid rank)" % rank
            )
        return (8 - int(rank))

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

        board.append([('P', True) for i in range(8)])
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
