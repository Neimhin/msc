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


ax = fig.add_subplot(1, 2, 1)
ax.set_xlabel('iteration')
ax.set_yscale("log")
for i,file in enumerate(infiles):
    df = pd.read_csv(file)
    if i == 0:
        function_name = df["function_name"][0]
        function = f if function_name == 'f' else g
        ax.set_ylabel(f"${function_name}(x,y)$")
    ax.plot(df['iteration'], df['f(x)'], label=df2label(df))
    print(df[['x0', 'x1']])

plt.legend()
plt.savefig(outfile)
