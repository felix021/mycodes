#!/usr/bin/python

"""

This snippet of code generates an q*n matrix R, where R[i][j] denotes 
the posibility of Pr(X = X[i] | Y = Y[j]), namely, the posibility of 
'X[i] is the symbol sent if Y[j] is the symbol received'.

"""

import sys
import random
from matlab import transpose

n = 63
k = 4

#in each column, there will be at least one entry with the
lowest_posibility = 0.4

#the posibilities is divided into
nshare = 10000

q = n + 1

R = []

for i in range(n):
    x = [random.randint(int(lowest_posibility*nshare), nshare)]
    left = nshare - x[0]
    nloop = q - 1
    while nloop > 0 and left > 0:
        r = random.randint(0, left)
        nloop -= 1
        x.append(r if nloop > 0 else left)
        left -= r
    x += [0] * nloop
    x = map(lambda x: float(x) / nshare, x)
    random.shuffle(x)
    R.append(x)

R = map(list, zip(*R))

s = '\n'.join(map(lambda i: '\t'.join(map(lambda i: '%.4f' % i, i)), R))
print 'Raw:\n' + s + '\n'

s = '[' + ',\n'.join('[' + i + ']' for i in map(lambda i: ','.join(map(lambda i: '%.4f' % i, i)), R)) + ']'
print 'Python:\n' + s + '\n'

s = '[' + ';\n'.join(map(lambda i: ' '.join(map(lambda i: '%.4f' % i, i)), R)) + ']'
print 'Matlab:\n' + s

