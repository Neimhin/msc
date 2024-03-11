import lib


def iterate(self):
    x_value = self._start
    old_x_value = None
    iteration = 0
    converged = False
    grad_value = self._gradient(x_value)

    z = 0

    def yielded():
        print(x_value)
        print(iteration)
        return {
            "alg": "heavy_ball",
            "iteration": iteration,
            "z": z,
            "x": x_value,
            "alpha": self._step_size,
            "beta1": self._beta,
            "f(x)": self._function(x_value),
            "epsilon": self._epsilon,
            "converged": converged,
            "gradient": grad_value,
        }

    yield yielded() # yield initial values

    while not converged:
        iteration += 1
        if self._max_iter > 0 and iteration > self._max_iter:
            break
        grad_value = self._gradient(x_value)
        old_x_value = x_value
        z = self._beta * z + self._step_size * grad_value
        x_value = x_value - z
        converged = self._converged(x_value, old_x_value)
        yield yielded()


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
    hb.set_iterate(iterate)
    hb.run2csv("hb.csv")
