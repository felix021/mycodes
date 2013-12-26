m = 3
q = 2^m
n = q - 1
k = 5

G.<a> = GF(q)
P = G['x']

alphas = [a^i for i in range(n)]
number = [0, 1, 2, 4, 3, 6, 7, 5]

Gmap = dict(zip(number, [0] + alphas))
Gmapr = dict(zip([0] + alphas, number))

print Gmap
print Gmapr

def dump(x):
    print [Gmapr[i] for i in x]

def rs_encode(msg):
    Pmsg = P([Gmap[i] for i in msg])
    return [Pmsg(i) for i in alphas]

msg = [5,2,0,1,3]
dump(P([Gmap[i] for i in msg]))

codeword = rs_encode(msg)
dump(codeword)

import sagelib
zero, one, two = Gmap[0], Gmap[1], Gmap[2]
points = [(zero, zero, 1), (one, one, 1), (two, two, 2)]

k = 5
weight_y = k - 1
Cost = sum([m * (m + 1) / 2 for x, y, m in points])
max_deg_y = int((1 + math.sqrt(1 + 8 * Cost / weight_y)) / 2) - 1 

print weight_y, Cost, max_deg_y

mons = sagelib.kv.gs_monomial_list(5, 1, 4)
#print mons

M = list(sagelib.kv.gs_interpol_matrix_by_mons(points, mons))
for i in M:
    print "\n", i
    dump(i)


