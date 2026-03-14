# experiments/policybundles.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
from game.policies_18oct import PolicyBundle, SamsPolicyLibrary, TestPolicyLibrary
from itertools import combinations

sam_pl, test_pl = SamsPolicyLibrary(), TestPolicyLibrary()

# DECLARE POLICY LIBRARIES

EXPERIMENTAL_POLICY_BUNDLE = PolicyBundle(
    #draw_policy = sam_pl.expected_draw_policy, # sam expected draw policy
    draw_policy = test_pl.never_bust, # draw policy
    blue_policy = sam_pl.joseph_blue_policy, # blue chip policy
    bust_policy = sam_pl.bust_policy, # bust policy
    #chip_buy_policy = sam_pl.chip_buy_policy, # chip buying policy
    chip_buy_policy = sam_pl.spend_all,
    #chip_buy_policy = sam_pl.orange_red,
    ruby_buy_policy = sam_pl.always_buy_ruby_droplet, # ruby spending policy
    flask_policy = sam_pl.flask_policy, # flask policy
    name = "Safe (never bust) Draw Policy + Joseph Blue + Always Take VPs when Bust, Spend All, Default Ruby and Flask",
)

BASELINE_NEVERBUST_SPENDALL = PolicyBundle(
    #draw_policy = sam_pl.expected_draw_policy, # sam expected draw policy
    draw_policy = test_pl.never_bust, # draw policy
    blue_policy = sam_pl.joseph_blue_policy, # blue chip policy
    bust_policy = sam_pl.bust_policy, # bust policy
    #chip_buy_policy = sam_pl.chip_buy_policy, # chip buying policy
    chip_buy_policy = sam_pl.spend_all,
    #chip_buy_policy = sam_pl.orange_red,
    ruby_buy_policy = sam_pl.ruby_buy_droplets_only, # ruby spending policy
    flask_policy = sam_pl.flask_random, # flask policy
    name = "Baseline - Never Bust, Spend All",
)

BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE= PolicyBundle(
    #draw_policy = sam_pl.expected_draw_policy, # sam expected draw policy
    draw_policy = test_pl.never_bust, # draw policy
    blue_policy = sam_pl.joseph_blue_policy, # blue chip policy
    bust_policy = sam_pl.bust_policy, # bust policy
    #chip_buy_policy = sam_pl.chip_buy_policy, # chip buying policy
    #chip_buy_policy = sam_pl.spend_all,
    chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
    ruby_buy_policy = sam_pl.ruby_buy_droplets_only, # ruby spending policy
    flask_policy = sam_pl.flask_random, # flask policy
    name = "Never Bust Baseline - Buy Only O, BL, R, P",
)

chip_colours = ["O", "BK", "BL", "R", "G", "P", "Y"]

all_combinations = [
    list(combo)
    for r in range(1, len(chip_colours) + 1)
    for combo in combinations(chip_colours, r)
]

#print(all_combinations)
#print(len(all_combinations))  # 127

def chip_prioritisation_bundles():

    policybundles_chip_prioritisation = []

    for combo in all_combinations:
        bundle = PolicyBundle(
            draw_policy = test_pl.never_bust,
            blue_policy = sam_pl.joseph_blue_policy,
            bust_policy = sam_pl.bust_policy,
            chip_buy_policy = lambda coins, state, shop, combo=combo:
                sam_pl.combination_buying(coins, state, shop, combo),
            ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
            flask_policy = sam_pl.flask_random,
            name = f"Chip Prioritisation - Buy only {combo}",
        )

        policybundles_chip_prioritisation.append(bundle)
    
    return policybundles_chip_prioritisation

# risk_factors = np.linspace(0.5, 2.5, 10)
def expected_draw_bundles(risk_factors, user_bust_policy):
    policybundles_expecteddraws = []

    for rf in risk_factors:
        bundle = PolicyBundle(
            draw_policy = lambda state, rf=rf, bp=user_bust_policy: 
                sam_pl.expected_draw_policy(state, risk_factor=rf, bust_policy=bp),
            blue_policy = sam_pl.joseph_blue_policy,
            bust_policy = user_bust_policy,  # Same bust policy
            chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
            ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
            flask_policy = sam_pl.flask_random,
            name = f"Expected Draw (rho={rf}) - Bust Policy {user_bust_policy}, Buy Only O, BL, R, P"
            )
        policybundles_expecteddraws.append(bundle)
    return policybundles_expecteddraws

def expected_draw_bundles_earlygamecoins(risk_factors, switch_rounds):
    policybundles_expecteddraws = []

    for rf in risk_factors:
        for tau in switch_rounds:
            earlycoins_bust_policy = lambda state, roundwhenvpsinstead = tau : sam_pl.bust_policy_earlylategame(state, roundwhenvpsinstead)
            bundle = PolicyBundle(
                draw_policy = lambda state, rf=rf, bp=earlycoins_bust_policy: 
                    sam_pl.expected_draw_policy(state, risk_factor=rf, bust_policy=bp),
                blue_policy = sam_pl.joseph_blue_policy,
                bust_policy = earlycoins_bust_policy,  # Same bust policy
                chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
                ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
                flask_policy = sam_pl.flask_random,
                name = f"Expected Draw (rho={rf}) - Switch to VPs at {tau}, Buy Only O, BL, R, P"
                )
            policybundles_expecteddraws.append(bundle)
    return policybundles_expecteddraws

EXPECTEDDRAW_RISKFACTOR2_ALWAYSVPS_ORANGEBLUEREDPURPLE = PolicyBundle(
        draw_policy = lambda state, risk_factor=2, bp=sam_pl.bust_policy: 
            sam_pl.expected_draw_policy(state, risk_factor, bust_policy=bp),
        blue_policy = sam_pl.joseph_blue_policy,
        bust_policy = sam_pl.bust_policy,  # Same bust policy
        chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
        ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
        flask_policy = sam_pl.flask_random,
        name = f"Expected Draw (rho=2) - Take VPs, Buy Only O, BL, R, P"
        )