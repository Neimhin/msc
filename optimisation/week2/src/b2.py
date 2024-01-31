import sympy as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from lib import GradientDescent

LINEWIDTH = 0.5
CONVERGENCE_THRESHOLD = 0.001
x = sp.symbols('x')
y = x**4
dydx = y.diff()

fig, ax = plt.subplots(1, 3, figsize=(12,4))

blowup = 0.8

# alpha * (blowup ** 3) * 4 = 1.2

results = {
    "$\\alpha$": [],
    "start": [],
    "convergence time": [],
    "final guess": [],
}
iota = 0.000000000000001
for (step_size, start, color) in [
            (0.01, 1, 'green'),
            (0.02, 1, 'green'),
            (0.03, 1, 'green'),
            (0.04, 1, 'green'),
            (0.05, 1, 'green'),
            (0.1, 1, 'green'),
            (0.5 - iota, 1, 'green'),
            (0.5, 1, 'blue'),
            ((2*blowup)/((blowup**3)*4) + iota, blowup, 'red'),
            ((2*blowup)/((blowup**3)*4) - iota, blowup, 'purple'),
            (0.8, 0.7, 'black')
        ]:
    print(step_size, start, color)
    g = GradientDescent()
    g.max_iter(99)
    g.step_size(step_size)
    g.start(start)
    g.function(lambda x1: float(y.subs(x, x1)))
    y_diff = y.diff()
    g.gradient(lambda x1: float(y_diff.subs(x, x1)))
    g.debug(True)

    def converged(x1, x2):
        import math
        if x1 == math.inf or x2 == math.inf:
            print(x1, x2, x1 == math.inf, x1 is math.inf)
            return True
        abs = np.abs(x1-x2)
        print(abs, x1, x2)
        return abs < CONVERGENCE_THRESHOLD

    g.converged(converged)
    iterations, estimates, y_of_x = zip(*[
        (x[0], x[1], x[2]) for x in g.iterate()])
    results["$\\alpha$"].append(step_size)
    results["start"].append(start)
    results["convergence time"].append(len(iterations))
    results["final guess"].append(estimates[-1])
    print('y_of_x', y_of_x)
    print('iterations', iterations)
    print('estimates', estimates)
    sns.lineplot(
        x=iterations,
        y=estimates,
        ax=ax[0],
        linewidth=LINEWIDTH,
        legend=False,
        color=color,
        label=f"$\\alpha={step_size}$, $x={start}$")
    sns.lineplot(
        x=iterations,
        y=y_of_x,
        ax=ax[1],
        linewidth=LINEWIDTH,
        color=color,
        label=f"$\\alpha={step_size}$, $x={start}$")
    ax[2].step(
        estimates,
        y_of_x,
        linewidth=LINEWIDTH,
        color=color,
        label=f"$\\alpha={step_size}$, $x={start}$")
    xs = np.arange(-2, 2,0.01)
    ys = [ y.subs(x,xi) for xi in xs]
    ax[2].plot(
        xs,
        ys,
        linewidth=LINEWIDTH,
        label=f"$x^4$",
        color='yellow',
    )
    ax[2].scatter(
        start,
        g._function(start),
        color=color)


ax[0].set_ylabel("estimate of $\\mathrm{arg\\,min}_x x^4$")
ax[0].set_xlabel("iteration")
ax[1].set_ylabel("$y(\\hat{x})$")
ax[1].set_xlabel("iteration")
ax[0].set_ylim([-7, 7])
ax[1].set_ylim([-1, 10])
ax[2].set_ylim([-0.2, 2.2])
ax[2].set_xlim([-2, 2])
plt.tight_layout()

outfile = "fig/gradient-descent-b2.pdf"
if len(sys.argv) > 1:
    outfile = sys.argv[1]
plt.savefig(outfile)
df = pd.DataFrame(results)
print(df)
df.to_csv("fig/gradient-descent-b2.csv", index=False)
