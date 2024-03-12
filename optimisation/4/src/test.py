import lib
import heavy_ball
import adam
import polyak
import rmsprop

if __name__ == "__main__":
    import numpy as np
    hb = lib.GradientDescent()
    hb.step_size(10**-3)
    hb.beta(0.5)
    hb.max_iter(-1)
    hb.start(np.array([0, 0]))

    def converged(x1, x2):
        d = np.max(x1-x2)
        return d < 0.000001

    def fn(x):
        return lib.f.subs(lib.x, x[0]).subs(lib.y, x[1])

    def grad(x):
        return np.array([
            lib.f.diff(var).subs(lib.x, x[0]).subs(lib.y, x[1])
            for var in (lib.x, lib.y)])
    hb.converged(converged)
    hb.function(fn)
    hb.gradient(grad)
    hb.set_iterate(heavy_ball.iterate)
    hb.run2csv("hb.csv")


if __name__ == "__main__":
    adam = lib.GradientDescent()
    adam.epsilon(0.0001)
    adam.step_size(10**-2)
    adam.beta(0.8)
    adam.beta2(0.9)
    adam.max_iter(-1)
    adam.start(np.array([0, 0]))

    def converged(x1, x2):
        d = np.max(x1-x2)
        return d < 0.000001

    def fn(x):
        return lib.f.subs(lib.x, x[0]).subs(lib.y, x[1])

    def grad(x):
        return np.array(
            [lib.f.diff(var).subs(lib.x, x[0]).subs(lib.y, x[1])
                for var in (lib.x, lib.y)])
    adam.converged(converged)
    adam.function(fn)
    adam.gradient(grad)
    adam.set_iterate(adam.iterate)
    adam.run2csv("adam.csv")

if __name__ == "__main__":
    gd = lib.GradientDescent()
    gd.epsilon(0.0001)
    gd.max_iter(-1)
    gd.start(np.array([4.5, 8.5]))

    def converged(x1, x2):
        d = np.max(x1-x2)
        print(f"converged: {d}")
        return abs(d) < 0.000001

    def fn(x):
        return lib.f.subs(lib.x, x[0]).subs(lib.y, x[1])

    def grad(x):
        return np.array(
            [lib.f.diff(var).subs(lib.x, x[0]).subs(lib.y, x[1])
                for var in (lib.x, lib.y)])
    gd.converged(converged)
    gd.function(fn)
    gd.gradient(grad)
    gd.set_iterate(polyak.iterate)
    gd.run2csv("polyak.csv")

if __name__ == "__main__":
    import numpy as np
    rms = lib.GradientDescent()
    rms.epsilon(0.0001)
    rms.step_size(10**-2)
    rms.beta(0.1)
    rms.max_iter(-1)
    rms.start(np.array([0, 0]))

    def converged(x1, x2):
        d = np.max(x1-x2)
        return d < 0.000001

    def fn(x):
        return lib.f.subs(lib.x, x[0]).subs(lib.y, x[1])

    def grad(x):
        return np.array([lib.f.diff(var).subs(lib.x, x[0]).subs(lib.y, x[1]) for var in (lib.x, lib.y)])
    rms.converged(converged)
    rms.function(fn)
    rms.gradient(grad)
    rms.set_iterate(rmsprop.iterate)
    rms.run2csv("rms2.csv")

