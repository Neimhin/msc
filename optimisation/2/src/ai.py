import sympy as sp
x = sp.symbols('x')
y = x**4
print(y.diff())  # 4*x**3
