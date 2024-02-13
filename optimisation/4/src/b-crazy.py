import sympy as sp
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from lib import GradientDescent

LINEWIDTH = 0.7
x = sp.symbols('x')
y = x**4
dydx = y.diff()

fig, ax = plt.subplots(1, 2)

for step_size in np.array([0.5]):
    for start in np.array([1.00001]):
        print(step_size, start)
        g = GradientDescent()
        g.max_iter(100)
        g.step_size(step_size)
        g.start(start)
        g.function(lambda x1: float(y.subs(x, x1)))
        y_diff = y.diff()
        g.gradient(lambda x1: float(y_diff.subs(x, x1)))
        g.debug(True)

        def converged(x1, x2):
            abs = np.abs(x1-x2)
            print(abs, x1, x2)
            return abs < 0.001
        g.converged(converged)
        iterations, estimates, y_of_x = zip(*[(x[0], x[1], x[2]) for x in g.iterate()])
        print('y_of_x', y_of_x)
        print('iterations', iterations)
        print('estimates', estimates)
        sns.lineplot(
            x=iterations,
            y=estimates,
            ax=ax[0],
            linewidth=LINEWIDTH,
            legend=False,
            label=f"$\\alpha={step_size}$, $x={start}$")
        sns.lineplot(
            x=iterations,
            y=y_of_x,
            ax=ax[1],
            linewidth=LINEWIDTH,
            label=f"$\\alpha={step_size}$, $x={start}$")

ax[0].set_ylabel("estimate of $\\mathrm{arg\\,min}_x x^4$")
ax[0].set_xlabel("iteration")
ax[1].set_ylabel("$y(\\hat{x})$")
ax[1].set_xlabel("iteration")
ax[0].set_ylim([-10000, 10000])
ax[1].set_ylim([-100, 10000])
plt.tight_layout()

outfile = "fig/gradient-descent-x^4-crazy.pdf"
if len(sys.argv) > 1:
    outfile = sys.argv[1]
print(outfile)
plt.savefig(outfile)
