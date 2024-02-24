import random

from .base.rollout_policy import BasePolicy
from .base.state import BaseState


class RandomMaxDepthPolicy(BasePolicy):

    def __init__(self, max_depth: int = 5):
        self.max_depth = max_depth

    def rollout(self, state: BaseState) -> float:
        for _ in range(self.max_depth):
            if state.isTerminal():
                break
            try:
                action = random.choice(state.getPossibleActions())
            except IndexError:
                raise Exception("Non-terminal state has no possible actions: " + str(state))
            state = state.takeAction(action)
        return state.getReward()
