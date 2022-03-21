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

    def __init__(self, env, explore_param=2, time_limit=10, show=False, max_depth=np.inf):
        self.env = env
        self.explore_param = explore_param
        self.time_limit = time_limit
        self.show = show
        self.max_depth = max_depth

    def pred(self, obs):
        root = MCTSNode(player=-obs[0], action=None, exploration_parameter=self.explore_param, parent=None)
        start_time = time.perf_counter()
        start = end = depth = reward = 0
        root.add_children(self.env.action_space)
        total_time = total_depth = 0
        for i in itertools.count():
            if self.show:
                print(f"\rIterations: {i}  -  Last rollout stats - time: {end-start:.4f}, depth: {depth}, reward: {reward}        ", end="")
            node = self._selection(root)
            node, env = self._expansion(self.env, node)
            start = time.perf_counter()
            reward, depth = self._rollout(env)
            end = time.perf_counter()
            total_time += end - start
            total_depth += depth
            self._backpropogation(reward, node)
            if time.perf_counter() - start_time > self.time_limit:
                break
        result = root.children[np.argmax([child.score["visits"] for child in root.children])].action
        if self.show:
            message = f"\rMCTS terminated after {i+1} iterations. Final result: {result}. Average rollout time: {total_time/i}. Average depth: {total_depth/i}\nMove - Ratio of visits - Average reward - Final UCB:\n"
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
        for i in itertools.count():
            if i < self.max_depth:
                obs, reward, done, info = env.step(env.sample_action())
                if done:
                    break
            else:
                reward = self._estimate_value(obs)
        return reward, i

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

    def _estimate_value(self, obs):
        ''' Estimates the value of a observation by summing relative piece values and check_status ''' 
        check_penalty = 5
        piece_values = {1:1, 2:3, 3:3, 4:5, 5:9, 6:0, 0:0, -1:-1, -2:-3, -3:-3, -4:-5, -5:-9, -6:0}
        reward_scaling_factor = 60  # scales the reward to be within range (-1, 1)
        reward = 0
        for index in range(64):
            reward += piece_values[obs[index+1]]
        if obs[-2]: # if white under check
            reward -= check_penalty
        elif obs[-1]: # if black under check
            reward += check_penalty
        return reward / reward_scaling_factor