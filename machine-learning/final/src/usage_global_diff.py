from click import DateTime
import pandas as pd
import argparse
import lib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import holidays

ie_holidays = holidays.Ireland()
def is_ie_holiday(d):
    return d in ie_holidays

def working_day(d):
    if is_ie_holiday(d):
        return "Non Working Day"
    if d.weekday() < 5:
        return "Working Day"
    return "Non Working Day"

def normalize(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("--input",type=str)
arg = argument_parser.parse_args()
print(arg.input)
directory = arg.input + ".d"
os.makedirs(directory,exist_ok=True)

# part 1: load the data
df = lib.read_csv(arg.input)
df = lib.even_30m_only(df)

global_available = df.groupby("TIME ROUND 5m")["AVAILABLE BIKES"].sum()
global_available_diff = global_available.diff().abs()
usage = global_available_diff.groupby(global_available_diff.index.date).sum()
usage.to_csv(directory + "/global_diff_usage.csv")

def workday_weekend(x):
    if x < 6:
        return "Workday"
    return "Weekend"


plt.figure(figsize=(8,4))
sns.scatterplot(x=usage.index, y=usage.values, hue=pd.to_datetime(usage.index,format="%Y-%m-%d").map(working_day))
plt.legend()
plt.title("Estimated Usage over Date")
plt.xlabel("Date")
plt.ylabel("Global Diff Usage Proxy")
plt.savefig(directory + "/global_diff_usage.pdf")
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
