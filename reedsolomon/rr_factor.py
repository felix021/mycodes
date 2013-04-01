import sys

from GF import GF
from matlab import *
from copy import copy
from hasse import hasse_deriv1
from poly import *

"""

This is copied from the codes downloaded from:
    http://en.pudn.com/downloads54/sourcecode/math/detail187807_en.html

In the  4 tests listed in the __main__ section, this function behaves exactly
as the rr_factor.m and rr_dfs.m, except for the TODO denoted, where this code
won't add a 0 to at the begining of the result.

"""

_debug = False

def rr_factor(Q, D, m):
    p = [-1]
    deg = [-1]
    t = 1
    u = 0
    coeff = GF([0], m)
    f = GF([], m)

    if len(Q) == 1:
        for r in poly(Q[0], reverse = True).roots():
            f.append([r])
        #[[0]] + f ?
        return f

    else:
        t, p, deg, coeff, f = rr_dfs(Q, D, u, t, p, deg, coeff, f, m)
        adjust_answers(f, m)
        return f

def adjust_answers(f, m):
    if f:
        maxlen = max(map(len, f))
        a = GF(0, m)
        for i in f:
            i += [a] * (maxlen - len(i))

def rr_dfs(Qu, D, u, t, p, deg, coeff, f, m):

    global _debug

    if _debug:
        print "Qu = \n"
        for i in Qu: print i
        print "D = %d, u = %d, t = %d, m = %d" % (D, u, t, m)
        print "p = ", p
        print "deg = ", deg
        print "coeff =", coeff
        print "f = ", f

    n_zero = reduce(lambda x, y: x + y, map(lambda x: x[0] == 0, Qu), 0)
    #print 'n_zero =', n_zero, ', len =', len(Qu)
    if n_zero == len(Qu):
        fnew = GF([0] * (deg[u] + 1), m)
        w = u;
        #print 'w =', w
        while w != 0:
            #print 'w =', w
            fnew[deg[w]] = \
                    fnew[deg[w]] + \
                    coeff[w]
            w = p[w]
        #print 'fnew =', fnew

        #print f
        f.append(fnew)
        #print f

    elif deg[u] < D:
        Qu0 = copy(Qu[0])
        Qu0.reverse()
        if _debug: print 'Qu0 =\n', Qu0
        R = poly_roots(Qu0)
        if _debug: print 'R =', R
        for i in range(len(R)):
            a = R[i]
            v = t
            t = t + 1

            if _debug: print 'i = %d, v = %d, t = %d' % (i, v, t), a

            
            """
            p[v]= u
            deg[v] = deg[u] + 1
            coeff[v] = a
            """
            p.append(u)
            deg.append(deg[u] + 1)
            coeff.append(a)

            Qv = GF(zeros(len(Qu) * 2 - 1, len(Qu)), m)
            for r in range(len(Qu)):
                gr_y = copy(Qu[r])
                #print 'gr_y =', gr_y
                for s in range(len(Qv[0])):
                    Qv[r + s][s] = hasse_deriv1(gr_y, a, s, m)
                    if _debug and r + s == 1 and s == 0:
                        print "INPUT:", gr_y, a, s, m
                        print "OUTPUT:", Qv[r+s][s]

            if _debug:
                for i in Qv: print i

            if len(Qv) > 1:
                while sum([1 for x in Qv[0] if x != 0]) == 0:
                    Qv = Qv[1:]

                n_row, n_col = len(Qv), len(Qv[0])
                maxi, maxj = 0, 0
                for i in range(n_row):
                    for j in range(n_col):
                        if Qv[i][j] != 0:
                            maxi = max(maxi, i)
                            maxj = max(maxj, j)

                Qv_new = []
                for i in range(maxi + 1):
                    #if sum([1 for j in range(maxj+1) if Qv[i][j] != 0]) > 0:
                    Qv_new.append(Qv[i][:maxj+1])
                Qv = Qv_new

            if _debug: 
                for i in Qv: print i
                sys.stdin.readline()

            t, p, deg, coeff, f = rr_dfs(Qv, D, v, t, p, deg, coeff, f, m)

            if _debug: print 'f=',f
        #endif

    return (t, p, deg, coeff, f)

if __name__ == "__main__":
    from GF import GF, set_debug
    set_debug(True)

    #_debug = True

    #"""

    Q = GF([
        [0 , 5 , 3],
        [7 , 7 , 6],
        [7 , 4 , 0],
        [1 , 3 , 0],
        [6 , 2 , 0],
        [5 , 6 , 0],
        [7 , 0 , 0],
        [1 , 0 , 0],
        [3 , 0 , 0],
    ], 3) 
    assert(rr_factor(Q, 6, 3) == [[0, 5, 6, 6, 1], [3, 7, 7, 5, 0]])
    
    Q = GF([
        [6,3],
        [3,3],
        [7,6],
        [4,6],
        [0,1],
        [0,1],
        [3,6],
        [0,6],
        [1,3],
        [4,3],
        [4,0],
        [3,0],
        [2,0],
        [5,0],
        ], 3)
    assert(rr_factor(Q, 6, 3) == [[2,3,3,4,3]])

    Q = GF([
        [6 , 7 , 2],
        [0 , 6 , 1],
        [0 , 1 , 2],
        [4 , 4 , 1],
        [0 , 4 , 7],
        [1 , 4 , 6],
        [0 , 4 , 0],
        [6 , 3 , 0],
        [2 , 2 , 0],
        [5 , 5 , 0],
        [3 , 0 , 0],
        [2 , 0 , 0],
        [6 , 0 , 0],
    ], 3) 
    assert(rr_factor(Q, 6, 3) == [[2, 7, 7, 7, 0], [4, 7, 4, 2, 4]])

    Q = GF([
        [0 ,0 ,2 ,7], 
        [0 ,0 ,7 ,5], 
        [5 ,3 ,5 ,0], 
        [3 ,6 ,0 ,0], 
        [2 ,5 ,7 ,0], 
        [5 ,1 ,0 ,0], 
        [6 ,5 ,0 ,0], 
        [5 ,1 ,0 ,0], 
        [6 ,7 ,0 ,0], 
        [7 ,5 ,0 ,0], 
        [0 ,0 ,0 ,0], 
        [0 ,0 ,0 ,0], 
        [7 ,0 ,0 ,0], 
    ], 3) 
    #_debug = True
    assert(rr_factor(Q, 6, 3) == [[0, 5, 6, 6, 1]] * 32 + [[3, 7, 7, 5, 0]])
    
    Q = GF([[0, 5, 0, 2]], 3) #[[0,5,5]]
    assert(rr_factor(Q, 6, 3) == [[0],[5],[5]])

    assert(rr_factor(GF([[6,7,2]], 3), 6, 3) == [[2],[4]])

    print 'all test passed'
