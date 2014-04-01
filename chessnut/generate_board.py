#!usr/bin/env Python

from PIL import Image

start = 'rnbqkbnrpppppppp00000000000000000000000000000000PPPPPPPPRNBQKBNR'


def board(state=start):
    BOARD = Image.open('static/board.png').copy()
    pieces = {'b': 'bishop', 'k': 'king', 'n': 'knight', 'q': 'queen',
              'p': 'pawn', 'r': 'rook'}
    glow = Image.open('static/glow.png')
    if len(state) == 68:
        BOARD.paste(glow, (89 + (200 * int(state[64])),
                           38 + (198 * int(state[65]))), glow)
        BOARD.paste(glow, (89 + (200 * int(state[66])),
                           38 + (198 * int(state[67]))), glow)
    for index, i in enumerate(state[:64]):
        if i != '0':
            c = index % 8 if i != 0 else 0
            r = (index - c) // 8 if i != 0 else 0
            p = Image.open('static/%s.png' % pieces[i.lower()])
            if i in "rnbqkbnrp":
                BOARD.paste(p, (90 + (200 * c), 38 + (200 * r)), p)
            else:
                BOARD.paste((91, 94, 243), (90 + (200 * c), 38 + (200 * r)), p)
    BOARD.save('static/boards/%s.png' % state)
    # BOARD.show()
    return BOARD

if __name__ == '__main__':
    board()
