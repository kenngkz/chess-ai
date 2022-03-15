from abc import ABC, abstractmethod
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

    def pred(self, obs):
        pass

    def _selection(self, root_node):
        ''' Selects the leaf node by successively picking branches with the highest UCB score '''
        current_node = root_node
        while True:
            children = current_node.children
            if len(children) == 0:
                return current_node
            current_node = children[np.argmax([child.ucb() for child in children])]

    def _expansion(self, env, node):
        env_copy = env.copy()
        actions = self._get_actions(node)
        for action in range(actions):
            env_copy.step(action)
        # TODO

    def _rollout(self, env):
        pass

    def _backpropogation(self, reward, terminal_node):
        pass

    def _get_actions(node):
        # get a list of actions to execute in order to get to the state of a node
        actions = []
        while True:
            if node.parent==None:
                actions.reverse()
                return actions
            actions.append(node.action)
            node = node.parent
