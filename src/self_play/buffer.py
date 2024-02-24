from typing import List

from .single_game import GameStep


class GameBuffer:

    def __init__(self, buffer_size: int) -> None:
        self.buffer_size = buffer_size
        self.reset()

    def reset(self) -> None:
        self.buffer = []

    def push(self, game_steps: List[GameStep]) -> None:
        overflow_steps = len(self.buffer) + len(game_steps) - self.buffer_size
        if overflow_steps > 0:
            self.buffer = self.buffer[overflow_steps:]
        self.buffer += game_steps

    def get_buffer(self) -> List[GameStep]:
        return self.buffer
