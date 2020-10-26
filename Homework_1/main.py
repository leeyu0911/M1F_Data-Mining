"""
macOS: 10.15.7（19H2）
python: 3.7
pycharm: 2020.2.3
"""
from Homework_1.FP_Growth import *
from Homework_1.apriori_algorithm import *
from time import time


def deal_lecture_data(chose_type=1):
    """ result:
    str:
    {('a',): 2, ('c',): 3, ('b',): 3, ('e',): 3,
     ('a', 'c'): 2, ('b', 'c'): 2, ('b', 'e'): 3, ('c', 'e'): 2,
     ('b', 'c', 'e'): 2}

    int:
    {('11',): 2, ('33',): 3, ('22',): 3,
     ('55',): 3, ('11', '33'): 2, ('22', '33'): 2, ('22', '55'): 3, ('33', '55'): 2,
     ('22', '33', '55'): 2}
    """
    if chose_type == 1:
        database = [['a', 'c', 'd'],
                    ['b', 'c', 'e'],
                    ['a', 'b', 'c', 'e'],
                    ['b', 'e']]
    else:
        database = [[11, 33, 44],
                    [22, 33, 55],
                    [11, 22, 33, 55],
                    [22, 55]]
    return database


def deal_kaggle_data(filename='./dataset/groceries - groceries.csv'):
    """
    https://www.kaggle.com/irfanasrullah/groceries?select=groceries+-+groceries.csv
    format:
    Item(s),Item 1,Item 2,Item 3,Item 4,Item 5,Item 6,Item 7,Item 8,Item 9,Item 10,Item 11,Item 12,Item 13,Item 14,Item 15,Item 16,Item 17,Item 18,Item 19,Item 20,Item 21,Item 22,Item 23,Item 24,Item 25,Item 26,Item 27,Item 28,Item 29,Item 30,Item 31,Item 32
    4,citrus fruit,semi-finished bread,margarine,ready soups
    3,tropical fruit,yogurt,coffee
    ...
    """
    with open(filename) as f:
        content = f.readlines()
    content = [s.strip() for s in content]
    # print(content)

    transactions = []
    for c in content[1:]:
        temp = c.split(',')[1:]
        transactions.append(temp)
    return transactions


def deal_IBM_data(filename='./dataset/IBM_data_generator.csv'):
    """
    format:
    TID,item
    1,118 266 364 427 628 673 868 904
    2,40 316 594 858 870 871 917
    ...
    """
    with open(filename) as f:
        content = f.readlines()
    content = [s.strip() for s in content]
    # print(content)

    transactions = []
    for c in content[1:]:
        temp = c.replace(',', ' ').split(' ')[1:]
        transactions.append(temp)
    # print(transactions)
    return transactions


class Apriori_test_set:

    # test from lecture
    @staticmethod
    def test_from_lecture(chose_type=1, min_support=2):
        transactions = deal_lecture_data(chose_type)
        return apriori(transactions, min_support)

    # test from kaggle (groceries_datatest)
    @staticmethod
    def test_from_kaggle(min_support=50):
        transactions = deal_kaggle_data()
        return apriori(transactions, min_support)
        # print('L_test_data_csv:', L_test_data_csv)

    # test from IBM data
    @staticmethod
    def test_from_IBMdata(min_support=18):
        transactions = deal_IBM_data()
        return apriori(transactions, min_support)
        # print('L_test_data_csv:', L_test_data_csv)


class FP_Growth_test_set:

    @staticmethod
    def test_from_lecture(**kwargs):
        """chose_type=1, min_support=2, confidence=0.6"""
        chose_type = kwargs.get('chose_type', 1)
        min_support = kwargs.get('min_support', 2)
        confidence = kwargs.get('confidence', 0.6)

        transactions = deal_lecture_data(chose_type)
        p = find_frequent_patterns(transactions, min_support)
        return generate_association_rules(p, confidence)

    @staticmethod
    def test_from_kaggle(min_support=50, confidence=0.6):
        transactions = deal_kaggle_data()
        p = find_frequent_patterns(transactions, min_support)
        return generate_association_rules(p, confidence)

    @staticmethod
    def test_from_IBMdata(min_support=18, confidence=0.6):
        transactions = deal_IBM_data()
        p = find_frequent_patterns(transactions, min_support)
        return generate_association_rules(p, confidence)


class Test_time:
    """
    Not only for test time
    add return result
    """

    def __init__(self, transactions=deal_lecture_data(), algo='apriori', **kwargs):
        self.transactions = transactions
        self.algo = algo
        self.min_support = kwargs.get('min_support')
        self.confidence = kwargs.get('confidence')
        t1 = time()
        self.result = self._algo()
        t2 = time()
        print(str(self.algo), str(kwargs), ':', round(t2 - t1, 3), 's')
        self.time = round(t2 - t1, 3)

    def _algo(self):
        if self.algo in ['Apriori', 'apriori']:
            return apriori(self.transactions, min_support=self.min_support)
        elif self.algo in ['FP_Growth', 'fp_growth', 'FP_growth', 'fpgrowth']:
            return find_frequent_patterns(self.transactions, min_support=self.min_support)


def to_file(content: dict, filename):
    # content = list(content.items())
    f = open('./result/' + filename, 'w+')
    # for i in content:
    #     # print(i)
    #     f.write(str(i) + '\n')
    f.write(str(content))
    f.close()


def add_args_to_filename(arg) -> str:
    s = ''
    order = ['chose_type', 'min_support', 'confidence']

    if type(arg) == dict:
        for key in order:
            if arg.get(key) is not None:
                s += '_' + str(key) + '_' + str(arg[key])
    else:
        s += '_' + str(arg)

    return s


if __name__ == '__main__':

    # -----Apriori test------
    task1 = [Apriori_test_set.test_from_lecture,
             Apriori_test_set.test_from_kaggle,
             Apriori_test_set.test_from_IBMdata]
    arg1 = [{'chose_type': 1, 'min_support': 3},
            {'min_support': 600},
            {'min_support': 50}]
    # run and write to file
    for i, t in enumerate(task1):
        to_file(t(**arg1[i]), str(task1[i]).split(' ')[1] + add_args_to_filename(arg1[i]) + '.json')

    # -----FP_Growth test-----
    task2 = [FP_Growth_test_set.test_from_lecture,
             FP_Growth_test_set.test_from_kaggle,
             FP_Growth_test_set.test_from_IBMdata]
    arg2 = [{'chose_type': 1, 'min_support': 2, 'confidence': 0.6},
            {'min_support': 50, 'confidence': 0.6},
            {'min_support': 18, 'confidence': 0.6}]
    # run and write to file
    for i, t in enumerate(task2):
        to_file(t(**arg2[i]), str(task2[i]).split(' ')[1] + add_args_to_filename(arg2[i]) + '.json')
        print(str(task2[i]).split(' ')[1])
        print(t(**arg2[i]))
        print()


    # -----test time-----
    k1 = []
    k2 = []
    print('Kaggle:')
    for i in range(10):
        k1.append(Test_time(deal_kaggle_data(), 'apriori', min_support=50).time)
        k2.append(Test_time(deal_kaggle_data(), 'FP_growth', min_support=50).time)

    print()

    i1 = []
    i2 = []
    print('IBM:')
    for i in range(10):
        i1.append(Test_time(deal_IBM_data(), 'apriori', min_support=18).time)
        i2.append(Test_time(deal_IBM_data(), 'FP_growth', min_support=18).time)