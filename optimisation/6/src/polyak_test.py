import sgd
import week6
import pandas as pd
import numpy as np

if __name__ == "__main__":
    T = pd.read_csv("data/T.csv").values
    o = sgd.StochasticGradientDescent().alg("polyak")
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.start(np.array([3, 3]))
    for i in range(100):
        o.step()
        print("grad", o._grad_value)
    print("polyak", o._x_value)
