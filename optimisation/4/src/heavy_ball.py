import lib


def iterate(self):
    self._x_value = self._start
    self._old_x_value = None
    self._iteration = 0
    self._converged_val = False
    self._grad_value = self._gradient(self._x_value)
    self._z = 0
    yield self.state_dict()  # yield initial values

    while not self._converged_val:
        self._iteration += 1
        if self._max_iter > 0 and self._iteration > self._max_iter:
            break
        self._grad_value = self._gradient(self._x_value)
        self._old_x_value = self._x_value
        self._z = self._beta * self._z + self._step_size * self._grad_value
        self._x_value = self._x_value - self._z
        self._converged_val = self._converged(self._x_value, self._old_x_value)
        yield self.state_dict()


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
