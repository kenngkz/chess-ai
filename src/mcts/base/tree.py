import math
import random
import time

from .node import MCTSNode
from .rollout_policy import BasePolicy, RandomPolicy
from .state import BaseState


class MCTS():
    def __init__(self, timeLimitSeconds:float=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy:BasePolicy=RandomPolicy):
        if timeLimitSeconds != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimitSeconds
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout_policy = rolloutPolicy

    def search(self, initialState:BaseState, needDetails:bool=False):
        self.root = MCTSNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        action=(action for action, node in self.root.children.items() if node is bestChild).__next__()
        if needDetails:
            return {"action": action, "expectedReward": bestChild.totalReward / bestChild.numVisits, "totalRollouts":self.root.numVisits}
        else:
            return action

    def executeRound(self):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        node = self.selectNode(self.root)
        reward = self.rollout_policy.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node: MCTSNode):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node: MCTSNode):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = MCTSNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node: MCTSNode, reward:float):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node:MCTSNode, explorationValue:float):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = node.state.getCurrentPlayer() * child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)
    