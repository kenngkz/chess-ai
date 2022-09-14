import chess
import time
import random
import itertools
import os
import numpy as np
import pandas as pd
from math import log

import utils

logger = utils.get_logger("mcts")

class MCTSNode:

    def __init__(self, player, action=None, parent=None):
        self.player = player
        self.action = action
        self.parent = parent
        self.score = {"reward":0, "visits":0}
        self.children = []

    def add_children(self, action_space):
        for action in action_space:
            child = MCTSNode(-self.player, action, self)
            self.children.append(child)

    def update_score(self, reward):
        self.score["reward"] += reward
        self.score["visits"] += 1

    def ucb(self, explore_param):
        if self.score["visits"] == 0:
            return np.inf
        avg_score = self.score["reward"]/self.score["visits"]
        exploration_term = explore_param * np.sqrt(log(self.parent.score["visits"])/self.score["visits"])
        return avg_score + exploration_term

class MCTSAgent:

    def __init__(self, explore_param=2, time_limit=10, show=0, max_depth=np.inf):
        '''
        Intialization args:
            expore_param: hyperparameter controlling incentive to explore unvisited nodes
            time_limit: search will quit after the specified number of seconds
            show: show results breakdown if 1, also show the search progress if 2
            max_depth: max number of steps to run rollout, if max_depth is hit during rollout, the agent will estimate the value of the state
        '''
        self.explore_param = explore_param
        self.time_limit = time_limit
        self.show = show
        self.max_depth = max_depth
        self.turn = 0

    def pred(self, fen):
        root = MCTSNode(int(fen.split(" ")[1]!="w") * 2 - 1)
        start_time = time.time()
        total_time = total_depth = start = end = depth = reward = 0
        root.add_children([move for move in chess.Board(fen).legal_moves])
        highest_children = []
        for i in itertools.count():
            if self.show > 0:
                print(f"\rIterations: {i}  -  Last rollout stats - time: {end-start:.4f}, depth: {depth}, reward: {reward:.4f}        ", end="")
            node = self._selection(root)
            node, board = self._expansion(fen, node)
            start = time.perf_counter()
            reward, depth = self._rollout(board)
            end = time.perf_counter()
            total_time += end - start
            total_depth += depth
            node = self._backpropogation(reward, node)
            if len(highest_children) < 2:
                highest_children.append(node)
            else:
                if node.score["visits"] > highest_children[0].score["visits"]:
                    highest_children = [node, highest_children[0]]
                elif node.score["visits"] > highest_children[1].score["visits"] and node != highest_children[0]:
                    highest_children[1] = node
                if highest_children[0].score["visits"] > highest_children[1].score["visits"] + 50:
                    why = "found"
                    break
            if time.time() - start_time > self.time_limit:
                why = "time"
                break
        max_visit = max([child.score["visits"] for child in root.children])
        most_visited_children = [child for child in root.children if child.score["visits"] == max_visit]
        max_reward = max([child.score["reward"] for child in most_visited_children])
        best_children = [child for child in most_visited_children if child.score["reward"] == max_reward]
        result = random.choice(best_children).action
        if self.show > 0:
            print(f"\rMCTS terminated after {i+1} iterations. Final result: {result} with {max_visit} visits. Average rollout time: {total_time/i:.4f}. Average depth: {total_depth/i:.4f}")
        logger.debug(f"MOVE - turn:{self.turn} reason:{why} action:{result.uci()} iters:{i+1} max_visit:{max_visit} avg_rollout_time:{total_time/i:.4f} avg_depth:{total_depth/i:.4f} state:{fen}")
        if self.show > 1:
            distribution = pd.DataFrame({
                "action":[child.action.uci() for child in root.children], 
                "visits":[child.score["visits"] for child in root.children], 
                "reward":[child.score["reward"] for child in root.children], 
                "ucb":[child.ucb(self.explore_param) for child in root.children]
                }, 
            columns=["turn", "state", "action", "visits", "reward", "ucb"]
            )
            distribution["turn"] = self.turn
            self.turn += 1
            distribution["state"] = fen
            distribution.to_csv("distribution.csv", mode="a", header=not os.path.exists("distribution.csv"), index=False)
        return result

        
    def _selection(self, root_node):
        ''' Selects the leaf node by successively picking branches with the highest UCB score '''
        current_node = root_node
        while True:
            children = current_node.children
            if len(children) == 0:
                return current_node
            max_ucb = max([child.ucb(self.explore_param) for child in children])
            current_node = random.choice([child for child in children if child.ucb(self.explore_param) == max_ucb])
        

    def _expansion(self, fen, node):
        board = chess.Board(fen)
        actions = self._get_actions(node)
        for action in actions:
            board.push(action)
        if node.ucb(self.explore_param) < np.inf:
            if not board.is_game_over():
                node.add_children([move for move in board.legal_moves])
                node = random.choice(node.children)
                board.push(node.action)
        return node, board


    def _rollout(self, board):
        outcome = board.outcome()
        if outcome:
            return int(outcome.winner) if outcome.winner != None else 0, 0
        for i in itertools.count():
            if i < self.max_depth:
                board.push(random.choice([move for move in board.legal_moves]))
                outcome = board.outcome()
                if outcome:
                    reward = int(outcome.winner) if outcome.winner != None else 0
                    break
            else:
                reward = self._estimate_value(board.fen())
                break
        return reward, i


    def _backpropogation(self, reward, node):
        scores = {1:reward, -1:1-reward}
        while True:
            node.update_score(scores[node.player])
            if node.parent.action == None:
                node.parent.update_score(scores[node.parent.player])
                return node
            node = node.parent


    def _get_actions(self, node):
        # get a list of actions to execute in order to get to the state of a node
        actions = []
        while True:
            if node.parent==None:
                actions.reverse()
                return actions
            actions.append(node.action)
            node = node.parent


    def _estimate_value(self, fen):
        ''' Estimates the value of a observation by summing relative piece values and check_status ''' 
        obs = utils.parse_fen(fen)
        check_penalty = 5
        piece_values = {1:1, 2:3, 3:3, 4:5, 5:9, 6:0, 0:0, -1:-1, -2:-3, -3:-3, -4:-5, -5:-9, -6:0}
        reward_scaling_factor = 70  # scales the reward to typically be within range (-0.5, 0.5)
        reward = 0
        for index in range(64):
            reward += piece_values[obs[index+1]]
        if obs[-2]: # if white under check
            reward -= check_penalty
        elif obs[-1]: # if black under check
            reward += check_penalty
        return 0.5 + reward / reward_scaling_factor


def render(board):
    print("-"*20)
    print(board)
    print("-"*20)

if __name__ == "__main__":
    board = chess.Board()
    mcts = MCTSAgent(show=0, max_depth=30, time_limit=15)

    # for i in range(20):
    #     board.push(random.choice([move for move in board.legal_moves]))

    for i in range(80):

        print("")
        action = mcts.pred(board.fen())
        if i % 2 == 0:
            print(f"White {action = }")
        else:
            print(f"Black {action = }")
        board.push(action)
        render(board)

        if board.is_game_over():
            break