import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

from src.preprocessing import pgn_to_shuffled_csv

if __name__ == "__main__":
    pgn_to_shuffled_csv(["data/pgn/chessgames2020.pgn", "data/pgn/chessgames2021.pgn"])