from abc import ABC, abstractmethod

import chess


class Player(ABC):
    """Base class for a player in a chess game"""

    @abstractmethod
    def select_move(self, fen_board: str) -> chess.Move:
        pass
