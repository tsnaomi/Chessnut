#!usr/bin/env Python

from os.path import isfile
from PIL import Image

start = 'rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR'


def board(state=start):
    if isfile('chessnut/static/boards/%s.png' % state):
        return Image.open('chessnut/static/boards/%s.png' % state)
    BOARD = Image.open('chessnut/static/elements/board.png').copy()
    pieces = {'b': 'bishop', 'k': 'king', 'n': 'knight', 'q': 'queen',
              'p': 'pawn', 'r': 'rook'}
    glow = Image.open('chessnut/static/elements/glow.png')
    if len(state) == 67:  # CASTLING GLOWS
        r = 0 if state[64] == "B" else 7
        columns = [4, 5, 6, 7] if state[65] == "K" else [0, 2, 3, 4]
        for c in columns:  # NORMAL GLOWS
            BOARD.paste(glow, (26 + (58 * c), 11 + (58 * r)), glow)
    if len(state) == 68:
        BOARD.paste(glow, (26 + (58 * int(state[64])),
                           11 + (58 * int(state[65]))), glow)
        BOARD.paste(glow, (26 + (58 * int(state[66])),
                           11 + (58 * int(state[67]))), glow)
    for index, i in enumerate(state[:64]):  # PLACING PIECES ON BOARD
        if i != '0':
            c = index % 8 if i != 0 else 0
            r = (index - c) // 8 if i != 0 else 0
            p = Image.open('chessnut/static/elements/%s.png' %
                           pieces[i.lower()])
            if i in 'rnbqkp':
                BOARD.paste(p, (26 + (58 * c), 11 + (58 * r)), p)
            else:
                BOARD.paste((91, 94, 243), (26 + (58 * c), 11 + (58 * r)), p)
    BOARD.save('chessnut/static/boards/%s.png' % state)
    return BOARD

if __name__ == '__main__':
    board().show()
