import numpy as np
from chess import Move
from tensorflow.python.keras import Model
from tensorflow.python.keras.models import load_model

from src.schema.player import Player
from src.transformations.fen_to_obs import parse_fen
from src.transformations.move import index_to_move


class NNPlayer(Player):

    def __init__(self, model: Model = None, ckpt_path: str = None) -> None:
        if not model and not ckpt_path:
            raise ValueError("Either one of `model` or `ckpt_path` is required.")
        if model:
            self.model = model
        else:
            self.model = load_model(ckpt_path)

    def select_move(self, fen_board: str) -> Move:
        obs = np.array([parse_fen(fen_board)])
        predictions = self.model.predict(obs)
        selection_index = np.argmax(predictions[0])
        return index_to_move(selection_index)
