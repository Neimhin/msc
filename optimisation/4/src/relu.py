import lib
import sys
import argparse
import numpy as np
import rmsprop
import adam
import heavy_ball

def converged(x1, x2):
    # return false if converged or likely diverged
    d = np.max(x1-x2)
    return abs(d) < 0.001; # or np.max(np.abs(x1)) > 1000

function_handle = lib.config["relu"]
function = function_handle['sym']


def fn(x):
    return np.max(x)


def grad(x):
    return np.array([
        function.diff(lib.x).subs(
            lib.x, x[0]
        )])


setups = [
    {"iterate": adam.iterate, "alg": "adam", "beta": 0.9, "beta2": 0.25, "alpha": 0.1},
    {"iterate": rmsprop.iterate, "alg": "rmsprop", "beta": 0.9, "beta2": 0.25, "alpha": 0.1},
    {"iterate": heavy_ball.iterate, "alg": "heavy_ball", "beta": 0.9, "beta2": 0.25, "alpha": 0.1},
]


gd = lib.GradientDescent()
gd.converged(converged)
gd.epsilon(0.0001)
gd.max_iter(-1)
# gd.sym_function(function_handle["sym"], function_name=args.function)
gd.function(fn, function_name="relu", dimension=2)
gd.gradient(grad)

def setup2file(setup, start):
    alg = setup['alg']
    beta = setup['beta']
    beta2 = setup['beta2']
    alpha = setup['alpha']
    return f"exp/{setup['alg']}-relu-{start}.csv"

for start in [-1, +1, +100]:
    for setup in setups:
        gd.algorithm(setup['alg'])
        gd.step_size(setup['alpha'])
        gd.beta(setup['beta'])
        gd.beta2(setup['beta2'])
        gd.start(np.array([start]))
        gd.run2csv(setup2file(setup,start),summarise=False)
