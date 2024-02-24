import numpy as np
import pandas as pd
import tensorflow as tf

from src.neural_network.common.evaluate import build_evaluate_on_files_function
from src.neural_network.common.train import build_train_on_files_function


def load_outcomes(df: pd.DataFrame) -> np.ndarray:
    return df["outcome"].values


accuracy = tf.keras.metrics.BinaryAccuracy(name="binary_accuracy", dtype=None, threshold=0.5)
cross_entropy = tf.keras.metrics.BinaryCrossentropy(
    name="binary_crossentropy", dtype=None, from_logits=False, label_smoothing=0
)


# train and evaluate functions
train_on_files = build_train_on_files_function(load_outcomes)
evaluate_on_files = build_evaluate_on_files_function([accuracy, cross_entropy], load_outcomes)
