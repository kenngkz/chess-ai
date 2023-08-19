import chess
from chess.pgn import read_game
import random
import pandas as pd

import constants
from transformations.fen_to_obs import parse_fen_board, parse_fen_misc


def split_pgn():
    """Split PGN games into moves in multiple CSV files with boards in FEN representation"""
    pgn_files = [f"data/raw/chessgames20{i}.pgn" for i in range(16, 22)]
    outcomes = {"1": 1.0, "1/2": 0.5, "0": 0.0}
    df = []
    file_counter = 1
    for pgn_file in pgn_files:
        print(f"{pgn_file = }")
        with open(pgn_file, "r") as f:
            game = read_game(f)
            while game != None:
                result = game.headers["Result"].split("-")
                result = outcomes[
                    result[0]
                ]  # 1 if white wins 0 if black wins 0.5 if stalemate
                board = game.board()
                for move in game.mainline_moves():
                    df.append(
                        {
                            "board": board.fen(),
                            "move": constants.uci_moves[move.uci()],
                            "outcome": result,
                        }
                    )
                    board.push(move)
                if len(df) >= 1000000:
                    df = pd.DataFrame(df)
                    df.to_csv(f"data/split/chess{file_counter}.csv", index=False)
                    file_counter += 1
                    df = []
                game = read_game(f)


def shuffle_csv(rounds=10, batch_size=10):
    files = [f"data/split/chess{i}.csv" for i in range(1, 27)]
    n_rows = 1000000
    leftover = pd.DataFrame([], columns=["board", "move", "outcome"])
    for i in range(rounds):
        print(f"round {i+1}/{rounds}")
        picked_files = random.sample(files, batch_size)
        df = pd.DataFrame([], columns=["board", "move", "outcome"])
        for file in picked_files:
            df = pd.concat([df, pd.read_csv(file)], ignore_index=True)
        df = df.sample(frac=1)
        for n, file in enumerate(picked_files):
            df.iloc[(n_rows * n) : (n_rows * (n + 1)), :].to_csv(file, index=False)
        leftover = pd.concat([leftover, df.iloc[(n_rows * (n + 1)) :, :]])
    leftover = leftover.sample(frac=1)
    for i in range(len(leftover) // n_rows + 1):
        leftover.iloc[(n_rows * i) : (n_rows * (i + 1))].to_csv(
            f"data/split/chess{27+i}.csv", index=False
        )


def process_df(df):
    df["obs_board"] = df["board"].map(parse_fen_board)
    df["obs_misc"] = df["board"].map(parse_fen_misc)
    return df


def process_file(file_numbers):
    for n in file_numbers:
        print(f"proccessing file {n}")
        df = pd.read_csv(f"data/split/chess{n}.csv")
        df = process_df(df)
        df.to_pickle(f"data/split/processed/chess{n}.pkl")


def process_raw_data(file_numbers=[1, 2, 3, 4, 5]):
    split_pgn()
    shuffle_csv()
    process_file(file_numbers)
