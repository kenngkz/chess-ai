from typing import Callable, Dict, List

import numpy as np
import pandas as pd
from tensorflow.python.keras import Model, metrics

from ._load_data import load_df_from_file_name, load_X_from_df


def build_evaluate_on_files_function(
    metrics: List[metrics.Metric], func_load_Y: Callable[[pd.DataFrame], np.ndarray]
) -> Callable[[Model, List[str]], Dict[str, float]]:

    def evaluate_on_files(model: Model, files: List[str]) -> Dict[str, float]:
        for metric in metrics:
            metric.reset_state()

        for file in files:
            df = load_df_from_file_name(file)
            X = load_X_from_df(df)
            Y = func_load_Y(df)
            predictions = model.predict(X)

            for metric in metrics:
                metric.update_state(Y, predictions)

        return {metric.name: float(metric.result().numpy()) for metric in metrics}

    return evaluate_on_files
