import re


class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game=None):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        #False means black's turn, True means white's.
        self.turn = True

        #Keep track of whether each player can queenside or kingside castle
        self.white_kingside = True
        self.white_queenside = True
        self.black_kingside = True
        self.black_queenside = True

        if game is not None:
            self.pgn = game
            self.board = self._pgn_to_board(game)
            self.image_string = None
        else:
            self.pgn = None
            self.board = self._initialize_chessboard()
            self.image_string = None

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        self._evaluate_move(move)

    def _pgn_to_board(self, game):
        """Converts PGN notation to a 2D array representing board state."""
        board = self._initialize_chessboard()
        moves = re.split(r'\s?\d+\.\s', self.pgn)

        self.move_count = 0
        for move in moves:
            self.move_count += 1
            half_moves = move.split()

            for half_move in half_moves:
                self._evaluate_move(half_move)

            if len(half_moves) == 1:
                self.turn = False

    def _board_to_image_string(self):
        """Converts the board state to an image string."""
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

        if match:
            groups = match.groupdict()
            if groups['piece'] is None:
                groups['piece'] = 'P'

            evaluator = self._get_evaluator(groups['piece'])

            #orow and ocol are origin row and origin column, the row and
            #column from which the piece is moving.
            orow, ocol = evaluator(groups)

            #drow and dcol are destination row and destination column,
            #the row and column to which the piece is moving.
            drow, dcol = self._pgn_move_to_coords(groups['dest'])

            self.board[orow][ocol], self.board[drow][dcol] = (0, 0), self.board[orow][ocol]

            #TO DO: castling, en passant capture, check and checkmate

        if not match:
            match = re.match(r'[0O]-[0O]-[0O]', move)
            if match:
                self._queenside_evaluator()

        if not match:
            match = re.match(r'[0O]-[0O]', move)
            if match:
                self._kingside_evaluator()

        if not match:
            raise NotationParseError

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

        raise NotationParseError(
            "_get_evaluator recieved a letter not corresponding to an evaluator.")

    def _pawn_evaluator(self, groups):
        """Return the coordinates of the pawn that will be making the move
        specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        if self.turn:
            rowmod = 1
        else:
            rowmod = -1

        #Compile a list of pawns that could make the given move.
        pieces = []
        try:
            if not groups['capture']:
                if self.board[drow + 1 * rowmod][dcol] == ('P', self.turn):
                    pieces.append((drow + 1 * rowmod, dcol))
                elif drow == (4 if self.turn else 3) and \
                        self.board[drow + 2 * rowmod][dcol] == ('P', self.turn) \
                        and self.board[drow + 1 * rowmod][dcol] == (0, 0):
                    pieces.append((drow + 2 * rowmod, dcol))
            else:
                try:
                    if self.board[drow + 1 * rowmod][dcol + 1] == ('P', self.turn):
                        pieces.append((drow + 1 * rowmod, dcol + 1))
                except IndexError:
                    pass

                try:
                    if self.board[drow + 1 * rowmod][dcol - 1] == ('P', self.turn):
                        pieces.append((drow + 1 * rowmod, dcol - 1))
                except IndexError:
                    pass

        except IndexError:
            #If an IndexError is raised, then the player has specified a
            #space on the top or bottom of the board, and the game logic
            #is looking for a pawn above or below the board to move to it.
            #The move is obviously not legal.
            raise MoveNotLegalError

        #If we haven't found any pieces that could make this move, the
        #move is not legal.
        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _rook_evaluator(self, groups):
        """Return the coordinates of the rook that will be making the move
        specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for rooks in each of the four horizontal directions from
        #the destination cell.
        for rowmod, colmod in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            row, col = drow, dcol
            while True:
                row += rowmod
                col += colmod
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('R', self.turn):
                            pieces.append((row, col))
                        break
                except IndexError:
                    break

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        piece = self._evaluate_rank_and_file(pieces, orow, ocol)

        if piece == (0, 0):
            self.black_queenside = False
        if piece == (0, 7):
            self.black_kingside = False
        if piece == (7, 0):
            self.white_queenside = False
        if piece == (7, 7):
            self.white_kingside = False

        return piece

    def _knight_evaluator(self, groups):
        """Return the coordinates of the knight that will be making the
        move specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of knights that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for knights in each of the legal spaces surrounding the
        #destination cell.
        for rowmod, colmod in [(-2, -1), (-2, 1), (2, -1), (2, 1),
                               (-1, -2), (-1, 2), (1, -2), (1, 2)]:
            row, col = drow, dcol
            row += rowmod
            col += colmod
            try:
                if self.board[row][col] != (0, 0):
                    if self.board[row][col] == ('N', self.turn):
                        pieces.append((row, col))
            except IndexError:
                pass

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _bishop_evaluator(self, groups):
        """Return the coordinates of the bishop that will be making the
        move specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for bishops in each of the four diagonal directions from
        #the destination cell.
        for rowmod, colmod in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            row, col = drow, dcol
            while True:
                row += rowmod
                col += colmod
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('B', self.turn):
                            pieces.append((row, col))
                        break
                except IndexError:
                    break

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _king_evaluator(self, groups):
        """Return the coordinates of the king that will be making the
        move specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        if self._is_check(drow, dcol):
            raise MoveNotLegalError

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for kings in a single space in each of the four horizontal
        #directions and each of the four diagonal directions from the
        #destination cell.
        for rowmod, colmod in [(-1, -1), (1, -1), (-1, 1), (1, 1),
                               (-1, 0), (1, 0), (0, 1), (0, -1)]:
            row, col = drow, dcol
            row += rowmod
            col += colmod
            try:
                if self.board[row][col] != (0, 0):
                    if self.board[row][col] == ('K', self.turn):
                        pieces.append((row, col))
            except IndexError:
                pass

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        piece = self._evaluate_rank_and_file(pieces, orow, ocol)

        if self.turn:
            self.white_kingside = False
            self.white_queenside = False
        else:
            self.black_kingside = False
            self.black_queenside = False

        return piece

    def _queen_evaluator(self, groups):
        """Return the coordinates of the queen that will be making the
        move specified.
        """
        dcol, drow = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == self.turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for queens in each of the four horizontal directions and
        #each of the four diagonal directions from the destination cell.
        for rowmod, colmod in [(-1, -1), (1, -1), (-1, 1), (1, 1),
                               (-1, 0), (1, 0), (0, 1), (0, -1)]:
            row, col = drow, dcol
            while True:
                row += rowmod
                col += colmod
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('Q', self.turn):
                            pieces.append((row, col))
                        break
                except IndexError:
                    break

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _evaluate_rank_and_file(self, pieces, orow, ocol):
        """Given a list of pieces that could potentially make any given
        move, and the rank and/or file from which the move has specifcally
        been requested made (if any), determine whether there is exactly
        one piece that can make the given move and return it, if so.
        """
        valid = []
        #If both the rank and file of the piece moving have been explicitly
        #given.
        if orow is not None and ocol is not None:
            for row, col in pieces:
                if row == orow and col == ocol:
                    valid.append((row, col))

        #If the rank of the piece moving has been explicitly given.
        elif orow is not None:
            for row, col in pieces:
                if row == orow:
                    valid.append((row, col))

        #If the file of the piece moving has been explicitly given.
        elif ocol is not None:
            for row, col in pieces:
                if col == ocol:
                    valid.append((row, col))

        #If neither the rank nor the file of the piece moving have been
        #explicitly given.
        else:
            valid = pieces

        #If more than one piece could make this move, raise a
        #MoveAmbiguousError.
        if len(valid) > 1:
            raise MoveAmbiguousError

        #If not pieces could make this move, raise a MoveNotLegalError.
        if len(valid) < 1:
            raise MoveNotLegalError

        #If we have exactly one piece, return it.
        return valid[0]

    def _queenside_evaluator(self):
        """Evaluator for queenside castling logic. Performs queenside
        castle for the current player, if legal, or raises an exception.
        """
        if self.turn and not self.white_queenside or not self.black_queenside:
            raise MoveNotLegalError

        row = 7 if self.turn else 0
        for col in [1, 2, 3]:
            if self.board[row][col] != (0, 0):
                raise MoveNotLegalError

        for col in [2, 3, 4]:
            if self._is_check(row, col):
                raise MoveNotLegalError

        self.board[row][4], self.board[row][0] = (0, 0), (0, 0)
        self.board[row][2], self.board[row][3] = \
            ('K', self.turn), ('R'. self.turn)

        if self.turn:
            self.white_queenside, self.white_kingside = False, False
        else:
            self.black_queenside, self.black_kingside = False, False

    def _kingside_evaluator(self):
        """Evaluator for kingside castling logic. Performs kingside
        castle for the current player, if legal, or raises an exception.
        """
        if self.turn and not self.white_kingside or not self.black_kingside:
            raise MoveNotLegalError

        row = 7 if self.turn else 0
        for col in [5, 6]:
            if self.board[row][col] != (0, 0):
                raise MoveNotLegalError

        for col in [4, 5, 6]:
            if self._is_check(row, col):
                raise MoveNotLegalError

        self.board[row][4], self.board[row][7] = (0, 0), (0, 0)
        self.board[row][6], self.board[row][5] = \
            ('K', self.turn), ('R'. self.turn)

        if self.turn:
            self.white_queenside, self.white_kingside = False, False
        else:
            self.black_queenside, self.black_kingside = False, False

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


class MoveAmbiguousError(ChessnutError):
    """Exception raised when a player tries to make a move and it can't
    be determined which specific piece was intended to make the move.
    """
    pass


class NotationParseError(ChessnutError):
    """Exception raised when a player submits chess notation that the
    game logic can't parse.
    """
    pass
