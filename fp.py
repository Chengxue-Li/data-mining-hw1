from commonfunctions import *
def combine(list1, list2):
    if not len(list1) == len(list2):
        return
    list = []
    for i in range(0, len(list1)):
        list.append([list1[i], list2[i]])
    return list
def count_item_num(all_items, rows):
    count = [0] * len(all_items)
    for row in rows:
        for i in range(0, len(all_items)):
            if all_items[i] in row:
                count[i] = count[i] + 1
    return count
def sort_each_row(rows, item_to_count_dict):
    #print(item_to_count_dict)
    for row in rows:
        #print('before:', row)
        row.sort(key = lambda item: (item_to_count_dict[item], item), reverse = True)
        #if {'Fudge', 'Jam'}.issubset(set(row)):
            #print(row)
        #print('after:', row)
def create_item_to_count_dict(all_items_and_count):
    item_to_count_dict = dict()
    for item_and_count in all_items_and_count:
        item_to_count_dict[item_and_count[0]] = item_and_count[1]
    return item_to_count_dict
class FP_node_small:
    def __init__(self, original_node, num):
        self.original_node = original_node
        self.num = num
        self.parent = None
        self.children = []
    def add_parent(self, parent_original_node):
        if not self.parent == None:
            print('this node has had a parent')
            return None
        parent = FP_node_small(parent_original_node, self.num)
        parent.children.append(self)
        self.parent = parent
        return parent
    def is_equal_to(self, target):
        return self.original_node == target.original_node
    def has_child(self, target):
        for child in self.children:
            if child.is_equal_to(target):
                return True
        return False
    def get_child(self, target):
        for child in self.children:
            if child.is_equal_to(target):
                return child
        print('don\'t contain child')
        return None
    def search(self, candidate_set):
        item = self.original_node.item
        #print('current item:', item)
        if item in candidate_set:
            #print('item in candidate')
            candidate_set.remove(item)
            if candidate_set == set():
                #print('after remove, candidate set is null')
                #print('return', self.num)
                return self.num
            else:
                #print('candidate set is still not empty')
                summation = 0
                for child in self.children:
                    #print('pass to child', child.original_node.item)
                    summation = summation + child.search(set(candidate_set))
                return summation
        else:
            #print('item is not in candidate')
            summation = 0
            for child in self.children:
                #print('pass to child', child.original_node.item)
                summation = summation + child.search(set(candidate_set))
            return summation
class FP_tree_small:
    def __init__(self, leaf_node):
        self.leaf_item = leaf_node.item
        self.set = set()
        position = leaf_node
        num = position.num
        position_small = FP_node_small(position, num)
        while not position.parent == None:
            position = position.parent
            if not position.item == None:
                self.set.add(position.item)
            position_small = position_small.add_parent(position)
        self.root = position_small
    def merge(self, target):
        self_position = self.root
        self.set = self.set | target.set
        target_position = target.root.children[0]
        while True:
            self_position.num = self_position.num + target_position.parent.num
            if self_position.has_child(target_position):
                self_position = self_position.get_child(target_position)
                target_position = target_position.children[0]
            else:
                self_position.children.append(target_position)
                target_position.parent = self_position
                break
    def generate_frequent_itemsets(self):
        #print(self.leaf_item)
        #item_list = list(self.set)
        exclude = []
        frequent_itemsets = []
        item_set = self.set
        #print('all items:', item_set)
        for i in range(1, len(item_set) + 1):
            #print('length of candidate:', i)
            if len(item_set) < i:
                break
            candidates = generate_itemsets(list(item_set), i)
            #print('candidates:', candidates)
            item_set = set()
            for candidate in candidates:
                candidate_set = set(candidate)
                #print('item:', self.leaf_item)
                candidate_set.add(self.leaf_item)#this may be removed
                #print('candidate_set:', candidate_set)
                def should_continue():
                    for exclude_set in exclude:
                        if exclude_set.issubset(candidate_set):
                            return True
                    return False
                if should_continue():
                    #print('in the exclude')
                    continue

                num = self.root.search(set(candidate_set))
                #print(candidate_set)
                #print('num:', num)
                if num < self.threshold:
                    exclude.append(candidate_set)
                    #print('add candidate to exclude:', candidate_set)
                    #print('exclude:', exclude)
                else:
                    item_set = item_set | candidate_set
                    item_set.remove(self.leaf_item)
                    frequent_itemsets.append([candidate_set, num])
        return frequent_itemsets
