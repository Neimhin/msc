import lib
import json


def iterate(self):
    import numpy as np
    self._x_value = self._start
    old_x_value = None
    self._iteration = 0
    self._sum = np.zeros(self._x_value.shape)
    alpha_n = np.zeros(self._x_value.shape)
    alpha_n.fill(self._step_size)
    self._converged_value = False
    self._grad_value = self._gradient(self._x_value)

    yield self.state_dict()

    while not self._converged_value:
        self._iteration += 1
        if self._max_iter > 0 and iteration > self._max_iter:
            break
        self._grad_value = self._gradient(self._x_value)
        old_x_value = self._x_value
        self._x_value = self._x_value - alpha_n * self._grad_value
        self._sum = self._beta * self._sum + (1-self._beta) * (self._grad_value**2)
        alpha_n = self._step_size / (self._sum**0.5+self._epsilon)
        self._converged_value = self._converged(self._x_value, old_x_value)
        yield self.state_dict()


def rms_gradient_descent():
    rms = lib.GradientDescent()
    rms.set_iterate(iterate)
    return rms


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
    rms.set_iterate(iterate)
    rms.run2csv("rms2.csv")
