import csv
def read_csv_file(file_name):
    with open(file_name) as file:
        rows = list(csv.reader(file))
    rows_ = []
    for i in range(0, len(rows)):
        rows_.append([])
        for j in range(0, len(rows[i])):
            if rows[i][j] != '':
                rows_[i].append(rows[i][j])
    return rows_
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("file", help = "the input file")
parser.add_argument("output", help = "the output file")
args = parser.parse_args()
file_name = args.file
output = args.output
rows = read_csv_file(file_name)
converted = []
for i in range(1, len(rows)):
    #print(converted)
    t = int(rows[i][2])
    if t > len(converted):
        converted.append([])
        converted[len(converted)-1].append(rows[i][3])
    else:
        if not rows[i][3] in converted[t-1]:
            converted[t-1].append(rows[i][3])

with open(output,'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(converted)
