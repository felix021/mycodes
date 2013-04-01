"""

This is an implementation of polynomials over GF(2^m)

"""

from copy import copy
from GF import *

class poly(object):
    """
        poly([1 2 3], 3) means x^2 + 2x + 3 over Galois Field(2^3)
            while poly([1, 2, 3], reverse = True) means 3x^2+2x+1

    """
    def __init__(self, coeff, m = 0, reverse = False):
        self.coeff = copy(coeff)
        if reverse:
            self.coeff.reverse()
        if m > 0:
            self.coeff = GF(self.coeff, m)

    def trim(self):
        self.coeff = poly_trim_leading_zeros(self.coeff)

    @staticmethod
    def xval(x):
        if isinstance(x, poly):
            return x.coeff
        return x

    def eval(self, x):
        return poly_eval(self.coeff, x)

    def __eq__(self, x):
        x = poly.xval(x)
        return self.coeff == x or \
            poly_trim_leading_zeros(self.coeff) == poly_trim_leading_zeros(x)

    def __ne__(self, x):
        return not self.__eq__(x)

    def __add__(self, x):
        return poly(poly_add(self.coeff, poly.xval(x)))

    def __sub__(self, x):
        return poly(poly_sub(self.coeff, poly.xval(x)))

    def __mul__(self, x):
        return poly(poly_mul(self.coeff, poly.xval(x)))

    def __div__(self, x):
        return poly(poly_div(self.coeff, poly.xval(x)))

    def __mod__(self, x):
        q, r = poly_div(self.coeff, poly.xval(x), need_remainder = True)
        return poly(r)

    def __radd__(self, x):
        return self.__add__(x)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __rsub__(self, x):
        return poly(poly_sub(poly.xval(x), self.coeff))

    def __rdiv__(self, x):
        return poly(poly_div(poly.xval(x), self.coeff))

    def __rmod__(self, x):
        q, r = poly_div(poly.xval(x), self.coeff, need_remainder = True)
        return poly(r)

    def __pow__(self, x):
        if x == 0:
            return poly([0])
        coeff = copy(self.coeff)
        for i in range(1, x):
            coeff = poly_mul(coeff, self.coeff)
        return poly(coeff)

    def roots(self):
        return poly_roots(self.coeff)

    def __str__(self):
        return str(self.coeff)

    def __repr__(self):
        return repr(self.coeff)

    def __hash__(self):
        return hash(self.coeff)

def poly_scale(p, x):
    return [p[i] * x for i in range(0, len(p))]

def poly_add(p, q):
    r = [0] * max(len(p), len(q))
    for i in range(0, len(p)):
        r[i + len(r) - len(p)] = p[i]
    for i in range(0, len(q)):
        r[i + len(r) - len(q)] += q[i]
    return r

def poly_sub(p, q):
    return poly_add(p, q)

def poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j in range(0, len(q)):
        for i in range(0, len(p)):
            r[i + j] += p[i] * q[j]
    return r

def poly_eval(p, x):
    y = p[0]
    for i in range(1, len(p)):
        y = x * y + p[i]
    return y

def poly_trim_leading_zeros(p):
    for i in range(len(p)):
        if p[i] != 0:
            return p[i:]
    return []

def poly_div(p, q, need_remainder = False):
    if len(q) == 0 or len(q) == 1 and q[0] == 0:
        raise ZeroDivisionError('q = ' + str(q))
    if len(p) < len(q):
        return [GF(0, 3)]

    p = copy(p)

    ans = []
    for i in range(0, len(p) - len(q) + 1):
        x = p[i] / q[0]
        ans.append(x)
        if x == 0:
            continue
        for j in range(len(q)):
            p[i + j] = p[i + j] - q[j] * x

    #remainder is not trimed, as in matlab
    #remainder = poly_trim_leading_zeros(p)
    if need_remainder:
        return ans, p
    return ans

def poly_roots_uniq(poly):
    ret = []
    if len(poly) == 0:
        return ret
    op = poly[0].op
    for i in GF(range(op.n + 1), op.m):
        if poly_eval(poly, i) == 0:
            ret.append(i)
    return ret

