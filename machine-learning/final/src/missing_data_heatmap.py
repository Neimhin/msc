import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pandas as pd
import numpy as np
directory = sys.argv[1] + ".d"
import os
os.makedirs(directory,exist_ok=True)

def cap(n=1000):
    def cap_n(x):
        return min(x, n)
    return cap_n

data = pd.read_csv(sys.argv[1])
data.set_index('TIME', inplace=True)
column_sums = data.sum()
sorted_columns = column_sums.sort_values().index
data = data[sorted_columns]
data = data.applymap(cap(1000))
plt.figure(figsize=(40, 300))
ax = sns.heatmap(data, cmap="viridis", cbar_kws={'label': 'Missing Samples'})
cbar = ax.collections[0].colorbar
cbar.set_ticks([cbar.vmin, 1000])
cbar.set_ticklabels([f"{cbar.vmin}", r"$\geq 1000$"])

plt.title('Heatmap of Missing Samples by Station and Date')
plt.xlabel('Station')
plt.ylabel('Date')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(directory + "/heatmap.pdf")