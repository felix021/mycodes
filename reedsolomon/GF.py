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

import sys
from copy import copy

_debug = False

def set_debug(debug = False):
    global _debug
    _debug = debug

_poly = {
    4: 7,
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

    def calc_elements(self):
        self.exp = [1] * (self.q * 2)
        self.log = [0] * self.q
        self.log[0] = -1
        x = 1
        prim_poly = _poly[self.q]
        for i in range(1, self.n):
            x <<= 1
            if x & self.q:
                x ^= prim_poly
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

    def pow(self, x, y):
        if y == 0:
            return 1
        if x == 0:
            return 0
        exp = self.log[x]
        return self.exp[exp * y % self.n]

    def div(self, x, y):
        if y == 0:
            raise ZeroDivisionError()
        if x == 0:
            return 0
        return self.exp[self.log[x] + self.n - self.log[y]]

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

    @staticmethod
    def val(x):
        if isinstance(x, GFobj):
            return x.value
        return int(x)

    def __eq__(self, x):
        if isinstance(x, GFobj):
            x = x.value
        return self.value == x

    def __ne__(self, x):
        return not self.__eq__(x)

    def __hash__(self):
        return self.value.__hash__()

    def __add__(self, x):
        return GFobj(self.op.add(self.value, GFobj.val(x)), self.m)

    def __sub__(self, x):
        return GFobj(self.op.sub(self.value, GFobj.val(x)), self.m)

    def __mul__(self, x):
        return GFobj(self.op.mul(self.value, GFobj.val(x)), self.m)

    def __div__(self, x):
        return GFobj(self.op.div(self.value, GFobj.val(x)), self.m)

    def __pow__(self, x):
        return GFobj(self.op.pow(self.value, x), self.m)
    
    def __radd__(self, x): #a + b = b + a
        return self.__add__(x)

    def __rmul__(self, x): #a * b = b * a
        return self.__mul__(x)

    def __rsub__(self, x):
        return GFobj(self.op.sub(GFobj.val(x), self.value), self.m)

    def __rdiv__(self, x):
        return GFobj(self.op.div(GFobj.val(x), self.value), self.m)

    def __pos__(self):
        return GFobj(self.value, self.m)

    def __neg__(self):
        return GFobj(self.value, self.m)

    def __int__(self):
        return self.value

    def __str__(self):
        return 'a^%d=%d' % (self.op.log[self.value], self.value)
        #return str(self.value)

    def __repr__(self):
        global _debug
        if _debug == False:
            return 'GFobj(%d, %d)' % (self.value, self.m)
        else: #debug, for easy view
            return str(self.value) # for test

    def log(self):
        if self.value != 0:
            return self.op.log[self.value]
        raise ValueError('math domain error: log(GF(0, %d)) is illegal' % self.m)


GF_EXP = True

def GF(x, m, exp_of_alpha = False):
    op = get_gf_op(m)

    if exp_of_alpha:
        x = op.exp[x] if isinstance(x, int) else [op.exp[i] for i in x]

    if isinstance(x, int):
        return GFobj(x, m)
    else:
        if len(x) == 0:
            return []
        if isinstance(x[0], int): #one dimension
            return map(lambda i: GFobj(i, m), x)
        #two dimension
        return [map(lambda i: GFobj(i, m), xi) for xi in x]

if __name__ == "__main__":

    #"""
    a = GF(2, 3)
    assert(a == GF(2, 3))
    assert(a == 2)
    assert(a != 3)
    assert(a != GF(4, 3))

    assert(a + 5 + 1 == GF(6, 3))
    assert(5 + a + 1 == GF(6, 3))
    assert(a - 5 - 1 == GF(6, 3))
    assert(5 - a - 1 == GF(6, 3))

    assert(a * a == GF(4, 3))
    assert(a * 4 == a * GF(4, 3))
    assert(4 * a == a * GF(4, 3))
    assert(a * a / a == a)
    assert(GF(3, 3) / a == GF(4, 3))
    assert(3 / a == GF(4, 3))

    z = GF(0, 3)
    assert(z ** 0 == 1)
    assert(z ** 2 == 0)
    assert(a ** 0 == GF(1, 3))
    assert(a ** 1 == GF(2, 3))
    assert(a ** 2 == GF(4, 3))
    assert(a ** 3 == GF(3, 3))
    assert(a ** 4 == GF(6, 3))
    assert(a ** 5 == GF(7, 3))
    assert(a ** 6 == GF(5, 3))
    assert(a ** 7 == GF(1, 3))
    assert(a ** 100 == a ** (100 % 7))
    assert(GF([], 3) == [])
    m = GF([0,1,2,3,4,5,6,7], 3)
    assert(m[1:] == GF([0,1,3,2,6,4,5], 3, GF_EXP))
    try:
        GF(0, 3).log()
        assert('log test fail')
    except:
        pass

    set_debug(True)
    print "support vectors:", GF(range(7), 3, GF_EXP), "\n"

    print 'all test passed'

