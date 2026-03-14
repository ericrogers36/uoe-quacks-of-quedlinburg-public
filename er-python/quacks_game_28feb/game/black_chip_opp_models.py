#game/black_chip_opp_models.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import random


# NOTE -
# functions return 2-tuples (L,R) - L is black chips for left player, R is black chips for right player

class OpponentBlackModels: 
    def __init__(self, model_name="never"):
        self.model_name = model_name

    
    def estimate(self, state):
        '''
        Estimate opponent black chip count based on model name.
        '''
        if self.model_name == "never":
            return self.never_opp_black_count(state)
        if self.model_name == "random":
            return self.random_opp_black_count(state)
        elif self.model_name == "scaled":
            return self.scaled_opp_black_count(state)
        elif self.model_name == "mirror":
            return self.mirror_opp_black_count(state)
        elif self.model_name == "mirror_noise":
            return self.mirror_opp_black_count_noise(state)
        elif self.model_name == "random_scaled":
            return self.random_scaled(state)
        elif self.model_name == "random_scaled_softer":
            return self.random_scaled_softer(state)
        elif self.model_name == "random_scaled_one_only":
            return self.random_scaled_one_only(state)
        else:
            raise ValueError("Invalid model name!")
    
    def never_opp_black_count(self, state):
        """
        Opponents never buys black chips
        """
        return (0, 0)
    
    def random_opp_black_count(self, state):
        # this is not very good
        return (random.randint(0, 3), random.randint(0, 3))
    
    def scaled_opp_black_count(self, state):
        thisround = state.round_number
        total_rounds = 9
        final_round_black_target = 4
        
    '''
    def scaled_opp_black_count(self, state):
        r = state.round_number
        total_rounds = 9
        player_black_count = state.black_count
        noise_l, noise_r = random.randint(-1, 1), random.randint(-1, 1) 

        target_black = min(3, int(5 * r / total_rounds + 0.5))  # +0.5 for rounding - target for final round
        
        left_black = max(0, min(3, target_black + noise_l))
        right_black = max(0, min(3, target_black + noise_r))
        
        return (left_black, right_black)
    '''
    def mirror_opp_black_count(self, state):
        # UNREALISTIC - but both players left and right have same black chips as player
        return (state.black_count, state.black_count)
    
    def mirror_opp_black_count_noise(self, state):
        # UNREALISTIC - but both players left and right have same black chips as player
        noise_l, noise_r = random.randint(-1, 1), random.randint(-1, 1)
        return (state.black_count+noise_l, state.black_count+noise_r)
    
    def random_scaled(self, state):
        this_round = state.round_number

        if this_round == 1:
            return (0, 0) # no black chips played in first round
        elif this_round < 4:
            return (random.randint(0, 1), random.randint(0, 1))
        elif this_round < 7:
            return (random.randint(0, 2), random.randint(0, 2))
        else:
            return (random.randint(0, 3), random.randint(0, 3))
    
    def random_scaled_softer(self, state):
        this_round = state.round_number

        if this_round == 1:
            return (0, 0) # no black chips played in first round
        elif this_round < 6:
            return (random.randint(0, 1), random.randint(0, 1))
        else:
            return (random.randint(0, 2), random.randint(0, 2))

    
    def random_scaled_one_only(self, state):
        this_round = state.round_number

        if this_round == 1:
            return (0, 0) # no black chips played in first round
        elif this_round < 4:
            return (0, random.randint(0, 1))
        elif this_round < 7:
            return (0, random.randint(0, 2))
        else:
            return (0, random.randint(0, 3))