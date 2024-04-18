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

def df2label(df):
    alg = df['alg'][0]
    alpha = df['alpha'][0]
    beta = df['beta1'][0]
    beta2 = df['beta2'][0]
    if alg == 'rmsprop':
        return f"RMSProp $\\alpha={alpha}, \\beta={beta}$"
    if alg == 'adam':
        return f"Adam $\\alpha={alpha}, \\beta_1={beta}, \\beta_2={beta2}$"
    if alg == 'heavy_ball':
        return f"HB $\\alpha={alpha}, \\beta={beta}$"
    raise Exception("alg nyi: " + alg)


for i,file in enumerate(infiles):
    df = pd.read_csv(file)

    function_name = df["function_name"][0]
    function = f if function_name == 'f' else g
    print(function)
    if i == 0:
        x = np.linspace(4, 7, 400)
        y = np.linspace(8, 11, 400)
        X, Y = np.meshgrid(x, y)
        Z_f = function(X, Y)
        ax = fig.add_subplot(1, 2, 1)
        ax.contour(X, Y, Z_f, cmap='viridis')

    ax.set_title(f'${function_name}(x, y)$')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.plot(df['x0'], df['x1'], label=df2label(df), marker='x', markersize=3, markeredgewidth=0.5)
    print(df[['x0', 'x1']])
ax.set_xlim(4, 7)
ax.set_ylim(8, 11)

plt.legend()
plt.savefig(outfile)
