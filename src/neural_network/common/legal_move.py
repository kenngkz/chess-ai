from typing import List

import chess
import tensorflow as tf

from src.transformations.move import index_to_move


def pick_top_legal_move(fen: str, predictions: List[float]) -> chess.Move:
    board = chess.Board(fen)
    predictions_with_index = [(idx, conf) for idx, conf in enumerate(predictions)]
    predictions_with_index.sort(key=lambda x: x[1], reverse=True)
    for idx, conf in predictions_with_index:
        move = index_to_move(idx)
        if board.is_legal(move):
            return move
    raise Exception(f"No legal move selected!")


def pick_prob_top_legal_move(fen: str, predictions: List[float]) -> chess.Move:
    board = chess.Board(fen)
    predictions_with_index = [[idx, conf] for idx, conf in enumerate(predictions)]
    for idx, conf in predictions_with_index:
        move = index_to_move(idx)
        if not board.is_legal(move):
            predictions_with_index[idx][1] = 0
    selected = tf.random.categorical(
        tf.math.log([[conf for idx, conf in predictions_with_index]]), num_samples=1
    )[0, 0]
    return index_to_move(int(selected))
