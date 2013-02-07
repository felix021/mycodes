#!/usr/bin/python

"""
Author: felix021@gmail.com

Date: 2013.04.01

This is a Galois Field (also known as Finit Field) implementation.
It behaves just like matlab's Galois Field related functions.
Actually, the default generator polynomials below are retrived from matlab ;-)

What's more, the `poly_roots` function will generate same result as in matlab.
If you need conv/deconf on polynomials, just use poly_mul/poly_div instead,
as is stated in the matlab's help.

Some of the code is copied from ReedSolo (http://pypi.python.org/pypi/reedsolo),
and ReedSolo copies them from Bobmath's:
    http://en.wikiversity.org/wiki/Reed%E2%80%93Solomon_codes_for_coders
    (this article is strongly recommended if you're a programmer)

"""

from copy import copy

_poly = {
    2: 7,
    8: 11,
    16: 19,
    32: 37,
    64: 67,
    128: 137,
    256: 285,
    512: 529,
    1024: 1033,
    2048: 2053,
    4096: 4179,
    8192: 8219,
    16384: 17475,
    32768: 32771,
    65536: 69643,
}

class GF_op(object):
    def __init__(self, m = 3):
        self.m = m
        self.q = 2 ** m
        self.n = self.q - 1
        self.calc_elements()
        self.alpha = 2

    def calc_elements(self):
        self.exp = [1] * (self.q * 2)
        self.log = [0] * self.q
        self.log[0] = -1
        x = 1
        poly = _poly[self.q]
        for i in range(1, self.n):
            x <<= 1
            if x & self.q:
                x ^= poly
            self.exp[i] = x
            self.log[x] = i
        for i in range(self.n, self.q * 2):
            self.exp[i] = self.exp[i - self.n]

    def __getitem__(self, i):
        return self.exp[i % self.n]

    def add(self, x, y):
        return x ^ y

    def sub(self, x, y):
        return x ^ y

    def mul(self, x, y):
        if x == 0 or y == 0:
            return 0
        return self.exp[self.log[x] + self.log[y]]

    def div(self, x, y):
        if y == 0:
            raise ZeroDivisionError()
        if x == 0:
            return 0
        return self.exp[self.log[x] + self.n - self.log[y]]

def poly_scale(p, x):
    return [p[i] * x for i in range(0, len(p))]

def poly_add(p, q):
    r = [0] * max(len(p), len(q))
    for i in range(0, len(p)):
        r[i + len(r) - len(p)] = p[i]
    for i in range(0, len(q)):
        r[i + len(r) - len(q)] += q[i]
    return r

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

def poly_div(p, q):
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
    if sum([1 for i in x if i != 0]) == 0:
        return ans
    m = x[0].m
    x = copy(x)
    for i in range(2**m):
        d = GF(i, m)
        factor = [GF(1, m), 1 / GF(i, m)]
        while poly_eval(x, d) == 0: #multiple root
            ans.append(d)
            x = poly_div(x, factor)
    return ans

_gf_cache = {}
def get_gf_op(m):
    if m not in _gf_cache:
        _gf_cache[m] = GF_op(m)
    return _gf_cache[m]

