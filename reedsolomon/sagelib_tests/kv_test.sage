#developing...

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

# ==== Encode a message = [5,2,0] ====
msg = map(lambda i: Gmap[i], [5, 2, 0])

Pmsg = P(msg)
print "msg polynomial:", Pmsg

codeword = [Pmsg(i) for i in alphas]
print 'codeword send:', codeword

#break sth in codeword (channel noise)
codeword[3] = 0

print 'codeword recv:', codeword

tau = 3
s, l = sagelib.gs_minimal_list(n, k, tau)
print s, l

points = zip(alphas, codeword)

wy = k - 1
Q = sagelib.kv.gs_construct_Q(points, tau, s, l, wy)
print Q

Pmsg_list = sagelib.factor_bivariate_linear(Q)
print 'decoded list of polynomials:', Pmsg_list

#transform to get the original data sent~
for p in Pmsg_list:
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    print 'original msg:', m + [0] * (k - len(m))
