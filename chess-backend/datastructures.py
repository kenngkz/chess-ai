import numpy as np
from math import log

class MCTSNode:
    ''' Store Q-values and actions in a tree '''

    def __init__(self, player, action, exploration_parameter, parent=None):
        self.player = player  # 1 for reward maximising player and -1 for reward minimizing player
        self.action = action
        self.exploration_parameter = exploration_parameter
        self.parent = parent
        self.score = {"reward":0, "visits":0}
        self.children = []

    def add_children(self, action_space):
        for action in action_space:
            child = MCTSNode(-self.player, action, self.exploration_parameter, self)
            self.children.append(child)

    def update_score(self, reward):
        self.score["reward"] += reward
        self.score["visits"] += 1

    def ucb(self):
        if self.score["visits"] == 0:
            return np.inf
        avg_score = self.score["reward"]/self.score["visits"]
        exploration_term = self.exploration_parameter * np.sqrt(log(self.parent.score["visits"])/self.score["visits"])
        return avg_score + exploration_term