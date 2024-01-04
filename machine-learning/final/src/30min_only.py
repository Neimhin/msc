import pandas as pd
import lib
import sys
infile = sys.argv[1]
outfile = sys.argv[2]

df = lib.read_csv(infile)
df = lib.even_30m_only(df)

df.to_csv(outfile)

print(df[df["TIME"].dt.month == 12 & df["TIME"].dt.year == 2023])