class FP_node:
    def __init__(self, item = None, parent = None):
        self.item = item
        self.parent = parent
        self.num = 0
        self.children = []
    def add_child(self, item_name):
        child = self.get_child(item_name)
        if not child == None:
            print('child', item_name, 'has existed')
            return
        child = FP_node(item = item_name, parent = self)
        self.children.append(child)
        return child
    def num_add(self):
        self.num = self.num + 1
        return self
    def get_num(self):
        return self.num
    def get_item_name(self):
        return self.item
    def get_child(self, item_name):
        for child in self.children:
            if child.get_item_name() == item_name:
                return child
        return None
class FP_tree:
    def __init__(self, rows):
        all_items = get_all_items(rows)
        count = count_item_num(all_items, rows)
        #print(count)
        all_items_and_count = combine(all_items, count)
        #print(all_items_and_count)
        all_items_and_count.sort(key = lambda item: (item[1], item[0]))
        self.all_items_and_count = all_items_and_count
        #print(all_items_and_count)
        #print(all_items_and_count)
        item_to_count_dict = create_item_to_count_dict(all_items_and_count)
        #print('before:', rows)
        sort_each_row(rows, item_to_count_dict)
        #print('after:', rows)
        self.root = FP_node()
        item_to_node_set_dict = dict()
        for row in rows:
            #if {'Fudge', 'Jam'}.issubset(set(row)):
                #sp=sp+1
                #print(sp)
            position = self.root
            for item in row:
                child = position.get_child(item)
                if child == None:
                    position = position.add_child(item).num_add()
                else:
                    position = child.num_add()
                if item in item_to_node_set_dict:
                    if not position in item_to_node_set_dict[item]:
                        item_to_node_set_dict[item].add(position)
                else:
                    item_to_node_set_dict[item] = {position}
        self.item_to_node_set_dict = item_to_node_set_dict
    def generate_small_trees(self, threshold):
        small_trees = []
        for i in range(0, len(self.all_items_and_count)):
            if self.all_items_and_count[i][1] < threshold:
                continue
            set_of_specific_item_nodes = self.item_to_node_set_dict[self.all_items_and_count[i][0]]
            small_tree = None
            for leaf_node in set_of_specific_item_nodes:
                if small_tree == None:
                    small_tree = FP_tree_small(leaf_node)
                else:
                    small_tree.merge(FP_tree_small(leaf_node))
            small_tree.threshold = threshold
            small_trees.append(small_tree)
        return small_trees
    def generate_frequent_itemsets(self, threshold):
        frequent_itemsets = []
        small_trees = self.generate_small_trees(threshold)
        for small_tree in small_trees:
            f = small_tree.generate_frequent_itemsets()
            for itemset in f:
                itemset[0] = list(itemset[0])
            frequent_itemsets.extend(f)
            #print('frequent itemsets:', f)
        for item_and_count in self.all_items_and_count:
            if item_and_count[1] >= threshold:
                frequent_itemsets.append([[item_and_count[0]], item_and_count[1]])
        return frequent_itemsets
rows = read_csv_file(file_name)
threshold = int(len(rows) * float(threshold_percentage) / 100)
tree = FP_tree(rows)
result = tree.generate_frequent_itemsets(threshold)
#print(result)
sort_result(result)
print_result(result)
