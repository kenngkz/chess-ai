""" FEN to obs """

import chess
import numpy as np

from src.constants import SYMBOL_PIECE_INDEX_MAPPING


def parse_fen(fen: str) -> np.ndarray:
    """Output: vector with length 70"""
    board = _parse_fen_board(fen)
    misc = _parse_fen_misc(fen)

    return np.concatenate([board, misc])


def _parse_fen_board(fen: str) -> np.ndarray:
    """Output: vector with length 64, values between -6 to 6 (13 possible values)"""
    obs = np.zeros(64, dtype=np.int16)
    sections = fen.split(" ")

    index = 0
    for char in sections[0]:
        if char == "/":
            continue
        elif char.isnumeric():
            index += int(char)
        elif char in SYMBOL_PIECE_INDEX_MAPPING:
            obs[index] = SYMBOL_PIECE_INDEX_MAPPING[char]
            index += 1
        else:
            raise KeyError(f"Char {char} in board section of fen not recognized")

    return obs


def _parse_fen_misc(fen: str) -> np.ndarray:
    obs = np.zeros(6, dtype=np.int16)
    sections = fen.split(" ")

    # player to move
    if sections[1] == "w":
        obs[0] = 1
    else:
        obs[0] = -1

    # castling status
    if sections[2] == "-":
        pass
    else:
        if "K" in sections[2]:
            obs[1] = 1
        if "Q" in sections[2]:
            obs[2] = 1
        if "k" in sections[2]:
            obs[3] = 1
        if "q" in sections[2]:
            obs[4] = 1

    # under_check status
    board = chess.Board(fen)
    obs[5] = int(board.is_check())

    return obs
