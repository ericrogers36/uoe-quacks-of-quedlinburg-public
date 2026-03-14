'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import math
import random
import matplotlib.pyplot as plt

# Game Parameters

bag_init = [(1, "W"), (1, "W"), (1, "W"), (1, "W"), (2, "W"), (3, "W")]
threshold = 7

def reward(pot_value):
    '''
    Reward function - for now just return pot value
    '''
    return pot_value

def draw_outcomes(bag):
    '''
    output is a tuple
    '''
    outcomes = []
    n = len(bag)
    for i, (val, chip_type) in enumerate(bag):
        new_bag = bag[:i] + bag[i+1:]
        outcomes.append((1/n, val, chip_type, new_bag))
    return outcomes

# Memoization dictionaries

dict_val = {}
dict_decision = {}

def V(white_sum, pot_value, bag_tuple):
    '''
    Returns optimal expected reward at current state
    Stores optimal decision in dict_decision
    '''
    state = (white_sum, pot_value, bag_tuple) # records the play state

    if state in dict_val:
        return dict_val[state]

    bag = list(bag_tuple)

    # Bust check
    if white_sum > threshold:
        dict_val[state] = 0 # set reward to 0 for going bust
        dict_decision[state] = "BUST"
        return 0

    # compute what happens if we stop
    stop_val = reward(pot_value)

    if not bag:  # bag empty, must stop drawing
        dict_val[state] = stop_val 
        dict_decision[state] = "STOP"
        return stop_val
    
    # compute what happens if we draw 
    draw_val = 0
    for p, val, chip_type, new_bag in draw_outcomes(bag):
        new_white_sum = white_sum + val if chip_type == "W" else white_sum
        new_pot_value = pot_value + val  # can be modified later for chip types
        draw_val += p * V(new_white_sum, new_pot_value, tuple(new_bag))

    # DECISION RULE
    # currently we stop when the stopping reward is greater or equal to the expected reward of drawing another token from the bag
    if stop_val >= draw_val:
        dict_val[state] = stop_val
        dict_decision[state] = "STOP"
        return stop_val
    else:
        dict_val[state] = draw_val
        dict_decision[state] = "DRAW"
        return draw_val

def optimal_value(bag):
    return V(0, 0, tuple(bag))

def optimal_policy(bag):
    '''
    Return starting decision and expected value
    '''
    start_state = (0, 0, tuple(bag))
    V(0, 0, tuple(bag))  # ensure state is computed
    return dict_decision[start_state], dict_val[start_state]