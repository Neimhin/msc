import lib
import numpy as np


def iterate(self):
    x_value = self._start
    old_x_value = None
    iteration = 0
    m = np.zeros(x_value.shape, dtype=np.float64)
    v = np.zeros(x_value.shape, dtype=np.float64)
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
            "m": m,
            "v": v,
            "beta1": self._beta,
            "beta2": self._beta2,
            "alpha": self._step_size,
        }

    yield yielded()

    while not converged:
        if self._max_iter > 0 and iteration > self._max_iter:
            break
        grad_value = self._gradient(x_value)
        m = self._beta * m + (1-self._beta)*grad_value
        # grad_value * grad_value gives element-wise product of np array
        v = self._beta2 * v + (1-self._beta2) * (grad_value*grad_value)
        old_x_value = x_value
        iteration += 1
        m_hat = m / (1-(self._beta ** iteration))
        v_hat = np.array(v / (1-(self._beta2 ** iteration)))
        print('v', v, type(v))
        print('v_hat', v_hat, type(v_hat))
        print(np, type(np))
        v_hat_aug = v_hat**(0.5) + self._epsilon
        adam_grad = m_hat / v_hat_aug
        x_value = x_value - self._step_size * adam_grad
        converged = self._converged(x_value, old_x_value)
        yield yielded()


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
