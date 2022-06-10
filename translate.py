'''
Translates the given pgn files.

Move tuple:
    one hot with the correct move index following uci_moves in constants.py
'''

import constants
import chess.pgn
import pandas as pd

def translate_pgn(filepath, writepath="game_data.csv"):

    data = []
    
    with open(filepath, "r") as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game == None:
                break
            board = game.board()
            for move in game.mainline_moves():
                data.append([board.fen(), constants.uci_moves[move.uci()]])
                board.push(move)
    
    data = pd.DataFrame(data, columns=["board", "move"])
    data.to_csv(writepath)

if __name__ == "__main__":
    filepath = "data/chessgames2016.pgn"
    writepath = "data/chess2016.csv"

    translate_pgn(filepath, writepath)
