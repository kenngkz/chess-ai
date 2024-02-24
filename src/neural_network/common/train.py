from typing import Callable, List, Optional

import numpy as np
import pandas as pd
from tensorflow.python.keras import Model

from ._load_data import load_df_from_file_name, load_X_from_df


def build_train_on_files_function(
    func_load_Y: Callable[[pd.DataFrame], np.ndarray]
) -> Callable[[Model, List[str], Optional[str]], Model]:

    def train_on_files(model: Model, files: List[str], ckpt_file: str = None):
        for file in files:
            print(f"Training on {file}")
            df = load_df_from_file_name(file)
            X = load_X_from_df(df)
            Y = func_load_Y(df)
            model.fit(X, Y)
            if ckpt_file:
                model.save(ckpt_file)
        return model

    return train_on_files
