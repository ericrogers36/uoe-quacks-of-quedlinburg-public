#state_18oct.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import random

class GameState:
    def __init__(self, bag, shop, threshold = 7, seed = None):
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
        if seed is None:
            seed = random.randint(1, 10**10)
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
    
    def round_events(self): # round management
        round = self.round_number

        if round == 2:
            # add yellow chips to shop in round 2
            self.shop.items.update({(1, "Y"): 8, (2, "Y"): 12, (4, "Y"): 18})
            #pass
        elif round == 3:
            # add purple chips to shop in round 3
            self.shop.items.update({(1, "P"): 9})
            #pass
        elif round == 5:
            # every player gets an extra white chip in round 5
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
        
