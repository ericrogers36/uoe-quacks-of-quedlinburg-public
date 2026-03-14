# experiments/simulations.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np  
import pandas as pd
from game.game import QuacksOfQuedlinburg
from game.state import GameState
from game.shop import Shop
from game.black_chip_opp_models import OpponentBlackModels

from concurrent.futures import ProcessPoolExecutor

init_bag = [(1, "W")] * 4 + [(2, "W"), (3, "W"), (1, "O"), (1, "G")]


def simulate_game(policybundle, opp_black_model="never"):
    '''
    Simulate a game
    '''
    state = GameState(init_bag, 
                      shop = Shop(), 
                      seed = None
                      )
    game = QuacksOfQuedlinburg(state)

    opp_black_model = OpponentBlackModels(opp_black_model)

    #policy = SamsPolicy()
    
    for round_num in range(1, 10): # we play 9 rounds like the board game
        #print(round)
        state = game.play_round(state, 
                                draw_policy = policybundle.draw_policy, # draw policy
                                blue_policy = policybundle.blue_policy, # blue chip policy
                                bust_policy = policybundle.bust_policy, # bust policy
                                chip_buy_policy = policybundle.chip_buy_policy, # chip buy policy
                                ruby_buy_policy = policybundle.ruby_buy_policy, # ruby spending policy
                                flask_policy = policybundle.flask_policy, # flask policy
                                opp_black_estimate = opp_black_model.estimate # opponent black behaviour
                                )
        state.record_round_state()
        state.round_advance()        
    return state

def simulate_game_vps_wrapper(args):
    policybundle, opp_black_model = args
    return simulate_game(policybundle, opp_black_model).VPs


### BROKEN!!!!
def simulate_multiple_parallel(policybundle, opp_black_model, n):
    with ProcessPoolExecutor() as ex:
        return np.array(list(ex.map(lambda _: simulate_game_vps_wrapper(policybundle, opp_black_model), range(n))))

def simulate_multiple(policybundle, n, opp_black_model = "never"):
    return np.array([simulate_game(policybundle, opp_black_model).VPs for _ in range(n)])

def simulate_multiple_print(policybundle, opp_black_model, n):
    results = np.array([simulate_game(policybundle, opp_black_model).VPs for _ in range(n)])
    print(f'n = {n}, Mean = {np.mean(results)}, S.D. = {np.std(results)}, Max = {np.max(results)}, Min = {np.min(results)}')





