from Homework_1.apriori_algorithm import *


# test from lecture
database = [['a', 'c', 'd'],
            ['b', 'c', 'e'],
            ['a', 'b', 'c', 'e'],
            ['b', 'e']]

database = [[11, 33, 44],
            [22, 33, 55],
            [11, 22, 33, 55],
            [22, 55]]

L = apriori(database, 2)
print('test from lecture:', L)
''' result:
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
'''

# test from kaggle



# test from IMB data


# test data
filename = 'test_data.csv'
with open(filename) as f:
    content = f.readlines()
content = [s.strip() for s in content]
# print(content)

transactions = []
for c in content[1:]:
    temp = c.replace(',', ' ').split(' ')[1:]
    transactions.append(temp)
# print(transactions)

L_test_data_csv = apriori(transactions, 18)
print('L_test_data_csv:', L_test_data_csv)
