"""
transactions: list
[['str',...],
 ...
 ['str',...]]
"""
import itertools
from collections import defaultdict


class FP_Node:

    def __init__(self, item, frequency, parent):
        """
        for FP_Tree use
        :param item: str
        :param frequency: int
        :param parent: FP_Node
        """
        self.item = item
        self.frequency = frequency
        self.children = []
        self.parent = parent
        self.next = None

    def get_child(self, item):
        for child in self.children:
            if child.item == item:
                return child
        return None

    def add_child(self, item):
        child = FP_Node(item, 1, self)
        self.children.append(child)
        return child


class FP_Tree:

    def __init__(self, transactions, min_support, root_value=None, root_count=None):
        self.frequent_items = self._find_frequent_items(transactions, min_support)  # type: dict
        self.header_table = self._build_header_table(self.frequent_items)  # type: dict
        self.root = self._build_FP_Tree(transactions, self.header_table, root_value, root_count)

    @staticmethod
    def _find_frequent_items(transactions, min_suport):
        """
        取得高於 min_support 的 items，並從大排到小
        """
        transaction_dict = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                transaction_dict[item] += 1

        transaction_dict = {k: v for k, v in transaction_dict.items() if v >= min_suport}

        # {'a': 2, 'b': 1, 'c': 3, 'd': 0} -> [('c', 3), ('a', 2), ('b', 1), ('d', 0)] -> ['c', 'a', 'b', 'd']
        # frequent_items = [item[0] for item in sorted(transaction_dict.items(), key=lambda x: x[1], reverse=True)]

        return transaction_dict

    @staticmethod
    def _build_header_table(frequent_items: dict):
        header_table = {}
        for item in frequent_items:
            header_table[item] = None
        return header_table

    @staticmethod  # TODO: 不用遞迴
    def _insert_node(items, node, header):
        for item in items:
            child = node.get_child(item)  # 會指到 child node
            if child is not None:
                child.frequency += 1
            else:
                child = node.add_child(item)

                # 處理header table next
                if header[item] is None:
                    header[item] = child
                else:
                    pointer = header[item]
                    while pointer.next is not None:
                        pointer = pointer.next
                    pointer.next = child
            node = child

    def _build_FP_Tree(self, transactions, header, root_value, root_count):
        root = FP_Node(root_value, root_count, None)

        for tt in transactions:
            # 取出存在frequent中的items，再對存在的item做原始frequent index排序 （越前面frequency越大）
            ordered = sorted([item for item in tt if item in self.frequent_items],
                             key=lambda x: self.frequent_items[x], reverse=True)
            if len(ordered) > 0:
                self._insert_node(ordered, root, header)

        return root

    # below all fork from https://github.com/evandempsey/fp-growth
    def tree_has_single_path(self, node):
        """
        If there is a single path in the tree,
        return True, else return False.
        """
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])  # TODO: True 是否可以省略？

    def mine_patterns(self, min_support):
        """
        Mine the constructed FP tree for frequent patterns.
        """
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(min_support))

    def zip_patterns(self, patterns):
        """
        Append suffix to patterns in dictionary if
        we are in a conditional FP tree.
        """
        suffix = self.root.item

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):
        """
        Generate a list of patterns with support counts.
        """
        patterns = {}
        items = self.frequent_items.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.item is None:
            suffix_value = []
        else:
            suffix_value = [self.root.item]
            patterns[tuple(suffix_value)] = self.root.frequency

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = min([self.frequent_items[x] for x in subset])

        return patterns

    def mine_sub_trees(self, min_support):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = {}
        mining_order = sorted(self.frequent_items.keys(), key=lambda x: self.frequent_items[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.header_table[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.next

            # For each occurrence of the item,
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.frequency
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.item)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FP_Tree(conditional_tree_input, min_support, item, self.frequent_items[item])
            subtree_patterns = subtree.mine_patterns(min_support)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, min_support):
    """
    Given a set of transactions, find the patterns in it
    over the specified support min_support.
    """
    tree = FP_Tree(transactions, min_support, None, None)
    return tree.mine_patterns(min_support)


def generate_association_rules(patterns: dict, confidence_threshold):
    """
    Given a set of frequent itemsets, return a dict
    of association rules in the form
    {(left): ((right), confidence)}
    """
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules
