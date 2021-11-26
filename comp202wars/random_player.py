import random
from consts import *

class Player(GamePlayer):
    def __init__(self):
        self.name = "Random"
        self.group = 'n/a'
    
    def step(self, game_map, turn, cur_pos):
        return random.choice(list(ACTIONS))