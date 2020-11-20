import numpy as np
from config import *
from typing import List

postfix = [7, 8, 6, 7, 3, 2, 2, 0, 7, 9, 0, 3, 3, 7, 6, 4, 4, 4, 7, 7, 5, 9, 3, 1, 1, 1]


def generate_postfix_test_data(postfix: List[int]):
    all_posible = []
    for i in range(10000):
        all_posible.append([int(j) for j in '{0:04}'.format(i)] + postfix)

    return all_posible


def gererate_test_data(data_size=100000, threshold: int = threshold):
    dataset = np.array([np.random.randint(0, 10, 30, np.int8) for _ in range(data_size)])

    target = np.zeros(data_size, np.int8)
    for i, dd in enumerate(dataset):
        cool_computer = [d for d in dd[:4] if d >= threshold]
        if len(cool_computer) >= 4:
            target[i] = 1

    return dataset, target


if __name__ == '__main__':
    all_posible = generate_postfix_test_data(postfix)
