import numpy as np
import pandas as pd
import tensorflow as tf

from src.constants import LEN_UCI_MOVES
from src.neural_network.common.evaluate import build_evaluate_on_files_function
from src.neural_network.common.train import build_train_on_files_function


def load_target_moves(df: pd.DataFrame) -> np.ndarray:
    return tf.one_hot(df["move"].values, depth=LEN_UCI_MOVES).numpy()


accuracy = tf.keras.metrics.CategoricalAccuracy(name="categorical_accuracy", dtype=None)
cross_entropy = tf.keras.metrics.CategoricalCrossentropy(
    name="categorical_crossentropy", dtype=None, from_logits=False, label_smoothing=0
)


# train and evaluate functions
train_on_files = build_train_on_files_function(load_target_moves)
evaluate_on_files = build_evaluate_on_files_function([accuracy, cross_entropy], load_target_moves)
