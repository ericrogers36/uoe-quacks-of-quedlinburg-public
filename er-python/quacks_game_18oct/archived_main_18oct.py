'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
import pandas as pd
import random
from collections import Counter
import matplotlib.pyplot as plt
from IPython.display import display
from game.game_18oct import QuacksOfQuedlinburg
from game.state_18oct import GameState
from game.shop_18oct import Shop
from game.policies_18oct import SamsPolicy
#from game.policies_18oct import TestPolicy


init_bag = [(1, "W")] * 4 + [(2, "W"), (3, "W"), (1, "O"), (1, "G")]


def simulate_game():
    '''
    Simulate a game
    '''
    state = GameState(init_bag, 
                      shop = Shop(), 
                      seed = None
                      )
    game = QuacksOfQuedlinburg(state)

    policy = SamsPolicy()
    
    for round_num in range(1, 10): # we play 9 rounds like the board game
        #print(round)
        #state = game.play_round(state, policies.strategic_draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy)
        state = game.play_round(state, 
                                #draw_policy = policy.expected_draw_policy, # sam expected draw policy
                                draw_policy = policy.draw_policy, # draw policy
                                blue_policy = policy.joseph_blue_policy, # blue chip policy
                                bust_policy = policy.bust_policy, # bust policy
                                #chip_buy_policy = policy.chip_buy_policy, # chip buying policy
                                chip_buy_policy = policy.spend_all,
                                #chip_buy_policy = policy.orange_red,
                                ruby_buy_policy = policy.ruby_buy_policy, # ruby spending policy
                                flask_policy = policy.flask_policy # flask policy
                                )
        state.record_round_state()
        state.round_advance()        
    return state

def one_game_df():
    game = simulate_game()
    df = pd.DataFrame(game.round_records)
    return df

def simulate_multiple_print(n):
    results = [simulate_game().VPs for _ in range(n)]
    print(f'n = {n}, Mean = {np.mean(results)}, S.D. = {np.std(results)}, Max = {np.max(results)}, Min = {np.min(results)}')

def simulate_multiple(n):
    return np.array([simulate_game().VPs for _ in range(n)])
#simulate_multiple_print(1000)
#simulate_multiple_print(1)
#simulate_multiple_print(150)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#    print(one_game_df())
    
#print(one_game_df())

def plot_multiple(n):
    results = [simulate_game().VPs for _ in range(n)]
    
    counts = Counter(results)

    xs = sorted(counts.keys())
    ys = [counts[x] for x in xs]

    plt.figure()
    plt.bar(xs, ys)
    plt.xlabel("Victory Points (final)")
    plt.ylabel("Frequency")
    plt.title(f"Quacks Sim - {n} games, Min = {np.min(results)}, Max = {np.max(results)}")
    plt.show()

plot_multiple(20000)