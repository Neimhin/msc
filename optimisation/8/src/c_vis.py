import json
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def fix_costs_monotonic(costs):
    costs_monotonic = []
    best_cost = costs[0]
    for cost in costs:
        if cost <= best_cost:
            best_cost = cost
        costs_monotonic.append(best_cost)
    return costs_monotonic

def visualize_stats_time_vs_it_best_costs(json_file, **kwargs):
    with open(json_file, 'r') as f:
        results = json.load(f)
    print(results)
    time = results['results']['stats']['time']
    it_best_costs = results['results']['stats']['it_best_costs']
    it_best_costs = fix_costs_monotonic(it_best_costs)
    plt.plot(list(range(len(it_best_costs))), it_best_costs, linestyle='-', **kwargs)

# c-a-N30.json  c-b_mod-N20-M3-n1000-it3.json  c-b_mod-N20-M3-n5000-it3.json  c-b_mod-N20-M3-n500-it3.json  c-b-N10-M4-n500-it3.json
if __name__ == "__main__":
    plt.figure(figsize=(8, 6))
    plt.ylim(1.5, 2.2)
    visualize_stats_time_vs_it_best_costs('data/c-a-N99.json', label='rnd search a $(N=99,n=1000)$', color='orange')
    visualize_stats_time_vs_it_best_costs('data/c-b_mod-N33-M10-n1000-it3.json', label='rnd search b_mod $(N=33,M=10,n=1000)$', color='purple')
    visualize_stats_time_vs_it_best_costs('data/c-b-N33-M10-n1000-it3.json', label='rnd search b $(N=33,M=10,n=1000)$', color='blue')
    # visualize_stats_time_vs_it_best_costs('data/c-a-N100-M-1-n1000-it3.json', label='rnd search b')

    plt.axhline(y=1.8646, color='red', linestyle='--')
    plt.xlabel('function evaluations')
    plt.ylabel('logistic loss on test ($n=10000$)')
    custom_lines = [
            Line2D([0], [0], color='blue', lw=2),
            Line2D([0], [0], color='orange', lw=2),
            Line2D([0], [0], color='purple', lw=2),
            Line2D([0], [0], color='red', lw=2, linestyle='--'),
            ]
    custom_labels = ['rnd search b $(N=33,M=10,n=1000)$', 'rnd search a $(N=99,n=1000)$', 'rnd search b_mod $(N=33,M=10,n=1000)$', 'baseline']
    plt.legend(custom_lines, custom_labels)
    plt.savefig('fig/c.pdf')
