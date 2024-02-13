import sympy as sp
# finite difference
def diff_with_pert(f, xval, pert=0.01):
    global x
    delta_x = pert
    return (f.subs(x, xval + delta_x) - f.subs(x, xval)) / (delta_x)
x = sp.symbols('x')
y = x**4
dydx = y.diff()
analytic_ys = [dydx.subs(x, i) for i in my_range()]
# ...
for pert in np.array([0.01, 0.1, 0.15]):
    dydx_finite = diff_with_pert(y, x, pert=pert)
    # ...
