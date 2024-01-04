import sys
import pandas as pd
from pandas.core.series import Series
from typing import List
import matplotlib.pyplot as plt
import os

def create_has_delta_column(TIME: "Series[pd.Timestamp]", LAST_UPDATED: "Series[pd.Timestamp]"):
    deltas: List[bool] = []
    five_min_timedelta = pd.Timedelta(minutes=5)
    previous_time = TIME[0] - five_min_timedelta
    for i in range(len(TIME)):
        has_delta = LAST_UPDATED[i] > previous_time
        deltas.append(has_delta)

        previous_time = TIME[i]

    return pd.Series(deltas,dtype=bool)
                             
def to_dt(series: pd.Series) -> "pd.Series[pd.Timestamp]":
    return pd.to_datetime(series, errors="coerce")
source_file = sys.argv[1]
directory = source_file + ".d"
os.makedirs(directory, exist_ok=True)
if __name__ == "__main__":
    df = pd.read_csv(source_file)
    df["TIME"] = to_dt(df["TIME"])
    df["LAST UPDATED"] = to_dt(df["LAST UPDATED"])
    df["HAS CHANGED"] = create_has_delta_column(df["TIME"], df["LAST UPDATED"])
    df["MISSED CHANGE"] = df["HAS CHANGED"] & (df["AVAILABLE BIKES"].diff() == 0)
    df["AVAILABLE BIKES DIFF"] = df["AVAILABLE BIKES"].diff()
    df["TIME SINCE LAST UPDATE"] = df["TIME"] - df["LAST UPDATED"]
    print(len(df))
    print("sum has changed,", df["HAS CHANGED"].sum())
    print("mean has changed,", df["HAS CHANGED"].mean())
    print("sum MISSED CHANGE,", df["MISSED CHANGE"].sum())
    print("mean MISSED CHANGE,",df["MISSED CHANGE"].mean())
    print("mean time since last update,", df["TIME SINCE LAST UPDATE"].mean())
    df.to_csv("test.csv")

    one_percent_df = df.sample(frac=0.01)
    one_percent_df.to_csv(directory + "/1-percent-sample.csv")

    time_since_last_update_seconds = df["TIME SINCE LAST UPDATE"].dt.total_seconds()
    plt.figure(figsize=(10, 6))
    plt.hist(time_since_last_update_seconds, bins=100, color='skyblue', edgecolor='black', range=(0, 3600))
    plt.title('Histogram of Time Since Last Update')
    plt.xlabel('Seconds Since Last Update')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(directory + "/time-since-last-hist.pdf")

    plt.figure(figsize=(10, 6))
    diff_abs = df["AVAILABLE BIKES DIFF"][df["HAS CHANGED"]].abs()
    plt.scatter(time_since_last_update_seconds[df["HAS CHANGED"]], diff_abs,s=1, alpha=0.5)
    plt.title('Scatter of Time Since Last Update and Delta')
    plt.xlabel('Seconds Since Last Update')
    plt.xscale("log")
    plt.ylabel('Available Bikes Diff given Has Changed')
    five_minutes_in_seconds = 5 * 60
    plt.xticks(list(plt.xticks()[0]) + [five_minutes_in_seconds], list(plt.xticks()[1]) + ['5 minutes'])

    plt.tight_layout()
    plt.savefig(directory + "/time-since-last-vs-diff-scatter.png", dpi=200)

