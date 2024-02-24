import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

import tensorflow as tf

from src.player.neural_network import NNPlayer
from src.self_play.single_game import play_game

actor_file = "ckpt/actor_model"
critic_file = "ckpt/critic_model"

actor_model = tf.keras.models.load_model(actor_file)
critic_model = tf.keras.models.load_model(critic_file)

player = NNPlayer(actor_model)
print(play_game(player, player))
