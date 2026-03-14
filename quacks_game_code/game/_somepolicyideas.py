# File to workshop policy ideas - this isn't connected to the game but please write functions here before sticking
# them into policies_[date].py
# Need - draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy

# Important things you might want from the state class:
# state.bag (the bag at the start of the round)
# state.round_bag (the bag that gets mutated throughout the round)
# state.play_board (an array which represents the board with the chips on it)
# state.threshold (this should be 7, but this is the threshold at which you go bust from white chips)
# state.pot_score (the combined total of the chip values on the board)
# state.white_sum (the sum of all the white chip values on the board)
# state.orange_count (how many orange chips have been played on the board)
# state.purple_count (how many purple chips have been played on the board)
# state.black_count (how many black chips have been played on the board)
# state.round_number (which round we're on - an integer from 1 to 9)
# state.rubies (how many rubies the player has)
# state.VPs (the number of victory points the player has)
# state.droplet (the droplet position)
# state.flask (flask status, either "FULL" or "EMPTY")
# state.bust (True if bust, False if not)
# state.round_records (an array containing the records of each round, see the function record_round_state for more info)

# ---------
# TEMPLATES
# ---------

def draw_policy_template(state):
    '''
    Inputs: state
    Returns: a string, either "DRAW" or "STOP"
    '''
    raise NotImplementedError

def blue_policy_template(chip_candidates, state): 
    '''
    Inputs: chip_candidates, state
    Returns: a chip from "chip_candidates" (NOT in an array please) or None
    '''
    raise NotImplementedError

def bust_policy_template(state):
    '''
    Inputs: state
    Returns: either "VPs" or "Coins" as a string
    '''
    raise NotImplementedError

def chip_buy_policy_template(coins, state, shop):
    '''
    Inputs: coins (how much money the player has to spend on chips), state, shop
    Returns: an array (this should be max length two) of the chips needed to be bought
    DO NOT subtract points here, this is handled by code elsewhere
    Make sure you have enough points/coins to buy all the chips you want to buy!
    '''
    raise NotImplementedError

def ruby_buy_policy_template(rubies, state):
    '''
    Inputs: rubies, state
    Returns: an array of strings containing the decisions - which are "BUY_DROPLET" or "BUY_FLASK"
    N.B. Note that the flask can only be bought when empty and (hence) can only be bought once (per round) or not at all
    Also, each decision costs two rubies so make sure that you take that into account (i.e. don't overspend)
    '''
    raise NotImplementedError

def flask_policy_template(state, drawn_chip):
    '''
    Inputs: state, drawn_chip
    Returns: True or False, whether to use the flask or not
    N.B. I think (???) this only gets called when the flask is "FULL"
    '''
    raise NotImplementedError

# ------------
# POLICY IDEAS
# ------------

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

def buylotsoforange_policy(coins, state, shop):
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