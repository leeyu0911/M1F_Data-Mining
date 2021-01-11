from pathlib import Path
import numpy as np


g1 = Path('./hw3dataset/graph_1.txt')
g2 = Path('./hw3dataset/graph_2.txt')
g3 = Path('./hw3dataset/graph_3.txt')
g4 = Path('./hw3dataset/graph_4.txt')
g5 = Path('./hw3dataset/graph_5.txt')
g6 = Path('./hw3dataset/graph_6.txt')
t1 = Path('./hw3dataset/test.txt')
l1 = Path('./hw3dataset/lecture.txt')
i1 = Path('./hw3dataset/IBM_testing_dataset.txt')

ig1 = Path('./hw3dataset/graph_1_increase.txt')
ig2 = Path('./hw3dataset/graph_2_increase.txt')
ig3 = Path('./hw3dataset/graph_3_increase.txt')


def load_txt(file_name):
    """
    :return: [('1', '2'), ('2', '3'), ('3', '4'), ('4', '5'), ('5', '6')]
    """
    with open(file_name) as f:
        text = f.read()
    text = [tuple(i for i in t.split(',')) for t in text.split('\n') if t != '']
    return text


def load_IBM_text(file_name):
    with open(file_name) as f:
        text = f.read()
    text = [t.split('       ')[2:] for t in text.split('\n')][:-1]
    text = [(str(int(t[0])), str(int(t[1]))) for t in text]
    return text


def list_to_adjacent_matrix(load_txt):
    """
    :return:
    """
    flatten_list = []
    for i in load_txt:
        flatten_list.extend(i)

    items = sorted(set(flatten_list), key=lambda x: int(x) if x.isdigit() else x)
    n = len(set(items))

    am = np.zeros((n, n))
    for i, j in load_txt:
        am[items.index(i)][items.index(j)] = 1
    return items, am


class 不看說明書的錯誤(Exception):
    """請看說明文件好嗎"""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g1))
    print(items)
    print(adjacent_matrix)

    IBM_items, am = list_to_adjacent_matrix(load_IBM_text(i1))

