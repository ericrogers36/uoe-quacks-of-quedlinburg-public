#policies_18oct.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import random
import copy
from collections import Counter
from mctspy.tree.nodes import MonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch

class Policy:
    """
    Policy class which contains all policies
    """
    # Need - draw_policy, blue_policy, bust_policy, chip_buy_policy, ruby_buy_policy, flask_policy
    # see _somepolicyideas.py for propre documentation but here will just be placeholders
    def draw_policy(self, state):
        return "DRAW"

    def blue_policy(self, chip_candidates, state):
        return None
    
    def bust_policy(self, state):
        return "VPs"
    
    def chip_buy_policy(self, coins, state, shop):
        return []
    
    def ruby_buy_policy(self, rubies, state):
        return []
    
    def flask_policy(self, state, drawn_chip):
        return False

# The way this code works, we create subclasses i.e. MyPolicy(Policy) which are groups of all 
# policies that we take forward into a game. For now I think it's best if between-round policy
# changes are handled by the policy functions. Each Policy subclass must contain all policies
# and we call these from the main file where we import the policy subclass.

class TestPolicy(Policy):
    def draw_policy(self, state):
        for value, type in state.round_bag:
            if type == "W" and state.white_sum + value > state.threshold:
                return "STOP"
            return "DRAW"

    def blue_policy(self, chip_candidates, state):
        return None
    
    def bust_policy(self, state):
        return "VPs"

    def chip_buy_policy(self, coins, state, shop):
        # buy orange if possible
        buy_list = []
        if coins >= 6:
            buy_list.append((1, "O"))
            buy_list.append((1, "O"))
        elif coins >= 3:
            buy_list.append((1, "O"))
        #print(f'buying {buy_list}')
        return buy_list
    
    def orange_red(self, coins, state, shop, ratio = .9):
        '''
        Buys only orange and red chips based on a given ratio, tries to keep orange and red chips at a certain ratio
        checks current ratio of orange and red chips, and buys the combination of 2 chips that gets the ratio closest to the optimum
        returns the chosen tokens
        '''
        counts = Counter([color for _, color in state.bag])
        orange = counts["O"]
        red = counts["R"]

        if red != 0:
            current_ratio = orange / red
        else:
            current_ratio = float('inf')

        # build options list (only orange/red and affordable)
        options = []
        for token, cost in shop.items.items():
            if token[1] in ["O", "R"] and cost <= coins:
                options.append((token, cost))

        best_combo = []
        best_diff = float('inf')

        for i in range(len(options)):
            for j in range(i, len(options)):
                combo = [options[i][0]]
                total_cost = options[i][1]
                if i != j:
                    total_cost += options[j][1]
                    combo.append(options[j][0])
                if total_cost <= coins:
                    # count new orange after buying combo
                    new_o = orange
                    for _, c in combo:
                        if c == "O":
                            new_o += 1
                    # count new red after buying combo
                    new_r = red
                    for _, c in combo:
                        if c == "R":
                            new_r += 1

                    if new_r != 0:
                        new_ratio = new_o / new_r
                    else:
                        new_ratio = float('inf')

                    diff = abs(new_ratio - ratio)
                    if diff < best_diff:
                        best_diff = diff
                        best_combo = combo

        return best_combo
    
    def spend_all(self, coins, state, shop):
        '''
        Stategy to spend all the money available
        checks all possible combinations of 2 tokens to spend as much money as possible
        makes a random choice if there is more than one option
        returns the chosen tokens
        '''
        options = list(shop.items.items())
        best_spend = 0
        best_combos = []

        for i in range(len(options)):
            for j in range(i, len(options)):
                combo = [options[i][0]]
                total_cost = options[i][1]
                if i != j:
                    total_cost += options[j][1]
                    combo.append(options[j][0])
                if total_cost <= coins:
                    if total_cost > best_spend:
                        best_spend = total_cost
                        best_combos = [combo]
                    elif total_cost == best_spend:
                        best_combos.append(combo)

        if best_combos:
            return random.choice(best_combos)
        return []
    
    def ruby_buy_policy(self, rubies, state):
        decisions = []
        rubies_to_spend = rubies
        while rubies_to_spend >= 2:
            decisions.append("BUY_DROPLET")
            rubies_to_spend -= 2
        #print(f'we have {rubies} rubies, so we buy {decisions}')
        return decisions
    
    def flask_policy(self, state, drawn_chip):
        return False
    
