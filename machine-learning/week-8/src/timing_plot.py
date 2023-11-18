import pandas as pd
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i',type=str)
parser.add_argument('-o',type=str)
args = parser.parse_args()
df = pd.read_csv(args.i)
df = df.sort_values(by='training-samples')  # Sorting data for a proper line plot

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['training-samples'], df['training-time'], marker='o')
plt.title('Training Time vs Number of Training Samples')
plt.xlabel('Number of Training Samples')
plt.ylabel('Training Time (seconds)')
plt.grid(True)
plt.savefig(args.o)

