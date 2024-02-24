import chess
import numpy as np
from tensorflow.python.keras import Model

from src.transformations.fen_to_obs import parse_fen
from src.transformations.move import index_to_move


class SelfPlay:

    def __init__(self, actor_model: Model, critic_model: Model):
        self.actor = actor_model
        self.critic = critic_model
        self.buffer = []  # TODO: make overflow prevention

    def play_game(self):
        board = chess.Board()

        game_history = []
        for _ in range(1000):
            obs = np.array([parse_fen(board.fen())])
            predictions = self.actor.predict(obs)
            selection_index = np.argmax(predictions[0])
            move = index_to_move(selection_index)
            game_history.append({"board": board.fen(), "outcome": None})
            board.push(move)
            outcome = board.outcome()
            if outcome:
                for step in game_history:
                    step["outcome"] = int(outcome.winner == chess.WHITE)
                break
        else:
            raise Exception(f"Max turns reached!")

        self.buffer += game_history
