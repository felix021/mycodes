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
G.<a> = GF(n + 1)

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

#rs encoder in sagelib
rs = sagelib.rs.GRS(G, n, k, alphas)        

#codeword to be sent: 
#   (a^2 + 1, a + 1, a^2 + 1, a^2 + 1, a, a^2 + a, a^2 + a + 1)
#   it's just the same as: codeword = [Pmsg(i) for i in alphas]
#   the latter is much faster, actually...
codeword = rs.encode(Pmsg)

# ==== Guruswami-Sudan algorithm ====

#choose tau
tau = 0
s, l = sagelib.gs_params(n, k, tau) #(2, 3)

points = zip(alphas, codeword)
"""
[
    (1, a^2 + 1),
    (a, a + 1),
    (a^2, a^2 + 1),
    (a + 1, a^2 + 1),
    (a^2 + a, a),
    (a^2 + a + 1, a^2 + a),
    (a^2 + 1, a^2 + a + 1)
]
"""

wy = k - 1 #(1, k-1)-degree?
Q = sagelib.gs_construct_Q(points, tau, (s, l), wy)
#the horibble Q(x, y) = (a^2)*x^13 + (a^2)*x^12 + (a^2 + a)*x^11 + (a^2 + a)*x^10 + (a^2)*x^9*y + (a)*x^9 + (a)*x^8*y + (a + 1)*x^8 + (a^2)*x^7*y + (a^2)*x^7 + (a)*x^6*y + (a + 1)*x^5*y^2 + (a)*x^4*y^2 + (a + 1)*x^3*y^2 + x^4 + (a^2 + a + 1)*x^3*y + (a^2 + a)*x^2*y^2 + (a + 1)*x*y^3 + (a^2 + a + 1)*x^3 + (a + 1)*x^2*y + (a^2 + 1)*x*y^2 + (a)*y^3 + (a^2 + 1)*x^2 + x*y + (a + 1)*y^2 + (a^2 + a + 1)*x + (a)*y + (a^2)

Pmsg_list = sagelib.factor_bivariate_linear(Q)
#returned: [(a + 1)*x^4 + x^3 + a*x + a^2 + 1]
#It's contains the Pmsg 'sent' before :)

#lets decode to the original data sent~
for p in Pmsg_list:
    m = list(p)
    print map(lambda x: Gmapr[x], m)

#Output: [5, 2, 0, 1, 3]
