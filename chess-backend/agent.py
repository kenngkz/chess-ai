from abc import ABC, abstractmethod
from math import log
import numpy as np
import random

class Agent(ABC):
    ''' Abstract class to define a template for agents '''
    
    @abstractmethod
    def pred(self, obs):
        pass

class RandomAgent(Agent):

    def pred(self, obs):
        return random.choice(obs)

class MCTSAgent(Agent):
    ''' Monte Carlo Tree Search Algorithm '''
    class Node:
        ''' Store Q-values and actions in a tree '''

        def __init__(self, action, exploration_parameter, parent=None):
            self.action = action
            self.exploration_parameter = exploration_parameter
            self.parent = parent
            self.score = {"reward":0, "visits":0}
            self.children = []

        def add_children(self, action_space):
            for action in action_space:
                child = Node(action, self.exploration_parameter, self)
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

    def pred(self, obs):
        pass

    def selection(root_node):
        current_node = root_node
        while True:
            children = current_node.children
            if len(children) == 0:
                return current_node
            current_node = children[np.argmax([child.ucb() for child in children])]

    def expansion(node):
        pass  # TODO