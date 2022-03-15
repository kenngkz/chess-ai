from game import Game, GameState
from agent import RandomAgent
import utils

import time
import os
import random

clear_console = lambda: os.system("cls")

class ChessEnv:
    '''
    Chess-v0

    observation structure: list of len 70
        - 64 entries specifying the piece index in each cell (order: row1col1, row1col2, ...)
        - 4 entries specifying the castle status (whether castling is allowed for each castle type)
            - order: black queenside, black queenside, white queenside, white kingside
        - 2 entries specifying whether each side is under check (order: white, black)
    '''

    def __init__(self, white=None, black=None):
        ''' Initialization. player=1 if human player is white, -1 if black. player not required if opponent=None '''
        self.game = None
        # built-in opponents
        built_in_opp = {"random":RandomAgent}
        self.players = {}
        players = {-1:black, 1:white}
        for side, agent in players.items():
            if isinstance(agent, str):
                if not agent in built_in_opp:
                    print(f"Warning: Agent {agent} with side {side} not in built-in opponents. Default to None")
                    agent = None
                else:
                    agent = built_in_opp.get(agent)()  # initialize the built-in opponent
            self.players[side] = agent


    @classmethod
    def load(cls, filepath, opponent=None):
        ''' Load env from gamestate save file. Opponent must be specified if not None '''
        gamestate = GameState.load(filepath)
        env = cls()
        env.set_state(gamestate)
        return env

    def reset(self):
        ''' Resets the env and returns the starting obs'''
        self.game = Game()
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        return tuple([*self.game.board.to_arr().flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])

    def step(self, action):
        ''' Take a single action in the environment '''
        assert action in self.action_space, f"Action {action} not in action_space"
        self.game.make_move(action, permanent=True)
        self.game.all_legal_moves()
        self.action_space = self.game.legal_moves[self.game.player_to_move]
        obs = tuple([*self.game.board.to_arr().flatten(), *list(self.game.castle_status.values()), *self.game.check_status.values()])
        game_over = self.game.game_over()
        reward = 0 if game_over==None else 0.5*(self.game.player_to_move*game_over+1)
        if self.players[self.game.player_to_move] != None and game_over!=None:
            return self.step_player()
        else:
            return obs, reward, game_over!=None, None

    def set_state(self, gamestate:"GameState", opponent=None):
        ''' Set the game to a specified gamestate '''
        self.game = Game.load(gamestate)
        self.opponent = opponent

    def render(self, delay=0, clear=False):
        ''' Prints the board position in console '''
        print(f"Turn {self.game.move_counter}")
        print(self.game.board)
        time.sleep(delay)
        if clear:
            clear_console()  # execute system call to clear console

    def render_actions(self):
        ''' Prints the legal moves in console '''
        for i, move in enumerate(self.action_space):
            print(f"{i} - {move}")

    def save(self, filename=None, folder=None):
        ''' Saves a GameState file at filepath. Returns GameState if filepath is not provided. '''
        gamestate = GameState(self.game)
        if filename:
            gamestate.save(filename, folder)
        else:
            return gamestate

    def step_player(self):
        ''' Get the player to select a move and executes it. Must an object that inherits from Agent.'''
        action = self.players[self.game.player_to_move].pred(self.action_space)
        return self.step(action)

    def sample_action(self):
        return random.choice(self.action_space)