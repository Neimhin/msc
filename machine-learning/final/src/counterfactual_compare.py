import lib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input",type=str)
parser.add_argument("--train",action='store_true')
arg = parser.parse_args()

if arg.train:
    df = lib.read_csv(arg.input)