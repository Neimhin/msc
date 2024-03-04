import lib


def iterate(self):
    import numpy as np
    x_value = self._start
    old_x_value = None
    iteration = 0
    sum = np.zeros(x_value.shape)
    alpha_n = np.zeros(x_value.shape)
    alpha_n.fill(self._step_size)
    converged = False
    grad_value = self._gradient(x_value)

    def yielded():
        print(x_value)
        print(iteration)
        return {
            "iteration": iteration,
            "x": x_value,
            "f(x)": self._function(x_value),
            "sum": sum,
            "epsilon": self._epsilon,
            "converged": converged,
            "gradient": grad_value,
            "alpha_n": alpha_n,
        }

    yield yielded()

    while not converged:
        iteration += 1
        if self._max_iter > 0 and iteration > self._max_iter:
            break
        grad_value = self._gradient(x_value)
        old_x_value = x_value
        print(grad_value, type(grad_value))
        print(alpha_n, type(alpha_n))
        print(x_value, type(x_value))
        x_value = x_value - alpha_n * grad_value
        sum = self._beta * sum + (1-self._beta) * (grad_value**2)
        alpha_n = self._step_size / (sum**0.5+self._epsilon)
        converged = self._converged(x_value, old_x_value)
        yield yielded()


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
