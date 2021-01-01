import pandas as pd
import numpy as np
import argparse

# splits into 70% train, 15% validate, 15% test
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="input csv file path")
parser.add_argument("output", help="output directory")
args = parser.parse_args()

df = pd.read_csv(args.input_csv, header=0)
train, validate, test = np.split(df.sample(frac=1, random_state=42), [int(.7*len(df)), int(.85*len(df))])

train.to_csv(str(args.output) + "/train.csv", index=False)
validate.to_csv(str(args.output) + "/dev.csv", index=False)
test.to_csv(str(args.output) + "/test.csv", index=False)
