from copy import copy

"""

Here I'll try to implement a bivariate polynomial class Q(x, y) Over F(q)

Its elements should be codes from a Galois Field.

not implemented yet = =.

"""

def degree(p, Wx, Wy):
    return p[0] * Wx + p[1] * Wy

def cmp_degree(p, q, Wx, Wy):
    if p == q:
        return 0
    deg_p = degree(p, Wx, Wy)
    deg_q = degree(q, Wx, Wy)
    if deg_p < deg_q or (deg_p == deg_q and p[0] > q[0]):
        return -1
    else:
        return 1


class poly2(object):

    def degree(self, p):
        return degree(p, self.Wx, self.Wy)

    def __init__(self, a, Wx=1, Wy=1):
        self.a = copy(a)
        self.Wx = Wx
        self.Wy = Wy
        #Q(x, y) = Sum[i=0:~]Sum[j=0:~](a[i][j * x[i] * y[j])

        list_ij = [(i, j) for j in range(len(a)) for i in range(len(a[0]))]
        list_ij.sort(cmp = lambda p, q: cmp_degree(p, q, Wx, Wy))

        Qmap = {}
        Qinv = {}
        coeff = []
        for idx in range(len(list_ij)):
            ij = list_ij[idx]
            Qmap[ij] = idx
            Qinv[idx] = ij
            coeff.append(a[ij[1]][ij[0]])

        self.Qmap = Qmap
        self.Qinv = Qinv
        self.coeff = coeff

        print self.Qmap, '\n', self.Qinv, '\n', self.coeff

    def __div__(self, x):
        if isinstance(x, list):
            x = poly2(x, self.Wx, self.Wy)
        if len(x.coeff) == 0:
            raise ZeroDivisionError("...")


if __name__ == "__main__":
    poly2([[1,2,3],[4,5,6]], 1, 1)
