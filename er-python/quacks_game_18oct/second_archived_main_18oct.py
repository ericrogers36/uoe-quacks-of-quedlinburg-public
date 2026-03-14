'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
import pandas as pd
import random
from collections import Counter
from itertools import combinations
import matplotlib.pyplot as plt
from IPython.display import display
from game.game_18oct import QuacksOfQuedlinburg
from game.state_18oct import GameState
from game.shop_18oct import Shop

from math import sqrt
from scipy.stats import t as student_t 

from game.policies_18oct import PolicyBundle, SamsPolicyLibrary, TestPolicyLibrary

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
    name = "Safe (never bust) Draw Policy + Joseph Blue + RubyOnly + RandomFlask",
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
    name = "O, BL, R, P + Joseph Blue + Always Take VPs when Bust, Default Ruby and Flask",
)

chip_colours = ["O", "BK", "BL", "R", "G", "P", "Y"]

all_combinations = [
    list(combo)
    for r in range(1, len(chip_colours) + 1)
    for combo in combinations(chip_colours, r)
]

#print(all_combinations)
#print(len(all_combinations))  # 127


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
        name = f"Buy only {combo}",
    )

    policybundles_chip_prioritisation.append(bundle)

policybundles_expecteddraws = []
risk_factors = np.linspace(0.5, 2.5, 10)
for rf in risk_factors:
    bundle = PolicyBundle(
        draw_policy = lambda state, rf=rf, bp=sam_pl.bust_policy: 
            sam_pl.expected_draw_policy(state, risk_factor=rf, bust_policy=bp),
        blue_policy = sam_pl.joseph_blue_policy,
        bust_policy = sam_pl.bust_policy,  # Same bust policy
        chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
        ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
        flask_policy = sam_pl.flask_random,
        name = f"Expected Draw (τ={rf}) - Take VPs, Buy Only O, BL, R, P"
        )
    policybundles_expecteddraws.append(bundle)

EXPECTEDDRAW_RISKFACTOR2_ALWAYSVPS_ORANGEBLUEREDPURPLE = PolicyBundle(
        draw_policy = lambda state, risk_factor=2, bp=sam_pl.bust_policy: 
            sam_pl.expected_draw_policy(state, risk_factor, bust_policy=bp),
        blue_policy = sam_pl.joseph_blue_policy,
        bust_policy = sam_pl.bust_policy,  # Same bust policy
        chip_buy_policy =  lambda coins, state, shop: sam_pl.combination_buying(coins, state, shop, ["O", "BL", "R", "P"]),
        ruby_buy_policy = sam_pl.ruby_buy_droplets_only,
        flask_policy = sam_pl.flask_random,
        name = f"Expected Draw (τ=2) - Take VPs, Buy Only O, BL, R, P"
        )

init_bag = [(1, "W")] * 4 + [(2, "W"), (3, "W"), (1, "O"), (1, "G")]


def simulate_game(policybundle):
    '''
    Simulate a game
    '''
    state = GameState(init_bag, 
                      shop = Shop(), 
                      seed = None
                      )
    game = QuacksOfQuedlinburg(state)

    #policy = SamsPolicy()
    
    for round_num in range(1, 10): # we play 9 rounds like the board game
        #print(round)
        state = game.play_round(state, 
                                draw_policy = policybundle.draw_policy, # draw policy
                                blue_policy = policybundle.blue_policy, # blue chip policy
                                bust_policy = policybundle.bust_policy, # bust policy
                                chip_buy_policy = policybundle.chip_buy_policy, # chip buy policy
                                ruby_buy_policy = policybundle.ruby_buy_policy, # ruby spending policy
                                flask_policy = policybundle.flask_policy # flask policy
                                )
        state.record_round_state()
        state.round_advance()        
    return state

def one_game_df():
    game = simulate_game()
    df = pd.DataFrame(game.round_records)
    return df

