"""
This is an example to use sagelib (https://bitbucket.org/jsrn/sagelib).

These codes should run in the sage CLI interface, not as standalone 
python script. It utilized the GS algorithm provided in sagelib to 
decode an encoded codeword.
"""

import sagelib

n = 7
k = 5

q = n + 1

#init a Galois Field on 2^3
#and then 'a' is the prim element of GF(8)
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

# ==== Encode a message = [5,2,0,1,3] ====
msg = map(lambda i: Gmap[i], [5, 2, 0, 1, 3])
#now msg = [a^2 + 1, a, 0, 1, a + 1]

#msg polynomial: (a + 1)*x^4 + x^3 + a*x + a^2 + 1
Pmsg = P(msg)
print "msg polynomial:", Pmsg

#codeword to be sent: 
#   (a^2 + 1, a + 1, a^2 + 1, a^2 + 1, a, a^2 + a, a^2 + a + 1)
#   it's just the same as: 
#       rs = sagelib.rs.GRS(G, n, k, alphas)        
#       codeword = rs.encode(Pmsg)
#   which is much slower, actually...
codeword = [Pmsg(i) for i in alphas]
print 'codeword send:', codeword

#break sth in codeword (channel noise)
codeword[3] = 0

print 'codeword recv:', codeword

# ==== Guruswami-Sudan algorithm ====

#choose 'tau' as the decoding radius of GS
#   It's noted as t in the GS article as the input of 
#   the algorithm, and shouldn't be larger than the
#   max possible radius tmax = (n - 1 - sqrt(n * (k - 1))
#   In the article, max(tau) is calculated from tmax/n
tau = 1
s, l = sagelib.gs_params(n, k, tau) #(2, 3)

points = zip(alphas, codeword)

"""
[
    (1, a^2 + 1
    (a, a + 1
    (a^2, a^2 + 1
    (a + 1, 0
    (a^2 + a, a
    (a^2 + a + 1, a^2 + a
    (a^2 + 1, a^2 + a + 1)
]
"""

wy = k - 1 #(1, k - 1)-degree?
Q = sagelib.gs_construct_Q(points, tau, (s, l), wy)
#Sorry, I won't list the horibble Q(x, y) here ...

Pmsg_list = sagelib.factor_bivariate_linear(Q)
#returned: [(a + 1)*x^4 + x^3 + a*x + a^2 + 1]
#It's contains the Pmsg 'sent' before :)
print 'decoded list of polynomials:', Pmsg_list

#transform to get the original data sent~
for p in Pmsg_list:
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    print 'original msg:', m + [0] * (k - len(m))

#Output: [5, 2, 0, 1, 3]
