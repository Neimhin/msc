import pandas as pd
import matplotlib.pyplot as plt
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i',type=str)
parser.add_argument('-o',type=str)
args = parser.parse_args()
plt.figure(figsize=(10, 6))
for input_spec in args.i.split(","):
    input_file, input_label = input_spec.split(":")
    df = pd.read_csv(input_file)
    df = df.sort_values(by='training-samples')

    plt.plot(df['training-samples'], df['training-time'], marker='o', label=input_label)
    plt.title('Training Time vs Number of Training Samples')
    plt.xlabel('Number of Training Samples')
    plt.ylabel('Training Time (seconds)')
    plt.grid(True)
    plt.legend()

plt.savefig(args.o)
    
