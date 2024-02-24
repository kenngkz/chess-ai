import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

import chess
import tensorflow as tf
from tensorflow.python.keras.models import load_model

from src.neural_network.self_play import SelfPlay

actor_file = "actor_model"
critic_file = "critic_model"

actor_model = tf.keras.models.load_model(actor_file)
critic_model = tf.keras.models.load_model(critic_file)

self_play = SelfPlay(actor_model, critic_model)

self_play.play_game()

print(self_play.buffer)
print(self_play.buffer[0]["outcome"])
for step in self_play.buffer:
    print(chess.Board(step["board"]))
