import pandas as pd
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    counts = []
    diff = df['AVAILABLE BIKES'].diff()
    for i in range(40):
        sub_df = df[df['AVAILABLE BIKES'].diff() > i]
        counts.append(len(sub_df))

    plt.figure()
    x = list(range(40))
    y = counts
    plt.plot(x,y)
    plt.xlabel('difference in bike occupancy')
    plt.ylabel('no. occurrences')
    plt.savefig('fig/num-bikes-diff-vs-num-occurrences.pdf')
    print(df)
