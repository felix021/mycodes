"""

Some humble functions trying to simulate as the matlab equivalents

"""


from copy import copy
import GF

def size(M, n = -1):
    ret = []
    t = M
    i = 0
    while n == -1 or i < n:
        if not isinstance(t, list) or isinstance(t, tuple):
            break
        ret.append(len(t))
        t = t[0]
        i += 1
    if n == -1:
        return ret
    return ret[n - 1]

def zeros(m, n = 0):
    if n == 0:
        n = m

    c = [0] * n

    r = []
    while m > 0:
        r.append(copy(c))
        m -= 1
    return r

def findmax(P):
    mi = 0
    mj = 0
    for i in range(len(P)):
        for j in range(len(P[i])):
            if P[i][j] > P[mi][mj]:
                mi = i
                mj = j
    return (mi, mj)

def dump_matrix2(M):
    print '[' + ';\n'.join(map(lambda i: ' '.join(map(str, i)), M)) + ']'

def reshape(M, r, c):
    R = zeros(r, c)
    i = j = 0
    for row in M:
        for col in row:
            R[i][j] = col
            j = (j + 1) % c
            if j == 0:
                i += 1
    return R

def transpose(R):
    return map(list, zip(*R))

if __name__ == "__main__":
    print size([1, 2, 3], 1)
    print zeros(3)
    R = reshape([[1,2,3],[4,5,6]],3,2)
    print map(str, R)
