# This file was *autogenerated* from the file rs.sage.
from sage.all_cmdline import *   # import sage library
_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_7 = Integer(7); _sage_const_6 = Integer(6); _sage_const_5 = Integer(5); _sage_const_4 = Integer(4); _sage_const_8 = Integer(8)
m = _sage_const_3 
q = _sage_const_2 **m
n = q - _sage_const_1 
k = _sage_const_5 

G = GF(q, names=('a',)); (a,) = G._first_ngens(1)
P = G['x']

alphas = [a**i for i in range(n)]
number = [_sage_const_0 , _sage_const_1 , _sage_const_2 , _sage_const_4 , _sage_const_3 , _sage_const_6 , _sage_const_7 , _sage_const_5 ]

Gmap = dict(zip(number, [_sage_const_0 ] + alphas))
Gmapr = dict(zip([_sage_const_0 ] + alphas, number))

print Gmap
print Gmapr

def dump(x):
    print [Gmapr[i] for i in x]

def rs_encode(msg):
    Pmsg = P([Gmap[i] for i in msg])
    return [Pmsg(i) for i in alphas]

msg = [_sage_const_5 ,_sage_const_2 ,_sage_const_0 ,_sage_const_1 ,_sage_const_3 ]
dump(P([Gmap[i] for i in msg]))

codeword = rs_encode(msg)
dump(codeword)

import sagelib
zero, one, two = Gmap[_sage_const_0 ], Gmap[_sage_const_1 ], Gmap[_sage_const_2 ]
points = [(zero, zero, _sage_const_1 ), (one, one, _sage_const_1 ), (two, two, _sage_const_2 )]

k = _sage_const_5 
weight_y = k - _sage_const_1 
Cost = sum([m * (m + _sage_const_1 ) / _sage_const_2  for x, y, m in points])
max_deg_y = int((_sage_const_1  + math.sqrt(_sage_const_1  + _sage_const_8  * Cost / weight_y)) / _sage_const_2 ) - _sage_const_1  

print weight_y, Cost, max_deg_y

mons = sagelib.kv.gs_monomial_list(_sage_const_5 , _sage_const_1 , _sage_const_4 )
#print mons

M = list(sagelib.kv.gs_interpol_matrix_by_mons(points, mons))
for i in M:
    print "\n", i
    dump(i)


