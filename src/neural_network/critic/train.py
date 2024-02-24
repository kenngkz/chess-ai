from typing import List

import numpy as np
import pandas as pd

from src.preprocessing import prep_obs_df


def train(model, files:List[str], ckpt_file:str=None):
    for file in files:
        print(f"Training on {file}")
        if file.split(".")[-1] == "pkl":
            df = pd.read_pickle(file)
        elif file.split(".")[-1] == "csv":
            df = pd.read_csv(file)
            df = prep_obs_df(df)
        else:
            raise Exception(f"Unhandled file: {file}")
        X = np.concatenate([np.array(df["obs_board"].values.tolist()), np.array(df["obs_misc"].values.tolist())], axis=1)
        Y = df["outcome"].values
        model.fit(X, Y)
        if ckpt_file:
            model.save(ckpt_file)
    return model