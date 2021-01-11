# V(i+1) = α * M * V(i) + (1−α) * V(i)
# https://blog.csdn.net/John_xyz/article/details/78915097
from common_func import *


def pagerank(am, d=0.15, iters=10000, error=1e-8):
    # items, am = list_to_adjacent_matrix(load_txt(file_name))
    n = len(am)
    for i in range(len(am)):
        if sum(am[i]) != 0:
            am[i] /= sum(am[i])

    v_0 = np.ones((n, 1)) / n
    # v_0 = np.random.random((n, 1))
    for i in range(iters):
        v = (1 - d) * am.transpose().dot(v_0) + d * v_0
        err = sum(abs(v - v_0))

        if err < error:
            break
        v_0 = v
    print('PageRank iter次數:', i, ', error <=', err[0])
    return v


if __name__ == '__main__':
    print('g1')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g1))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [5.54209455e-18 6.33646144e-16 3.44465808e-14 1.18408636e-12 2.88712443e-11 5.30931709e-10]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig1))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [0.38277512 0.07655502 0.11483254 0.13397129 0.14354067 0.14832536]

    print('g2')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g2))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [0.2 0.2 0.2 0.2 0.2]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig2))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [0.39506173 0.09876543 0.14814815 0.17283951 0.18518518]

    print('g3')
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(g3))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [0.16666667 0.33333333 0.33333333 0.16666667]
    items, adjacent_matrix = list_to_adjacent_matrix(load_txt(ig3))
    r = pagerank(adjacent_matrix)
    print(r.reshape(-1))
    # [0.3 0.2 0.3 0.2]


    from time import time
    print()
    tesk = [g1, g2, g3, g4, g5, g6]
    tt = time()
    for i in tesk:
        t = time()
        items, adjacent_matrix = list_to_adjacent_matrix(load_txt(i))
        s = pagerank(adjacent_matrix)
        print('%.8f' % (time() - t))
    print('%.8f' % (time() - tt))