class SamsPolicy(Policy):
    def draw_policy(self, state):
        stop_flag = False
        for value, type in state.round_bag:
            if type == "W" and state.white_sum + value > state.threshold:
                stop_flag = True
            
        if stop_flag == True:
            return "STOP"
        else:  
            return "DRAW"
    
    def expected_draw_policy(self, state):
        """
        Decide whether to DRAW or STOP based on expected gain vs expected loss.
        """

       
        money_per_space = [
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,15,16,16,17,17,18,18,19,19,
            20,20,21,21,22,22,23,23,24,24,25,25,26,26,27,27,28,28,29,29,30,
            30,31,31,32,32,33,33,35
        ]

        VPs_per_space = [
            0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,
            8,8,8,9,9,9,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,15
        ]

        # tunable risk factor
        risk_factor = 1

        total = len(state.round_bag)
        if total == 0:
            return "STOP"

        # current pot position
        current_pos = state.pot_score
        current_scoring_space = current_pos + 1

        # get current money
        if current_scoring_space < len(money_per_space):
            money_now = money_per_space[current_scoring_space]
        else:
            money_now = money_per_space[-1]

        #Expected Gain
        expected_gain = 0.0

        for chip in state.round_bag:
            value, colour = chip

            #probability of drawing this exact chip
            prob = 1 / total

            # red/orange interaction
            effective_value = value
            if colour == "R":
                if state.orange_count == 1 or state.orange_count == 2:
                    effective_value = value + 1
                elif state.orange_count >= 3:
                    effective_value = value + 2

            #future score space
            new_pos = current_pos + effective_value
            new_scoring_space = new_pos + 1

            if new_scoring_space < len(money_per_space):
                money_after = money_per_space[new_scoring_space]
            else:
                money_after = money_per_space[-1]

            gain = money_after - money_now
            expected_gain += prob * gain

        #Expected Loss
        probability_of_bust = 0.0

        for chip in state.round_bag:
            value, colour = chip

            if colour == "W":
                prob = 1 / total
                if state.white_sum + value > state.threshold:
                    probability_of_bust += prob

        # VP loss = VP you would earn right now
        if current_scoring_space < len(VPs_per_space):
            VP_loss = VPs_per_space[current_scoring_space]
        else:
            VP_loss = VPs_per_space[-1]

        expected_loss = probability_of_bust * VP_loss

        #Decision
        if expected_gain > risk_factor * expected_loss:
            return "DRAW"
        return "STOP"
    
    def draw_policy_safety_net_flask(self, state):
        """
        Draw decision based on probability of bust and flask status.
        If flask is full then we tolerate higher risk.
        If flask is empty then we are more cautious.
        """

        total = len(state.round_bag)
        if total == 0:
            return "STOP"

        # compute probability that the next chip will bust us
        bust_count = 0
        for value, colour in state.round_bag:
            if colour == "W":
                if state.white_sum + value > state.threshold:
                    bust_count += 1

        bust_probability = bust_count / total

        # thresholds
        if state.flask == "FULL":
            # more aggressive 
            bust_threshold = 0.6   
        else:
            # more cautious without safety net
            bust_threshold = 0.3   

        if bust_probability < bust_threshold:
            return "DRAW"
        else:
            return "STOP"

    def blue_policy(self, chip_candidates, state):
        return None
    
    def bust_policy(self, state):
        return "VPs"
    
    def bust_policy_coins(self, state):
        return "Coins"
    
    
    def chip_buy_policy(self, coins, state, shop):
        # buy orange if possible
        buy_list = []
        if coins >= 6:
            buy_list.append((1, "O"))
            buy_list.append((1, "O"))
        elif coins >= 3:
            buy_list.append((1, "O"))
        #print(f'buying {buy_list}')
        return buy_list
    
    def ruby_buy_policy(self, rubies, state):
        decisions = []
        rubies_to_spend = rubies
        while rubies_to_spend >= 2:
            decisions.append("BUY_DROPLET")
            rubies_to_spend -= 2
        #print(f'we have {rubies} rubies, so we buy {decisions}')
        return decisions
    
    def flask_policy(self, state, drawn_chip):
        return False

    def random_buying(self, coins, state, shop):
        '''
        Buys random token based on available coins and current state.
        Picks a a random token from the shop
        checks if it can afford another one
        if it can, picks another random one
        returns the chosen tokens
        '''
        chosen = []
        available_items = list(shop.items.items())
        remaining_coins = coins

        while remaining_coins > 0 and len(chosen) < 2:
            # build affordable list using explicit loop and if
            affordable = []
            for item, cost in available_items:
                if cost <= remaining_coins:
                    affordable.append(item)

            if not affordable:
                break

            choice = random.choice(affordable)
            remaining_coins -= shop.items[choice]
            chosen.append(choice)

        return chosen


    def orange_red(self, coins, state, shop):
        '''
        Buys only orange and red chips based on a given ratio.
        Always attempts to buy 2 chips if possible.
        Returns the combination of 2 chips that gets the ratio closest to the target.
        '''

        # Desired orange:red ratio (change this value if needed)
        ratio = 2

        # Count existing orange/red chips in the bag
        counts = Counter([color for _, color in state.bag])
        orange = counts["O"]
        red = counts["R"]

        # Build list of all affordable orange/red tokens
        options = []
        for token, cost in shop.items.items():
            if token[1] == "O" or token[1] == "R":
                if cost <= coins:
                    options.append((token, cost))

        # If nothing can be bought
        if len(options) == 0:
            return []

        best_combo = None
        best_diff = float('inf')

        # Try ALL PAIRS including 
        for i in range(len(options)):
            for j in range(len(options)):

                token1, cost1 = options[i]
                token2, cost2 = options[j]

                total_cost = cost1 + cost2

                # Skip combos we cannot afford
                if total_cost > coins:
                    continue

                # Compute new orange/red counts after buying these 2
                new_o = orange
                new_r = red

                # First chip
                if token1[1] == "O":
                    new_o += 1
                else:
                    new_r += 1

                # Second chip
                if token2[1] == "O":
                    new_o += 1
                else:
                    new_r += 1

                # Compute new ratio
                if new_r != 0:
                    new_ratio = new_o / new_r
                else:
                    new_ratio = float('inf')

                diff = abs(new_ratio - ratio)

                # Keep the best pair
                if diff < best_diff:
                    best_diff = diff
                    best_combo = [token1, token2]

        # If a 2-chip combo is affordable, return it
        if best_combo is not None:
            return best_combo

        # If 2 chips could NOT be afforded, fall back to the best single
        best_single = None
        best_single_diff = float('inf')

        for token, cost in options:
            if cost <= coins:
                new_o = orange
                new_r = red

                if token[1] == "O":
                    new_o += 1
                else:
                    new_r += 1

                if new_r != 0:
                    new_ratio = new_o / new_r
                else:
                    new_ratio = float('inf')

                diff = abs(new_ratio - ratio)

                if diff < best_single_diff:
                    best_single_diff = diff
                    best_single = token

        if best_single is not None:
            return [best_single]

        # Fallback (should never happen)
        return []


    def blue_black_purple(self, coins, state, shop):
        '''
        Buys only blue, black and purple chips
        prioritises buying black and purple chips first, then blue chips to maximise the chance of getting the black and purple chips
        returns the chosen tokens
        '''
        priorities = ["BK", "P", "BL"]
        chosen = []
        remaining_coins = coins

        for color in priorities:
            # build affordable list for this color
            affordable = []
            for token, cost in shop.items.items():
                if token[1] == color and cost <= remaining_coins:
                    affordable.append((token, cost))

            # prefer higher-value tokens of the same colour
            affordable.sort(key=lambda x: x[0][0], reverse=True)

            if affordable:
                token, cost = affordable[0]
                chosen.append(token)
                remaining_coins -= cost
                if len(chosen) >= 2:
                    break

        return chosen


    def spend_all(self, coins, state, shop):
        '''
        Stategy to spend all the money available
        checks all possible combinations of 2 tokens to spend as much money as possible
        makes a random choice if there is more than one option
        returns the chosen tokens
        '''
        options = list(shop.items.items())
        best_spend = 0
        best_combos = []

        for i in range(len(options)):
            for j in range(i, len(options)):
                combo = [options[i][0]]
                total_cost = options[i][1]
                if i != j:
                    total_cost += options[j][1]
                    combo.append(options[j][0])
                if total_cost <= coins:
                    if total_cost > best_spend:
                        best_spend = total_cost
                        best_combos = [combo]
                    elif total_cost == best_spend:
                        best_combos.append(combo)

        if best_combos:
            return random.choice(best_combos)
        return []


    def combination_buying(self, coins, state, shop, chosen_tokens):
        '''
        Buys tokens based on the chosen tokens
        chosen_tokens is a list of token colours that we want
        try to keep the same number of each of the chosen tokens
        will check which token we own the least of and try to buy that one
        if there is a tie, will pick randomly between the tied tokens
        '''

        # build counts from bag explicitly (keeps original style)
        bag_colors = []
        for _, color in state.bag:
            bag_colors.append(color)
        counts = Counter(bag_colors)

        # build target_counts dict without comprehension
        target_counts = {}
        for c in chosen_tokens:
            target_counts[c] = counts.get(c, 0)

        # find min_count explicitly
        min_count = None
        for c in target_counts:
            if min_count is None or target_counts[c] < min_count:
                min_count = target_counts[c]

        # build least_owned list explicitly
        least_owned = []
        for c, count in target_counts.items():
            if count == min_count:
                least_owned.append(c)

        # list affordable tokens from least-owned colours
        affordable = []
        for token, cost in shop.items.items():
            if token[1] in least_owned and cost <= coins:
                affordable.append((token, cost))

        if not affordable:
            return []

        # prefer higher-value tokens
        affordable.sort(key=lambda x: x[0][0], reverse=True)
        chosen = [affordable[0][0]]
        remaining = coins - affordable[0][1]

        # try to buy another from the chosen set if we can afford it
        more_affordable = []
        for token, cost in shop.items.items():
            if token[1] in chosen_tokens and cost <= remaining:
                more_affordable.append((token, cost))

        if more_affordable:
            chosen.append(random.choice(more_affordable)[0])

        return chosen
    
    def flask_always(self, state, drawn_chip):
        """
        Always uses the flask whenever a white chip is drawn (if available).
        """
        value, colour = drawn_chip

        # Safety checks to ensure the chip is white, the flask is full and we havent gone bust.
        if state.flask != "FULL":
            return False

        if colour != "W":
            return False

        if state.white_sum + value > state.threshold:
            return False

        return True
    
    def flask_safe_next(self, state, drawn_chip):
        """
        Uses flask only when the next chip drawn could cause a bust.
        """
        value, colour = drawn_chip

        # Safety checks to ensure the chip is white, the flask is full and we havent gone bust.
        if state.flask != "FULL":
            return False

        if colour != "W":
            return False

        if state.white_sum + value > state.threshold:
            return False

        future_white_sum = state.white_sum + value

        # If any future white would bust then we want to use flask now.
        for chip in state.round_bag:
            next_value, next_colour = chip

            if next_colour == "W":
                if future_white_sum + next_value > state.threshold:
                    return True

        # No white chip in the bag could cause bust
        return False
    
    def flask_random(self, state, drawn_chip):
        """
        Randomly decides to use flask when a white chip is drawn.
        Default probability = 50%.
        """
        value, colour = drawn_chip

        if state.flask != "FULL":
            return False

        if colour != "W":
            return False

        if state.white_sum + value > state.threshold:
            return False
        
        probability = 0.5 

        rand = random.random()
        if rand < probability:
            return True
        return False

    def flask_prob_threshold(self, state, drawn_chip):
        """
        Uses the flask if the probability of busting on the next draw exceeds a chosen threshold.
        """

        # threshold defined here
        # change this to whatever you like (0.2 = 20%)
        threshold = 0.25

        value, colour = drawn_chip

        # flask must be full and chip must be white
        if state.flask != "FULL":
            return False

        if colour != "W":
            return False

        # illegal flask use check (should not happen)
        if state.white_sum + value > state.threshold:
            return False


        #Compute future white sum if we do not use flask
        future_white_sum = state.white_sum + value

        
        #Compute probability of busting next draw
        total = len(state.round_bag)
        if total == 0:
            return False  # nothing dangerous

        bust_probability = 0.0

        for chip in state.round_bag:
            next_value, next_colour = chip

            if next_colour == "W":
                # probability of this specific chip
                p = 1 / total

                if future_white_sum + next_value > state.threshold:
                    bust_probability += p

        if bust_probability > threshold:
            return True

        return False
    
    def ruby_buy_flask_only(self, rubies, state):
        """
        Buys only flasks.
        Never buys droplets.
        If the flask is full, returns no purchases.
        """

        decisions = []
        rubies_left = rubies

        # can only buy flask if it's empty and we have at least 2 rubies
        if state.flask == "EMPTY":
            if rubies_left >= 2:
                decisions.append("BUY_FLASK")
                return decisions

        return decisions

    def ruby_buy_droplets_only(self, rubies, state):
        """
        Always buys droplets when possible. Never refills the flask.
        """

        decisions = []
        rubies_left = rubies

        while rubies_left >= 2:
            decisions.append("BUY_DROPLET")
            rubies_left -= 2

        return decisions
    
    def joseph_blue_policy(self, chip_candidates, state):
        filtered_candidates = chip_candidates
        for chip in filtered_candidates:
            if chip[1] == "W":
                filtered_candidates.remove(chip)
            elif chip[1] == "R" and state.orange_count == 0:
                filtered_candidates.remove(chip)
            elif chip[1] == "Y" and self.draw_policy(state) == "DRAW":
                filtered_candidates.remove(chip)
            elif chip[1] == "G" and self.draw_policy(state) == "DRAW":
                filtered_candidates.remove(chip)

        if not filtered_candidates:
            return None
        
        else:
            return max(filtered_candidates, key=lambda x: x[0])