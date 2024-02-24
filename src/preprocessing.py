import os
import random
from typing import List

import pandas as pd
from chess.pgn import read_game

from src.constants import UCI_MOVES
from src.transformations.fen_to_obs import _parse_fen_board, _parse_fen_misc


def split_pgn(pgn_files):
    """Split PGN games into moves in multiple CSV files with boards in FEN representation"""
    outcomes = {"1": 1.0, "1/2": 0.5, "0": 0.0}
    df = []
    file_counter = 1
    for pgn_file in pgn_files:
        print(f"{pgn_file = }")
        with open(pgn_file, "r") as f:
            game = read_game(f)
            while game != None:
                result = game.headers["Result"].split("-")
                result = outcomes[result[0]]  # 1 if white wins 0 if black wins 0.5 if stalemate
                board = game.board()
                for move in game.mainline_moves():
                    df.append(
                        {
                            "board": board.fen(),
                            "move": UCI_MOVES[move.uci()],
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


def shuffle_csv(sample_file_path, rounds=10, batch_size=10):
    files = [
        f"data/split/chess{i}.csv"
        for i in range(1, len(os.listdir(os.path.dirname(sample_file_path))) + 1)
    ]
    n_rows = 1000000
    leftover = pd.DataFrame([], columns=["board", "move", "outcome"])
    for i in range(rounds):
        print(f"round {i+1}/{rounds}")
        picked_files = random.sample(files, min(batch_size, len(files)))
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
            f"data/split/chess{len(files)+i}.csv", index=False
        )


def prep_obs_df(df: pd.DataFrame) -> pd.DataFrame:
    df["obs_board"] = df["board"].map(_parse_fen_board)
    df["obs_misc"] = df["board"].map(_parse_fen_misc)
    return df


def prep_obs_file(file_numbers):
    for n in file_numbers:
        print(f"proccessing file {n}")
        df = pd.read_csv(f"data/split/chess{n}.csv")
        df = prep_obs_df(df)
        df.to_pickle(f"data/split/processed/chess{n}.pkl")


def pgn_to_shuffled_csv(pgn_files: List[str]):
    split_pgn(pgn_files)
    shuffle_csv(pgn_files[0])
