import week6
import pandas as pd
import sympy as sp

T = pd.read_csv("data/T.csv").values

sympy_loss = week6.sympy_loss(T)

x1, x2 = sp.symbols('x1 x2', real=True)

dydx1 = sp.diff(sympy_loss, x1)
dydx2 = sp.diff(sympy_loss, x2)

solutions = sp.solve([sp.Eq(dydx1,0), sp.Eq(dydx2,0)], (x1, x2), simplify=False, rational=False, verbose=True)

print(solutions)
