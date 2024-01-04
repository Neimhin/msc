import pandas as pd
import sys
import lib
import matplotlib.pyplot as plt
import seaborn as sns
import os
infile = sys.argv[1]
df = pd.read_csv(infile)
directory = infile + ".d"
os.makedirs(directory,exist_ok=True)
df["TIME ROUND 5m"] = lib.to_datetime(df["TIME ROUND 5m"])
df["MONTH"] = lib.months_since_epoch(df["TIME ROUND 5m"])
df.set_index(df["TIME ROUND 5m"],inplace=True)

date_df = df.groupby(df["TIME ROUND 5m"].dt.date)[["true","pred"]].sum()
date_df.index = pd.to_datetime(date_df.index)
date_df.index.name = None


month_df = df.groupby(pd.Grouper(freq="M"))[["true","pred"]].sum()
print(month_df)
month_df.set_index(pd.to_datetime(month_df.index),inplace=True)

fig,ax = plt.subplots(2, 1, figsize=(8,8))
# sns.scatterplot(x=df["TIME ROUND 5m"], y="pred", data=df, edgecolor='none',alpha=0.4, ax=ax[0],hue=df["TIME ROUND 5m"].map(lib.working_day_text))
# plt.xlabel("Time")
# plt.ylabel("Predicted Pseudo-usage")

pandemic_start = lib.PANDEMIC_START
pandemic_end = lib.PANDEMIC_END

sns.scatterplot(x=date_df.index, y="pred", data=date_df, edgecolor='none',alpha=0.4, ax=ax[0],hue=date_df.index.map(lib.working_day_text))
ax[0].set_title("Predicted Pseudo-usage for Each Day")
ax[0].axvline(x=pandemic_start, color='r', linestyle='--', label='Pandemic Start')
ax[0].axvline(x=pandemic_end, color='g', linestyle='--', label='Pandemic End')
ax[0].set_xlabel("Time")
ax[0].set_ylabel("Predicted Pseudo-usage")
ax[0].legend()

sns.lineplot(x=month_df.index, y="pred", marker='o',linewidth=0.1, data=month_df,ax=ax[1],label="predictions")
sns.lineplot(x=month_df.index, y="true", marker='o',linewidth=0.1, data=month_df,ax=ax[1],label="true")
ax[1].set_title("Predicted Pseudo-usage for Each Month")
ax[1].axvline(x=pandemic_start, color='r', linestyle='--', label='Pandemic Start')
ax[1].axvline(x=pandemic_end, color='g', linestyle='--', label='Pandemic End')
ax[1].set_xlabel("Time")
ax[1].set_ylabel("Predicted Pseudo-usage")
ax[1].legend()

plt.tight_layout()
plt.savefig(directory + "/predicted-usage.pdf")

print("mean error pandemic era:", (month_df["true"] - month_df["pred"]).abs().mean())
print("mean error post pandemic era")