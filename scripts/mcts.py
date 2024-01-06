import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

import random

import chess

from src.constants import STARTING_FEN
from src.mcts import MCTS, ChessState, RandomMaxDepthPolicy
from src.mcts.render import render


def random_fen():
    board = chess.Board(STARTING_FEN)
    for i in range(random.randint(10, 30)):
        board.push(random.choice([move for move in board.legal_moves]))
    return board.fen()


fen = STARTING_FEN

board = chess.Board(fen)
white_mcts = MCTS(
    timeLimitSeconds=10,
    rolloutPolicy=RandomMaxDepthPolicy(5)
)
black_mcts = MCTS(
    timeLimitSeconds=1,
    rolloutPolicy=RandomMaxDepthPolicy(5)
)

for i in range(3):
    board.push(random.choice([move for move in board.legal_moves]))



print("Starting Board")
render(board)
for _ in range(1000):
    if board.turn == chess.WHITE:
        action = white_mcts.search(ChessState(board.fen()), True)
        print(f"White {action = }")
    else:
        action = black_mcts.search(ChessState(board.fen()), True)
        print(f"Black {action = }")
    board.push(action["action"])
    print(board.fen())
    render(board)

    if board.is_game_over():
        print(board.outcome())
        break