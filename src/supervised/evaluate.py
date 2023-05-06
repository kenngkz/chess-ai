import os
import numpy as np
import pandas as pd
import tensorflow as tf

from src.processing.data import process_df

def evaluate_model(model_names, model_type, datafile="data/split/processed/chess25.pkl", ckpt_dir="ckpt/aunty"):

    if model_type == "actor":
        y_col = "move"
        metric = "sparse_categorical_accuracy"
    elif model_type == "critic":
        y_col = "outcome"
        metric = "binary_crossentropy"
    else:
        raise Exception(f"Unknown model type {model_type}")

    models = []
    for model_name in model_names:
        checkpoints = [(ckpt_dir, model_name, name) for name in os.listdir(os.path.join(ckpt_dir, model_name))]
        if checkpoints:
            latest_checkpoint = max(checkpoints, key=os.path.getctime)
            print("Restoring from", latest_checkpoint)
            model = tf.keras.models.load_model(latest_checkpoint)
            models.append(model)
        else:
            print("No checkpoint available")

    # load data
    extension = datafile.split(".")[-1]
    if extension == "csv":
        data = pd.read_csv(datafile)
        print(f"Processing {datafile} ...", end="")
        data = process_df(data)
        print("Complete")
    elif extension == "pkl":
        data = pd.read_pickle(datafile)
    else:
        print(f"Unknown extension {extension}")

    # convert to numpy arrays
    x = np.array(data["obs"].values.tolist())
    y = data[y_col].values

    performance = []
    for model_name, model in zip(model_names, models):
        performance.append([model_name, model.evaluate(x, y, batch_size=128, return_dict=True)[metric]])

    return pd.DataFrame(performance, columns=["model_name", metric])