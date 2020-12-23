import argparse
import csv
from pathlib import Path

# take arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("directory_path", help="directory file path")
parser.add_argument("data_path", help="dataset path")
parser.add_argument("output", help="output csv file path")
args = parser.parse_args()

# set arguments as variables
directory_file = open(args.directory_path, "r")
output_file = open(args.output, "wb")
writer = csv.writer(output_file, delimeter=",")
data_path = args.data_path

writer.writerow(["wav_filename", "wav_filesize", "transcript"])

for line in directory_file:
    pair = line.split()
    wav_name = pair[0]
    transcript_file = pair[1]
    transcript = open(transcript_file, "r").read()
    filesize = Path(str(data_path)+"/"+wav_name).stat().st_size
    writer.writerow([wav_name, filesize, transcript])

directory_file.close()
output_file.close()
