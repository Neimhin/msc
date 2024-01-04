import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

infile = sys.argv[1]
directory = infile + ".d"
os.makedirs(directory,exist_ok=True)
df = pd.read_csv(infile,parse_dates=["DATE"])
df = df.dropna()

plt.figure(figsize=(8,4))
fig = sns.scatterplot(x=df["DATE"], y=df["0"])
plt.ylabel("total available bikes")
plt.savefig(directory + "/max-bikes.pdf")
