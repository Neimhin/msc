class GradientDescent():
# ...
    def iterate(self):
        import math
        x_value = self._start
        old_x_value = None
        iteration = 0
        while True:
            yield [iteration, float(x_value), float(self._function(x_value))]
            iteration += 1
            if self._max_iter > 0 and iteration > self._max_iter:
                break
            grad_value = self._gradient(x_value)
            x_value -= self._step_size * grad_value  # Update step
            if old_x_value is not None and self._converged(x_value, old_x_value):
                yield [iteration, float(x_value), float(self._function(old_x_value))]
                print("converged")
                break
            old_x_value = x_value
