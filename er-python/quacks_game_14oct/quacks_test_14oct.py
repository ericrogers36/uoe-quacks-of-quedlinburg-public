'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''
import random
from collections import Counter
import math
import time
import numpy as np
import scipy as sp
import pandas as pd
import policies_14oct as policies

init_bag = [(1, "W")] * 4 + [(2, "W"), (3, "W")]

class Shop:
    def __init__(self):
        self.items = {
            (1, "O"): 3,
            (1, "BK"): 10,
            (1, "G"): 6,
            (2, "G"): 8,
            (4, "G"): 14,
            (1, "R"): 6,
            (2, "R"): 10,
            (4, "R"): 16,
            (1, "BL"): 5,
            (2, "BL"): 10,
            (4, "BL"): 19,
        }

class GameState: # TODO - review
    def __init__(self, bag, shop, threshold = 7, seed = 1234):
        self.bag = bag.copy() # the bag at the start of the round
        self.round_bag = bag.copy() # the bag that's mutated with draws
        self.play_board = []
        self.threshold = threshold
        self.shop = shop

        # scores and counts
        self.pot_score = 0
        self.white_sum = 0
        self.orange_count = 0
        self.purple_count = 0
        self.black_count = 0

        # round
        self.round_number = 1

        # random seed
        self.rng_seed = seed

        # resources and points
        self.rubies = 2 # every player starts round 1 with 2 rubies
        self.VPs = 0
        self.droplet = 0
        self.flask = "FULL"

        self.bust = False

        # recording
        self.round_records = []
    
    def round_advance(self):
        self.round_number += 1
        self.round_events()
    
    def round_events(self):
        round = self.round_number

        if round == 2:
            # add yellow chips to shop
            self.shop.items.update({(1, "Y"): 8, (2, "Y"): 12, (4, "Y"): 18})
            #pass
        elif round == 3:
            # add purple chips to shop
            self.shop.items.update({(1, "P"): 9})
            #pass
        elif round == 5:
            self.bag.append((1, "W"))
        
    def state_copy(self):
        """
        copy the game state for repeats
        """
        new_state = GameState(self.bag, self.shop, threshold=self.threshold, seed = self.rng)
        new_state.__dict__.update(self.__dict__.copy())
        new_state.bag = self.bag.copy()
        new_state.round_bag = self.bag.copy()
        new_state.play_board = self.play_board.copy()
        
        new_state.pot_score = self.pot_score
        new_state.white_sum = self.white_sum
        new_state.orange_count = self.orange_count 
        new_state.purple_count = self.purple_count
        new_state.black_count = self.black_count

        new_state.rubies = self.rubies
        new_state.VPs = self.VPs
        new_state.droplet = self.droplet
        new_state.flask = self.flask
        return new_state

    def record_round_state(self):
        """
        saves the game state
        """
        self.round_records.append({
            "round_number": self.round_number,
            "victory_points": self.VPs,
            "rubies": self.rubies,
            "pot_score": self.pot_score,
            "bust": self.bust,
            "starting_bag": self.bag.copy(),
            "white_sum": self.white_sum,
            "orange_count": self.orange_count,
            "purple_count": self.purple_count,
            "black_count": self.black_count,
            "flask_status": self.flask
        })
    #pass


# N.B. Blue is BL, Black is BK

