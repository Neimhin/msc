import numpy as np


def polyak_step_size(self, sp_func, sp_x, x, f_star):
    assert len(sp_x) == len(x)
    subs = {sp_xi: xi for sp_xi, xi in zip(sp_x, x)}
    fx = sp_func.subs(subs)
    grad = [sp_func.diff(sp_xi).subs(subs) for sp_xi in sp_x]
    grad = np.array(grad)
    denominator = sum(grad * grad)
    numerator = fx - f_star
    return numerator / denominator
