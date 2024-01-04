import pandas as pd
import lib
import sys
infile = sys.argv[1]
outfile = sys.argv[2]
df = pd.read_csv(infile)
df["TIME ROUND 5min"] = lib.to_datetime(df["TIME"]).dt.round("5min")
deduped_df = df.drop_duplicates(subset=["STATION ID", "TIME ROUND 5min"])
deduped_df["IS 30min"] = (deduped_df["TIME ROUND 5min"].dt.minute % 30) == 0
deduped_df[deduped_df["IS 30min"]].to_csv(outfile, index=False)