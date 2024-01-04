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
arg = argument_parser.parse_args()
print(arg.input)
directory = arg.input + ".d"
os.makedirs(directory,exist_ok=True)

df = lib.read_csv(arg.input)
df = lib.even_30m_only(df)
df["STATUS"] = df["STATUS"].str.title()

def total_available_bikes_open(group):
    return group[group["STATUS"] == "Open"]["AVAILABLE BIKES"].sum()

def total_available_bikes(group):
    return group["AVAILABLE BIKES"].sum()


df["DATE"] = df["TIME"].dt.date
date_to_max_bikes_open = df.groupby(["DATE", "TIME ROUND 5m"]).apply(total_available_bikes_open).groupby("DATE").max()
date_to_max_bikes_open.to_csv(directory + "/date_to_max_bikes_open.csv")
date_to_max_bikes = df.groupby(["DATE", "TIME ROUND 5m"]).apply(total_available_bikes).groupby("DATE").max()
date_to_max_bikes.to_csv(directory + "/date_to_max_bikes.csv")

df["MAX AVAILABLE BIKES"] = df["DATE"].map(date_to_max_bikes)
def bikes_in_use(group):
    return group["MAX AVAILABLE BIKES"].mode() - group["AVAILABLE BIKES"].sum()

bikes_used = df.groupby(["DATE", "TIME ROUND 5m"]).apply(bikes_in_use)
bikes_used.name = "CONFIRMED BIKES USED"
bikes_used.to_csv(directory + "/bikes_used.csv")
bikes_used.groupby("DATE").sum().to_csv(directory + "/bikes_used_by_date.csv")