import lib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i",type=str)
parser.add_argument("-o",type=str)
parser.add_argument("--year",type=int,default=None)
arg = parser.parse_args()
df = lib.read_csv(arg.i)
if arg.year:
    df = df[df["TIME"].dt.year == arg.year]
df.to_csv(arg.o)



