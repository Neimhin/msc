import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input",type=str)
parser.add_argument("--xlabel",type=str,default=None)
parser.add_argument("--ylabel",type=str,default=None)
parser.add_argument("--title",type=str,default=None)
arg = parser.parse_args()

infile =  arg.input
directory = infile + ".d"
os.makedirs(directory,exist_ok=True)
df = pd.read_csv(infile,parse_dates=["DATE"])
df["IS WEEKDAY"] = df["DATE"].dt.weekday
weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
               4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
df['IS WEEKDAY'] = df['IS WEEKDAY'].map(weekday_map)


plt.figure(figsize=(8,4))
fig = sns.scatterplot(
    x=df["DATE"],
    y=df["0"],
    hue=df["IS WEEKDAY"],
    alpha=0.8,
    size=1,
    edgecolor='none')
plt.title(arg.title)
if arg.ylabel:
    plt.ylabel(arg.ylabel)
if arg.xlabel:
    plt.xlabel(arg.xlabel)
plt.legend()
plt.tight_layout()
plt.savefig(directory + "/vis.pdf")
