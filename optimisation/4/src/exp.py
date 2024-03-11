import lib
import sys
import argparse
import numpy as np
import rmsprop
import adam
import heavy_ball

def converged(x1, x2):
    d = np.max(x1-x2)
    return d < 0.001


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
gd.algorithm(args.algorithm)
gd.start(np.array([0, 0]))
gd.converged(converged)
gd.step_size(args.alpha)
gd.beta(args.beta)
gd.beta2(args.beta2)
gd.epsilon(0.0001)
gd.max_iter(-1)
gd.converged(converged)
gd.sym_function(function_handle["sym"], function_name=args.function)
gd.run2csv(args.filename)
