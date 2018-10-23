from commonfunctions import *
def bool_sum(b1, b2, b3):
    a = int(b1) + int(b2) + int(b3)
    result = bool(a % 2)
    carry = bool(int(a / 2))
    return result, carry
def next_bool_array(bool_array):
    carry = False;
    for i in range(0, len(bool_array)):
        bool_array[i], carry = bool_sum(i == 0, bool_array[i], carry)
        if carry == False:
            break
def generate_candidates(all_items):
    bool_array = [False] * len(all_items)
    candidates = []
    for i in range(0, 2 ** len(bool_array) - 1):
        next_bool_array(bool_array)
        tmp = []
        for j in range(0, len(bool_array)):
            if bool_array[j]:
                tmp.append(all_items[j])
        candidates.append(tmp)
    return candidates

rows = read_csv_file(file_name)
all_items = get_all_items(rows)
threshold = int(len(rows) * float(threshold_percentage) / 100)
candidates = generate_candidates(all_items)
count = [0] * len(candidates)
for i in range(0, len(candidates)):
    for j in range(0, len(rows)):
        if set(candidates[i]).issubset(set(rows[j])):
            count[i] = count[i] + 1
result = []
for i in range(0, len(candidates)):
    if count[i] >= threshold:
        result.append([candidates[i], count[i]])
sort_result(result)
print_result(result)
