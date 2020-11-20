import pandas as pd
import numpy as np
from config import *


np.random.seed(random_seed)
columns = ['CPU', 'RAM', 'GPU', 'SSD'] + [chr(s) for s in range(ord('A'), ord('Z') + 1)]
dataset = np.array([np.random.randint(0, 10, 30, np.int8) for _ in range(data_size)])

# 標注資料
target = np.zeros(data_size, np.int8)
c = 0
for i, dd in enumerate(dataset):
    cool_computer = [d for d in dd[:4] if d >= threshold]
    if len(cool_computer) >= 4:
        target[i] = 1
        c += 1

# for i in dataset[target == 1]:
#     print(i)

df = pd.DataFrame(dataset, columns=columns)
df['target'] = target

df.to_csv(file_name)

