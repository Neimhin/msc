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

fig,ax = plt.subplots(1,1,figsize=(8,4))
# sns.scatterplot(x=df["TIME ROUND 5m"], y="pred", data=df, edgecolor='none',alpha=0.4, ax=ax,hue=df["TIME ROUND 5m"].map(lib.working_day_text))
# plt.xlabel("Time")
# plt.ylabel("Predicted Pseudo-usage")

pandemic_start = lib.PANDEMIC_START
pandemic_end = lib.PANDEMIC_END

sns.scatterplot(x=date_df.index, y="pred", data=date_df, edgecolor='none',alpha=0.4, ax=ax,hue=date_df.index.map(lib.working_day_text))
ax.set_title("Predicted Pseudo-usage for Each Day")
ax.axvline(x=pandemic_start, color='r', linestyle='--', label='Pandemic Start')
ax.axvline(x=pandemic_end, color='g', linestyle='--', label='Pandemic End')
ax.set_xlabel("Time")
ax.set_ylabel("Predicted Pseudo-usage")
ax.legend()
plt.savefig(directory + "/predicted-usage-day.pdf")


fig, ax = plt.subplots(1,1,figsize=(8,4))
sns.lineplot(x=month_df.index, y="pred", marker='o',linewidth=0.1, data=month_df,ax=ax,label="predictions")
sns.lineplot(x=month_df.index, y="true", marker='o',linewidth=0.1, data=month_df,ax=ax,label="true")
ax.set_title("Predicted Pseudo-usage for Each Month")
ax.axvline(x=pandemic_start, color='r', linestyle='--', label='Pandemic Start')
ax.axvline(x=pandemic_end, color='g', linestyle='--', label='Pandemic End')
ax.set_xlabel("Time")
ax.set_ylabel("Predicted Pseudo-usage")
ax.legend()

plt.tight_layout()
plt.savefig(directory + "/predicted-usage-month.pdf")

file = open(directory + "/prediction-difference-month.txt", "w")
month_df_pre_pandemic_era = month_df[(month_df.index < lib.PANDEMIC_START)]
lib.tee("Mean Month Difference Pre-Pandemic Era:", (month_df_pre_pandemic_era["true"] - month_df_pre_pandemic_era["pred"]).mean(), file=file)
month_df_pandemic_era = month_df[(month_df.index > lib.PANDEMIC_START) & (month_df.index < lib.PANDEMIC_END)]
lib.tee("Mean Month Difference Pandemic Era:", (month_df_pandemic_era["true"] - month_df_pandemic_era["pred"]).mean(), file=file)
month_df_post_pandemic_era = month_df[(month_df.index > lib.PANDEMIC_END)]
lib.tee("Mean Month Difference Pandemic Era:", (month_df_post_pandemic_era["true"] - month_df_post_pandemic_era["pred"]).mean(),file=file)