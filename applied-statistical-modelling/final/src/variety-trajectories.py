import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
model = sys.argv[1]

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Define colors for the colormap
colors = [(0, 0, 1), (1, 1, 0), (1, 0, 0)]  # Blue, Yellow, Red

# Create a colormap
cmap = LinearSegmentedColormap.from_list('my_colormap', colors)

# Define a function to interpolate between 0 and 43
def interpolate_color(value):
    # Normalize value between 0 and 1
    normalized_value = value / 43.0
    # Interpolate color from the colormap
    interpolated_color = cmap(normalized_value)
    return interpolated_color

ranef = pd.read_csv(model+".ranef.csv", index_col=0, quoting=csv.QUOTE_NONE)
fixef = pd.read_csv(model+".fixef.csv", index_col=0, quoting=csv.QUOTE_NONE)

intercept = fixef.loc["Intercept"]["Estimate"]
log_price = fixef.loc["log_price"]["Estimate"]
print(ranef)

plt.figure()
vs = pd.Series(ranef.index)
for i, variety in enumerate(ranef.index):
    pert = ranef["variety.Estimate.log_price"][variety]
    lp = log_price - pert
    print(lp)
    log_price_in = np.linspace(1, 8)
    price_linear = np.exp(log_price_in)
    points = pd.Series(intercept + lp * log_price_in).apply(lambda x: min(100,x))

    plt.plot(log_price_in, points, color=interpolate_color(i), label=variety)
plt.plot(-5,90,alpha=0)
plt.legend(loc='upper left')
plt.show()
