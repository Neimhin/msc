import lib
import numpy as np
import json


def iterate(self):
    self._x_value = self._start
    self._old_x_value = None
    self._iteration = 0
    self._m = np.zeros(self._x_value.shape, dtype=np.float64)
    self._v = np.zeros(self._x_value.shape, dtype=np.float64)
    self._converged_value = False
    self._grad_value = self._gradient(self._x_value)

    yield self.state_dict()

    while not self._converged_value:
        if self._max_iter > 0 and self._iteration > self._max_iter:
            break
        self._grad_value = self._gradient(self._x_value)
        self._m = self._beta * self._m + (1-self._beta)*self._grad_value
        # grad_value * grad_value gives element-wise product of np array
        self._v = self._beta2 * self._v + (1-self._beta2) * (self._grad_value*self._grad_value)
        self._old_x_value = self._x_value
        self._iteration += 1
        m_hat = self._m / (1-(self._beta ** self._iteration))
        v_hat = np.array(self._v / (1-(self._beta2 ** self._iteration)))
        v_hat_aug = v_hat**(0.5) + self._epsilon
        adam_grad = m_hat / v_hat_aug
        self._x_value = self._x_value - self._step_size * adam_grad
        self._converged_value = self._converged(self._x_value, self._old_x_value)
        print(self._converged_value, self._converged)
        yield self.state_dict()


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
    adam.set_iterate(iterate)
    adam.run2csv("adam.csv")
