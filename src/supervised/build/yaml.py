import yaml

from src import constants

def parse(file):
    with open(file, "r") as f:
        base_config = yaml.safe_load(f)
    
    config = {"name": base_config["name"]}

    # identify model type + set related config
    if base_config["type"] == "actor":
        final_output_units = constants.LEN_UCI_MOVES
        loss = "sparse_cat_crossentropy"
        metric = "sparse_cat_accuracy"
    elif base_config["type"] == "critic":
        final_output_units = 1
        loss = "binary_crossentropy"
        metric = "binary_crossentropy"
    else:
        raise Exception(f"Model type {base_config['type']} unknown")

    default_activation = base_config.get("activation")

    return config

# example_config = {
#     "name": "example_model", 
#     "conv": {
#         "hidden_layers": [
#             {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}, 
#             {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}, 
#             {"type":"conv2d", "filters":32, "kernel_size":3, "padding":"same", "activation":"relu"}
#         ], 
#         "output_layer": {"units": 256, "activation": "relu"}
#     }, 
#     "dense": {
#         "hidden_layers": [
#             {"type": "dense", "units": 128, "activation": "relu"}
#         ],
#         "output_layer": {"units": 1, "activation": "sigmoid"}
#     }, 
#     "optimizer": {"type": "adam", "learning_rate": 0.001}, 
#     "loss": "binary_crossentropy", 
#     "metric": "binary_crossentropy"
# }