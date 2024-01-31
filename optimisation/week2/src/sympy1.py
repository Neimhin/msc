import sympy as sp

x = sp.symbols('x')
print(x)
f = x ** 4
print(f)
print(f.diff())
print(f.subs(x, x**2))
print(f.conjugate())
print(f)
print(f.subs())
