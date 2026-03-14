#game/game.py

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
import matplotlib.pyplot as plt

# N.B. Blue is BL, Black is BK

class QuacksOfQuedlinburg:
    def __init__(self, state):

        self.money_per_space = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,16,16,17,17,18,18,19,19,20,20,21,21,22,22,23,23,24,24,25,25,26,26,27,27,28,28,29,29,30,30,31,31,32,32,33,33,35]
        self.VPs_per_space = [0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,15]
        assert len(self.money_per_space) == len(self.VPs_per_space)
        self.ruby_spaces = [6, 10, 14, 17, 21, 25, 29, 31, 35, 37, 41, 43, 47, 51, 53]


    def draw(self, bag):
        """
        This is the draw action - draw an element from the bag, returns chip and new bag.
        """
        if not bag: # empty bag
            return None, bag
        chip = self.rng.choice(bag)
        bag = bag.copy()
        bag.remove(chip)
        return chip, bag

    def multidraw(self, bag, n):
        """
        Draw n chips without replacement, return 2 arrays - one of the drawn chips, one of the remaining bag.
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
        For now, just return the chip value.
        """
        value, chiptype = chip
        return value
    
    def use_flask(self, state, drawn_chip):
        """
        Called when the flask is used in game.
        """
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
        
    def end_chip_check(self, state, chip):
        # check to see if at final stage
        value, chiptype = chip
        if value + state.pot_score > len(self.VPs_per_space):
            chip = (len(self.VPs_per_space)-state.pot_score, chiptype + "_TRUNCATEDDUETOEND")
        
        return chip
    def play_chip(self, chip, state, blue_policy, flask_policy):
        """
        Called when a chip is drawn to 'play' the chip.
        """
        value, chiptype = chip
        
        # WHITE CHIPS
        if chiptype == "W":
                if state.flask == "FULL":
                    use_flask_decision = flask_policy(state, chip)
                    #print(f'flask decision is {use_flask_decision}')
                    if use_flask_decision == True:
                        self.use_flask(state, chip)
                    elif use_flask_decision == False:
                        state.white_sum += value
                        #print(f'white sum is {state.white_sum}')
                        chip = self.end_chip_check(state, chip)
                        state.pot_score += self.token_score(chip)
                        state.play_board.append(chip)
                    else:
                        raise ValueError(f'Invalid Flask Decision - {use_flask_decision}')
                elif state.flask == "EMPTY": # don't even bother processing the flask
                    state.white_sum += value
                    #print(f'white sum is {state.white_sum}')
                    chip = self.end_chip_check(state, chip)
                    state.pot_score += self.token_score(chip)
                    state.play_board.append(chip)
                else:
                    return ValueError('Flask neither Empty or Full?!?')

        # ORANGE CHIPS
        elif chiptype == "O":
            state.orange_count += 1 # add one to number of orange chips in bag
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            
        elif chiptype == "Y":
            # if chip before played yellow is white, return it to the bag, but keep position
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            if len(state.play_board)>= 2 and state.play_board[-2][1] == "W":
               white_chip_before = state.play_board[-2]
               state.round_bag.append(white_chip_before) # add chip back into bag
               white_before_value, _ = white_chip_before
               state.white_sum -= white_before_value # deduct from white sum
               state.play_board[-2] = (white_before_value, "WhiteRemovedByYellow") # add a placeholder to the chip before the played yellow

        # GREEN CHIPS
        elif chiptype == "G": # green only needed in end of round eval
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)

        # RED CHIPS
        elif chiptype == "R":
            #print('red chip played')
            # if chip is red, move forward +1 more if 1/2 oranges, +2 more if 3 or more orange
            if state.orange_count == 1 or state.orange_count == 2:
                red_score, _ = chip
                red_score += 1
                #print(f'new red score is {red_score}')
                chip = (red_score, "R") # update chip

            if state.orange_count >= 3:
                red_score, _ = chip
                red_score += 2
                chip = (red_score, "R") # update chip
                
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)

        # PURPLE CHIPS
        elif chiptype == "P":
            state.purple_count +=1
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)

        # BLACK CHIPS
        elif chiptype == "BK":
            state.black_count += 1
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
        
        # BLUE CHIPS
        elif chiptype == "BL":
            chip = self.end_chip_check(state, chip)
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
        
        # ISSUE HANDLING
        else: # chip type not accounted for
            chip = self.end_chip_check(state, chip)
            state.pot_score += self.token_score(chip)
            state.play_board.append(chip)
            raise ValueError(f"I've added the chip score on, but I don't recognise the type of chip: {chiptype}?")
        
        return state
    
    def play_round(self, state, draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy, opp_black_estimate):
        """
        Simulate one round
        Return: state for next round
        """
        # re-init rng
        # rng seed changes each round based on initial seed and round number to ensure repeatability
        self.rng = random.Random(hash(state.rng_seed + state.round_number)) 

        state.pot_score = 0 # reset pot score
        state.white_sum = 0 # reset cumulative white score
        state.orange_count = 0 
        state.purple_count = 0 
        state.black_count = 0
        state.play_board = [] # reset the board
        state.bust = False # reset bust

        state.round_bag = state.bag.copy() # copy the bag for the round to the mutatable round_bag
        #print(f'Length of Bag is {len(state.round_bag)}')
        if state.droplet > 0: # account for droplet - we're adding a dummy chip to represent the droplet on the board
            state.pot_score += state.droplet
            state.play_board.append((state.droplet, 'DropletScore'))

        # N.B. the fortune cards aren't implemented 
        while True: # drawing and playing loop
            action = draw_policy(state) # determine draw action - "DRAW" or "STOP"

            if action == "STOP" or not state.round_bag or state.pot_score >= len(self.VPs_per_space): # draw_policy says to stop or bag empty
                break
            if action != "DRAW": # inavlid action
                raise ValueError(f"Your draw_policy returned somethng other than \"DRAW\" or \"STOP\" - your action was {action}")
            
            chip, state.round_bag = self.draw(state.round_bag) # draw a chip 
            
            state = self.play_chip(chip, state, blue_policy, flask_policy) # play the chip
            
            if state.white_sum > state.threshold: # bust check
                state.bust = True
                #print('Bust! stopping draws') # for debugging
                break
            #else:
                #print("not bust yet!")
        
        # drawing has finished
        gained_rubies, gained_VPs, new_bag = self.round_end(state, bust_policy, chip_buy_policy, ruby_buy_policy, opp_black_estimate) 
        state.rubies += gained_rubies
        state.VPs += gained_VPs
        state.bag = new_bag

        # for debug
        #print(f"Round {state.round_number}: pot={state.pot_score}, bust={state.bust}, totalVP={state.VPs}, board = {state.play_board}, bag = {state.bag}")
        return state


    def round_end(self, state, bust_policy, chip_buy_policy, ruby_buy_policy, opp_black_estimate):
        """
        Does all the round ending stuff
        """
        gained_rubies, gained_VPs = 0, 0
        scoring_space = state.pot_score + 1
        give_VPs = True
        give_rubies = True
        give_coins = True
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
            # 28/2/26 - implement black chip logic for opponents!
            black_chips_l_player, black_chips_r_player = opp_black_estimate(state)

            opponents_beaten = 0
            if state.black_count > black_chips_l_player:
                opponents_beaten += 1
            if state.black_count > black_chips_r_player:
                opponents_beaten += 1
            
            # Apply rules based on how many opponents were beaten
            if opponents_beaten >= 1:
                state.droplet += 1  # Push droplet forward for beating at least one opponent
            
            if opponents_beaten == 2:
                gained_rubies += 1  # Extra ruby for beating both opponents
            #pass # just do nothing now for black chips

        # check if we went bust in the round
        if state.bust:
            # apply bust decision logic
            decision = bust_policy(state)
            if decision == "VPs":
                give_coins = False
            elif decision == "Coins":
                give_VPs = False
            elif decision == "Rubies":
                raise ValueError("Please don't pass this decision because it's not actually one! Pass coins instead.")
            else:
                raise ValueError(f"Unknown Bust Policy Decision: {decision}")
        
        # 3 - rubies
        if give_rubies:
            if scoring_space in self.ruby_spaces:
                gained_rubies += 1

        # 4 - VPs
        if give_VPs:
            if scoring_space >= len(self.VPs_per_space):
                gained_VPs += self.VPs_per_space[-1]
            else:
                gained_VPs += self.VPs_per_space[scoring_space]
            #print(gained_VPs)
        
        # 5 - Buy Chips
        if give_coins:
            if scoring_space >= len(self.money_per_space):
                coins = self.money_per_space[-1]
            else:
                coins = self.money_per_space[scoring_space]
            #debug
            #print(f'coins are {coins}')
        else: # account for bust scenario when player chooses VPs over coins
            coins = 0

        bought_chips = chip_buy_policy(coins, state, shop = state.shop)
        new_round_bag = state.bag.copy() # copy the non-mutated bag
        
        if bought_chips:
            try:
                #debug
                #print(f'bought chips are {bought_chips}')
                if len(bought_chips) > 2:
                    raise ValueError("Something's wrong with your chip_buy_policy() - you can't buy more than two chips!")
                for chip in bought_chips:
                    new_round_bag.append(chip)
            except TypeError:
                raise ValueError("Something's wrong with your chip_buy_policy() - it should be an array of chips")

        # 6 - Spend Rubies
        ruby_decisions = ruby_buy_policy(state.rubies, state) # ruby decision is an array - contains strings "BUY_DROPLET" or "BUY_FLASK"
        if ruby_decisions:
            for decision in ruby_decisions:
                if decision == "BUY_DROPLET":
                    #debug
                    #print('bought droplet!')
                    self.buy_droplet_advance(state)
                elif decision == "BUY_FLASK":
                    self.buy_flask_refill(state)
                else:
                    raise ValueError(f'Did not recognise item in ruby_decisions {decision}!')
                
        # final round
        
        if state.round_number == 9:
            while coins >= 5:
                coins -= 5
                gained_VPs += 1

            gained_VPs += state.rubies//2
        

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
        else:
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
        else:
            return False # not enough money or full flask already