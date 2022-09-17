
import tensorflow as tf
from tensorflow import keras

import constants

# conv2d operating on board position, dense model operating on leftover inputs + conv model output


def base():
    # conv: layers 3 size 64 output 128 (kernel 3)
    # dense: layers 2 size 256
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(128)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(134),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def base_dx():
    # expanded dense model: + 1 layer with size 512
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(128)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(134),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(512, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_dx")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def base_cox():
    # expanded conv model (output)
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(192)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(198),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cx")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def base_csx():
    # expanded conv model size
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(128, 3, padding="same", activation=activation),
        keras.layers.Conv2D(128, 3, padding="same", activation=activation),
        keras.layers.Conv2D(128, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(128)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(134),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cx2")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def cox_dr():
    # conv output 192
    # dense layer 1
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(192)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(198),
        keras.layers.Dense(256, activation=activation),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cx_dr")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def co192_d0():
    # conv output 192
    # dense layer 0
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(192)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(198),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cx_dr2")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def co192_cl2_d0():
    # conv output 192, layer 2
    # dense layer 0
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        # keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(192)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(198),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cx3_dr2")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def co256_d0():
    # conv output 256
    # dense layer 0
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(256)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(262),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_cxx_dr2")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def co256_cl4_d0():
    # conv output 256, layer 4
    # dense layer 0
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(256)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(262),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_c4_d0")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model

def co256_cl5_d0():
    # conv output 256, layer 5
    # dense layer 0
    activation = "relu"
    inputs = keras.Input(shape=(70), name="all_input")
    input1 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 0), (-1, 1)), name="player_input")(inputs)
    input2 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 1), (-1, 64)), name="board_input")(inputs)
    input3 = keras.layers.Lambda(lambda x: tf.slice(x, (0, 65), (-1, 5)), name="misc_input")(inputs)

    conv_model = tf.keras.models.Sequential([  # 1:65
        keras.layers.Reshape((8, 8, 1), input_shape=(64,)),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Conv2D(64, 3, padding="same", activation=activation),
        keras.layers.Flatten(),
        keras.layers.Dense(256)
    ], name="conv_model")
    conv_output = conv_model(input2)

    dense_inputs = keras.layers.concatenate([input1, conv_output, input3])
    dense_model = tf.keras.models.Sequential([  # tf.concat([input[:1], conv_model_output, input[65:]], axis=0)
        keras.layers.Input(262),
        keras.layers.Dense(constants.LEN_UCI_MOVES, activation="softmax")
    ], name="dense_model")
    dense_output = dense_model(dense_inputs)

    model = tf.keras.models.Model(inputs, dense_output, name="conv2d_seq_c5_d0")
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate=0.001),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    return model