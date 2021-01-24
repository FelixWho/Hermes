from pydub import AudioSegment
import argparse
import string
import re
import math
import os
from pathlib import Path
import csv
# by default, script attempts to generate 15 second clips

# take arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("input_mp3", help="input mp3 file path")
parser.add_argument("input_cha", help="input cha file path")
parser.add_argument("output", help="output directory")
args = parser.parse_args()

transcriptsA = []
transcriptsB = []
tokensA = []
tokensB = []
intervalsA = []
intervalsB = []
rows = []

with open(args.input_cha, 'r') as content_file:
    content = content_file.read()
tokens = re.split(r'\*|%', content)

#print(tokens[:5])

for token in tokens:
    token = token.strip()
    if token[:1] != "A" and token[:1] != "B":
        continue
    if token[:1] == "A":
        tokensA.append(token[2:].strip().lower())
    if token[:1] == "B":
        tokensB.append(token[2:].strip().lower())

#print("Splitting by speaker. Speaker B:")
#print(tokensB[:5])

def removeSounds(tokens):
    ret = []
    for token in tokens:
        whole = token.split("\x15")
        text = whole[0].split(" ")
        formatted = ""
        for word in text:
            if word[0:2] == "&=": # sound
                continue
            if word == "xxx": # non-decipherable
                continue
            formatted += " " + str(word)
        whole[0] = formatted.strip()
        ret.append("\x15".join(whole))
    return ret

tokensB = removeSounds(tokensB)
tokensA = removeSounds(tokensA) 

#print(tokensB[:5])

def removePunc(tokens):
    ret = []
    for token in tokens:
        spl = token.split('\x15')
        for c in string.punctuation:
            if c == '\'':
                continue
            spl[0] = spl[0].replace(c, " ")
            spl[0] = spl[0].replace('\n', " ")
            spl[0] = spl[0].replace('\t', " ")
        if spl[0].isspace() or spl[0] == "":
            continue # don't want empty text
        for i in range(len(spl)):
            spl[i] = spl[i].strip()
        token = "\x15".join(spl)
        ret.append(token.strip())
    return ret

tokensB = removePunc(tokensB)
tokensA = removePunc(tokensA)

#print(tokensB[:5])

def removeLinesWithoutTime(tokens):
    '''
    This function joins lines when a line doesn't have a time frame at the end of it.
    i.e.
    *A:	I'm sorry.                          <--- NO TIME FRAME AT END!!! ATTEMPT TO COMBINE IT WITH OTHER LINES
    *A:	We'll blame him. 376270_377420
    '''
    ret = []

    i = 0
    n = len(tokens)-1
    while i < n-1:
        spl = tokens[i].split('\x15')
        spl2 = tokens[i+1].split('\x15')
        if (len(spl) < 3 or '_' not in spl[-2]) and (len(spl2) < 3 or '_' not in spl2[-2]):
            spl[0] = spl[0].strip()+" "+spl2[0].strip()
            tokens[i] = '\x15'.join(spl)
            del tokens[i+1]
            n = n - 1
        else:
            i = i + 1

    #print(tokens)

    i = 0
    n = len(tokens)
    while i < n:
        spl = tokens[i].split('\x15')
        if len(spl) < 3 or '_' not in spl[-2]:
            if len(ret) == 0:
                i = i + 1
                continue
            if i == n-1:
                i = i + 1
                continue
            # combine ret[-1] with tokens[i]
            spl2 = ret[-1].split('\x15')
            spl3 = tokens[i+1].split('\x15')
            spl2[0] = spl2[0].strip()+" "+spl[0].strip()+" "+spl3[0].strip()
            spl2[1] = spl2[1].split("_")[0]+"_"+spl3[1].split("_")[1]
            ret.append('\x15'.join(spl2).strip())
            i = i + 2
        else:
            ret.append(tokens[i].strip())
            i = i + 1

    return ret

tokensB = removeLinesWithoutTime(tokensB)
tokensA = removeLinesWithoutTime(tokensA)

#print(tokensB[:5])

def tokensToDict(tokens):
    ret = []
    for token in tokens:
        spl = token.split("\x15")
        curr = {}
        curr["text"] = spl[0].strip()
        curr["text"] = ' '.join(curr["text"].split())
        curr["start"] = spl[1].split("_")[0]
        curr["end"] = spl[1].split("_")[1]
        ret.append(curr)
    return ret

tokensA = tokensToDict(tokensA)
tokensB = tokensToDict(tokensB)

#print(tokensB[:5])

def splitSeconds(transcripts, intervals, tokens):
    '''
    split tokens into ~15s pieces and add the text to transcripts, add time frames to intervals
    Note: TalkBank data is annotated in milliseconds
    '''
    # get when person first starts speaking
    start = int(tokens[0]["start"])
    end = int(tokens[0]["end"])

    words_in_interval = []

    for token in tokens:
        if(int(token["start"]) - start > 15000):
            # load current time intervals and transcripts into arrays
            transcripts.append(" ".join(words_in_interval))
            intervals.append({"starttime": start, "endtime": end})

            # reset variables
            start = int(token["start"])
            end = int(token["end"])
            words_in_interval.clear()

        words_in_interval.append(token["text"])
        end = int(token["end"])
    
    transcripts.append(" ".join(words_in_interval))
    intervals.append({"starttime": start, "endtime": end})

splitSeconds(transcriptsA, intervalsA, tokensA)
splitSeconds(transcriptsB, intervalsB, tokensB)

count = 0
offset = 5 # start the sound segment a bit earlier, to ensure the first word is captured
orig_audio = AudioSegment.from_mp3(args.input_mp3)
orig_audio = orig_audio.set_frame_rate(16000)
base = os.path.basename(args.input_mp3)
name = os.path.splitext(base)[0]

# split left, right audio channels
speakerA_audio = orig_audio.split_to_mono()[0]
speakerB_audio = orig_audio.split_to_mono()[1]

def formatForOutput(transcripts, intervals, speaker):
    global count
    for i in range(0, len(intervals)):
        interval = intervals[i]
        # getting rid of small audio segments less than 2s in length
        if interval["endtime"] - interval["starttime"] < 2:
            continue

        new_audio = speaker[int(interval["starttime"]) - offset : int(interval["endtime"])]
        audio_name = str(args.output) + "/" + name + "_audio_" + str(count) + ".wav"
        new_audio.export(audio_name, format="wav")

        rows.append(name + "_audio_" + str(count) + ".wav\t" + transcripts[i])

        count+=1

formatForOutput(transcriptsA, intervalsA, speakerA_audio)
formatForOutput(transcriptsB, intervalsB, speakerB_audio)

# output to plain txt file
with open(str(args.output) + "/" + name + ".txt", 'w') as file:  
    for line in rows:
        file.write(line+"\n")