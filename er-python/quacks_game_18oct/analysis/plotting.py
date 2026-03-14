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

def risk_factor_plot(risk_factors, bundles_list, labels, n):

    plt.figure(figsize=(10, 6))

    for bundles, label in zip(bundles_list, labels):
        means = []
        errors = []

        #print(len(risk_factors), len(bundles))
        for bundle in bundles:
            results = simulate_multiple(bundle, n)

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
    plt.title(f'Expected Victory Points vs Risk Factor for Different Policy Bundles, n = {n}')
    plt.legend()
    plt.grid(True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'./plots/expected_vps_vs_risk_factor_{ts}.png')
    print(f'graph saved as expected_vps_vs_risk_factor_{ts}.png')
    #plt.show()
    #plt.save