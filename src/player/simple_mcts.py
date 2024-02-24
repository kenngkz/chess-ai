import math

from chess import Move

from src.mcts import MCTS, ChessState, RandomMaxDepthPolicy
from src.schema.player import Player


class SimpleMCTSPlayer(Player):

    def __init__(
        self,
        timeLimitSeconds: float = None,
        iterationLimit=None,
        explorationConstant=1 / math.sqrt(2),
    ) -> None:
        self.mcts = MCTS(
            timeLimitSeconds,
            iterationLimit,
            explorationConstant,
            rolloutPolicy=RandomMaxDepthPolicy,
        )

    def select_move(self, fen_board: str) -> Move:
        prediction = self.mcts.search(ChessState(fen_board))
        return prediction["action"]
