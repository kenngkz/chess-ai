'''
Translates the given pgn files.

Move tuple:
    one hot with the correct move index following uci_moves in constants.py
'''

import constants
import chess.pgn
import utils

def translate_pgn(filepath, writepath="game_data.txt"):

    data = []
    
    with open(filepath, "r") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game == None:
                break
            board = game.board()
            for move in game.mainline_moves():
                move_tup = list(range(272))
                move_tup[constants.uci_moves[move.uci()]] = 1
                data.append([utils.parse_fen(board.fen()), tuple(move_tup)])
                board.push(move)
    
    with open(writepath, "w") as f:
        f.write(data)
                


if __name__ == "__main__":
    filepath = "data/test.pgn"
    writepath = "data/test.txt"

    translate_pgn(filepath, writepath)
