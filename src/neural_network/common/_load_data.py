import numpy as np
import pandas as pd

from src.preprocessing import prep_obs_df


def load_df_from_file_name(file: str) -> pd.DataFrame:
    if file.split(".")[-1] == "pkl":
        df = pd.read_pickle(file)
    elif file.split(".")[-1] == "csv":
        df = pd.read_csv(file)
        df = prep_obs_df(df)
    else:
        raise Exception(f"Unhandled file: {file}")
    return df


def load_X_from_df(df: pd.DataFrame) -> np.ndarray:
    return np.concatenate(
        [np.array(df["obs_board"].values.tolist()), np.array(df["obs_misc"].values.tolist())],
        axis=1,
    )
