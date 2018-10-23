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
class hash_node:
    def __init__(self, mod, level):
        self.children = [None] * mod
        self.level = level
        self.is_leaf = False
        self.mod = mod
    def add(self, candidate, candidate_to_count):
        if self.level == len(candidate) - 1:
            self.is_leaf = True
            index = hash(candidate[self.level]) % self.mod
            if self.children[index] == None:
                candidate_and_count = [set(candidate), 0]
                candidate_to_count[tuple(candidate)] = candidate_and_count
                self.children[index] = [candidate_and_count]
            else:
                candidate_and_count = [set(candidate), 0]
                candidate_to_count[tuple(candidate)] = candidate_and_count
                self.children[index].append(candidate_and_count)
        else:
            index = hash(candidate[self.level]) % self.mod
            if self.children[index] == None:
                child_node = hash_node(self.mod, self.level + 1)
                self.children[index] = child_node
            self.children[index].add(candidate, candidate_to_count)
    def feed_row(self, row, candidate_length, removed):
        #print('removed =', removed)
        for i in range(0, len(row) - candidate_length + 1):
            #print('--hash--:', row[i])
            index = hash(row[i]) % self.mod
            #print('index:', index)
            child = self.children[index]
            if child == None:
                #print('child = None')
                continue
            if self.is_leaf:
                #print('is leaf')
                #print('child:', child)
                for candidate in child:
                    if candidate[0] == {row[i]} | removed:
                        #print('set found:', candidate[0])
                        candidate[1] = candidate[1] + 1
            else:
                removed_next = set(removed)
                removed_next.add(row[i])
                #print('pass to child:', row[i + 1:])
                child.feed_row(row[i + 1:], candidate_length - 1, removed_next)
    def count(self):
        count = []
        if self.is_leaf:
            for child in self.children:
                if child == None:
                    continue
                for candidate_count in child:
                    if not candidate_count == None:
                        count.append(candidate_count)
            return count
        else:
            for child in self.children:
                if not child == None:
                    count.extend(child.count())
            return count
class hash_tree:
    def __init__(self, candidates, mod):
        candidate_to_count = dict()
        root = hash_node(mod, 0)
        for candidate in candidates:
            candidate.sort()
            root.add(candidate, candidate_to_count)
        self.root = root
        #print(candidates)
        self.candidate_length = len(candidates[0])
        self.candidate_to_count = candidate_to_count
    def feed_row(self, row):
        row.sort()
        self.root.feed_row(row, self.candidate_length, set())
    def count(self):#, threshold):
        count = []
        for k in self.candidate_to_count:
            count.append([list(k), self.candidate_to_count[k][1]])
        return count
#mod = 5000
rows = read_csv_file(file_name)
all_items = get_all_items(rows)
threshold = int(len(rows) * float(threshold_percentage) / 100)
result = []
exclude_target = []
space = 50
for i in range(1, len(all_items) + 1):
    #print('i =', i)
    #print('all items =', all_items)
    itemsets_c = generate_itemsets(list(all_items), i)
    itemsets_c = exclude(itemsets_c, exclude_target)
    #print('C =', itemsets_c)
    if len(itemsets_c) == 0:
        break
    mod = int((len(itemsets_c) * space) ** (1 / i))
    tree = hash_tree(itemsets_c, mod)
    for row in rows:
        tree.feed_row(row)
    count = tree.count()
    itemsets_l = []
    #print(count)
    exclude_target = []
    for each_candidate_count in count:
        #print(each_candidate_count)
        if each_candidate_count[1] < threshold:
            exclude_target.append(each_candidate_count[0])
        else:
            itemsets_l.append(each_candidate_count[0])

            result.append([list(each_candidate_count[0]), each_candidate_count[1]])
    num = search_num(itemsets_c, rows)
    all_items = itemsets_union(itemsets_l)
    if len(all_items) < i:
        break
sort_result(result)
print_result(result)