class GFobj(object):
    def __init__(self, value, m):
        self.m = m
        self.value = value
        self.op = get_gf_op(m)

    def val(self, x):
        if isinstance(x, GFobj):
            return x.value
        return x

    def __eq__(self, x):
        return self.value == (x.value if isinstance(x, GFobj) else x)

    def __ne__(self, x):
        return not self.__eq__(x)

    def __hash__(self):
        return self.value.__hash__()

    def __add__(self, x):
        return GFobj(self.op.add(self.value, self.val(x)), self.op.m)

    def __sub__(self, x):
        return GFobj(self.op.sub(self.value, self.val(x)), self.op.m)

    def __mul__(self, x):
        return GFobj(self.op.mul(self.value, self.val(x)), self.op.m)

    def __div__(self, x):
        return GFobj(self.op.div(self.value, self.val(x)), self.op.m)

    def __pow__(self, x):
        val = reduce(lambda x, y: self.op.mul(x, y), [self.value] * x, 1)
        return GFobj(val, self.op.m)
    
    def __radd__(self, x):
        return self.__add__(x)

    def __rsub__(self, x):
        return self.__sub__(x)

    def __rmul__(self, x):
        return self.__mul__(x)

    def __rdiv__(self, x):
        return self.__div__(x)

    def __pos__(self):
        return GF(self.value, self.m)

    def __neg__(self):
        return GF(self.value, self.m)

    def __int__(self):
        return self.value

    def __str__(self):
        return 'a^%d=%d' % (self.op.log[self.value], self.value)
        #return str(self.value)

    def __repr__(self):
        return 'GF(%d, %d)' % (self.value, self.m)
        #return str(self.value)

    @staticmethod
    def val(x):
        return x.value

    def log(self):
        return self.op.log(self.value)

GF_EXP = True

def GF(x, m, exp_of_alpha = False):
    #if isinstance(x, GFobj): return x
    op = get_gf_op(m)
    if exp_of_alpha:
        x = op.exp[x] if isinstance(x, int) else [op.exp[i] for i in x]
    if isinstance(x, int):
        return GFobj(x, m)
    else:
        if len(x) == 0:
            return []
        if isinstance(x[0], int):
            return map(lambda i: GFobj(i, m), x)
        return [map(lambda i: GFobj(i, m), xi) for xi in x]

if __name__ == "__main__":
    """
    a = GF(2, 3)
    print a + 5 + 1
    print a ** 3
    print a * a * a

    b = GF(3, 3)
    print b
    print a + b
    print b / a

    m = GF([0,1,2,3,4,5,6,7], 3)
    print m

    n = GF([], 3)
    print n
    """

    """ #poly_div test
    print poly_div(GF([0], 3), GF([1, 0, 2], 3)) #0
    try:
        print poly_div(GF([0], 3), GF([0], 3))
    except:
        print 'ZeroDivisionError catched'
    print poly_div(GF([6,2,3,3,6], 3), GF([1,0,2],3)) #6,2,4
    print poly_div(GF([6,2,3,3,6], 4), GF([2,0,2],4)) #6,2,15
    """

    """ #poly_roots test
    r = poly_roots(GF([0,1,2,3,0,4,0,0], 3)) #0 0 7
    print 'ans =', map(str, r)
    r = poly_roots(GF([2, 0, 5, 0, 0], 3)) #5 5
    print 'ans =', map(str, r)
    r = poly_roots(GF([2,7,6], 3)) #5 5
    print 'ans =', map(str, r)
    """

    """
    print "support vector:", GF(range(7), 3, GF_EXP), "\n"

    #msg = GF([5, 2, 2, 2, 2], 3)
    msg = GF([2, 0, 1], 3)
    c = [poly_eval(msg, i) for i in GF(range(7), 3, GF_EXP)]
    print map(str, c)
    print 'value:', map(GFobj.val, c)
    print 'expon:', map(lambda x: get_gf_op(3).log[x.value], c)
    # ['a^0=1', 'a^0=1', 'a^0=1', 'a^1=2', 'a^5=7', 'a^0=0', 'a^0=1']
    #value: [1, 1, 1, 2, 7, 0, 1]
    #expon: ['a^0', 'a^0', 'a^0', 'a^1', 'a^5', 'a^0', 'a^0']
    """

    def poly2_eval(poly2, x, y):
        print poly2
        ans = 0
        yi = 1
        for i in range(len(poly2)):
            ans = ans + poly_eval(poly2[i], x) * yi
            yi = yi * y
        return ans

    Q = [[2, 5]]
    print poly2_eval(Q, 3, 1)
    print poly_eval([2, 5], 3)

