import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
np.random.seed(0)
x = np.random.normal(0, 1, 10)
y = np.zeros(10)

x = np.append(x, 8)
y = np.append(y, 3)

x = x.reshape(-1, 1)

model = Lasso()
model.fit(x, y)

x_plot = np.linspace(-3, 12, 200).reshape(-1, 1)
y_plot = model.predict(x_plot)

plt.figure(figsize=(4, 4))
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x_plot, y_plot, color='red', label='Regression line')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression with an Outlier')
plt.legend()
plt.tight_layout()
plt.savefig("fig/outlier_example_linear_regression.pdf")
