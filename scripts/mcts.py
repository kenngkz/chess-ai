import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

import chess

from src.constants import STARTING_FEN
from src.mcts.agent import MCTSAgent, render

if __name__ == "__main__":
    state = STARTING_FEN
    board = chess.Board(state)
    white_mcts = MCTSAgent(
        side_is_white=True,
        show=MCTSAgent.ShowLevel.MOVE,
        max_depth=5,
        time_limit=60,
        explore_param=0.2,
        ucb_base=None,
    )
    black_mcts = MCTSAgent(
        side_is_white=False,
        show=MCTSAgent.ShowLevel.MOVE,
        max_depth=5,
        time_limit=60,
        explore_param=0.2,
    )

    # for i in range(20):
    #     board.push(random.choice([move for move in board.legal_moves]))

    for _ in range(1000):
        if board.turn == chess.WHITE:
            action = white_mcts.pred(board.fen())
            print(f"White {action = }")
        else:
            action = black_mcts.pred(board.fen())
            print(f"Black {action = }")
        board.push(action)
        render(board)

        if board.is_game_over():
            print(board.outcome())
            break
