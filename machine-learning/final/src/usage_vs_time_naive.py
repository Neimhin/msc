from importlib.machinery import WindowsRegistryFinder
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

def relu(x):
    if x > 0:
        return x
    return 0
def neg(x):
    return -x

def mask_context(mask,num):
    for i in range(num):
        shift = i+1
        mask = mask | mask.shift(-shift,fill_value=0) | mask.shift(shift,fill_value=0)
    return mask

if __name__ == "__main__":
    df = pd.read_csv(source_file)
    df["TIME"] = to_dt(df["TIME"])
    df["LAST UPDATED"] = to_dt(df["LAST UPDATED"])
    df["HAS CHANGED"] = lib.create_has_delta_column(df)
    df["MISSED CHANGE"] = df["HAS CHANGED"] & (df["AVAILABLE BIKES"].diff() == 0)
    df["AVAILABLE BIKES DIFF"] = df["AVAILABLE BIKES"].diff()
    df["TIME SINCE LAST UPDATE"] = df["TIME"] - df["LAST UPDATED"]
    df["AVAILABLE BIKES DIFF ABS"] = df["AVAILABLE BIKES DIFF"].abs()
    df["AVAILABLE BIKES DIFF RELU"] = df["AVAILABLE BIKES DIFF"].apply(relu)
    df["AVAILABLE BIKES DIFF NEG RELU"] = df["AVAILABLE BIKES DIFF"].apply(neg).apply(relu)
    df["DATE"] = df["TIME"].dt.date
    df["MONTH"] = df["TIME"].dt.month
    df["YEAR"] = df["TIME"].dt.year

    weird_mask = df["HAS CHANGED"].apply(lambda x: not x) & (df["AVAILABLE BIKES DIFF"] != 0) # & (df["AVAILABLE BIKES DIFF ABS"] > 5)
    last_updated_bug_df = df[mask_context(weird_mask, 0)]
    print(last_updated_bug_df)
    print(len(weird_mask.sum()))

    def periodic_take_outs(period):
        take_outs = df.groupby(period)["AVAILABLE BIKES DIFF RELU"].sum()
        print(take_outs)
        take_outs.to_csv(directory + f"/take-outs-diff-relu-{period}.csv")
    periodic_take_outs("DATE")
    periodic_take_outs("MONTH")
    periodic_take_outs("YEAR")

    def periodic_take_outs_neg(period):
        take_outs = df.groupby(period)["AVAILABLE BIKES DIFF NEG RELU"].sum()
        print(take_outs)
        take_outs.to_csv(directory + f"/take-outs-diff-neg-relu-{period}.csv")
    periodic_take_outs_neg("DATE")
    periodic_take_outs_neg("MONTH")
    periodic_take_outs_neg("YEAR")
