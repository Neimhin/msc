import sys
import pandas as pd
import matplotlib.pyplot as plt
if __name__ == "__main__":
    in_file = sys.argv[1]
    df = pd.read_csv(in_file)
    print(df.describe())
    for col in df.columns:
        u =  df[col].unique()
        if len(u) < 23:
            print(col,"\t",len(u),"\t", u)
            print(df.value_counts(col))
        else:
            print(col,"\t",len(u),"...")
    hist = df.plot.hist()
    plt.show()