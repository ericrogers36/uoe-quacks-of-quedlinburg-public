'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
from experiments.policybundles import *
from analysis.statistics import t_test
from analysis.plotting import risk_factor_plot


#print(t_test(EXPECTEDDRAW_RISKFACTOR2_ALWAYSVPS_ORANGEBLUEREDPURPLE, BASELINE_NEVERBUST_ORANGEBLUEREDPURPLE, 10000))

risk_factors = np.linspace(0.1, 3, 20)

switch_rounds = [2, 3, 4, 5, 6, 7, 8]

always_vp_bundles = expected_draw_bundles(risk_factors, sam_pl.bust_policy)
always_coins_bundles = expected_draw_bundles(risk_factors, sam_pl.bust_policy_coins)

tau_bundles_groups = []
tau_labels = []
for tau in switch_rounds:
    tau_bundles_groups.append(expected_draw_bundles_earlygamecoins(risk_factors, [tau]))
    tau_labels.append(f"Switch to VPs at Round {tau}")

all_bundle_groups = [always_vp_bundles, always_coins_bundles] + tau_bundles_groups
all_labels = ["Always Take VPs when Bust", "Always Take Coins when Bust"] + tau_labels
print("starting plot...")
risk_factor_plot(risk_factors,all_bundle_groups, all_labels, 1000)