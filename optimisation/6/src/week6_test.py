import week6
import numpy as np

if __name__ == "__main__":
    T = week6.generate_trainingdata()
    import pandas as pd
    df = pd.read_csv("data/T.csv")
    T = df.values

    x = np.array([3, 3])
    print(week6.f(x, T) - week6.f_clear(x, T))

    generator = week6.generate_minibatches(T, N=2, shuffle=False)
    for i in range(3):
        n = next(generator)
        print(len(n), n)

    fgen = week6.generate_optimisation_functions(T, minibatch_size=5)
    zipped = zip(range(10), fgen)
    for (i, f) in zipped:
        print(f[0](x), f[1](x))
