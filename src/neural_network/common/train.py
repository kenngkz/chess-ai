from typing import Callable, List, Optional

import numpy as np
import pandas as pd
import tensorflow as tf

from src.preprocessing import prep_obs_df


def define_train_function(func_load_Y:Callable[[pd.DataFrame], np.ndarray], func_load_X:Callable[[pd.DataFrame], np.ndarray]=None) -> Callable[[tf.keras.Model, List[str], Optional[str]], tf.keras.Model]:
    if not func_load_X:
        func_load_X = _load_X_from_df

    def train(model:tf.keras.Model, files:List[str], ckpt_file:str=None):
        for file in files:
            print(f"Training on {file}")
            df = _load_df_from_file(file)
            X = func_load_X(df)
            Y = func_load_Y(df)
            model.fit(X, Y)
            if ckpt_file:
                model.save(ckpt_file)
        return model
    
    return train


def _load_df_from_file(file:str) -> pd.DataFrame:
    if file.split(".")[-1] == "pkl":
        df = pd.read_pickle(file)
    elif file.split(".")[-1] == "csv":
        df = pd.read_csv(file)
        df = prep_obs_df(df)
    else:
        raise Exception(f"Unhandled file: {file}")
    return df

def _load_X_from_df(df:pd.DataFrame) -> np.ndarray:
    return np.concatenate([np.array(df["obs_board"].values.tolist()), np.array(df["obs_misc"].values.tolist())], axis=1)