"""
transactions: list
[['str',...],
 ...
 ['str',...]]
"""

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

    def __init__(self, transactions, min_support):
        self.frequent_items = self.transaction_frequent(transactions, min_support)  # type: list
        self.header_table = self.build_header_table(self.frequent_items)  # type: dict
        self.root = self._build_FP_Tree(transactions, self.frequent_items, self.header_table)

    @staticmethod
    def transaction_frequent(transactions, min_suport):
        """
        取得高於 min_support 的 items，並從大排到小
        """
        transaction_dict = defaultdict(int)
        for i in range(len(transactions)):
            for j in range(len(transactions[i])):
                transaction_dict[str(transactions[i][j])] += 1  # 在這邊把元素都轉成str

        transaction_dict = {k: v for k, v in transaction_dict.items() if v >= min_suport}

        # {'a': 2, 'b': 1, 'c': 3, 'd': 0} -> [('c', 3), ('a', 2), ('b', 1), ('d', 0)] -> ['c', 'a', 'b', 'd']
        frequent_items = [item[0] for item in sorted(transaction_dict.items(), key=lambda x: x[1], reverse=True)]

        return frequent_items

    @staticmethod
    def build_header_table(frequent_items):
        header = {}
        for item in frequent_items:
            header[item] = None
        return header

    def _insert_node(self, items, node, header):
        item = items[0]
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

        recursive_items = items[1:]
        if len(recursive_items) > 0:
            self._insert_node(recursive_items, child, header)

    def _build_FP_Tree(self, transactions, frequent, header):
        root = FP_Node(None, None, None)

        for tt in transactions:
            # 取出存在frequent中的items，再對存在的item做原始frequent index排序 （越前面frequency越大）
            ordered = sorted([item for item in tt if item in self.frequent_items],
                             key=lambda x: frequent.index(x))
            if len(ordered) > 0:
                self._insert_node(ordered, root, header)

        return root

    def result(self):
        pass
