'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
from experiments.policybundles import *
from analysis.statistics import t_test, compare_means_to_baseline_opp_black_model, compare_means_to_baseline, simulate_multiple_print
from analysis.plotting import risk_factor_plot, flask_threshold_plot, ruby_stop_round_plot, ruby_stop_round_bar_plot, ruby_cap_bar_plot
from experiments.simulations import simulate_game

#print(t_test(EXPECTEDDRAW_RISKFACTOR2_ALWAYSVPS_ORANGEBLUEREDPURPLE, BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE, 10000))

# Risk Factor Code

'''
risk_factors = np.linspace(0, 3, 30)

switch_rounds = [2, 3, 4, 5, 6, 7, 8]

always_vp_bundles = expected_draw_bundles(risk_factors, sam_pl.bust_policy)
always_coins_bundles = expected_draw_bundles(risk_factors, sam_pl.bust_policy_coins)

tau_bundles_groups = []
tau_labels = []
for tau in switch_rounds:
    tau_bundles_groups.append(expected_draw_bundles_earlygamecoins(risk_factors, [tau]))
    tau_labels.append(f'Switch to VPs at Round {tau}')

all_bundle_groups = [always_vp_bundles, always_coins_bundles] + tau_bundles_groups
all_labels = ["Always Take VPs when Bust", "Always Take Coins when Bust"] + tau_labels
print("starting plot...")
risk_factor_plot(risk_factors,all_bundle_groups, all_labels, 3000, opp_black_model="never")
'''

'''
for opp_black_model in ["never", "random", "mirror"]:
    print(f"Comparing to baseline with opponent black model: {opp_black_model} ")
    df = compare_means_to_baseline_opp_black_model(BASELINE_NEVERBUST_SPENDALL, chip_prioritisation_bundles(), opp_black_model, 3000)
    
    print(df.to_markdown())
'''

#print(t_test(BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE, BASELINE_NEVERBUST_SPENDALL, 10000, "random"))

'''
df = compare_means_to_baseline_opp_black_model(BASELINE_NEVERBUST_SPENDALL, chip_prioritisation_bundles_with_a_black(), "random_scaled", 10000)
print(df.to_markdown())
'''
'''
df = compare_means_to_baseline_opp_black_model(CHIP_BUYING_POLICY_BASELINE, chip_prioritisation_bundles(), "never", 10000)
print(df.to_markdown())
'''
'''
df = compare_means_to_baseline_opp_black_model(CHIP_BUYING_POLICY_BASELINE, chip_prioritisation_bundles(), "random_scaled_one_only", 3000)
print(df.to_markdown())

df = compare_means_to_baseline_opp_black_model(CHIP_BUYING_POLICY_BASELINE, chip_prioritisation_bundles(), "random_scaled", 10000)
print(df.to_markdown())
'''
'''
thresholds = np.linspace(0, 1, 50)

all_bundle_groups = [flask_prob_threshold_policy_bundles(thresholds)]
all_labels = ["Threshold Flask Policy"]
print("starting plot...")
flask_threshold_plot(thresholds, all_bundle_groups, all_labels, 3000, opp_black_model="never")
'''

'''
print('Never use flask - \n')
simulate_multiple_print(BASELINE_NEVERUSEFLASK, "never", 3000)

print('Randomly use flask (prob 0.5)- \n')
simulate_multiple_print(BASELINE_RANDOMLYUSEFLASK, "never", 3000)

print('Always use flask (prob 0.5)- \n')
simulate_multiple_print(BASELINE_ALWAYSUSEFLASK, "never", 3000)
'''

'''
stop_rounds = list(range(0, 9))  # rounds 1–9

all_bundle_groups = [ruby_stop_round_policy_bundles(stop_rounds)]
all_labels = ["Ruby Droplets Until Round Policy"]

print("starting plot...")
ruby_stop_round_bar_plot(stop_rounds, all_bundle_groups, all_labels, 20000, opp_black_model="never")
'''
'''
caps = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

all_bundle_groups = [ruby_cap_policy_bundles(caps)]
all_labels = ["Ruby Droplet Cap Policy"]

ruby_cap_bar_plot(caps, all_bundle_groups, all_labels, 5000, opp_black_model="never")
'''

#print(t_test(BEST_OPPSNEVERBLACK_POLICY, CHIP_BUYING_POLICY_BASELINE, 10000, "never"))
#print(t_test(BEST_OPPSRANDOMSCALEDBLACK_POLICY, CHIP_BUYING_POLICY_BASELINE, 10000, "random_scaled"))

simulate_multiple_print(CHIP_BUYING_POLICY_BASELINE, "never", 3000)
simulate_multiple_print(CHIP_BUYING_POLICY_BASELINE_SPENDALLWITHBLACK, "never", 3000)

'''
df = compare_means_to_baseline_opp_black_model(CHIP_BUYING_POLICY_BASELINE, chip_prioritisation_bundles(), "random_scaled_softer", 10000)
print(df.to_markdown())
'''