import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("fig/histograms", exist_ok=True)
df = pd.read_csv("wine_review.csv")
num_varieties = len(df["variety"].unique())

translation = str.maketrans(" ", "-")
def safe(name):
    return name.translate(translation) 

for variety in df["variety"].unique():
    dfv = df[df["variety"] == variety]

    plt.figure()
    plt.hist(dfv['points'], bins=min(len(dfv["points"].unique()), 20), color='skyblue', edgecolor='black')
    plt.title(variety)
    plt.xlabel("points")
    plt.ylabel("frequency")
    plt.xlim(80,100)
    safe_name = safe(variety)
    plt.savefig("fig/histograms/" + safe_name + ".pdf")
    plt.close()
