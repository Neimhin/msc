import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

df = pd.read_csv("wine_review.csv")

variety = sys.argv[1]
other_var = sys.argv[2]
print(variety, other_var)

df = df[df["variety"] == variety]
df["log_price"] = np.log(df["price"])

plt.figure()


# Scatter plot for Rich = 0
plt.scatter(df[df[other_var] == 0]["log_price"], df[df[other_var] == 0]["points"], c="blue", label=f"{other_var}: 0")

# Scatter plot for Rich = 1
plt.scatter(df[df[other_var] == 1]["log_price"], df[df[other_var] == 1]["points"], c="red", label=f"{other_var}: 1")

plt.legend()
plt.title("Variety: " + variety)
plt.xlabel("Log Price")
plt.ylabel("Points")
xticks = df["log_price"].unique()
# max_ticks = 5
# if len(xticks) > max_ticks:
#     stride = int(len(xticks)/max_ticks)
#     xticks = xticks[::stride]
# plt.xticks(xticks)
# plt.gca().set_xticklabels(map(lambda x: "€" + str(round(x, 2)), np.exp(xticks)))
plt.show()

