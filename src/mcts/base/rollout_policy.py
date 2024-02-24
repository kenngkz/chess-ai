import random
from abc import ABC, abstractmethod

from .state import BaseState


class BasePolicy(ABC):

    @abstractmethod
    def rollout(self, state: BaseState) -> float:
        pass


class RandomPolicy(BasePolicy):
    "Take random action until terminal state is reached"

    def rollout(self, state: BaseState) -> float:
        while not state.isTerminal():
            try:
                action = random.choice(state.getPossibleActions())
            except IndexError:
                raise Exception("Non-terminal state has no possible actions: " + str(state))
            state = state.takeAction(action)
        return state.getReward()
