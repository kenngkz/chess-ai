import pandas as pd
import tensorflow as tf

from src.constants import LEN_UCI_MOVES
from src.neural_network.common.train import build_train_on_files_function


def load_moves(df:pd.DataFrame):
    return tf.one_hot(df["move"].values, depth=LEN_UCI_MOVES).numpy()
train_on_file = build_train_on_files_function(load_moves)

