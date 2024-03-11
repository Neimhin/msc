import lib
import sys
import argparse
import numpy as np
import rms2
import adam
import hb


def converged(x1, x2):
    d = np.max(x1-x2)
    return d < 0.0001


parser = argparse.ArgumentParser(
    prog="Run Gradient Descent A Step Size Algorithm")

parser.add_argument('-al', '--algorithm', choices=[
    'rmsprop', 'adam', 'polyak', 'heavy_ball'], required=True)

parser.add_argument('-b', '--beta', type=float)
parser.add_argument('-b2', '--beta2', type=float)
parser.add_argument('-a', '--alpha', type=float)
parser.add_argument('filename')

args = parser.parse_args()

print(args.filename)

gd = lib.GradientDescent()
if 0:
    pass
elif args.algorithm == 'rmsprop':
    gd.set_iterate(rms2.iterate)
elif args.algorithm == 'adam':
    gd.set_iterate(adam.iterate)
elif args.algorithm == 'heavy_ball':
    gd.set_iterate(hb.iterate)
else:
    print("no algorithm")
    sys.exit(1)

gd.start(np.array([4, 8]))
gd.converged(converged)
gd.step_size(args.alpha)
gd.beta(args.beta)
gd.beta2(args.beta2)
gd.epsilon(0.0001)
gd.max_iter(-1)


def fn(x):
    return lib.f.subs(lib.x, x[0]).subs(lib.y, x[1])


def grad(x):
    return np.array([
        lib.f.diff(var).subs(
            lib.x, x[0]
        ).subs(
            lib.y, x[1]
        ) for var in (lib.x, lib.y)])


gd.converged(converged)
gd.function(fn)
gd.gradient(grad)
gd.run2csv(args.filename)
