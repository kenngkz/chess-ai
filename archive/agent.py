from abc import ABC, abstractmethod
import numpy as np
import random
import time
import itertools
from math import log

class Agent(ABC):
    ''' Abstract class to define a template for agents '''
    
    @abstractmethod
    def pred(self, obs):
        pass
##################
###   Random   ###
##################

class RandomAgent(Agent):

    def __init__(self, env):
        self.env = env

    def pred(self, obs):
        return random.choice(self.env.action_space)

###################################
###   Monte Carlo Tree Search   ###
###################################

class MCTSNode:

    def __init__(self, player, action, exploration_parameter, parent=None):
        self.player = player  # 1 for reward maximising player and -1 for reward minimizing player
        self.action = action
        self.exploration_parameter = exploration_parameter
        self.parent = parent
        self.score = {"reward":0, "visits":0}
        self.update = False
        self.last_ucb = np.inf
        self.children = []

    def add_children(self, action_space):
        for action in action_space:
            child = MCTSNode(-self.player, action, self.exploration_parameter, self)
            self.children.append(child)

    def update_score(self, reward):
        self.score["reward"] += reward
        self.score["visits"] += 1
        self.update = True

    def ucb(self):
        if self.update:
            avg_score = self.score["reward"]/self.score["visits"]
            exploration_term = self.exploration_parameter * np.sqrt(log(self.parent.score["visits"])/self.score["visits"])
            self.last_ucb = avg_score + exploration_term
            self.update = False
        return self.last_ucb

class MCTSAgent(Agent):
    '''
    Monte Carlo Tree Search Algorithm
    Assumptions: 
      - 2 players in a zero-sum game: 1 representing reward maximising player and -1 representing reward minimizing player
      - reward ranges between 0 and 1
      - ucb = average_score + explore_param*sqrt(parent_visit_count/node_visit_count)
    '''

    def __init__(self, env, explore_param=2, time_limit=10, show=0, max_depth=np.inf):
        '''
        Intialization args:
            env: The environment that the agent will be operating in (env requires .copy() method)
            expore_param: hyperparameter controlling incentive to explore unvisited nodes
            time_limit: search will quit after the specified number of seconds
            show: show results breakdown if 1, also show the search progress if 2
            max_depth: max number of steps to run rollout, if max_depth is hit during rollout, the agent will estimate the value of the state
        '''
        self.env = env
        self.explore_param = explore_param
        self.time_limit = time_limit
        self.show = show
        self.max_depth = max_depth

    def pred(self, obs):
        ''' Predict the best action from the env.action_space (given during init). Require obs[0] to specify player '''
        root = MCTSNode(player=-obs[0], action=None, exploration_parameter=self.explore_param, parent=None)
        start_time = time.perf_counter()
        start = end = depth = reward = 0
        root.add_children(self.env.action_space)
        total_time = total_depth = 0
        for i in itertools.count():
            if self.show == 2:
                print(f"\rIterations: {i}  -  Last rollout stats - time: {end-start:.4f}, depth: {depth}, reward: {reward:.4f}        ", end="")
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
        max_visit = max([child.score["visits"] for child in root.children])
        most_visited_children = [child for child in root.children if child.score["visits"] == max_visit]
        max_reward = max([child.score["reward"] for child in most_visited_children])
        best_children = [child for child in most_visited_children if child.score["reward"] == max_reward]
        result = random.choice(best_children).action
        if self.show > 0:
            message = f"\rMCTS terminated after {i+1} iterations. Final result: {result} with {max_visit} visits. Average rollout time: {total_time/i:.4f}. Average depth: {total_depth/i:.4f}\nMove    - Visit ratio - Average reward - Final UCB:\n"
            moves = {child:child.score["visits"] for child in root.children}
            total = sum(moves.values())
            for child, visits in moves.items():
                message += f"{child.action}".ljust(7) + " - "
                message += f"{visits/total if total != 0 else visits:.5f}".ljust(11) + " - "
                message += f"{child.score['reward']/visits if visits != 0 else 0:.5f}".ljust(14) + " - "
                message += f"{child.ucb():.5f}".ljust(9) + "\n"
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
            return env.last_reward, 0
        for i in itertools.count():
            if i < self.max_depth:
                obs, reward, done, info = env.step(env.sample_action())
                if done:
                    break
            else:
                reward = self._estimate_value(obs)
                break
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
        reward_scaling_factor = 30  # scales the reward to typically be within range (0, 1)
        reward = 0
        for index in range(64):
            reward += piece_values[obs[index+1]]
        if obs[-2]: # if white under check
            reward -= check_penalty
        elif obs[-1]: # if black under check
            reward += check_penalty
        return 0.5 + reward / reward_scaling_factor