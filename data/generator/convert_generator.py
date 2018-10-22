import csv
def clearspace(str):
    for i in range(len(str)):
        if str[i] != ' ':
            return str[i:]
def getstr(str):
    for i in range(0, len(str)):
        if str[i] == ' ':
            return str[:i], str[i:]
def removelast(str):
    return str[:len(str) - 2]
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("file", help = "the input file")
args = parser.parse_args()
file_name = args.file
converted = []
with open(file_name, 'r') as file:
    for line in file:
        str = clearspace(line)
        index, str = getstr(str)
        str = clearspace(str)
        index, str = getstr(str)
        str = clearspace(str)
        if str[len(str) - 1] == '\n':
            item = str[:len(str) - 1]
        else:
            item = str
        t = int(index)
        if t > len(converted):
            converted.append([])
            converted[len(converted)-1].append(item)
        else:
            if not item in converted[t-1]:
                converted[t-1].append(item)
with open(file_name + '.csv','w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(converted)
