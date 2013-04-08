import GF
from matlab import *
from copy import copy
from scipy.misc import comb as nchoosek
import math

"""
This code calculate the hasse derivation of a f(x).

This is copied from the code 'hasse_deriv1.m' downloaded from:
    http://en.pudn.com/downloads54/sourcecode/math/detail187807_en.html
"""

def hasse_deriv1(g, x, r, m):
    val = GF.GF(0, m)
    for i in range(r, len(g)):
        binom = nchoosek(i, r)
        tmp = (binom - 2 * math.floor(binom / 2))
        if abs(tmp - 1) < 1e-8:
            val = val + g[i] * (x**(i - r))
    return val

if __name__ == "__main__":
    g = GF.GF([0, 5, 3], 3)
    x = GF.GF(0, 3)
    r = 0
    m = 3
    assert(hasse_deriv1(g, x, r, m) == 0)
   

    g = GF.GF([3, 3, 7, 7], 3)
    a = GF.GF(5, 3)
    r = 1
    m = 3
    assert(hasse_deriv1(g, a, r, m) == 0)

    g = GF.GF([7, 7, 6], 3)
    a = GF.GF(0, 3)
    r = 0
    m = 3
    assert(hasse_deriv1(g, a, r, m) == 7)

    print 'all test passed'
