import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

LINEWIDTH = 0.7


def my_range():
    return np.arange(100, 100.0001, step=0.00001)


# finite difference
def diff_with_pert(f, xval, pert=0.01):
    global x
    delta_x = pert
    return (f.subs(x, xval + delta_x) - f.subs(x, xval)) / (delta_x)


x = sp.symbols('x')
y = x**4
dydx = y.diff()
analytic_ys = [dydx.subs(x, i) for i in my_range()]

plt.figure(figsize=(8, 4))
plt.plot(
        np.array(list(my_range())),
        analytic_ys,
        linewidth=LINEWIDTH,
        label="analytic")

for pert in np.array([0.001, 0.01, 0.02, 0.03, 0.04, 0.1]):
    dydx_finite = diff_with_pert(y, x, pert=pert)
    finite_diff_ys = [dydx_finite.subs(x, i) for i in my_range()]
    plt.plot(
            my_range(),
            finite_diff_ys,
            linewidth=LINEWIDTH,
            label=f"finite diff $\\delta={pert}$")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.legend()
plt.tight_layout()
plt.savefig("fig/finite-diff.pdf")
