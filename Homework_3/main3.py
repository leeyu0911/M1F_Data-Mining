# coding=utf-8
from common_func import *
import os
import pandas as pd
import HITS
import PageRank
import SimRank


def main(file_name: Path, is_IBM=False, run_sim=True):
    """
    file_name: 請使用 Path('檔案名稱')，可參考 common_func.py
    """
    if not isinstance(file_name, Path):
        raise 不看說明書的錯誤('\n\n\t\t參數請用 Path 傳遞，參考 common_func.py')

    if is_IBM:
        items, am = list_to_adjacent_matrix(load_IBM_text(file_name))
    else:
        items, am = list_to_adjacent_matrix(load_txt(file_name))

    if not os.path.exists('./result/'):
        os.mkdir('./result')

    print(file_name.stem)
    print(pd.DataFrame(am, index=items, columns=items))

    # HITS
    h_2, a_2 = HITS.hits(am)
    print('Authority:', a_2.reshape(-1), sep='\n')
    print('Hub:', h_2.reshape(-1), sep='\n', end='\n\n')
    np.savetxt('./result/' + file_name.stem + '_HITS_authority.txt', a_2.reshape(1, -1), fmt='%.8f', encoding=None)
    np.savetxt('./result/' + file_name.stem + '_HITS_hub.txt', h_2.reshape(1, -1), fmt='%.8f', encoding=None)

    # PageRank
    r = PageRank.pagerank(am)
    print('PageRank:', r.reshape(-1), sep='\n', end='\n\n')
    np.savetxt('./result/' + file_name.stem + '_PageRank.txt', r.reshape(1, -1), fmt='%.8f')

    # SimRank
    if run_sim:
        sim = SimRank.simrank(am)
        print('SimRank:', sim, sep='\n', end='\n\n')
        np.savetxt('./result/' + file_name.stem + '_SimRank.txt', sim, fmt='%.8f')


if __name__ == '__main__':
    from time import time
    '''
    請使用 Path('檔案名稱') 可參考 common_func.py
    '''
    # main('./hw3dataset/graph_1.txt')
    t = time()
    main(g1)
    main(g2)
    main(g3)
    main(g4)
    main(g5)
    main(g6, run_sim=False)
    main(t1)
    main(i1, is_IBM=True, run_sim=False)
    print(time() - t, 's')


