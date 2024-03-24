import numpy as np
minibatch = np.array([
    [0.0918635, -0.0468714],
    [-0.66994666, -0.133955],
    [-0.08386569, 0.3052427],
    [-0.00564624, -0.12876412],
    [-0.38826176, 0.23831869]
])

x = [0.80697696, 1.05286489]

import week6
print(minibatch)
print("gradient:", week6.gradient_function_fd(minibatch)(x))
