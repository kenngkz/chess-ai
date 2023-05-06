import tensorflow as tf
from tensorflow import keras

from keras import Model
from keras import layers
from keras import optimizers
from keras import losses
from keras import metrics

layer_objs = {"conv2d": layers.Conv2D, "dense": layers.Dense}
optimizer_objs = {"adam": optimizers.Adam}
loss_objs = {"binary_crossentropy": losses.BinaryCrossentropy, "sparse_cat_crossentropy":losses.SparseCategoricalCrossentropy}
metric_objs = {"binary_crossentropy": metrics.BinaryCrossentropy, "sparse_cat_accuracy": metrics.SparseCategoricalAccuracy}

def input_layer():
    board_input = keras.Input(shape=(64, 13), name="board")
    misc_input = keras.Input(shape=(6), name="misc")
    return board_input, misc_input

def build_conv(input, hidden_layers, output_layer):
    x = layers.Reshape((8, 8, 13), input_shape=(64,13))(input)
    for layer_config in hidden_layers:
        layer = layer_objs[layer_config["type"]]
        layer_config = {key:val for key, val in layer_config.items() if key != "type"}
        x = layer(**layer_config)(x)
        
    x = layers.Flatten()(x)
    output = layers.Dense(**output_layer)(x)
    model = Model(inputs=input, outputs=output, name="convolutional_model")
    return model

def build_dense(input, hidden_layers, output_layer):
    x = input
    for layer_config in hidden_layers:
        layer = layer_objs[layer_config["type"]]
        layer_config = {key:val for key, val in layer_config.items() if key != "type"}
        x = layer(**layer_config)(x)
    
    output = layers.Dense(**output_layer)(x)
    model = Model(inputs=input, outputs=output, name="dense_model")
    return model

def build_optimizer(optimizer_config):
    optimizer = optimizer_objs[optimizer_config["type"]]
    optimizer_config = {key:val for key, val in optimizer_config.items() if key != "type"}
    return optimizer(**optimizer_config)


def full_model(config):
    board_input, misc_input = input_layer()

    conv_model = build_conv(input=board_input, **config["conv"])
    conv_outputs = conv_model(board_input)

    dense_inputs = layers.concatenate([conv_outputs, misc_input])
    dense_model = build_dense(input=dense_inputs, **config["dense"])
    dense_outputs = dense_model(dense_inputs)

    model = Model(inputs=[board_input, misc_input], outputs=dense_outputs, name=config["name"])
    
    optimizer = build_optimizer(config["optimizer"])
    model.compile(
        optimizer = optimizer,
        loss = loss_objs[config["loss"]](),
        metrics = metric_objs[config["metric"]]()
    )
    return model

example_config = {
    "name": "example_model", 
    "conv": {
        "hidden_layers": [
            {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}, 
            {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}, 
            {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}
        ], 
        "output_layer": {"units": 256, "activation": "relu"}
    }, 
    "dense": {
        "hidden_layers": [
            {"type": "dense", "units": 128, "activation": "relu"}
        ],
        "output_layer": {"units": 1, "activation": "sigmoid"}
    }, 
    "optimizer": {"type": "adam", "learning_rate": 0.001}, 
    "loss": "binary_crossentropy", 
    "metric": "binary_crossentropy"
}