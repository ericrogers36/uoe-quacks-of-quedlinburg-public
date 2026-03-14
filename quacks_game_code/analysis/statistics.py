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

def compare_means_to_baseline_opp_black_model(baseline_bundle, bundles, opp_black_model, n):
    # Compute baseline once
    baseline_results = simulate_multiple(baseline_bundle, n)
    baseline_mean = np.mean(baseline_results)
    baseline_sem = np.std(baseline_results, ddof=1) / np.sqrt(n) 

    records = []

    for bundle in bundles:
        results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)
        mean_score = np.mean(results)
        sem = np.std(results, ddof=1) / np.sqrt(n)

        diff_error = np.sqrt(sem**2 + baseline_sem**2)

        records.append({
            "Policy": bundle.name,
            "Black Model": opp_black_model,
            "Mean VP": mean_score,
            #"Baseline Mean": baseline_mean,
            "Difference (Policy - Baseline)": mean_score - baseline_mean,
            "Difference Std. Error": diff_error,

        })

    df = pd.DataFrame(records)
    df = df.sort_values("Mean VP", ascending=False).reset_index(drop=True)

    return df
def t_test(bundle_a, bundle_b, n, opp_black_model):
    '''
    bundle_a tested against the baseline bundle_b
    '''
    # compute bundle stats
    results_a = simulate_multiple(bundle_a, n, opp_black_model=opp_black_model)
    results_b = simulate_multiple(bundle_b, n, opp_black_model=opp_black_model)
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

def simulate_multiple_print(policybundle, opp_black_model, n):
    results = np.array([simulate_game(policybundle, opp_black_model).VPs for _ in range(n)])
    print(f'n = {n}, Mean = {np.mean(results)}, S.D. = {np.std(results)}, Max = {np.max(results)}, Min = {np.min(results)}')