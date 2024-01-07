import numpy as np
import pandas as pd
import tensorflow as tf


def evaluate(model, files):
    accuracy = tf.keras.metrics.BinaryAccuracy(
            name='binary_accuracy', dtype=None, threshold=0.5
        )
    cross_entropy = tf.keras.metrics.BinaryCrossentropy(
            name='binary_crossentropy',
            dtype=None,
            from_logits=False,
            label_smoothing=0
        )
    
    for file in files:
        df = pd.read_pickle(file)
        X = np.concatenate([np.array(df["obs_board"].values.tolist()), np.array(df["obs_misc"].values.tolist())], axis=1)
        Y = df["outcome"].values
        predictions = model.predict(X)

        
        accuracy.update_state(Y, predictions)
        cross_entropy.update_state(Y, predictions)
    return float(accuracy.result().numpy()), float(cross_entropy.result().numpy())

