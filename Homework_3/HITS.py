from common_func import *


def hits(am, iters=10000, error=1e-8):
    # items, am = list_to_adjacent_matrix(load_txt(file_name))
    n = len(am)

    # h_0 = np.ones((n, 1)) / n**(1/2)
    a_0 = np.ones((n, 1)) / n#**(1/2)
    temp = am.dot(a_0)
    h_1 = temp / np.linalg.norm(temp, 1)  # 1: max(sum(abs(x), axis=0))
    temp = np.transpose(am).dot(h_1)
    a_2 = temp / np.linalg.norm(temp, 1)
    h_2 = h_1  # for UnboundLocalError: referenced before assignment
    for i in range(3, iters):
        a_2_old = a_2
        h_2_old = h_2
        if i % 2 == 1:
            temp = am.dot(a_2)
            h_2 = temp / np.linalg.norm(temp, 1)
            err = sum((h_2 - h_2_old) ** 2)
        else:
            temp = np.transpose(am).dot(h_2)
            a_2 = temp / np.linalg.norm(temp, 1)
            err = sum((a_2 - a_2_old) ** 2)

        if err < error:
            break

    print('HITS iter次數:', i, ', error <=', err[0])
    return h_2, a_2


if __name__ == '__main__':
    print('g1')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g1))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.2, 0.2, 0.2, 0.2, 0.2, 0. ]
    # [0. , 0.2, 0.2, 0.2, 0.2, 0.2]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig1))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.26966472 0.15771299 0.15771299 0.15771299 0.15771299 0.09948333]
    # [0.2694944  0.09954299 0.15774065 0.15774065 0.15774065 0.15774065]

    print('g2')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g2))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.2 0.2 0.2 0.2 0.2]
    # [0.2 0.2 0.2 0.2 0.2]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig2))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.28906618 0.19784222 0.19784222 0.19784222 0.11740716]
    # [0.28891232 0.11747195 0.19787191 0.19787191 0.19787191]

    print('g3')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g3))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.19097222 0.30902778 0.30902778 0.19097222]
    # [0.19098712 0.30901288 0.30901288 0.19098712]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig3))
    h_2, a_2 = hits(adjacent_matrix)
    print(h_2.reshape(-1))
    print(a_2.reshape(-1))
    # [0.28079505 0.21920495 0.28079505 0.21920495]
    # [0.28074582 0.21925418 0.28074582 0.21925418]

    from time import time
    print()
    tesk = [g1, g2, g3, g4, g5, g6]
    for i in tesk:
        t = time()
        items, adjacent_matrix = list_to_adjacent_matrix(load_txt(i))
        h_2, a_2 = hits(adjacent_matrix)
        print('%.8f'%(time() - t))