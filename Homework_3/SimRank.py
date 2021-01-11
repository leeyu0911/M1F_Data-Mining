from common_func import *
from tqdm import tqdm


def sub_simrank(am, a, b, c=0.8):
    if a == b:
        return 1
    # id_matrix = np.identity(len(am))
    column_a = am[:, a]
    column_b = am[:, b]
    temp = column_a.sum() * column_b.sum()
    if temp == 0:
        return 0
    else:
        front_func = c / temp


    end_func = 0
    # 非常耗時
    # for i, i_tf in enumerate(column_a):
    #     for j, j_tf in enumerate(column_b):
    #         if i_tf and j_tf and i == j:
    #             end_func += 1

    # for i, i_tf in enumerate(column_a):
    #     if i_tf:
    #         for j, j_tf in enumerate(column_b):
    #             if j_tf and i == j:
    #                 end_func += 1

    a_1 = np.argwhere(column_a == 1)
    b_1 = np.argwhere(column_b == 1)
    if len(a_1) < len(b_1):
        for i in a_1:
            if i in b_1:
                end_func += 1
    else:
        for i in b_1:
            if i in a_1:
                end_func += 1
    return front_func * end_func


def simrank(am, c=0.8):
    n = len(am)
    sim_matrix = np.identity(n)
    for i in tqdm(range(n)):
        # print()
        for j in range(n):
            sim_matrix[i, j] = sub_simrank(am, i, j, c)
            # print(i, j, end='\r')
    return sim_matrix


if __name__ == '__main__':
    # lecture
    a1 = [[0, 0, 1, 0, 1],
         [0, 0, 1, 0, 1],
         [0, 0, 0, 1, 0],
         [1, 0, 1, 0, 0],
         [0, 0, 0, 0, 0]]
    a1 = np.array(a1)
    print(simrank(a1))

    from time import time
    t = time()
    items, am = list_to_adjacent_matrix(load_txt(g6))
    s = simrank(am)
    print(time() - t)
    #
    # t = time()
    # items, am = list_to_adjacent_matrix(load_IBM_text(i1))
    # s = simrank(am)
    # print(time() - t)

    # from time import time
    #
    # print()
    # tesk = [g1, g2, g3, g4, g5, g6]
    # tt = time()
    # for i in tesk:
    #     t = time()
    #     items, adjacent_matrix = list_to_adjacent_matrix(load_txt(i))
    #     s = simrank(adjacent_matrix)
    #     print('%.8f' % (time() - t))
    # print('%.8f' % (time() - tt))


# a = [[0] * 3] * 3
# a = [[0 for _ in range(3)] for _ in range(3)]
# a[0][1] = 1
# print(a)
#
# a1 = [[1, 2], [2, 3], [3, 4]]
# a2 = zip(*a1)
# print(list(a2))