def poly_roots(x):
    ans = []

    x = poly_trim_leading_zeros(x)
    if len(x) == 0:
        return ans

    m = x[0].m
    one = GFobj(1, m)
    zero = GFobj(0, m)

    start = 0
    """ #this segment is for performance improvement, not necessary, though
    x.reverse()
    for i in range(len(x)):
        if x[i] != zero:
            x = x[i:]
            x.reverse()
            break
        ans.append(zero)
    start = 1
    """

    for i in GF(range(start, 2**m), m):
        factor = [GF(1, m), i]
        while poly_eval(x, i) == 0: #multiple root
            ans.append(i)
            x = poly_div(x, factor)
    return ans


if __name__ == "__main__":
    #"""
    #poly_add/sub test
    assert(poly([1,2,3,4,5],3) + poly([5,4,3,2,1],3) == GF([4,6,0,6,4],3))
    assert(poly([1,2,3,4],3) + GF([5,4,3,2,1],3) == GF([5,5,1,1,5],3))
    assert(GF([1,2,3,4,5],3) + poly([4,3,2,1],3) == GF([1,6,0,6,4],3))
    assert(poly([1,2,3,4,5],3) - poly([5,4,3,2,1],3) == GF([4,6,0,6,4],3))
    assert(poly([1,2,3,4],3) - GF([5,4,3,2,1],3) == GF([5,5,1,1,5],3))
    assert(GF([1,2,3,4,5],3) - poly([4,3,2,1],3) == GF([1,6,0,6,4],3))
    print 'poly_add/sub test ok'

    #"""
    #poly_mul/poly_eval/poly_div test
    assert(poly([3,0,4,2,5], 3).eval(1) == 0)
    assert(poly([5,2,4,0,3], 3, reverse=True).eval(1) == 0)
    assert(poly([3,0,4,2,5], 3).eval(5) == 0)

    assert(poly([1,0,2], 3) * poly([6,2,4],3) == GF([6,2,3,4,3],3))
    assert(poly([1,0,2], 4) * GF([6,2,4],4) == GF([6,2,8,4,8],4))
    assert(GF([1,0,2],3) * poly([6,2,4],3)== GF([6,2,3,4,3],3))

    assert(poly(GF([0], 3)) / poly(GF([1, 0, 2], 3)) == GF([0], 3))
    assert(poly(GF([0], 3)) / GF([1, 0, 2], 3) == GF([0], 3))
    assert(GF([0], 3) / poly(GF([1, 0, 2], 3)) == GF([0], 3))
    try:
        print poly(GF([0], 3)) / GF([0], 3)
        print 'ZeroDivisionError not catched'
    except:
        pass
    assert(poly(GF([6,2,3,3,6], 3)) / GF([1,0,2],3) == GF([6,2,4], 3))
    assert(poly(GF([6,2,3,3,6], 3)) % GF([1,0,2],3) == GF([7,5],3))
    assert(poly(GF([6,2,3,3,6], 4)) / GF([2,0,2],4) == GF([3,1,11], 4))
    assert(poly(GF([6,2,3,3,6], 4)) % GF([2,0,2],4) == GF([1,3],4))
    print 'poly_eval/mul/div test ok'
    #"""

    #"""
    #poly_roots test
    assert(poly(GF([0,1,2,3,0,4,0,0], 3)).roots() == GF([0, 0, 7], 3))
    assert(poly(GF([2, 0, 5, 0, 0], 3)).roots() == GF([0,0,5,5],3))
    assert(poly(GF([0, 2, 7, 6, 0], 4)).roots() == GF([0, 2, 8], 4))
    print 'poly_roots test ok'
    #"""

    """
    #msg = GF([5, 2, 2, 2, 2], 3)
    msg = GF([2, 0, 1], 3)
    c = [poly_eval(msg, i) for i in GF(range(7), 3, GF_EXP)]
    print map(str, c)
    print 'value:', map(GFobj.val, c)
    print 'expon:', map(lambda x: get_gf_op(3).log[x.value], c)
    # ['a^0=1', 'a^0=1', 'a^0=1', 'a^1=2', 'a^5=7', 'a^0=0', 'a^0=1']
    #value: [1, 1, 1, 2, 7, 0, 1]
    #expon: ['a^0', 'a^0', 'a^0', 'a^1', 'a^5', 'a^0', 'a^0']
    #"""
