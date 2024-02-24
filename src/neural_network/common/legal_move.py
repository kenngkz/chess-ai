from typing import List

import chess

from src.transformations.move import index_to_move


def pick_top_legal_move(fen: str, predictions: List[float]) -> chess.Move:
    board = chess.Board(fen)
    predictions_with_index = [(idx, conf) for idx, conf in enumerate(predictions)]
    predictions_with_index.sort(key=lambda x: x[1], reverse=True)å
    for idx, conf in predictions_with_index:
        move = index_to_move(idx)
        if board.is_legal(move):
            return move
    raise Exception(f"No legal move selected!")
