import pandas as pd
import numpy as np
import argparse

# take arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="input csv file path")
args = parser.parse_args()

df = pd.read_csv(args.input_csv, header=0)
ds = df.sample(frac=1)
ds.to_csv(args.input_csv, index=False)

