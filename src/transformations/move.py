from typing import Union

import chess

from src.constants import UCI_MOVES

index_to_move_mapping = [move for move, idx in list(UCI_MOVES.items())]


def move_to_index(move: Union[str, chess.Move]):
    if isinstance(move, chess.Move):
        move = move.uci()
    return UCI_MOVES[move]


def index_to_move(index: int) -> chess.Move:
    return index_to_move_mapping[index]
