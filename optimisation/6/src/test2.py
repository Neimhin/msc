import numpy as np
import pandas as pd
import week6
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm

# Global variables for extents
x_min, x_max = -5, 5
y_min, y_max = -5, 5

def plot_wireframe_and_contour(f, T, resolution=100):
    global x_min, x_max, y_min, y_max

    # Generate data for wireframe plot
    x_range = np.linspace(x_min, x_max, resolution)
    y_range = np.linspace(y_min, y_max, resolution)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            Z[i, j] = f([X[i, j], Y[i, j]], T)

    # Plot wireframe
    fig = plt.figure(figsize=(12, 6))

    ax_wireframe = fig.add_subplot(121, projection='3d')
    ax_wireframe.plot_wireframe(X, Y, Z, color='blue')
    ax_wireframe.set_xlabel('X')
    ax_wireframe.set_ylabel('Y')
    ax_wireframe.set_zlabel('f(x, T)')
    ax_wireframe.set_title('Wireframe Plot of f(x, T)')

    # Generate data for contour plot
    Z_contour = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            Z_contour[i, j] = f([X[i, j], Y[i, j]], T)

    # Plot contour with log scale color
    ax_contour = fig.add_subplot(122)
    contour = ax_contour.contourf(X, Y, Z_contour, levels=20, norm=LogNorm(), cmap='viridis')
    plt.colorbar(contour, ax=ax_contour, label='f(x, T)')
    ax_contour.set_xlabel('X')
    ax_contour.set_ylabel('Y')
    ax_contour.set_title('Contour Plot of f(x, T)')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv("data/T.csv")
    T = df.values
    plot_wireframe_and_contour(week6.f, T)  # Call the function to plot wireframe and contour

