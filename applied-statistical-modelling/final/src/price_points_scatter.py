import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv("wine_review.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Create a scatter plot of price vs points
plt.scatter(np.log(df['price']), df['points'], color='blue', alpha=0.5)

# Add labels and title
plt.xlabel('log(Price)')
plt.ylabel('Points')
# plt.xscale('log', base=2)
plt.yticks(df['points'].unique())
plt.title('Scatter Plot of Price vs Points')

# Show the plot
plt.savefig("fig/price-points-scatter.pdf")
print(df["points"].mean())
plt.show()

