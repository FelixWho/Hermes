import argparse
from lxml import etree
import string
import re

# take arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="input xml file path")
parser.add_argument("output", help="output txt file path")
args = parser.parse_args()

# set arguments as variables
input_file = args.input
output_file = args.output

# get inner text from xml
root = etree.parse(input_file)
content = root.xpath("//text()")
#print(content)

# format text
for i in range(0, len(content)):
    content[i] = content[i].strip()

#print(content)

formatted_content = []

for text in content:
    if not text.isspace() and text not in string.punctuation:
        formatted_content.append(text.lower())

single_string = " ".join(formatted_content)
#print(single_string)

f = open(output_file, "w")
f.write(single_string)
f.close()

print(str(len(formatted_content)) + " words processed")




