import pandas as pd
import argparse
import lib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--input",type=str)
argument_parser.add_argument("--usage-one",action="store_true")
argument_parser.add_argument("--usage-two",action="store_true")
argument_parser.add_argument("--usage-three",action="store_true")
arg = argument_parser.parse_args()
print(arg.input)
directory = arg.input + ".d"
os.makedirs(directory,exist_ok=True)

# part 1: load the data
df = lib.read_csv(arg.input)
df = lib.even_30m_only(df)

# part 2: assign date idx, week idx, month idx, etc.

# part 3: group by date idx, week idx, month idx, etc. to compute usage for each group

def usage_by_diffs_abs(group):
    mean_diffs =  group["AVAILABLE BIKES"].diff().abs().mean()
    return mean_diffs

df["TIME SINCE LAST UPDATE"] = df["TIME"] - df["LAST UPDATED"]
df["HAS UPDATE"] = df["TIME SINCE LAST UPDATE"].dt.total_seconds() < (30*60)

def usage_by_last_updated(group):
    return group["HAS UPDATE"].mean()

def usage_by_weighted_last_updated(group):
    print(".",end="")
    return group["LAST UPDATE USAGE"].mean()

df["DATE"] = df["TIME"].dt.date

if arg.usage_one:
    print("usage 1")
    date_to_usage = df.groupby(["DATE", "STATION ID"]).apply(usage_by_diffs_abs)
    date_sum = date_to_usage.groupby(level="DATE").sum()
    date_sum.name = "USAGE DIFF ABS"
    date_sum.to_csv(directory + "/date_to_usage.csv")
    print("normalizing")
    date_sum = normalize(date_sum)

if arg.usage_two:
    print("usage 2",end="")
    date_to_usage_by_time_since = df.groupby(["DATE", "STATION ID"]).apply(usage_by_last_updated)
    date_to_usage_by_time_since = date_to_usage_by_time_since.groupby(level="DATE").sum()
    date_to_usage_by_time_since.name = "USAGE NUM UPDATES"
    date_to_usage_by_time_since.to_csv(directory + "/date_to_usage_by_time_since.csv")
    print("normalizing")
    date_to_usage_by_time_since = normalize(date_to_usage_by_time_since)

if arg.usage_three:
    print("usage 3")
    df["LAST UPDATE WEIGHT"] = ((30*60) - df["TIME SINCE LAST UPDATE"].dt.total_seconds())
    df["LAST UPDATE USAGE"] = df["HAS UPDATE"] * df["LAST UPDATE WEIGHT"]
    date_to_usage_by_weighted_time_since = df.groupby(["DATE", "STATION ID"]).apply(usage_by_weighted_last_updated)
    date_to_usage_by_weighted_time_since = date_to_usage_by_weighted_time_since.groupby(level="DATE").sum()
    date_to_usage_by_weighted_time_since.name = "USAGE WEIGHTED NUM UPDATES"
    date_to_usage_by_weighted_time_since.to_csv(directory + "/date_to_usage_by_weighted_time_since.csv")
    print("normalizing")
    date_to_usage_by_weighted_time_since = normalize(date_to_usage_by_weighted_time_since)

# # part 4: plot usage over time
# plt.figure(figsize=(8,4))
# plt.scatter(date_sum.index, date_sum.values,label="DIFF ABS")
# plt.scatter(date_to_usage_by_time_since.index, date_to_usage_by_time_since.values,label="NUM UPDATES")
# if arg.with_weighted:
#     plt.scatter(date_to_usage_by_weighted_time_since.index, date_to_usage_by_weighted_time_since.values, label="WEIGHTED NUM UPDATES")
# plt.title("usage over time")
# plt.xlabel("Date")
# plt.ylabel("Usage")
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.savefig(directory + "/date_to_usage_diff_abs.pdf")
