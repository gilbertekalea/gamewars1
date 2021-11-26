import random
from consts import *

class Player(GamePlayer):
    def __init__(self):
        self.name = "your team name here"
        self.group = "your group here (e.g., 1A)"
    
    def step(self, game_map, turn, cur_pos):
        pass # remove this line and implement the method
