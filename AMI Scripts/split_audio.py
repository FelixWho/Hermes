from pydub import AudioSegment
import argparse
import xml.etree.ElementTree as ET 
import string
import re
import math
import os
from pathlib import Path
import csv
# by default, script attempts to generate 15 second clips

# take arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("input_audio", help="input audio file path")
parser.add_argument("input_xml", help="input xml file path")
parser.add_argument("output", help="output directory")
args = parser.parse_args()

tree_root = ET.parse(args.input_xml).getroot()

# filter all useless entries from xml
entries = []
for entry in tree_root.iter("w"):
    if entry.attrib.get("punc", False) == True:
        continue
    text = entry.text
    if text.isspace() or text in string.punctuation:
        continue
    for c in string.punctuation:
        if c == '\'':
            continue
        text = text.replace(c, "")
    if text == "":
        continue
    # if passed all cases, this is a valid entry
    entries.append(entry)

transcripts = []
intervals = []
csv_rows = []

# get when person first starts speaking
start = float(entries[0].attrib["starttime"])
end = float(entries[0].attrib["endtime"])

words_in_interval = []

for entry in entries:
    if(float(entry.attrib["starttime"]) - start > 15):
        # load current time intervals and transcripts into arrays
        transcripts.append(" ".join(words_in_interval))
        intervals.append({"starttime": start, "endtime": end})

        # reset variables
        start = float(entry.attrib["starttime"])
        end = float(entry.attrib["endtime"])
        words_in_interval.clear()

    text = entry.text.strip()
    if not text.isspace() and text not in string.punctuation:
        for c in string.punctuation:
            if c == '\'':
                continue
            text = text.replace(c, "")
        if text.lower() == "mmhmm": # AMI corpus technicality
            text = "mhm"
        words_in_interval.append(text.lower())
    end = float(entry.attrib["endtime"])

# add final entries
transcripts.append(" ".join(words_in_interval))
intervals.append({"starttime": start, "endtime": end})

# At this point, the intervals and transcripts arrays holds 
# time intervals and text associated with each interval
#print(intervals[31])
#print(transcripts[31])
#print(intervals)

count = 0
offset = 5
orig_audio = AudioSegment.from_wav(args.input_audio) + 10
base = os.path.basename(args.input_audio)
name = os.path.splitext(base)[0] # use the base filename for naming each segment

for i in range(0, len(intervals)):
    interval = intervals[i]
    # getting rid of small audio segments less than 2s in length
    if interval["endtime"] - interval["starttime"] < 2:
        continue

    new_audio = orig_audio[(interval["starttime"]*1000) - offset : interval["endtime"]*1000]
    audio_name = str(args.output) + "/" + name + "_audio_" + str(count) + ".wav"
    new_audio.export(audio_name, format="wav")

    csv_rows.append([name + "_audio_" + str(count) + ".wav", Path(audio_name).stat().st_size, transcripts[i]])

    count+=1

# output results to csv file
fields = ["wav_filename", "wav_filesize", "transcript"]

with open(str(args.output) + "/" + name + ".csv", 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(fields)  
    csvwriter.writerows(csv_rows) 

