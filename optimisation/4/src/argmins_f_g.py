from sympy import symbols, diff, solve
import sympy as sp

# Define the symbolic variables
x, y = symbols('x y',real=True)

# Define the functions
f = 3 * (x - 5)**4 + 10 * (y - 9)**2
g = sp.Max(x - 5, 0) + 10 * sp.Abs(y - 9)

grad_f = [diff(f, var) for var in (x, y)]
argmin_f = solve(grad_f, (x, y))
print(f"Argmin of f(x, y): {argmin_f}")

grad_g = [diff(g, var) for var in (x, y)]
argmin_g = solve(grad_g, (x, y))
print(f"Argmin of g(x, y): {argmin_g}")
