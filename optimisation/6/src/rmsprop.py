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
    self._step_coeff = self._step_size

    yield self.state_dict()

    while not self._converged_value:
        self._iteration += 1
        if self._max_iter > 0 and self._iteration > self._max_iter:
            break
        self._grad_value = self._gradient(self._x_value)
        old_x_value = self._x_value
        self._x_value = self._x_value - alpha_n * self._grad_value
        self._sum = self._beta * self._sum + (1-self._beta) * (self._grad_value**2)
        alpha_n = self._step_size / (self._sum**0.5+self._epsilon)
        self._step_coeff = alpha_n
        self._converged_value = self._converged(self._x_value, old_x_value)
        yield self.state_dict()
