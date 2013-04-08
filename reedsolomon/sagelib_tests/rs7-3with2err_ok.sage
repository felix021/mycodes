"""
This is an example to use sagelib (https://bitbucket.org/jsrn/sagelib).

detailed comment is in 'rs7-5with1err_ok.sage'
"""

import sagelib

n = 7
k = 3

q = n + 1

#init a Galois Field on 2^3
G.<a> = GF(q)

#calculate the support vector of GF(8)
alphas = [a^i for i in range(n)]

#calculate map and reverse map from GF(8) to integers
Gmap  = {}
Gmapr = {}
for i in range(8):
    binary = map(int, bin(i)[2:])
    binary.reverse()
    alpha = G(binary)
    Gmap[i] = alpha
    Gmapr[alpha] = i

#P: univariable polynomial class over G
P = G['x']

# ==== Encode a message ====
msg = map(lambda i: Gmap[i], [5, 2, 0])

Pmsg = P(msg)
print "msg polynomial:", Pmsg

codeword = [Pmsg(i) for i in alphas]
print 'codeword send:', codeword

#break sth in codeword (channel noise)
codeword[3] = 0
codeword[4] = 0

print 'codeword recv:', codeword

# ==== Guruswami-Sudan algorithm ====

#choose tau. tau = 3 to run longer and get more result.
tau = 2
s, l = sagelib.gs_minimal_list(n, k, tau)

points = zip(alphas, codeword)

wy = k - 1 #(1, k-1)-degree?
Q = sagelib.gs_construct_Q(points, tau, (s, l), wy)

Pmsg_list = sagelib.factor_bivariate_linear(Q)

for p in Pmsg_list:
    print p
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    print 'original msg:', m + [0] * (k - len(m))
