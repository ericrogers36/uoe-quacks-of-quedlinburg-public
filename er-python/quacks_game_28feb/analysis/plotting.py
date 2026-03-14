# analysis/plotting.py

'''
Author - Eric Rogers
Institution: The University of Edinburgh, School of Mathematics
Year 4 Project - "How to win the board game 'Quacks of Quedlinburg'"
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from experiments.simulations import simulate_game, simulate_multiple, simulate_multiple_parallel

def risk_factor_plot(risk_factors, bundles_list, labels, n, opp_black_model):

    plt.figure(figsize=(10, 6))

    for bundles, label in zip(bundles_list, labels):
        means = []
        errors = []

        #print(len(risk_factors), len(bundles))
        for bundle in bundles:
            results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)

            mean = np.mean(results)
            se = np.std(results)/np.sqrt(len(results))
            means.append(mean)
            errors.append(se)

        plt.errorbar(
                risk_factors,
                means,
                yerr=errors,
                label=label,
                capsize=5,
                marker='o'
            )
    
    #print(len(means), len(errors))
    plt.xlabel(r"Risk Factor $\varrho$ (lower is riskier)")
    plt.ylabel('Expected Victory Points')
    plt.title(f'Expected Victory Points vs Risk Factor for Different Policy Bundles, n = {n}, Opponent Black Model: {opp_black_model}')
    plt.legend()
    plt.grid(True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_risk_factor_{ts}.png')
    print(f'graph saved as expected_vps_vs_risk_factor_{ts}.png')

def flask_threshold_plot(thresholds, bundles_list, labels, n, opp_black_model):

    plt.figure(figsize=(10, 6))

    for bundles, label in zip(bundles_list, labels):
        means = []
        errors = []

        #print(len(risk_factors), len(bundles))
        for bundle in bundles:
            results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)

            mean = np.mean(results)
            se = np.std(results)/np.sqrt(len(results))
            means.append(mean)
            errors.append(se)

        plt.errorbar(
                thresholds,
                means,
                yerr=errors,
                label=label,
                capsize=5,
                marker='o'
            )
    
    #print(len(means), len(errors))
    plt.xlabel(r"Flask Threshold Value")
    plt.ylabel('Expected Victory Points')
    plt.title(f'Expected Victory Points vs Threshold for Different Policy Bundles, n = {n}, Opponent Black Model: {opp_black_model}')
    plt.legend()
    plt.grid(True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_flask_threshold_{ts}.png')
    print(f'graph saved as expected_vps_vs_flask_threshold_{ts}.png')
    #plt.show()
    #plt.save

def ruby_stop_round_plot(stop_rounds, bundles_list, labels, n, opp_black_model):
    plt.figure(figsize=(10, 6))

    for bundles, label in zip(bundles_list, labels):
        means = []
        errors = []

        for bundle in bundles:
            results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)

            mean = np.mean(results)
            se = np.std(results) / np.sqrt(len(results))
            means.append(mean)
            errors.append(se)

        plt.errorbar(
            stop_rounds,
            means,
            yerr=errors,
            label=label,
            capsize=5,
            marker='o'
        )

    plt.xlabel("Ruby Droplet Stop Round")
    plt.ylabel("Expected Victory Points")
    plt.title(
        f"Expected Victory Points vs Ruby Stop Round for Different Policy Bundles, "
        f"n = {n}, Opponent Black Model: {opp_black_model}"
    )
    plt.legend()
    plt.grid(True)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_ruby_stop_round_{ts}.png')
    print(f'graph saved as expected_vps_vs_ruby_stop_round_{ts}.png')

def ruby_stop_round_bar_plot(stop_rounds, bundles_list, labels, n, opp_black_model):
    plt.figure(figsize=(10, 6))

    num_groups = len(bundles_list)
    x = np.arange(len(stop_rounds))
    bar_width = 0.8 / num_groups

    for i, (bundles, label) in enumerate(zip(bundles_list, labels)):
        means = []
        errors = []

        for bundle in bundles:
            results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)

            mean = np.mean(results)
            se = np.std(results) / np.sqrt(len(results))
            means.append(mean)
            errors.append(se)

        positions = x + i * bar_width - (num_groups - 1) * bar_width / 2

        bars = plt.bar(
            positions,
            means,
            width=bar_width,
            yerr=errors,
            capsize=5,
            label=label
        )

        # label each bar with its value
        for bar, mean in zip(bars, means):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                mean + 0.2,
                f"{mean:.2f}",
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.xlabel("Ruby Droplet Stop Round")
    plt.ylabel("Expected Victory Points")

    plt.title(
        f"Expected Victory Points vs Ruby Stop Round for Different Policy Bundles, "
        f"n = {n}, Opponent Black Model: {opp_black_model}"
    )

    plt.xticks(x, stop_rounds)

    # zoom in
    plt.ylim(bottom=35)

    plt.legend()
    plt.grid(True, axis='y')

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_ruby_stop_round_{ts}.png')
    print(f'graph saved as expected_vps_vs_ruby_stop_round_{ts}.png')

def ruby_cap_bar_plot(caps, bundles_list, labels, n, opp_black_model):
    plt.figure(figsize=(10, 6))

    num_groups = len(bundles_list)
    x = np.arange(len(caps))
    bar_width = 0.8 / num_groups

    for i, (bundles, label) in enumerate(zip(bundles_list, labels)):
        means = []
        errors = []

        for bundle in bundles:
            results = simulate_multiple(bundle, n, opp_black_model=opp_black_model)

            mean = np.mean(results)
            se = np.std(results) / np.sqrt(len(results))
            means.append(mean)
            errors.append(se)

        positions = x + i * bar_width - (num_groups - 1) * bar_width / 2

        bars = plt.bar(
            positions,
            means,
            width=bar_width,
            yerr=errors,
            capsize=5,
            label=label
        )

        # label each bar with its value
        for bar, mean in zip(bars, means):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                mean + 0.2,
                f"{mean:.2f}",
                ha='center',
                va='bottom',
                fontsize=9
            )

    plt.xlabel("Ruby Droplet Cap")
    plt.ylabel("Expected Victory Points")

    plt.title(
        f"Expected Victory Points vs Ruby Droplet Cap for Different Policy Bundles, "
        f"n = {n}, Opponent Black Model: {opp_black_model}"
    )

    plt.xticks(x, caps)

    # zoom in
    plt.ylim(bottom=35)

    plt.legend()
    plt.grid(True, axis='y')

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_ruby_cap_{ts}.png')
    print(f'graph saved as expected_vps_vs_ruby_cap_{ts}.png')