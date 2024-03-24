import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/T.csv")


plt.scatter(df["0"], df["1"])
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.title("Traning Data")
plt.savefig("fig/T.pdf")