def simulate_multiple_print(policybundle, n):
    results = np.array([simulate_game(policybundle).VPs for _ in range(n)])
    print(f'n = {n}, Mean = {np.mean(results)}, S.D. = {np.std(results)}, Max = {np.max(results)}, Min = {np.min(results)}')

def simulate_multiple(policybundle, n):
    return np.array([simulate_game(policybundle).VPs for _ in range(n)])

def plot_multiple(policybundle, n):
    results = [simulate_game(policybundle).VPs for _ in range(n)]
    
    counts = Counter(results)

    xs = sorted(counts.keys())
    ys = [counts[x] for x in xs]

    plt.figure()
    plt.bar(xs, ys)
    plt.xlabel("Victory Points (final)")
    plt.ylabel("Frequency")
    plt.title(f"Quacks Sim - {n} games, Min = {np.min(results)}, Max = {np.max(results)}")
    plt.show()

def results_stats(results):
    return {
        "mean": np.mean(results),
        "std": np.std(results),
        "median": np.median(results),
        "min": np.min(results),
        "max": np.max(results),
        "q1": np.percentile(results, 25),
        "q3": np.percentile(results, 75), 

    }

def t_test(bundle_a, bundle_b, n):
    '''
    bundle_a tested against the baseline bundle_b
    '''
    # compute bundle stats
    results_a = simulate_multiple(bundle_a, n)
    results_b = simulate_multiple(bundle_b, n)
    mean_a, mean_b = np.mean(results_a), np.mean(results_b)
    var_a, var_b = np.var(results_a, ddof=1), np.var(results_b, ddof=1)

    se = sqrt(var_a/n + var_b/n)
    df = (var_a/n + var_b/n)**2 / (((var_a/n)**2)/(n-1) + ((var_b/n)**2)/(n-1))

    t_stat = (mean_a - mean_b) / se
    p_value = 1 - student_t.cdf(t_stat, df)

    return {
        "bundle_a": bundle_a.name,
        "bundle_b": bundle_b.name,
        "mean_a": mean_a,
        "mean_b": mean_b,
        "difference": mean_a - mean_b,
        "t_statistic": t_stat,
        "degrees_of_freedom": df,
        "p_value": p_value
    }
#print(results_stats(simulate_multiple(EXPERIMENTAL_POLICY_BUNDLE, 10000)))

#print(results_stats(simulate_multiple(BASELINE_NEVERBUST_SPENDALL, 10000)))

#print(t_test(BASELINE_NEVERBUST_SPENDALL, BASELINE_NEVERBUST_ORANGERED, 10000))

def compare_means_to_baseline(baseline_bundle, bundles, n):
    
    # Compute baseline once
    baseline_results = simulate_multiple(baseline_bundle, n)
    baseline_mean = np.mean(baseline_results)

    records = []

    for bundle in bundles:
        results = simulate_multiple(bundle, n)
        mean_score = np.mean(results)

        records.append({
            "Policy": bundle.name,
            "Mean VP": mean_score,
            "Baseline Mean": baseline_mean,
            "Difference (Policy - Baseline)": mean_score - baseline_mean
        })

    df = pd.DataFrame(records)
    df = df.sort_values("Mean VP", ascending=False).reset_index(drop=True)

    return df
'''
df_results = compare_means_to_baseline(
    BASELINE_NEVERBUST_SPENDALL,
    policybundles_chip_prioritisation,
    3000   # adjust as needed
)

print("\nBaseline:", BASELINE_NEVERBUST_SPENDALL.name)
display(df_results)
'''

#print(t_test(BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE, BASELINE_NEVERBUST_SPENDALL, 10000))
print(t_test(EXPECTEDDRAW_RISKFACTOR2_ALWAYSVPS_ORANGEBLUEREDPURPLE, BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE, 10000))
'''
df_results = compare_means_to_baseline(
    BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE,
    policybundles_expecteddraws,
    5000   # adjust as needed
)

print("\nBaseline:", BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE.name)
display(df_results)
'''