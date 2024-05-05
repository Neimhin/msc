import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

font = {'size'   : 19}
matplotlib.rc('font', **font)

# Read the data
df = pd.read_csv("wine_review.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Create a scatter plot of price vs points
dfs = df[df["superior_rating"] == 1]
plt.scatter(dfs['price'], dfs['points'], alpha=0.3, label='superior')
dfs = df[df["superior_rating"] == 0]
plt.scatter(dfs['price'], dfs['points'], alpha=0.3, label='not superior')

# Add labels and title
plt.xlabel('price')
plt.ylabel('points')
plt.yticks(df['points'].unique())
plt.title('$\\log($price$)$ vs points')

# Show the plot
plt.savefig("fig/price-points-scatter.pdf")
plt.xscale('log', base=10)
plt.legend()
plt.tight_layout()
plt.savefig("fig/price-points-scatter-log10.pdf")
plt.tight_layout()
plt.xscale('log', base=2)
plt.tight_layout()
plt.savefig("fig/price-points-scatter-log2.pdf")

