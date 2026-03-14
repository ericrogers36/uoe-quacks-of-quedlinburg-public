# analysis/statistics.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
import pandas as pd
from math import sqrt
from scipy.stats import t as student_t 
from experiments.simulations import simulate_game, simulate_multiple, simulate_multiple_parallel

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

def one_game_df():
    game = simulate_game()
    df = pd.DataFrame(game.round_records)
    return df
