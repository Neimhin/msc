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


parser = argparse.ArgumentParser(
    prog="Run Gradient Descent A Step Size Algorithm")

parser.add_argument('-al', '--algorithm', choices=[
    'rmsprop', 'adam', 'polyak', 'heavy_ball'], required=True)

parser.add_argument('-b', '--beta', type=float)
parser.add_argument('-b2', '--beta2', type=float)
parser.add_argument('-a', '--alpha', type=float)
parser.add_argument('-f', '--function', type=str,
                    choices=['f', 'g', 'relu'])
parser.add_argument('filename')

args = parser.parse_args()

print(args.filename)

gd = lib.GradientDescent()
function_handle = lib.config[args.function]
function = function_handle['sym']


def fn(x):
    return function.subs(lib.x, x[0]).subs(lib.y, x[1])


def grad(x):
    return np.array([
        function.diff(var).subs(
            lib.x, x[0]
        ).subs(
            lib.y, x[1]
        ) for var in (lib.x, lib.y)])

gd.algorithm(args.algorithm)
gd.start(np.array([6, 10]))
gd.converged(converged)
gd.step_size(args.alpha)
gd.beta(args.beta)
gd.beta2(args.beta2)
gd.epsilon(0.0001)
gd.max_iter(300)
# gd.sym_function(function_handle["sym"], function_name=args.function)
gd.function(fn, function_name=args.function, dimension=2)
gd.gradient(grad)
gd.run2csv(args.filename)
