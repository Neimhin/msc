import sympy as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from lib import GradientDescent

LINEWIDTH = 0.1
x = sp.symbols('x')
y = x**4
dydx = y.diff()

fig, ax = plt.subplots(1, 3, figsize=(12,4))

blowup = 0.8

# alpha * (blowup ** 3) * 4 = 1.2

results = {
    "alpha": [],
    "start": [],
    "gamma": [],
    "$f(x)$": [],
    "convergence time": [],
    "final guess": [],
}
iota = 0.005
def run(gamma, color, max_iter=99, plot=True):
    g = GradientDescent()
    g.max_iter(max_iter)
    alpha = 1
    start = 1
    g.step_size(alpha)
    g.start(start)
    y = gamma * (x**2)
    g.function(lambda x1: float(y.subs(x, x1)))
    y_diff = y.diff()
    g.gradient(lambda x1: float(y_diff.subs(x, x1)))
    g.debug(True)

    def is_inf(x):
        import math
        if x == math.inf or x == -math.inf:
            return True

    def converged(x1, x2):
        if is_inf(x1) or is_inf(x2):
            return True
        abs = np.abs(x1-x2)
        print(abs, x1, x2)
        return abs < 0.001
    g.converged(converged)
    iterations, estimates, y_of_x = zip(*[
        (x[0], x[1], x[2]) for x in g.iterate()])
    results["alpha"].append(alpha)
    results["gamma"].append(gamma)
    results["$f(x)$"].append(str(y))
    results["start"].append(start)
    results["convergence time"].append(len(iterations))
    results["final guess"].append(estimates[-1])
    if plot:
        sns.lineplot(
            x=iterations,
            y=estimates,
            ax=ax[0],
            linewidth=LINEWIDTH,
            legend=False,
            color=color,
            label=f"$\\gamma={gamma}$")
        sns.lineplot(
            x=iterations,
            y=y_of_x,
            ax=ax[1],
            linewidth=LINEWIDTH,
            color=color,
            label=f"$\\gamma={gamma}$")
        ax[2].step(
            estimates,
            y_of_x,
            linewidth=LINEWIDTH,
            color=color,
            label=f"$\\gamma={gamma}$")
        xs = np.arange(-2, 2, 0.01)
        ys = [y.subs(x, xi) for xi in xs]
        ax[2].plot(
            xs,
            ys,
            linewidth=LINEWIDTH,
            label="$\\gamma x^2$",
            color='yellow',
        )
        ax[2].scatter(
            start,
            g._function(start),
            color=color)


for (gamma, color) in [
            ( 0.01, 'green'),
            ( 0.1, 'blue'),
            ( 1 - iota, 'black'),
            (1 + iota, 'orange'),
            ( 1, 'red'),
            (-0.05, 'purple'),
        ]:
    run(gamma, color)

run(-1000, 'pink', max_iter=10000, plot=False)

ax[0].set_ylabel("$x$")
ax[0].set_xlabel("iteration")
ax[0].set_title("(a)")
ax[1].set_ylabel("$y(\\hat{x})$")
ax[1].set_xlabel("iteration")
ax[1].set_title("(b)")
ax[2].set_xlabel("$x$")
ax[2].set_ylabel("$y$")
ax[2].set_title("(c)")
ax[0].set_ylim([-7, 7])
ax[1].set_ylim([-1, 4])
ax[2].set_ylim([-1, 2.2])
ax[2].set_xlim([-2, 2])
plt.tight_layout()

outfile = "fig/gradient-descent-ci.pdf"
if len(sys.argv) > 1:
    outfile = sys.argv[1]
plt.savefig(outfile)
df = pd.DataFrame(results)
print(df)
df.to_csv("fig/gradient-descent-ci.csv")
