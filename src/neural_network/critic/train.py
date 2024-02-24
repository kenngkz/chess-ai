import pandas as pd

from src.neural_network.common.train import build_train_on_files_function


def load_outcomes(df:pd.DataFrame):
    return df["outcome"].values
train_on_file = build_train_on_files_function(load_outcomes)

