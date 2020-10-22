import itertools
from collections import defaultdict

# d = {'a':1, 'b': 2, 'c': 3}

# TODO: hash tree實作
def combinations_by_hash_tree(sequence, length, result):
    if not sequence:
        return
    sequence = sorted(sequence)
    for i in range(len(sequence) - length + 1):
        result.append(sequence[i:])
        combinations_by_hash_tree(sequence[i + 1:], length, result)

# finish
def transaction_frequent(transactions, min_suport):
    """
    計算元素個數，並返回高於min_support的元素及個數
    :param transaction: list
    :param min_suport: int
    :return: dict{transactions: sum}
    """
    transaction_dict = defaultdict(int)
    for i in range(len(transactions)):
        for j in range(len(transactions[i])):
            transaction_dict[str(transactions[i][j])] += 1  # 在這邊把元素都轉成str

    transaction_dict = {k: v for k, v in transaction_dict.items() if v >= min_suport}

    # for key in transaction_dict.copy():  # avoid RuntimeError: dictionary changed size during iteration
    #     if transaction_dict[key] < min_suport:
    #         del transaction_dict[key]

    return transaction_dict

# finish
def search_and_delete(database, ck, min_support):
    """
    搜尋資料表，並刪除ck中小於min_support的元素
    :param database: list
    :param ck: list  # type: [(a, b, ...), ...]
    :param min_support: int
    :return: dict{tuple: int}
    """
    if not ck:
        return {}

    ck_dict = defaultdict(int)

    for k in ck:  # 每一筆組合對database做搜尋
        for data in database:
            if set(k).issubset([str(i) for i in data]):  # 轉成 str 以處理 row data 為 int
                ck_dict[k] += 1

    ck_dict = {k: v for k, v in ck_dict.items() if v >= min_support}
    # print('ck_dict:', ck_dict)

    # for key in ck_dict:  # RuntimeError: dictionary changed size during iteration
    #     if ck_dict[key] < min_support:
    #         del ck_dict[key]

    return ck_dict

# finish
def flatten_element(element):
    """
    把元素展成一維
    :param element: dict {tuple, int}
    :return:
    """
    # print('element:', element)
    flatten_list = []
    for key in element:
        if type(key) is tuple:  # 有第二層以後才拆
            for i in key:  # 不吃int
                flatten_list.append(i)
        else:
            flatten_list.append(key)

    return sorted(set(flatten_list))

# main finish
def apriori(database: list, min_support: int):

    L1 = transaction_frequent(database, min_support)  # type: dict
    L = [0, L1]
    # print('L1:', L1)

    k = 2
    while len(L[k - 1]) > 0:
        # print(k)
        # print('L%d' % k, L[k - 1])
        fe = flatten_element(L[k - 1].keys())
        # print('fe:', fe)
        Ck = sorted(set(itertools.combinations(fe, k)))  # TODO: 是否用set? type: [(a, b), ...]
        # print('Ck:', Ck)
        Lk = search_and_delete(database, Ck, min_support)  # type: dict
        L.append(Lk)
        k += 1

    return L
