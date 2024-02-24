from tensorflow.python.keras import Model

from .buffer import GameBuffer
from .single_game import play_game


class SimpleSelfPlay:

    def __init__(self, actor_model: Model, critic_model: Model, buffer_size: int):
        self.actor = actor_model
        self.buffer = GameBuffer(buffer_size)

    def train(self, n_games: int, train_frequency_games: int, ckpt_path: str = None) -> Model:

        training_counter = 0
        for i in range(n_games):
            game_steps = play_game(self.actor, self.actor)
            self.buffer.push(game_steps)
            training_counter += 1
            if training_counter >= train_frequency_games:
                training_counter = 0
                # train actor model here...
                if ckpt_path:
                    self.actor.save(ckpt_path)
        return self.actor
