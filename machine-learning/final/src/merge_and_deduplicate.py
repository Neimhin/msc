import pandas as pd
import os
import glob
import lib
import sys

data_directory = 'data'
pattern = os.path.join(data_directory, 'db-*.csv')
csv_files = glob.glob(pattern)
dataframes = []
outfile = sys.argv[1]
for file in csv_files:
    df = lib.read_csv(file)
    print("reading", file, len(df))
    dataframes.append(df)
df = pd.concat(dataframes, ignore_index=True)

print("total length", len(df))
df["TIME ROUND 5min"] = df["TIME"].dt.round("5min")
df = df.drop_duplicates(subset=["STATION ID", "TIME ROUND 5min"])
df["IS 30min"] = (df["TIME ROUND 5min"].dt.minute % 30) == 0
print(len(df), df["IS 30min"].sum())
df.to_csv(outfile + '-all-deduped.csv', index=False)
df[df["IS 30min"]].to_csv(outfile + '-all-30min.csv', index=False)
