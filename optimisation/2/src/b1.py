import sympy as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import seaborn as sns
import pandas as pd
from lib import GradientDescent

LINEWIDTH = 0.5
x = sp.symbols('x')
y = x**4
dydx = y.diff()

fig, ax = plt.subplots(1, 3, figsize=(12, 8))

blowup = 0.8

# alpha * (blowup ** 3) * 4 = 1.2

results = {
    "alpha": [],
    "start": [],
    "convergence time": [],
    "final guess": [],
}
iota = 0.00000000001
settings = [
            (0.1, 1),
            (0.03, 1),
            (0.5, 1),
            (0.25, 1),
            ((2*blowup)/((blowup**3)*4) + iota, blowup),
            ((2*blowup)/((blowup**3)*4) - iota, blowup),
            (0.05, 0.7),
            (0.1, 0.7),
            (0.15, 0.7),
            (0.1, 2),
]
color = cm.rainbow(np.linspace(0, 1, len(settings)))
settings_with_color = zip(settings, color)
for ((step_size, start), color) in settings_with_color:
    print(step_size, start, color)
    g = GradientDescent()
    g.max_iter(100)
    g.step_size(step_size)
    g.start(start)
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
    results["alpha"].append(step_size)
    results["start"].append(start)
    results["convergence time"].append(len(iterations))
    results["final guess"].append(estimates[-1])
    print('y_of_x', y_of_x)
    print('iterations', iterations)
    print('estimates', estimates)
    sns.lineplot(
        x=iterations,
        y=np.abs(np.array(estimates)),
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
    xs = np.arange(-2, 2, 0.01)
    ys = [y.subs(x, xi) for xi in xs]
    ax[2].plot(
        xs,
        ys,
        linewidth=LINEWIDTH,
        label="$x^4$",
        color='yellow',
    )
    ax[2].scatter(
        start,
        g._function(start),
        color=color)

ax[1].legend(framealpha=1)
ax[0].set_ylabel("$|\\hat x|$")
ax[0].set_xlabel("iteration")
ax[0].set_yscale('log')
ax[1].set_yscale('log')
ax[0].set_title("(a)")
ax[1].set_ylabel("$y(\\hat{x})$")
ax[1].set_xlabel("iteration")
ax[1].set_title("(b)")
ax[2].set_xlabel("$x$")
ax[2].set_ylabel("$y$")
ax[2].set_title("(c)")
ax[0].set_ylim([10**-2, 1.5])
ax[1].set_ylim([10**-6, 1.5])
ax[2].set_ylim([-0.2, 2.2])
ax[2].set_xlim([-2, 2])

plt.tight_layout()

outfile = "fig/gradient-descent-b1.pdf"
if len(sys.argv) > 1:
    outfile = sys.argv[1]
plt.savefig(outfile)
df = pd.DataFrame(results)
print(df)
df.to_csv("fig/gradient-descent-b1.csv")
