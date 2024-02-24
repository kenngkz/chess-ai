import numpy as np
from chess import Move
from tensorflow.python.keras import Model
from tensorflow.python.keras.models import load_model

from src.neural_network.common.legal_move import pick_top_legal_move
from src.schema.player import Player
from src.transformations.fen_to_obs import parse_fen


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
        predictions = self.model.predict(obs, verbose=0)
        return pick_top_legal_move(fen_board, predictions[0])
