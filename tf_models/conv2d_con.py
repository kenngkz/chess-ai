''' Concurrent convolutional 2d networks '''
''' board position feeds into multiple conv2d models before compiling in dense '''

import tensorflow as tf
from tensorflow import keras

import constants

# conv2d operating on board position, dense model operating on leftover inputs + conv model output


def conv2d_357():
    # 3 conv2d models with kernel sizes 3 5 7
    # each 2 layers with 32 size and 64 output
    # dense: layers 2 size 256
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv3_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(32, 3, padding="same", activation=activation),
        keras.layers.Conv2D(32, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64)
    ], name="conv_model_k3")
    conv3_output = conv3_model(input2)

    conv5_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(32, 5, padding="same", activation=activation),
        keras.layers.Conv2D(32, 5, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64)
    ], name="conv_model_k5")
    conv5_output = conv5_model(input2)

    conv7_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(32, 7, padding="same", activation=activation),
        keras.layers.Conv2D(32, 7, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64)
    ], name="conv_model_k7")
    conv7_output = conv7_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv3_output, conv5_output, conv7_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(198),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_357")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def conv2d_35():
    # 2 conv2d models with kernel sizes 3 5
    # each 3 layers with 32 size and 128 output
    # dense: layers 2 size 256
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv3_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(32, 3, padding="same", activation=activation),
        keras.layers.Conv2D(32, 3, padding="same", activation=activation),
        keras.layers.Conv2D(32, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(128)
    ], name="conv_model_k3")
    conv3_output = conv3_model(input2)

    conv5_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(32, 5, padding="same", activation=activation),
        keras.layers.Conv2D(32, 5, padding="same", activation=activation),
        keras.layers.Conv2D(32, 5, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(128)
    ], name="conv_model_k5")
    conv5_output = conv5_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv3_output, conv5_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(262),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_35")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def conv2d_35x():
    # conv2d_35 with extra size in conv models
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv3_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64)
    ], name="conv_model_k3")
    conv3_output = conv3_model(input2)

    conv5_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 5, padding="same", activation=activation),
        keras.layers.Conv2D(64, 5, padding="same", activation=activation),
        keras.layers.Conv2D(64, 5, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(64)
    ], name="conv_model_k5")
    conv5_output = conv5_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv3_output, conv5_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(134),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_35x1")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model