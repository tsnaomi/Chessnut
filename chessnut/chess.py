import re


class ChessnutGame(object):
    """Class that encapsulates all Chessnut game logic."""

    def __init__(self, game=None):
        """Takes as argument the game referenced (possibly as a PGN)
        string - details TBD.
        """
        if isinstance(game, str):
            game = game.rstrip()

        #False means black's turn, True means white's.
        self.turn = True

        self.is_over = False
        self.winner = None

        #Keep track of whether each player can queenside or kingside castle
        self.white_kingside = True
        self.white_queenside = True
        self.black_kingside = True
        self.black_queenside = True

        #Keep track of where the king currently is for each player.
        self.white_king = (7, 4)
        self.black_king = (0, 4)

        #Keep track of which pawns (if any) can be en-passant captured.
        #Pawns are in buckets according to the player they belong to.
        self.en_passant = {True: [], False: []}
        #Set to true when an en passant capture has just been determined
        #to have been made by the pawn evaluator. Signals to evaluate_move
        #that it needs to perform an en passant capture.
        self.en_passant_capture = False

        self.move_count = 0
        self.board = self._initialize_chessboard()
        self.pgn = ''
        self.image_string = None

        if game is not None:
            self._reconstruct_incoming_game(game)

    def __call__(self, move):
        """Takes as its argument the move being attempted an evaluates
        that move, making it if it's legal.
        """
        self.evaluate_move(move)

    def evaluate_move(self, move):
        """Take in a move in PGN/SAN notation, evaluate it, and perform
        it, if legal. Set attributes on the class representing the changed
        state of the game.
        """
        if self.is_over:
            raise GameOverError

        #Any pawns in the en_passant bucket corresponding to the current
        #player are no longer eligible for en passant capture (which
        #must happen immediately after the pawn to be captured has moved).
        #Clear the en passant bucket corresponding to the current player.
        self.en_passant[self.turn] = []

        #Attempt to parse the SAN notation.
        match = re.match(
            r'^(?P<piece>[RNBKQP])?(?P<file>[a-h])?(?P<rank>\d)?(?P<capture>x)?(?P<dest>\w\d)(?P<check>\+)?(?P<checkmate>#)?$',
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

            self.board[orow][ocol], self.board[drow][dcol] = \
                (0, 0), self.board[orow][ocol]

            #If an en passant capture has just been performed, clear the
            #appropriate space on the board.
            if self.en_passant_capture:
                self.board[drow + 1 if self.turn else drow - 1][dcol] = \
                    (0, 0)
                self.en_passant_capture = False

            #If the king was just moved, update its position.
            if groups['piece'] == 'K' and self.turn:
                self.white_king = (drow, dcol)
            elif groups['piece'] == 'K':
                self.black_king = (drow, dcol)

            #TO DO: en passant capture, stalemate, forfeit, promotion

            #Keep track of whether or not each player is still allowed to
            #castle. The first time a piece is moved from these locations,
            #the piece must be a king or a rook, so we take away the
            #relevant castling privilege.
            if (orow, ocol) == (7, 4):
                self.white_kingside = False
                self.white_queenside = False
            elif (orow, ocol) == (0, 4):
                self.black_kingside = False
                self.black_queenside = False
            elif (orow, ocol) == (0, 0):
                self.black_queenside = False
            elif (orow, ocol) == (0, 7):
                self.black_kingside = False
            elif (orow, ocol) == (7, 0):
                self.white_queenside = False
            elif (orow, ocol) == (7, 7):
                self.white_kingside = False

            #Construct an image string representing this board state and
            #the move just made.
            self.image_string = "%s%s%s%s%s" % \
                (self._board_to_image_string(), ocol, orow, dcol, drow)

        if not match:
            match = re.match(r'[0O]-[0O]-[0O]', move)
            if match:
                self._queenside_evaluator()

            self.image_string = "%s%sQC" % \
                (self._board_to_image_string(), ('W' if self.turn else 'B'))

        if not match:
            match = re.match(r'[0O]-[0O]', move)
            if match:
                self._kingside_evaluator()

            self.image_string = "%s%sKC" % \
                (self._board_to_image_string(), ('W' if self.turn else 'B'))

        if not match:
            raise NotationParseError

        #If, at the end of any move, either king is under checkmate,
        #then the game is over. We have to flip the turn bit here so
        #that we can evaluate whether the king is checkmated from the
        #other player's perspective.
        #import pdb; pdb.set_trace()
        self.turn = not self.turn
        if not self.turn and self._is_checkmate(*self.black_king):
            self.is_over = True
            self.winner = True
        elif self.turn and self._is_checkmate(*self.white_king):
            self.is_over = True
            self.winner = False
        self.turn = not self.turn

        #If, at the end of any move, that player's king is under
        #check, then that move was illegal. The player must act to
        #take their king out of check.
        if self.turn and self._is_check(*self.white_king):
            raise MoveNotLegalError(
                "Player's king was under check at the end of their turn.")
        elif not self.turn and self._is_check(*self.black_king):
            raise MoveNotLegalError(
                "Player's king was under check at the end of their turn.")

        #If white has just made a move, then we're entering a new move
        #(pair of half_moves) from a PGN perspective. Increment the
        #move_count.
        if self.turn:
            self.move_count += 1

        #If we made a legal move, update the pgn game-state string.
        prefix = (" %s. " % str(self.move_count)) if self.turn else " "
        self.pgn += "%s%s" % (prefix, move)
        self.pgn = self.pgn.strip()

    def _reconstruct_incoming_game(self, game):
        """Walks through the PGN-represented game used to instantiate
        this game object and performs every move annotated, reconstructing
        a game in the state proscribed.
        """
        moves = re.split(r'\s?\d+\.\s', game)

        #Because the split field appears at the front of the string being
        #split, we always end up with an empty string as the first element
        #in the moves array. Get rid of it.
        moves.pop(0)

        for move in moves:
            half_moves = move.split()

            for half_move in half_moves:
                self.evaluate_move(half_move)
                self.turn = not self.turn

    def _board_to_image_string(self):
        """Converts the board state to an image string."""
        string = ''
        for row in self.board:
            for cell in row:
                if cell[1] is False:
                    string += cell[0].lower()
                elif cell[1] is True:
                    string += cell[0]
                else:
                    string += str(cell[0])

        return string

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

    def _pawn_evaluator(self, groups, turn=None):
        """Return the coordinates of the pawn that will be making the move
        specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
                 not groups['capture']):
            raise MoveNotLegalError

        if turn:
            rowmod = 1
        else:
            rowmod = -1

        #Compile a list of pawns that could make the given move.
        pieces = []
        try:
            if drow + 1 * rowmod < 0:
                raise IndexError
            if not groups['capture']:
                if self.board[drow + 1 * rowmod][dcol] == ('P', turn):
                    pieces.append((drow + 1 * rowmod, dcol))
                elif drow == (4 if turn else 3) and \
                        self.board[drow + 2 * rowmod][dcol] == ('P', turn) \
                        and self.board[drow + 1 * rowmod][dcol] == (0, 0):
                    pieces.append((drow + 2 * rowmod, dcol))
                    self.en_passant[self.turn].append(
                        (drow, dcol))
            else:
                if self.board[drow][dcol][1] is not (not self.turn):
                    if (drow + 1 * rowmod, dcol) not in self.en_passant[not self.turn]:
                        raise MoveNotLegalError
                    else:
                        self.en_passant_capture = True

                try:
                    if self.board[drow + 1 * rowmod][dcol + 1] == ('P', turn):
                        pieces.append((drow + 1 * rowmod, dcol + 1))
                except IndexError:
                    pass

                try:
                    if self.board[drow + 1 * rowmod][dcol - 1] == ('P', turn):
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

    def _rook_evaluator(self, groups, turn=None):
        """Return the coordinates of the rook that will be making the move
        specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for rooks in each of the four horizontal directions from
        #the destination cell.
        for rowmod, colmod in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            row, col = drow, dcol
            while True:
                row += rowmod
                col += colmod
                if row < 0 or col < 0:
                    break
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('R', turn):
                            pieces.append((row, col))
                        break
                except IndexError:
                    break

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _knight_evaluator(self, groups, turn=None):
        """Return the coordinates of the knight that will be making the
        move specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of knights that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for knights in each of the legal spaces surrounding the
        #destination cell.
        for rowmod, colmod in [(-2, -1), (-2, 1), (2, -1), (2, 1),
                               (-1, -2), (-1, 2), (1, -2), (1, 2)]:
            row, col = drow, dcol
            row += rowmod
            col += colmod
            if row < 0 or col < 0:
                continue
            try:
                if self.board[row][col] != (0, 0):
                    if self.board[row][col] == ('N', turn):
                        pieces.append((row, col))
            except IndexError:
                pass

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _bishop_evaluator(self, groups, turn=None):
        """Return the coordinates of the bishop that will be making the
        move specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
                 not groups['capture']):
            raise MoveNotLegalError

        #Look for bishops in each of the four diagonal directions from
        #the destination cell.
        for rowmod, colmod in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            row, col = drow, dcol
            while True:
                row += rowmod
                col += colmod
                if row < 0 or col < 0:
                    break
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('B', turn):
                            pieces.append((row, col))
                        break
                except IndexError:
                    break

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _king_evaluator(self, groups, turn=None):
        """Return the coordinates of the king that will be making the
        move specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        if self._is_check(drow, dcol):
            raise MoveNotLegalError

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
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
            if row < 0 or col < 0:
                continue
            try:
                if self.board[row][col] != (0, 0):
                    if self.board[row][col] == ('K', turn):
                        pieces.append((row, col))
            except IndexError:
                pass

        if not pieces:
            raise MoveNotLegalError

        orow = self._pgn_rank_to_row(groups['rank']) if groups['rank'] else None
        ocol = self._pgn_file_to_col(groups['file']) if groups['file'] else None

        return self._evaluate_rank_and_file(pieces, orow, ocol)

    def _queen_evaluator(self, groups, turn=None):
        """Return the coordinates of the queen that will be making the
        move specified.
        """
        if turn is None:
            turn = self.turn

        drow, dcol = self._pgn_move_to_coords(groups['dest'])

        #Compile a list of rooks that could make the given move.
        pieces = []

        #Check whether there's already a piece at the destination cell.
        if self.board[drow][dcol] != (0, 0) and \
                (self.board[drow][dcol][1] == turn or
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
                if row < 0 or col < 0:
                    break
                try:
                    if self.board[row][col] != (0, 0):
                        if self.board[row][col] == ('Q', turn):
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

        #If no pieces could make this move, raise a MoveNotLegalError.
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
        if self.board[row][4] != ('K', self.turn) or \
                self.board[row][0] != ('R', self.turn):
            raise MoveNotLegalError

        for col in [1, 2, 3]:
            if self.board[row][col] != (0, 0):
                raise MoveNotLegalError

        for col in [2, 3, 4]:
            if self._is_check(row, col):
                raise MoveNotLegalError

        self.board[row][4], self.board[row][0] = (0, 0), (0, 0)
        self.board[row][2], self.board[row][3] = \
            ('K', self.turn), ('R', self.turn)

        if self.turn:
            self.white_queenside, self.white_kingside = False, False
        else:
            self.black_queenside, self.black_kingside = False, False

        if self.turn:
            self.white_king = (7, 2)
        else:
            self.black_king = (0, 2)

    def _kingside_evaluator(self):
        """Evaluator for kingside castling logic. Performs kingside
        castle for the current player, if legal, or raises an exception.
        """
        if self.turn and not self.white_kingside or not self.black_kingside:
            raise MoveNotLegalError

        row = 7 if self.turn else 0
        if self.board[row][4] != ('K', self.turn) or \
                self.board[row][7] != ('R', self.turn):
            raise MoveNotLegalError

        for col in [5, 6]:
            if self.board[row][col] != (0, 0):
                raise MoveNotLegalError

        for col in [4, 5, 6]:
            if self._is_check(row, col):
                raise MoveNotLegalError

        self.board[row][4], self.board[row][7] = (0, 0), (0, 0)
        self.board[row][6], self.board[row][5] = \
            ('K', self.turn), ('R', self.turn)

        if self.turn:
            self.white_queenside, self.white_kingside = False, False
        else:
            self.black_queenside, self.black_kingside = False, False

        if self.turn:
            self.white_king = (7, 6)
        else:
            self.black_king = (0, 6)

    def _is_check(self, row, col):
        """Determines whether the space denoted by the given row and
        column is currently under check.
        """
        try:
            dest = self._coords_to_pgn_move(row, col)
        except ValueError:
            return False

        groups = {
            'piece': None,
            'dest': dest,
            'rank': None,
            'file': None,
            'capture': 'x',
            'check': None,
            'checkmate': None,
        }

        check = False

        dummy = False
        if self.board[row][col][1] is not self.turn:
            old_space = self.board[row][col]
            dummy = True
            self.board[row][col] = ('P', self.turn)

        for piece in ['P', 'R', 'N', 'B', 'Q']:
            evaluator = self._get_evaluator(piece)
            groups['piece'] = piece
            try:
                evaluator(groups, turn=not self.turn)
                check = True
                break
            except MoveAmbiguousError:
                check = True
                break
            except MoveNotLegalError:
                pass

        #The King evaluator uses _is_check to determine whether the move
        #the king wants to make is legal (as the king cannot move into
        #check). Using the king evaluator here thus causes infinite
        #recursion. We have to check separately whether the given spot
        #is under threat from an enemy king.
        for i in range(row - 1, row + 2):
            if i < 0:
                continue
            for j in range(col - 1, col + 2):
                if j < 0:
                    continue
                try:
                    if self.board[i][j] == ('K', not self.turn):
                        check = True
                        break
                except IndexError:
                    pass

        if dummy:
            self.board[row][col] = old_space

        return check

    def _is_checkmate(self, row, col):
        """Determines whether the space denoted by the given row and
        column is currently under checkmate.
        """
        #If any space surrounding the king can be moved to without putting
        #the king in check, we do not have a checkmate. The space on which
        #the king rests is included; it evaluates to False when we check
        #if we can move there, so doesn't harm anything.
        for i in range(row - 1, row + 2):
            if i < 0:
                continue
            for j in range(col - 1, col + 2):
                if j < 0:
                    continue
                try:
                    if self.board[i][j][1] is not self.turn and \
                            not self._is_check(i, j):
                        return False
                except (IndexError, ValueError):
                    pass

        #If any space around the king can be moved to or captured to by
        #another piece of the same color, and doing so removes the king
        #from check, then we do not have a checkmate.
        for i in range(row - 1, row + 2):
            if i < 0 or i > 7:
                continue
            for j in range(col - 1, col + 2):
                if j < 0 or j > 7:
                    continue
                for piece in ['P', 'R', 'N', 'B', 'Q']:
                    for capture in [None, 'x']:
                        groups = {
                            'piece': piece,
                            'dest': self._coords_to_pgn_move(i, j),
                            'rank': None,
                            'file': None,
                            'capture': capture,
                            'check': None,
                            'checkmate': None,
                        }
                        evaluator = self._get_evaluator(piece)
                        try:
                            evaluator(groups)
                            old_space, self.board[i][j] = \
                                self.board[i][j], ('P', self.turn)
                            relieved = not self._is_check(row, col)
                            self.board[i][j] = old_space
                            if relieved:
                                return False
                        except MoveNotLegalError:
                            continue
                        except MoveAmbiguousError:
                            old_space, self.board[i][j] = \
                                self.board[i][j], ('P', self.turn)
                            relieved = not self._is_check(row, col)
                            self.board[i][j] = old_space
                            if relieved:
                                return False

        #If the king cannot move anywhere, and no other piece can save
        #it, but it is safe on its current square, then we do not have a
        #checkmate (but we might have a stalemate).
        if not self._is_check(row, col):
            return False

        return True

    def _is_stalemate(self, row, column):
        """Determines whether the game has ended in a stalemate (the
        player whose turn it is only has a king remaining, and that king
        is not under check, but also cannot move without becoming checked).
        """
        return False

    def _only_king_remains(self, turn=None):
        """Determines whether a king is the only piece remaining for the
        given player. Used to determine whether a game has ended in
        stalemate.
        """
        if turn is None:
            turn = self.turn

        for row in self.board:
            for cell in row:
                if cell[0] != 'K' and cell[1] == turn:
                    return False

        return True

    def _pgn_move_to_coords(self, move):
        """Converts a single move in PGN notation to board-state array
        coordinates.
        """
        move = list(move)
        if len(move) != 2:
            raise ValueError("_pgn_move_to_coords got input of length != 2")

        return self._pgn_rank_to_row(move[1]), self._pgn_file_to_col(move[0])

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

    def _coords_to_pgn_move(self, row, col):
        """Converts a row and column in the board-state array to a position
        in PGN (SAN) notation.
        """
        return self._col_to_pgn_file(col) + self._row_to_pgn_rank(row)

    def _row_to_pgn_rank(self, row):
        """Convert a row in the 2D board array to a numbered rank."""
        if not (0 <= row <= 7):
            raise ValueError(
                "_row_to_pgn_rank got %s (not a valid row)" % row
            )
        return str(8 - row)

    def _col_to_pgn_file(self, col):
        """Convert a column in the 2D board array to a lettered file."""
        if not (0 <= col <= 7):
            raise ValueError(
                "_col_to_pgn_file got %s (not a valid column)" % col
            )
        return chr(col + 97)

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


class GameOverError(ChessnutError):
    """Exception raised when we try to evaluate a move, but this game
    has ended.
    """
    pass
