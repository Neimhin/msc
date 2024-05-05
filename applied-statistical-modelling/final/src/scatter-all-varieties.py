import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs("fig/scatters", exist_ok=True)
df = pd.read_csv("wine_review.csv")
num_varieties = len(df["variety"].unique())

translation = str.maketrans(" ", "-")
def safe(name):
    return name.translate(translation) 

for variety in df["variety"].unique():
    print(variety)
    dfv = df[df["variety"] == variety]

    plt.figure()
    plt.scatter(dfv['price'], dfv['points'])
    plt.title(variety)
    plt.xlabel("price")
    plt.ylabel("points")
    safe_name = safe(variety)
    plt.savefig("fig/scatters/" + safe_name + ".pdf")
    plt.close()

import subprocess
subprocess.run("/usr/bin/pdfunite fig/scatters/*.pdf fig/scatters-all.pdf".split(), shell=True)
