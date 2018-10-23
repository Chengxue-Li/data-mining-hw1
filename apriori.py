from commonfunctions import *
def exclude(itemsets, target):
    itemsets_exclude = itemsets[:]
    if target == []:
        return itemsets_exclude
    delete_list = []
    for i in range(0, len(itemsets_exclude)):
        for j in range(0, len(target)):
            if set(target[j]).issubset(set(itemsets_exclude[i])):
                delete_list.append(i)
                break
    for index in sorted(delete_list, reverse=True):
        del itemsets_exclude[index]
    return itemsets_exclude
def itemsets_union(itemsets):
    u = set()
    for itemset in itemsets:
        u = u.union(set(itemset))
    return u
def search_num(itemsets, rows):
    count = [0] * len(itemsets)
    for i in range(0, len(itemsets)):
        for j in range(0, len(rows)):
            if set(itemsets[i]).issubset(set(rows[j])):
                count[i] = count[i] + 1
    return count
rows = read_csv_file(file_name)
all_items = get_all_items(rows)
threshold = int(len(rows) * float(threshold_percentage) / 100)
exclude_target = []
result = []
for i in range(1, len(all_items) + 1):
    #print('i =', i)
    #print('all items =', all_items)
    itemsets_c = generate_itemsets(list(all_items), i)
    itemsets_c = exclude(itemsets_c, exclude_target)
    if len(itemsets_c) == 0:
        break
    num = search_num(itemsets_c, rows)
    itemsets_l = []
    #exclude_target = []
    exclude_target = []
    for j in range(0, len(itemsets_c)):
        if num[j] < threshold:
            exclude_target.append(itemsets_c[j])
        else:
            itemsets_l.append(itemsets_c[j])
            result.append([itemsets_c[j], num[j]])
            #print(itemsets_c[j], ':', num[j])
    #print('L =', itemsets_l)
    #print('exclude =', exclude_target)
    all_items = itemsets_union(itemsets_l)
    if len(all_items) < i:
        break
sort_result(result)
print_result(result)
