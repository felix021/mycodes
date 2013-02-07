import math
from matlab import *
from copy import copy

"""

This function just calculates the Multiplicity Matrix fromthe Reliability Matrix, 
as is stated in the Koetter Vardy's article "Algebraic soft-decision decoding of 
Reed Solomon Codes".

The interpolation step is not implemented here.

"""

def koetter_vardy(P, s):
    Ps = copy(P)
    M = zeros(len(P), len(P[0]))
    for i in range(s):
        i, j = findmax(Ps)
        Ps[i][j] = P[i][j] / (M[i][j] + 2)
        M[i][j] += 1
    return M

if __name__ == "__main__":
    P = [[0.0, 0.4331, 0.0001, 0.0295, 0.4829, 0.0544, 0.0], [0.1538, 0.2779, 0.5417, 0.0029, 0.0059, 0.0171, 0.0007], [0.8861, 0.0049, 0.0063, 0.0074, 0.0509, 0.0294, 0.015], [0.0006, 0.9337, 0.0, 0.0001, 0.0656, 0.0, 0.0], [0.1011, 0.0042, 0.0102, 0.0329, 0.6786, 0.0003, 0.1727], [0.0026, 0.0006, 0.0917, 0.1758, 0.0032, 0.339, 0.3871], [0.0132, 0.0417, 0.0464, 0.1082, 0.5145, 0.2209, 0.0551], [0.0001, 0.0043, 0.1866, 0.0338, 0.0486, 0.6061, 0.1205]]

    M = koetter_vardy(P, 50)
    dump_matrix2(M)
