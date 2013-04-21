#evaluation encoding

from GF import *
from poly import *

m = 3
q = 2**m
n = q - 1
k = 5

#print m, q, n, k
#print map(str, GF(range(q), m, GF_EXP))

alphas = GF(range(n), m, GF_EXP)

def P(msg):
    return poly(msg, m, reverse=True)

def dump(msg):
    print msg

def rs_encode(msg):
    p = P(msg)
    return [p.eval(i) for i in alphas]


msg = [5,2,0,1,3]
dump(msg)
codeword = rs_encode(msg)
dump(codeword)

