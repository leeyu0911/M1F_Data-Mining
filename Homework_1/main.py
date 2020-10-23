from Homework_1.apriori_algorithm import *


# test from lecture
def test_from_lecture(chose_type=1):
    """ result:
    str:
    [0,
    {'a': 2, 'c': 3, 'b': 3, 'e': 3},
    {('a', 'c'): 2, ('b', 'c'): 2, ('b', 'e'): 3, ('c', 'e'): 2},
    {('b', 'c', 'e'): 2},
    {}]

    int:
    [0,
    {'11': 2, '33': 3, '22': 3, '55': 3},
    {('11', '33'): 2, ('22', '33'): 2, ('22', '55'): 3, ('33', '55'): 2},
    {('22', '33', '55'): 2},
    {}]
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

    L = apriori(database, 2)
    print('test from lecture:', L)


# test from kaggle (groceries_datatest)
def test_from_kaggle(min_support=50):
    filename = './dataset/groceries - groceries.csv'
    with open(filename) as f:
        content = f.readlines()
    content = [s.strip() for s in content]
    # print(content)

    transactions = []
    for c in content[1:]:
        temp = c.split(',')[1:]
        transactions.append(temp)
    # print(transactions)

    L_test_data_csv = apriori(transactions, min_support)
    print('L_test_data_csv:', L_test_data_csv)


# test from IBM data
def test_from_IBMdata(filename='./dataset/test_data.csv', min_support=18):
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

    L_test_data_csv = apriori(transactions, min_support)
    print('L_test_data_csv:', L_test_data_csv)


if __name__ == '__main__':
    pass