class QuacksOfQuedlinburg:
    def __init__(self, state):

        self.money_per_space = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,16,16,17,17,18,18,19,19,20,20,21,21,22,22,23,23,24,24,25,25,26,26,27,27,28,28,29,29,30,30,31,31,32,32,33,33,35]
        self.VPs_per_space = [0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,15]
        assert len(self.money_per_space) == len(self.VPs_per_space)
        self.ruby_spaces = [6,10, 14, 17, 21, 25, 29, 31, 35, 37, 41, 43, 47, 51, 53]


    def draw(self, bag):
        """
        Draw an element from the bag, returns chip and new bag
        """
        if not bag: # empty bag
            return None, bag
        chip = self.rng.choice(bag)
        bag = bag.copy()
        bag.remove(chip)
        return chip, bag

    def multidraw(self, bag, n):
        """
        Draw n chips without replacement, return 2 arrays - one of the drawn chips, one of the remaining bag
        """
        if len(bag) < n: # deals with edge case of fewer chips in the bag than we've been asked to draw
            n = len(bag)
        bag = bag.copy()
        drawn_chips = self.rng.sample(bag, n)
        for chip in drawn_chips:
            bag.remove(chip)
        return drawn_chips, bag
    
    def token_score(self, chip):
        """
        For now, just return the chip value
        """
        value, chiptype = chip
        return value
    
    def use_flask(self, state, drawn_chip):
        value, chiptype = drawn_chip
        if chiptype != "W":
            raise ValueError("Can only use flask if chip drawn is white")
        
        if state.white_sum + value > state.threshold:
            raise ValueError("Can only use flask if chip doesn't result in bust")
        
        if state.flask == "EMPTY":
            raise ValueError("Can't use an empty flask! Check your policy maybe?")

        if state.flask == "FULL": # safeguard
            state.round_bag.append(drawn_chip)
            state.flask = "EMPTY"
            return state
        
    def play_chip(self, chip, state, blue_policy, flask_policy):
        value, chiptype = chip

        if chiptype == "W":
                if state.flask == "FULL":
                    use_flask_decision = flask_policy(state, chip)
                    #print(f'flask decision is {use_flask_decision}')
                    if use_flask_decision == True:
                        self.use_flask(state, chip)
                    elif use_flask_decision == False:
                        state.white_sum += value
                        #print(f'white sum is {state.white_sum}')
                        state.pot_score += self.token_score(chip)
                        state.play_board.append(chip)
                    else:
                        raise ValueError(f'Invalid Flask Decision - {use_flask_decision}')
                elif state.flask == "EMPTY":
                    state.white_sum += value
                    #print(f'white sum is {state.white_sum}')
                    state.pot_score += self.token_score(chip)
                    state.play_board.append(chip)
                else:
                    return ValueError('Flask neither Empty or Full?!?')

        elif chiptype == "O":
            state.orange_count += 1 # add one to number of orange chips in bag
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            
        elif chiptype == "Y":
            # if chip before played yellow is white, return it to the bag, but keep position
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            if len(state.play_board)>= 2 and state.play_board[-2][1] == "W":
               white_chip_before = state.play_board[-2]
               state.round_bag.append(white_chip_before) # add chip back into bag
               white_before_value, _ = white_chip_before
               state.white_sum -= white_before_value # deduct from white sum
               state.play_board[-2] = (white_before_value, "WhiteRemovedByYellow") # add a placeholder to the chip before the played yellow


        elif chiptype == "G": # green only needed in end of round ecal
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            #pass

        elif chiptype == "R":
            # if chip is red, move forward +1 more if 1/2 oranges, +2 more if 3 or more orange
            if state.orange_count == 1 or state.orange_count == 2:
                red_score, _ = chip
                red_score += 1
                chip = (red_score, "R") # update chip

            if state.orange_count >= 3:
                red_score, _ = chip
                red_score += 2
                chip = (red_score, "R") # update chip
                
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)

        elif chiptype == "P":
            state.purple_count +=1
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)

        elif chiptype == "BK":
            state.black_count += 1
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            
        elif chiptype == "BL":
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            drawnbluescore = value
            chip_candidates, state.round_bag = self.multidraw(state.round_bag, drawnbluescore) # draw chips to peek at given by number of blue chip
            chosenchip = blue_policy(chip_candidates, state) # blue_policy should return a chip or None
            if chosenchip is not None:
                state.round_bag.extend([chip for chip in chip_candidates if chip != chosenchip])
                state = self.play_chip(chosenchip, state, blue_policy, flask_policy)
            else:
                state.round_bag.extend(chip_candidates) # put chips back in the bag if none played
        else: # chip type not accounted for
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            raise ValueError(f"I've added the chip score on, but I don't recognise the type of chip: {chiptype}?")
        
        return state
    
    def play_round(self, state, draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy):
        """
        Simulate one round
        Return: state for next round
        """
        # re-init rng
        # rng seed changes each round based on initial seed and round number to ensure repeatability
        self.rng = random.Random(hash(state.rng_seed + state.round_number)) 

        state.pot_score = 0
        state.white_sum = 0 # cumulative white SCORE
        state.orange_count = 0 # number of orange chips played
        state.purple_count = 0 # number of purple chips played
        state.black_count = 0
        state.play_board = []
        state.bust = False

        state.round_bag = state.bag.copy()

        while True: # drawing and playing loop
            action = draw_policy(state)

            if action == "STOP" or not state.round_bag:
                break
            if action != "DRAW":
                raise ValueError(f"Your draw_policy returned somethng other than \"DRAW\" or \"STOP\" - your action was {action}")
            
            chip, state.round_bag = self.draw(state.round_bag)
            
            # draw chip
            state = self.play_chip(chip, state, blue_policy, flask_policy)
            
            if state.white_sum > state.threshold:
                state.bust = True
                #print('Bust! stopping draws')
                break
        
        gained_rubies, gained_VPs, new_bag = self.round_end(state, bust_policy, chip_buy_policy, ruby_buy_policy) 
        state.rubies += gained_rubies
        state.VPs += gained_VPs
        state.bag = new_bag

        # for debug
        print(f"Round {state.round_number}: pot={state.pot_score}, bust={state.bust}, totalVP={state.VPs}, board = {state.play_board}, bag = {state.bag}")

        return state


    def round_end(self, state, bust_policy, chip_buy_policy, ruby_buy_policy):
        gained_rubies, gained_VPs = 0, 0
        scoring_space = state.pot_score + 1
        give_VPs = True
        give_rubies = True
        # stage 1 - dice - skipping this for now
        # stage 2 - chip actions
        # 2a - green chips
        # len(play_board) >= 2 will always hold but just to stop any indexing errors
        if len(state.play_board) >= 2 and state.play_board[-1][1] == "G":
            gained_rubies += 1
        if len(state.play_board) >= 2 and state.play_board[-2][1] == "G":
            gained_rubies += 1
        
        # 2b - purple chips
        if state.purple_count == 1: 
            gained_VPs += 1 
        elif state.purple_count == 2:
            gained_rubies += 1
            gained_VPs += 1
        elif state.purple_count >= 3:
            gained_VPs += 2
            state.droplet += 1

        # 2c - black chips
        if state.black_count >= 1:
            pass # just do nothing now for black chips

        # bust check
        if state.bust:
            # apply bust decision logic
            decision = bust_policy(state)
            if decision == "VPs":
                give_rubies = False
            elif decision == "Rubies":
                give_VPs = False
            else:
                raise ValueError(f"Unknown Bust Policy Decision: {decision}")
        # 3 - rubies
        if give_rubies:
            if scoring_space in self.ruby_spaces:
                gained_rubies += 1

        # 4 - VPs
        if give_VPs:
            gained_VPs += self.VPs_per_space[scoring_space]
            #print(gained_VPs)
        
        # 5 - Buy Chips
        coins = self.money_per_space[scoring_space]

        bought_chips = chip_buy_policy(coins, state, shop = state.shop)
        new_round_bag = state.bag.copy() # copy the non-mutated bag
        
        if bought_chips:
            try:
                if len(bought_chips) > 2:
                    raise ValueError("Something's wrong with your chip_buy_policy() - you can't buy more than two chips!")
                for chip in bought_chips:
                    new_round_bag.append(chip)
            except TypeError:
                raise ValueError("Something's wrong with your chip_ buy_policy() - it should be an array of chips")

        # 6 - Spend Rubies
        ruby_decisions = ruby_buy_policy(state.rubies, state.pot_score) # ruby decision is an array - contains strings "BUY_DROPLET" or "BUY_FLASK"
        if ruby_decisions:
            for decision in ruby_decisions:
                if decision == "BUY_DROPLET":
                    self.buy_droplet_advance(state)
                elif decision == "BUY_FLASK":
                    self.buy_flask_refill(state)
                else:
                    raise ValueError(f'Did not recognise item in ruby_decisions {decision}!')
                
        
        

        return gained_rubies, gained_VPs, new_round_bag

    def buy_droplet_advance(self, state):
        '''
        True if bought, False if not
        This updates state
        '''
        if state.rubies >= 2:
            state.droplet += 1
            state.rubies -= 2
            return True
        return False # not enough money
    
    def buy_flask_refill(self, state):
        '''
        True if bought, False if not
        This updates state
        '''
        if state.rubies >= 2 and state.flask == "EMPTY":
            state.flask = "FULL"
            state.rubies -= 2
            return True
        return False # not enough money or full flask already


def simulate_game():
    state = GameState(init_bag, shop = Shop())
    game = QuacksOfQuedlinburg(state)
    #shop = Shop()
    
    for round_num in range(1, 10): # we play 9 rounds like the board game
        #print(round)
        #state = game.play_round(state, policies.strategic_draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy)
        state = game.play_round(state, policies.strategic_draw_policy, 
                                policies.never_pick_from_blue_chips, 
                                policies.always_vps_when_bust, 
                                policies.buy_simple_policy, 
                                policies.buy_droplet_rubies,
                                policies.never_use_flask
                                )
        state.record_round_state()
        state.round_advance()        
    return state

final_state = simulate_game()
df = pd.DataFrame(final_state.round_records)
print(df)