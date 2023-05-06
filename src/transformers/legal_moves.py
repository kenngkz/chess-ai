import chess
import numpy as np

from src import constants

def restrict_legal(move_arr, fen):
    ''' Restricts the move probability array to only legal moves and rescale remaining legal move probabilities '''
    board = chess.Board(fen)
    legal_arr = np.zeros(constants.LEN_UCI_MOVES, dtype=np.int16)
    for move in board.legal_moves:
        legal_arr[constants.uci_moves[move.uci()]] = 1
    for i in range(constants.LEN_UCI_MOVES):
        if legal_arr[i] == 0:
            move_arr[i] = 0
    return move_arr / np.sum(move_arr)