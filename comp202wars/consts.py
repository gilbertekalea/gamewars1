from enum import Enum

GAMEOBJECT_TYPES = {
    "banana": 0,
    "coin": 1,
    "cauldron": 2
}

DEFAULT_CONFIG = {
    "gameObjects_max_prop": 0.4,
    "max_turns": 200,
}

ACTIONS = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3
}

def pretty_print(game_map):
    print("**** GAME MAP ****")
    for row in game_map:
        print('\t -- '.join([str(x) for x in row]))
    print("******************")

def get_action_for_delta(dx, dy):
    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == 1:
        return 'down'
    elif dy == -1:
        return 'up'
    raise ValueError("dx, dy must be -1 or 1")

class GameStatus(Enum):
    IN_PROGRESS = 0
    TIMEOUT = 1
    GAMEOBJECT_COLLECTED = 2
    ALL_GAMEOBJECTS_COLLECTED = 3


class GamePlayer:
    pass


class GameState:
    def __init__(self, bots, map_, turn):
        self.bots = bots
        self.map = map_
        self.turn = turn

class GameObject:
    def __init__(self, pos, obj_type):
        self.position = pos
        self.obj_type = obj_type

    def __repr__(self):
        return f"GameObject:{{{self.position[0]}, {self.position[1]}| {self.obj_type}}}"
    
    def get_name(self):
        return f"f{self.obj_type+1}"


class Bot:
    def __init__(self, player, i, position=None, collected_objects=None, prev_collected_objects=None, category_tops=0):
        self.name = 'n/a'
        self.player = player
        if player is not None:
            self.player.i = i
            self.name = self.player.name
            self.grop = self.player.group
        self.i = i
        self.collected_objects = [0, 0, 0] if collected_objects is None else collected_objects
        self.prev_collected_objects = [0, 0, 0] if prev_collected_objects is None else prev_collected_objects
        self.position = position
        self.category_tops = category_tops
    
    def __repr__(self):
        return f"Bot:{{{self.position[0]}, {self.position[1]} | {self.get_name()} | {self.collected_objects}}}"

    def get_name(self):
        return f"b{self.i+1}"

    def pos(self):
        return (self.position[0], self.position[1])

    def set_pos(self, pos):
        self.position = pos
    
    def add_object(self, obj):
        self.prev_collected_objects = self.collected_objects[:]
        self.collected_objects[obj] += 1
    
    def step(self, game_map, turn):
        return self.player.step(game_map, turn, tuple(self.position))
