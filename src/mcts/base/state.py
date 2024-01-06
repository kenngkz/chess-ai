from abc import ABC, abstractmethod
from typing import Any, List, Literal


class BaseState(ABC):

    @abstractmethod
    def getCurrentPlayer(self) -> Literal[1, -1]:
        pass

    @abstractmethod
    def getPossibleActions(self) -> List[Any]:
        pass

    @abstractmethod
    def takeAction(self, Any) -> "BaseState":
        pass

    @abstractmethod
    def isTerminal(self) -> bool:
        pass
    
    @abstractmethod
    def getReward(self) -> float:
        pass
