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
    import os

    years = ["2016", "2017", "2018", "2019", "2020", "2021"]
    for year in years:
        print(f"Processing year {year}")

        filepath = f"data/chessgames{year}.pgn"
        writepath = f"data/chess{year}.csv"

        if not os.path.exists(writepath):
            translate_pgn(filepath, writepath)
