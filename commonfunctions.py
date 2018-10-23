import csv
from argparse import ArgumentParser
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
def get_all_items(rows):
    all_items = []
    for row in rows:
        for item in row:
            if item not in all_items and item != "":
                all_items.append(item)
    return all_items
def combination(data, r, start, k, bag, itemsets):
    if(k == r):
        itemsets.append(bag[:])
        return
    for i in range(start, len(data)):
        bag[k] = data[i]
        combination(data, r, i + 1, k + 1, bag, itemsets)
def generate_itemsets(items, num):
    itemsets = []
    combination(items, num, 0, 0, [''] * num, itemsets)
    return itemsets
def sort_result(result):
    for set in result:
        set[0].sort()
    result.sort(key = lambda set: (set[1], set[0]))
def print_result(result):
    for set in result:
        print(set[0], ':', set[1])
parser = ArgumentParser()
parser.add_argument("file", help = "the input csv file")
parser.add_argument("-t", "--threshold", help = "the threshold (or minimum support) percentage (0 - 100)", dest = "threshold", default = "10")
args = parser.parse_args()
file_name = args.file
threshold_percentage = args.threshold
