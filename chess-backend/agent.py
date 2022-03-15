from abc import ABC, abstractmethod
import numpy as np
import random
import time
import itertools

from datastructures import MCTSNode

class Agent(ABC):
    ''' Abstract class to define a template for agents '''
    
    @abstractmethod
    def pred(self, obs):
        pass

class RandomAgent(Agent):

    def pred(self, obs):
        return random.choice(obs)

class MCTSAgent(Agent):
    '''
    Monte Carlo Tree Search Algorithm
    Assumptions: 
      - 2 players in a zero-sum game
      - reward ranges between 0 and 1
      - ucb = average_score + explore_param*sqrt(parent_visit_count/node_visit_count)
    '''

    def __init__(self, env, explore_param=2, time_limit=10, show=False):
        self.env = env
        self.explore_param = explore_param
        self.time_limit = time_limit
        self.show = show

    def pred(self, obs):
        root = MCTSNode(player=-obs[0], action=None, exploration_parameter=self.explore_param, parent=None)
        start_time = time.perf_counter()
        root.add_children(self.env.action_space)
        for i in itertools.count():
            if self.show:
                print(f"\rIterations: {i}", end="")
            node = self._selection(root)
            node, env = self._expansion(self.env, node)
            reward = self._rollout(env)
            self._backpropogation(reward, node)
            if time.perf_counter() - start_time > self.time_limit:
                break
        result = root.children[np.argmax([child.score["visits"] for child in root.children])].action
        if self.show:
            message = f"\rMCTS terminated after {i+1} iterations. Final result: {result}\nMove - Ratio of visits - Average reward - Final UCB:\n"
            moves = {child:child.score["visits"] for child in root.children}
            total = sum(moves.values())
            for child, visits in moves.items():
                message += f"{child.action} - {visits/total if total != 0 else visits} - {child.score['reward']/visits if visits != 0 else 0} - {child.ucb()}\n"
            print(message)
        return result

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
        for action in actions:
            env_copy.step(action)
        if node.ucb() < np.inf:
            if not env_copy.done:
                node.add_children(env_copy.action_space)
                node = random.choice(node.children)
                env_copy.step(node.action)
        return node, env_copy

    def _rollout(self, env):
        if env.done:
            return env.last_reward
        while True:
            obs, reward, done, info = env.step(env.sample_action())
            if done:
                break
        return reward

    def _backpropogation(self, reward, node):
        scores = {1:reward, -1:1-reward}
        while True:
            node.update_score(scores[node.player])
            node = node.parent
            if node == None:
                return

    def _get_actions(self, node):
        # get a list of actions to execute in order to get to the state of a node
        actions = []
        while True:
            if node.parent==None:
                actions.reverse()
                return actions
            actions.append(node.action)
            node = node.parent
