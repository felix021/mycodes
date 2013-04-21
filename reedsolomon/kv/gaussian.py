#Gaussian Elimination for Number-Field equations
from copy import copy

def float_is_zero(n):
    return abs(n) < 1e-10

def gaussian(matrix, default = 1, is_zero = float_is_zero):
    m = [map(float, row) for row in matrix] #m = copy(matrix)
    nrow, ncol = len(m), len(m[0])
    for c in range(min(ncol, nrow)):
        maxrow = c
        for r in range(c + 1, nrow):
            if abs(m[r][c]) > abs(m[maxrow][c]):
                maxrow = r
        m[maxrow], m[c] = m[c], m[maxrow]
        for cidx in range(c, ncol):
            if not is_zero(m[c][cidx]):
                break
        else:
            continue
        for r in range(c + 1, nrow):
            coeff = m[r][cidx] / m[c][cidx]
            for cc in range(cidx, ncol):
                m[r][cc] -= m[c][cc] * coeff

    n_zero = {}
    for row in m:
        n = 0
        for col in row:
            if not is_zero(col):
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

    """
    for i in m:
        print i
    print ""
    """

    return sol

m = [
    [1,2,3,4,5,6,6],
    [1,0,0,3,4,6,0],
    [1,2,0,3,3,6,0],
    [1,2,0,3,3,6,0],
    [1,2,0,3,3,3,0],
]

"""

m = [
    [4,2,3,9],
    [2,1,1,4],
    [2,1,2,5],
]

m = [
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,1],
]
"""

m = [
    [1,2,3,4,5,6],
    [1,1,1,3,4,6],
    [1,2,2,3,3,6],
    [1,2,3,3,3,6],
    [1,2,4,3,3,3],
]

m = [
    [1, 0, 0, 0, 0, 0] ,
    [1, 1, 1, 1, 1, 1] ,
    [1, 2, 4, 8, 16, 2] ,
    [0, 0, 0, 0, 0, 1] ,
    [0, 1, 4, 12, 32, 0] ,
]

for i in m:
    i.append(0)
    print i

sol = gaussian(m, default = 1)

sol = [round(i, 9) for i in sol]
print 'sol =', sol

for r in m:
    print sum(map(lambda x, y: x * y, r[:-1], sol)) + r[-1]
