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
            game_data = []
            for move in game.mainline_moves():
                game_data.append([board.fen(), constants.uci_moves[move.uci()], None])
                board.push(move)
            outcome = board.outcome()
            for row in game_data:
                row[2] = outcome
            data += game_data   
    
    data = pd.DataFrame(data, columns=["board", "move", "outcome"])
    data.to_csv(writepath)

if __name__ == "__main__":
    import os

    # years = ["2016", "2017", "2018", "2019", "2020", "2021"]
    # for year in years:
    #     print(f"Processing year {year}")

    #     filepath = f"data/chessgames{year}.pgn"
    #     writepath = f"data/chess{year}.csv"

    #     if not os.path.exists(writepath):
    #         translate_pgn(filepath, writepath)

    translate_pgn("data/test.pgn", "data/test.csv")