import sys
import pandas as pd
import lib
import numpy as np
import matplotlib.pyplot as plt

outfile = sys.argv[1]
infiles = sys.argv[2:]

print('out', outfile)
print('in', infiles)

def f(x, y):
    return 3 * (x - 5)**4 + 10 * (y - 9)**2


def g(x, y):
    return np.maximum(x - 5, 0) + 10 * np.abs(y - 9)


fig = plt.figure(figsize=(12, 6))

for f in infiles:
    df = pd.read_csv(f)

    function_name = df["function_name"][0]
    function = f if function_name == 'f' else g

    x = np.linspace(0, 10, 400)
    y = np.linspace(0, 18, 400)
    X, Y = np.meshgrid(x, y)
    Z_f = function(X, Y)

    ax = fig.add_subplot(1, 2, 1)
    ax.contour(X, Y, Z_f, cmap='viridis')
    ax.set_title(f'${function_name}(x, y)$')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.step(df['x0'], df['x1'])
    print(df[['x0','x1']])

plt.savefig(outfile)
