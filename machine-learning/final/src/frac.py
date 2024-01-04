import sys
import pandas as pd

infile = sys.argv[1]
outfile = sys.argv[2]
df = pd.read_csv(infile)
df.sample(frac=0.001).to_csv(outfile)
