''' Dense models '''
from tensorflow import keras

import constants

def base():
    # base model
    activation = "relu"
    model = keras.Sequential([
        keras.layers.Input(shape=(70)),
        keras.layers.Dense(210, activation=activation),
        keras.layers.Dense(630, activation=activation),
        keras.layers.Dense(210, activation=activation),
        keras.layers.Dense(1200, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense1")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def base_drop():
    # base with dropout of 0.5
    activation = "relu"
    model = keras.Sequential([
        keras.layers.Input(shape=(70)),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(630, activation=activation),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(630, activation=activation),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(630, activation=activation),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(1200, activation=activation),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_drop")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def deep1():
    # model deep: 16 hidden layers
    activation = "relu"
    model = keras.Sequential([
        keras.layers.Input(shape=(70)),
    ], name="dense_deep")
    for _ in range(16):
        model.add(keras.layers.Dense(256, activation=activation))
    model.add(keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax"))
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def deep1_drop():
    # model deep with dropout
    activation = "relu"
    model = keras.Sequential([
        keras.layers.Input(shape=(70)),
    ], name="dense_deep_drop")
    for _ in range(16):
        model.add(keras.layers.Dense(256, activation=activation))
        model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax"))
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model