#This is an example to use kv.sage
#
#The PI example used is copied from:
#   http://www.comm.csl.uiuc.edu/~koetter/publications/gkkg_jvlsisp.pdf (Page.7)
#

import sagelib

import sys

if len(sys.argv) < 2:
    print 'usage: %s filename' % sys.argv[0]
    sys.exit(1)

f = open(sys.argv[1])

q, k = map(int, f.next().strip().split())
n = q - 1

PI = []
for i in range(q):
    PI.append(map(float, f.next().strip().split()))
    print PI[i]

Lambda = float(f.next())

f.close()
#========

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

def rs_encode(Pmsg):
    return [Pmsg(i) for i in alphas]

# ==== message ====
Pmsg = P(a + a^4*x + a^4 * x^2 + a^3*x^3 + x^4)
print "msg polynomial:", Pmsg

msg = map(lambda i: Gmap[i], [2,6,6,3,1])
print "msg:", msg
print "msg polynomial':", P(msg) #same with the previous one

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
print Q

Pmsg_list = sagelib.factor_bivariate_linear(Q, weight_y)
print 'decoded list of polynomials:', Pmsg_list

#transform to get the original data sent~
print '\n\nResult:\n'

for p in Pmsg_list:
    m = map(lambda x: Gmapr[x], p)
    #zero padding at the rear end
    print 'original msg:', m + [0] * (k - len(m))

    cw = rs_encode(p)
    possibility = 0.0
    for i, x in enumerate(cw):
        possibility += float(PI[Gmapr[x]][i])
    print 'possibility:', possibility
