#!/usr/bin/python

import math

from GF import *
from poly import *

def binomial(n, m):
    Anm = reduce(lambda x, y: x * y, range(n - m + 1, n + 1), 1)
    Cnm = reduce(lambda x, y: x / y, range(2, m + 1), Anm)
    return Cnm

#inplace gaussian elimination, need adjustment for Galois Field
def gaussian(matrix, default = 1):
    m = matrix
    nrow, ncol = len(m), len(m[0])
    for c in range(min(ncol, nrow)):
        maxrow = c
        for r in range(c + 1, nrow):
            if m[r][c] != 0:
                maxrow = r
                break
        m[maxrow], m[c] = m[c], m[maxrow]
        for cidx in range(c, ncol):
            if m[c][cidx] != 0:
                break
        else:
            continue
        for r in range(c + 1, nrow):
            coeff = m[r][cidx] / m[c][cidx]
            for cc in range(cidx, ncol):
                m[r][cc] = m[r][cc] - m[c][cc] * coeff

    n_zero = {}
    for row in m:
        n = 0
        for col in row:
            if col != 0:
                break
            n += 1
        n_zero[id(row)] = n

    m.sort(cmp = lambda x, y: n_zero[id(x)] - n_zero[id(y)])

    sol = [0] * (ncol - 1)
    sid = ncol - 1
    for r in range(nrow - 1, 0 - 1, -1):
        row = m[r]
        zeros = n_zero[id(row)]
        if zeros == ncol:
            continue
        elif zeros == ncol - 1 and row[ncol - 1] != 0:
            raise Exception('no solution')
        else:
            pos = zeros
            for c in range(pos + 1, sid):
                sol[c] = default
            right = row[-1] + sum(map(lambda x, y: x * y, row[pos+1:-1], sol[pos+1:]))
            sol[pos] = -(right / row[pos])
            sid = zeros
    for c in range(0, sid):
        sol[c] = default

    return sol

def right_kernel(matrix):
    M = []
    for row in matrix:
        M.append(row + [0])
    return gaussian(M, default = 1)

def monomial_list(max_deg_Q, max_deg_y, weight_y):
    mons = []
    for y in range(max_deg_y + 1):
        for x in range(max_deg_Q - weight_y * y):
            mons.append((x, y))
    return mons

def interpolation(points, mons):
    n = len(points)
    def eqs_affine(x, y, m):
        eqs = []
        for i in range(0, m):
            for j in range(0, m - i):
                eq = dict()
                for mon in mons:
                    ihat = mon[0]
                    jhat = mon[1]
                    if ihat >= i and jhat >= j:
                        if ihat > i:
                            C = binomial(ihat, i)
                            p = 0
                            icoeff = GF(0, 3)
                            while p < C:
                                icoeff = icoeff + (x **(ihat - i))
                                p += 1
                        else:
                            icoeff = GF(1, 3)
                        if jhat > j:
                            C = binomial(jhat, j)
                            p = 0
                            jcoeff = GF(0, 3)
                            while p < C:
                                jcoeff = jcoeff + (x **(jhat - j))
                                p += 1
                        else:
                            jcoeff = GF(1, 3)

                        """
                        icoeff = binomial(ihat, i) * (x**(ihat - i)) \
                            if ihat > i else 1
                        jcoeff = binomial(jhat, j) * (y**(jhat - j)) \
                            if jhat > j else 1
                        """
                        eq[mon] = jcoeff * icoeff
                eqs.append([eq.get(mon, GF(0, 3)) for mon in mons])
            print 'EQS:', eqs
        return eqs
    eqs = []
    for p in points:
        for eq in eqs_affine(*p):
            eqs.append(eq)
    return eqs

"""test
mons = monomial_list(6, 2, 3)
points = [(0, 0, 1), (1, 1, 1), (2, 2, 2)]
for i in interpolation(points, mons):
    print i
"""

def interpolation_matrix(points, max_deg_y, weight_y):
    C = sum([m * (m + 1) / 2 for x, y, m in points])
    max_deg_Q = int((math.sqrt(2 * weight_y * C) - weight_y / 2 + 1))
    print "C = %d, max_deg_Q = %d, max_deg_y = %d" % (C, max_deg_Q, max_deg_y)
    mons = monomial_list(max_deg_Q, max_deg_y, weight_y)
    M = interpolation(points, mons)
    return M, mons

def construct_Q_from_matrix(M, mons):
    if len(M) >= len(M[0]):
        raise Exception("More rows than columns!")
    matrix = []
    for row in M:
        matrix.append(row + [0])
    sol = right_kernel(matrix)
    Q = [(sol[i], mons[i][0], mons[i][1]) for i in range(len(mons))]
    return Q

#test
#points = [(0, 0, 1), (1, 1, 1), (2, 2, 2)]
zero, one, two = GF([0, 1, 2], 3, GF_EXP)
points = [(zero, zero, 1), (one, one, 1), (two, two, 2)]

k = 5
weight_y = k - 1 

Cost = sum([m * (m + 1) / 2 for x, y, m in points])

max_deg_y = int((1 + math.sqrt(1 + 8 * Cost / weight_y)) / 2) - 1

mons = monomial_list(5, 1, 4)
#print mons

#print weight_y, Cost, max_deg_y

M = interpolation(points, mons)

#M, mons = interpolation_matrix(points, max_deg_y, weight_y)
for i in M:
    print i, ","

print right_kernel(M)
