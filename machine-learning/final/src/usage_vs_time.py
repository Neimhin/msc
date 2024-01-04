import sys
import pandas as pd
from pandas.core.series import Series
from typing import List
import matplotlib.pyplot as plt
import os

from sympy import per
import lib

def to_dt(series: pd.Series) -> "pd.Series[pd.Timestamp]":
    return pd.to_datetime(series, errors="coerce")

source_file = sys.argv[1]
directory = source_file + ".d"
os.makedirs(directory, exist_ok=True)
if __name__ == "__main__":
    df = pd.read_csv(source_file)
    df["TIME"] = to_dt(df["TIME"])
    df["LAST UPDATED"] = to_dt(df["LAST UPDATED"])
    df = df.sort_values(by=["STATION ID", "TIME"])
    df["HAS CHANGED"] = lib.create_has_delta_column(df)
    df["MISSED CHANGE"] = df["HAS CHANGED"] & (df["AVAILABLE BIKES"].diff() == 0)
    df["AVAILABLE BIKES DIFF"] = df["AVAILABLE BIKES"].diff()
    df["TIME SINCE LAST UPDATE"] = df["TIME"] - df["LAST UPDATED"]

    def negative_linear_unit(x: int) -> int:
        if x < 0:
            return x
        return 0
    
    df["DIFF TAKE OUTS"] = df["AVAILABLE BIKES DIFF"].apply(negative_linear_unit).abs()
    def true_to_1(x):
        if x:
            return 1
        return 0
    df["MISSED TAKE OUTS"] = df["MISSED CHANGE"].apply(true_to_1)
    df["LOWER BOUND TAKE OUTS"] = df["DIFF TAKE OUTS"] + df["MISSED TAKE OUTS"]
    # remove time component from date
    df["DATE"] = df["TIME"].dt.date
    df["MONTH"] = df["TIME"].dt.month
    df["YEAR"] = df["TIME"].dt.year

    def periodic_take_outs(period):
        take_outs = df.groupby(period)["LOWER BOUND TAKE OUTS"].sum()
        num_samples = df.groupby(period).size()
        print(take_outs)
        print(num_samples)
        take_outs.to_csv(directory + f"/take-outs-{period}.csv")
        num_samples.to_csv(directory + f"/num-samples-{period}.csv")

    periodic_take_outs("DATE")
    periodic_take_outs("MONTH")
    periodic_take_outs("YEAR")
