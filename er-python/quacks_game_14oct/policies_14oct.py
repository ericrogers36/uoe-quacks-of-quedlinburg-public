'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

# Need - draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy

def draw_policy_template(state):
    '''
    Inputs: pot score, white sum so far, chips in bag and play board
    Returns: "DRAW" or "STOP"
    '''
    pass

def blue_policy_template(chip_candidates, state): 
    '''
    Inputs: chip_candidates, pot_score, white_sum, round_bag
    Returns: the array of a chip from "chip_candidates" or None
    '''
    pass

def bust_policy_template(state):
    '''
    No Inputs yet
    Returns: either "VPs" or "Rubies"
    '''
    pass

def chip_buy_policy_template(coins, state, shop):
    pass

def ruby_buy_policy_template(rubies, state):
    pass

def strategic_draw_policy(state):
    '''
    TODO: write a docstring eric
    '''
    for value, type in state.round_bag:
        if type == "W" and state.white_sum + value > state.threshold:
            return "STOP"
    return "DRAW"

def never_buy_with_rubies(rubies, state):
    return None

def buy_droplet_rubies(rubies, state):
    decisions = []
    rubies_to_spend = rubies
    while rubies_to_spend >= 2:
        decisions.append("BUY_DROPLET")
        rubies_to_spend -= 2
    #print(f'we have {rubies} rubies, so we buy {decisions}')
    return decisions


def never_buy_tokens(coins, state, shop):
    return None

def always_vps_when_bust(state):
    return "VPs"

def always_rubies_when_bust(state):
    return "Rubies"

def never_pick_from_blue_chips(chip_candidates, state): 
    '''
    Inputs: chip_candidates, pot_score, white_sum, round_bag
    Returns: the array of a chip from "chip_candidates" or None
    '''
    return None

def always_draw_policy(state):
    return "DRAW"

def buy_simple_policy(coins, state, shop):
    # buy orange if possible
    buy_list = []
    if coins >= 6:
        buy_list.append((1, "O"))
        buy_list.append((1, "O"))
    elif coins >= 3:
        buy_list.append((1, "O"))
    #print(f'buying {buy_list}')
    return buy_list

def never_use_flask(state, drawn_chip):
    return False

def use_flask_if_can(state, drawn_chip):
    value, chiptype = drawn_chip
    if chiptype == "W" and state.flask == "FULL" and value + state.white_sum <= state.threshold:
        #print('using flask!')
        return True
    return False
#class Policies:
