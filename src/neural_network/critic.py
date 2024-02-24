from typing import Dict, List

import numpy as np
import pandas as pd
from tensorflow.python.keras import Model, metrics

from src.neural_network.common.evaluate import build_evaluate_on_files_function
from src.neural_network.common.train import build_train_on_files_function


def load_target_outcomes(df: pd.DataFrame) -> np.ndarray:
    return df["outcome"].values


accuracy = metrics.BinaryAccuracy(name="binary_accuracy", dtype=None, threshold=0.5)
cross_entropy = metrics.BinaryCrossentropy(
    name="binary_crossentropy", dtype=None, from_logits=False, label_smoothing=0
)


def train_on_files(model: Model, files: List[str], ckpt_file: str = None) -> Model: ...


def evaluate_on_files(model: Model, files: List[str]) -> Dict[str, float]: ...


train_on_files = build_train_on_files_function(load_target_outcomes)
evaluate_on_files = build_evaluate_on_files_function(
    [accuracy, cross_entropy], load_target_outcomes
)
