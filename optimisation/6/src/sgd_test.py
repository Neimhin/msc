import sgd
import week6
import pandas as pd
import numpy as np

if __name__ == "__main__":
    T = pd.read_csv("data/T.csv").values

    o = sgd.StochasticGradientDescent().alg("constant")
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.step_size(0.01)
    o.start(np.array([3, 3]))
    for i in range(100):
        o.step()
    print("constant", o._x_value)

    o = sgd.StochasticGradientDescent().alg("polyak")
    fg = week6.generate_optimisation_functions(T, minibatch_size=10, shuffle=False)
    o.function_generator(fg)
    o.start(np.array([0.9, 0.9]))
    for i in range(100):
        o.step()
    print("polyak", o._x_value)

    o = sgd.StochasticGradientDescent().alg("polyak")
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.start(np.array([3, 3]))
    for i in range(100):
        o.step()
    print("polyak", o._x_value)

    o = sgd.StochasticGradientDescent()
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.start(np.array([3, 3]))
    o.step_size(0.00001)
    o.beta(0.99)
    o.alg("rmsprop")
    for i in range(100):
        o.step()
    print("rmsprop", o._x_value)

    o = sgd.StochasticGradientDescent()
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.start(np.array([3, 3]))
    o.step_size(0.00001)
    o.beta(0.99)
    o.alg("heavy_ball")
    for i in range(100):
        o.step()
    print("heavy_ball", o._x_value)

    o = sgd.StochasticGradientDescent()
    fg = week6.generate_optimisation_functions(T, minibatch_size=5)
    o.function_generator(fg)
    o.start(np.array([3, 3]))
    o.step_size(0.00001)
    o.beta(0.99)
    o.beta2(0.25)
    o.alg("adam")
    for i in range(100):
        o.step()
    print("adam", o._x_value)
