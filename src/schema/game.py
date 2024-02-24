from typing import TypedDict


class GameStep(TypedDict):
    board: str
    outcome: float  # 1 for white win, 0 for black win, 0.5 for stalemate
