import os
import sys

# this is the directory name of this __init__ file
SCRIPTS_DIRNAME = "scripts"
if os.path.basename(os.getcwd()) == SCRIPTS_DIRNAME:
    os.chdir("..")  # change to the project directory
sys.path.append(os.getcwd())

from src.preprocessing import process_raw_data

if __name__ == "__main__":
    process_raw_data(["data/pgn/chessgames2020.pgn", "data/pgn/chessgames2021.pgn"])