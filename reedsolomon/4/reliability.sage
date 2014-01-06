#!/usr/bin/python

"""

This snippet of code generates an q*n matrix R, where R[i][j] denotes 
the posibility of Pr(X = X[i] | Y = Y[j]), namely, the posibility of 
'X[i] is the symbol sent if Y[j] is the symbol received'.

"""

import sys
import random

n = 63
q = n + 1
k = 4

G.<a> = GF(q)
P = G['x']
alphas = [a^i for i in range(n)]
Gmap  = {}
Gmapr = {}
for i in range(q):
    binary = map(int, bin(i)[2:])
    binary.reverse()
    alpha = G(binary)
    Gmap[i] = alpha
    Gmapr[alpha] = i

alphasr = {0: 0}
for i,x in enumerate(alphas): alphasr[x] = i + 1

def rs_encode(Pmsg):
    return [Pmsg(i) for i in alphas]

msg = [3,20,44,15]
Gmsg = map(lambda i: Gmap[i], msg)
Pmsg = P(Gmsg)
cw = rs_encode(Pmsg)

idx = [alphasr[i] for i in cw]
print >>sys.stderr, idx

#introduce some error:
for i in range(60):
    pos = randint(0, 62)
    idx[pos] = randint(0, 63)

print >>sys.stderr, idx

#in each column, there will be at least one entry with the
lowest_posibility = 0.4

#the posibilities is divided into
nshare = 10000

q = n + 1

R = []

for i in range(n):
    t = random.randint(int(lowest_posibility*nshare), nshare)
    x = []
    left = nshare - t
    nloop = q - 1
    while nloop > 0 and left > 0:
        r = random.randint(0, left)
        nloop -= 1
        x.append(r if nloop > 0 else left)
        left -= r
    x += [0] * nloop
    x = map(lambda x: float(x) / nshare, x)
    random.shuffle(x)
    pos = idx[i]
    #x[0], x[idx[i]] = x[idx[i]], x[0]
    R.append(x[:pos] + [float(t) / nshare] + x[pos:])

R = map(list, zip(*R))

s = '\n'.join(map(lambda i: '\t'.join(map(lambda i: '%.4f' % i, i)), R))
print '%d %d\n%s\n%f\n' % (q, k, s, 2.5)
