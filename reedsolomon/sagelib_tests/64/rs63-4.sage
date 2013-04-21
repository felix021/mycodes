import sagelib

n = 63
k = 4
q = n + 1

G.<a> = GF(q)
alphas = [a^i for i in range(n)]
Gmap  = {}
Gmapr = {}
for i in range(q):
    binary = map(int, bin(i)[2:])
    binary.reverse()
    alpha = G(binary)
    Gmap[i] = alpha
    Gmapr[alpha] = i
P = G['x']

cw = [0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8, 0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8, 0, 27, 46, 7, 35, 52, 58, 17, 37, 4, 59, 25, 62, 49, 18, 61, 41, 63, 57, 9, 8]

codeword = [Gmap[i] for i in cw]
print 'codeword send:', codeword

#break sth in codeword (channel noise)
err = 15
codeword[err:] = [0] * (n - err)

print 'codeword recv:', codeword

"""
points = zip(alphas, codeword)

tau = 1
s, l = sagelib.gs_minimal_list(n, k, tau)
print 's,l:', s, l

#Guruswami Sudan
wy = k - 1 #(1, k - 1)-degree?
Q = sagelib.gs_construct_Q(points, tau, (s, l), wy)

Pmsg_list = sagelib.factor_bivariate_linear(Q, wy)
print 'decoded list of polynomials:', Pmsg_list
"""

#Koetter Vardy
points = zip(alphas, codeword, [2] * n)
Cost = sum([m * (m + 1) / 2 for x,y,m in points])

weight_y = k - 1

max_deg_y = floor((1 + sqrt(1 + 8 * Cost / weight_y)) / 2) - 1
Q = sagelib.kv.gs_construct_Q(points, max_deg_y, weight_y)

Pmsg_list = sagelib.factor_bivariate_linear(Q, weight_y)
print 'decoded list of polynomials:', Pmsg_list
#end of kv


#transform to get the original data sent~
for p in Pmsg_list:
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    print 'original msg:', m + [0] * (k - len(m))
