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

                # DOCUMENTATION for next steps
                # ActorModel with custom fit function that uses the prediction of CriticModel as the loss
                # Implementation
                #   inherit from keras.Model
                #   __init__ -> load the NN, feed in loss function (default to model's loss)
                #   train_step -> use the loss function (this would be the CriticModel's prediction)
                #       see https://www.tensorflow.org/guide/keras/customizing_what_happens_in_fit
                # Loss function based on CriticModel predictions
                #   take care that the loss for black would be inverted
                if ckpt_path:
                    self.actor.save(ckpt_path)
        return self.actor


# two ideas for how to fit the actor
# 1. one-step lookahead
#   - for a board state in training, we compute the critic prediction for the states after every legal action
#   - use critic prediction
