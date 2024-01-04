import pandas as pd
import sys
import lib

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile)
df["TIME"] = lib.to_datetime(df["TIME"])
df["TIME ROUND 5min"] = df["TIME"].dt.round("5min")

df.to_csv(outfile)
