''' grid search exploration parameter for mcts '''
import os
import chess
import random
import numpy as np

from src.unsupervised.mcts.agent import MCTSAgent


def search(grid_values, max_depth, n_games, max_turns=100, time_limit=5):
    agents = {v:MCTSAgent(explore_param=v, time_limit=time_limit, max_depth=max_depth, show=0) for v in grid_values}
    scores = {v:[] for v in grid_values}

    v_started = []
    si = 0
    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as f:
            scores = eval(f.read())
        v_started = [v for v, ls in scores.items() if len(ls) > 0]
        si = len(scores[max(v_started)]) if len(v_started) > 0 else 0

    for v, agent in agents.items():
        opps = [a for a in agents.values() if a != agent]
        if len(scores[v]) >= n_games:
            continue
        for i in range(si, n_games):
            opp = random.choice(opps)
            board = chess.Board()
            player_to_start = random.choice([True, False])
            player_to_move = player_to_start
            players = {True:agent, False:opp}
            for t in range(max_turns):
                print(f"\rAgent value: {v} Game: {i+1}/{n_games} Turn: {t+1}/{max_turns}", end="")
                player = players[player_to_move]
                player_to_move = not player_to_move
                board.push(player.pred(board.fen()))
                outcome = board.outcome()
                if outcome:
                    scores[v].append(int(outcome.winner == player_to_start))
                    break
            else:
                scores[v].append(agent._estimate_value(board.fen()))
            print("")
            with open("scores.txt", "w") as f:
                f.write(str(scores))
        si = 0
    return {v:sum(l) for v, l in scores.items()}

if __name__ == "__main__":
    grid = np.linspace(0,3,7)
    print(grid)
    scores = search(grid_values=grid, max_depth=10, n_games=20, max_turns=100, time_limit=5)
    print(scores)