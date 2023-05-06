import os
import numpy as np
import pandas as pd
import tensorflow as tf

from src.processing.data import process_df

def train_model(model, model_type, data_dir="data/split/", n_files=25, epochs=1, ckpt_dir="ckpt/"):

    if model_type == "actor":
        y_col = "move"
    elif model_type == "critic":
        y_col = "outcome"
    else:
        raise Exception(f"Unknown model type {model_type}")

    file_order = list(range(1, n_files+1))

    # if not os.path.exists(ckpt_dir):
    #     os.makedirs(ckpt_dir)
    if not os.path.exists(os.path.join(ckpt_dir, model.name)):
        os.makedirs(os.path.join(ckpt_dir, model.name))

    checkpoints = [os.path.join(ckpt_dir, model.name, name) for name in os.listdir(os.path.join(ckpt_dir, model.name))]
    if checkpoints:
        latest_checkpoint = max(checkpoints, key=os.path.getctime)
        print("Restoring from", latest_checkpoint)
        model = tf.keras.models.load_model(latest_checkpoint)
        n = latest_checkpoint.split("-")[-1][0]
    else:
        n = 0

    processed_files = [filename.split(".")[0] for filename in os.listdir(os.path.join(data_dir, "processed"))]
    for file in file_order:
        if file <= int(n):
            continue
        filename = f"chess{file}"
        print(f"Training on file {filename}")

        # load data from .csv file
        if filename in processed_files:
            df = pd.read_pickle(os.path.join(data_dir, "processed", filename + ".pkl"))
        else:
            df = pd.read_csv(os.path.join(data_dir, filename + ".csv"))

            # translate from fen to obs arr
            print("Processing...", end="")
            df = process_df(df)
            print("complete")

        # convert to numpy arrays
        x = {
            "board": tf.keras.utils.to_categorical(np.array(df["obs_board"].values.tolist()), num_classes=13), 
            "misc":np.array(df["obs_misc"].values.tolist())
        }
        y = df[y_col].values

        # train
        model.fit(x, y, batch_size=64, epochs=epochs, validation_split=0.1)

        # save checkpoint between files
        model.save(os.path.join(ckpt_dir, model.name, f"{model.name}-{file}.h5"))
    print(f"Training completed. Final save file: {os.path.join(ckpt_dir, model.name, f'{model.name}-{file}.h5')}")