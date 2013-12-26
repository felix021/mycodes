#This is an example to use kv.sage
#
#The PI example used is copied from:
#   http://www.comm.csl.uiuc.edu/~koetter/publications/gkkg_jvlsisp.pdf (Page.7)
#

import sagelib

n = 7
k = 5

q = n + 1

#========

G.<a> = GF(q)
P = G['x']
alphas = [a^i for i in range(n)]
Gmap  = {}
Gmapr = {}
for i in range(8):
    binary = map(int, bin(i)[2:])
    binary.reverse()
    alpha = G(binary)
    Gmap[i] = alpha
    Gmapr[alpha] = i

def rs_encode(Pmsg):
    return [Pmsg(i) for i in alphas]

# ==== message ====
Pmsg = P(a + a^4*x + a^4 * x^2 + a^3*x^3 + x^4)
print "msg polynomial:", Pmsg

msg = map(lambda i: Gmap[i], [2,6,6,3,1])
print "msg:", msg
print "msg polynomial':", P(msg) #same with the previous one

print "codeword:", rs_encode(Pmsg);

# ==== Probabilities ====
PI = \
[
    [0.959796, 0.214170, 0.005453, 0.461070, 0.001125, 0.000505, 0.691729],
    [0.001749, 0.005760, 0.000000, 0.525038, 0.897551, 0.025948, 0.000209],
    [0.028559, 0.005205, 0.000148, 0.003293, 0.000126, 0.018571, 0.020798],
    [0.000052, 0.000140, 0.000000, 0.003750, 0.100855, 0.954880, 0.000006],
    [0.009543, 0.736533, 0.968097, 0.003180, 0.000000, 0.000000, 0.278789],
    [0.000017, 0.019810, 0.000006, 0.003621, 0.000307, 0.000003, 0.000084],
    [0.000284, 0.017900, 0.026295, 0.000023, 0.000000, 0.000002, 0.008382],
    [0.000001, 0.000481, 0.000000, 0.000026, 0.000035, 0.000092, 0.000003],
]

Lambda = 2.50 #the article uses s=12 to iterate, which can be replaced by floor(Lambda * PI)

received = []
for i in range(n):
    maxi = 0
    for j in range(q):
        if PI[j][i] > PI[j][maxi]:
            maxi = i
    received.append(a^(maxi-1) if maxi > 0 else 0)
print 'received:', received


print 'M ='
M = []
for i in range(q):
    M.append([0] * n)
    for j in range(n):
        M[i][j] = floor(PI[i][j] * Lambda)
    print M[i]

#points with multiplicity > 0
Cost = 0
points = []
for j in range(n):
    for i in range(q):
        if M[i][j] > 0:
            mij = M[i][j]
            Cost += mij * (mij + 1) / 2
            points.append((a^j, a^(i-1) if i > 0 else 0, mij))

print 'Cost:', Cost
print 'points:', points

weight_y = k - 1

max_deg_y = floor((1 + sqrt(1 + 8 * Cost / weight_y)) / 2) - 1

Q = sagelib.kv.gs_construct_Q(points, max_deg_y, weight_y)

Pmsg_list = sagelib.factor_bivariate_linear(Q, weight_y)
#print 'decoded list of polynomials:', Pmsg_list

def rs_poly2msg(p):
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    return m + [0] * (k - len(m))

def prod(x): #how to cope with zero entries?
    x = map(lambda t: t if t > 0 else 0.00001, x)
    return reduce(lambda x, y: x * y, x, 1)

#which one is better? (calculate the possibility of codeword according to PI)

maxp = None
maxPr = 0
for p in Pmsg_list:
    cw = rs_encode(p)

    print '\npoly:', p
    print 'msg: ', rs_poly2msg(p)
    print 'cw:  ', cw

    Pr = []
    for i, mon in enumerate(cw):
        Pr.append(float(PI[Gmapr[mon]][i]))
    print 'posibility:', Pr, '=', prod(Pr), prod(Pr)

    #sum seems not the way to calculate possibility
    if prod(Pr) > maxPr:
        maxPr = prod(Pr)
        maxp = p

print '\nfinal result:', maxp

