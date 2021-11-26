# v1.3
# November 25

# Changelog
# 1.0: initial release
# 1.1: fix for windows
# 1.2: fix GUI showing transposed grid; fix for two bots in same location (now each position is a list); add pretty_print function.
# 1.2.2: fix movement issue, better exception message for invalid return value
# 1.3: new bot attributes: previously_collected_bots, category_tops(int), name, group; tie in individual categories is considered loss.

from game import main
from importlib import util
from collections import defaultdict

##
# You can modify the variables below to change various properties of the game.
##

NUM_GAMES = 1
MAP_SIZE = 5
GUI = True
CHECK_TIMING = False
PLAYER_MODULES = ['random_player', 'random_player']
VERSION = "1.3"

##
# Do not change any lines below.
##

def run(num_games, map_size, gui, check_timing, player_modules):
    wins = defaultdict(int)
    times = defaultdict(int)
    for i in range(num_games):
        players = []
        for player_module in player_modules:
            spec = util.spec_from_file_location("module.name", player_module + ".py")
            foo = util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            players.append(foo.Player())
    
        winners, timings, final_turn = main(players, map_size, show_gui=gui, check_timing=check_timing)
        for w in winners:
            wins[w] += 1
        for t in timings:
            times[t] += timings[t] / final_turn
    
    game_feedback = f"The results of the {num_games} games were as follows:\n"
    game_feedback += '\n'.join([f"{player_modules[i]}: {wins[i]}" for i in range(len(player_modules))])
    print(game_feedback)
    
    timing_feedback = ''
    if check_timing:
        timing_feedback = f"It took the following average number of seconds for each player's step method to be executed:\n"
        timing_feedback += '\n'.join([f"{player_modules[i]}: {times[i]}" for i in range(len(player_modules))])
        print(timing_feedback)
    
    return game_feedback, timing_feedback, wins, times

if __name__ == '__main__':
    run(NUM_GAMES, MAP_SIZE, GUI, CHECK_TIMING, PLAYER_MODULES)