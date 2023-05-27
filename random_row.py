import sys
import numpy as np

e = [(2, 0, 0), (-1, 0, 0), (0, 2, 0), (0, -1, 0), (0, 0, 2), (0, 0, -1), (0, 0, 0)]
p = [0.15, 0.05, 0.1, 0.1, 0.1, 0.1, 0.4]
for i in range(200):
    j = np.random.choice(7, p=p)
    print(*e[j])
    #print(e[j][0] * np.random.rand(), e[j][1] * np.random.rand(), e[j][2] * np.random.rand())