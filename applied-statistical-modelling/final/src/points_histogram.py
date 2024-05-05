import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("wine_review.csv")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

plt.hist(df['points'], bins=20, color='skyblue', edgecolor='black')

# Add labels and title
plt.xlabel('Points')
plt.ylabel('Frequency')
plt.title('Histogram of Wine Points')

# Show the plot
plt.savefig("fig/points-histogram.pdf")
plt.show()

