import os
import glob
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to search for csvs")
args = parser.parse_args()

os.chdir(args.dir)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, header=0) for f in all_filenames ])
#export to csv
combined_csv.to_csv(str(args.dir) + "/combined_csv.csv", index=False, encoding='utf-8-sig')
