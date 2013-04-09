#Copyright Johan S. R. Nielsen
#This file is part of the Personal Sage Library of Johan S. R. Nielsen.
#This library is free software released under the GPL v3 or any later version as
#published by the Free Software Foundation.

#CopyLeft(?) Felix021
#This file is modified from the gs.sage to provide the koetter-vardy algorithm.
#To use it, you should put 'from sagelib import kv' in sagelib/all.py,
#and call sagelib.kv.gs_construct_Q(points, k - 1), where points consists of 
#tuples like (x, y, m), which denotes multiplicity m on point (x, y).

from sagelib.util import *

#####################################################
### CONSTRUCTING AN INTERPOLATION POLYNOMIAL
#####################################################

def gs_monomial_list(max_deg_Q, max_deg_y, weight_y):
    """Return a list of the (x,y) powers of all monomials in F[x,y] whose
    (1,weight_y)-weighted degree is less than maxdeg and whose y-degree <= l."""
    mons = []
    for y in range(0, max_deg_y + 1):
        for x in range(0,  ceil(max_deg_Q - y*weight_y)):
            mons.append((x, y))
    return mons

def gs_interpol_matrix_by_mons(points, mons):
    """Return the interpolation matrix whose nullspace gives the coefficients
    for all interpolation polynomials, given the list of monomials allowed. The
    ith column will be the coefficients on the ith monomial in mons."""
    n = len(points)
    def eqs_affine(x0, y0, m):
        """Make equation for the affine point x0, y0. Return a list of
        equations, each equation being a list of coefficients corresponding to
        the monomials in mons. m is the multiplicity of point (x0, y0)."""
        eqs = []
        for i in range(0, m):
            for j in range(0, m-i):
                eq = dict()
                for mon in mons:
                    ihat = mon[0]
                    jhat = mon[1]
                    if ihat >= i and jhat >= j:
                        icoeff = binomial(ihat, i)*x0^(ihat-i) \
                                    if ihat > i else 1
                        jcoeff = binomial(jhat, j)*(y0^(jhat-j)) \
                                    if jhat > j else 1
                        eq[mon] = jcoeff*icoeff
                eqs.append([eq.get(mon, 0) for mon in mons])
        return eqs
    return flatten_once([ eqs_affine(*point) for point in points ])

def gs_interpol_matrix_problem(points, max_deg_y, weight_y):
    """Return the linear system of equations which Q should be a solution to.
    Returns a matrix M and a list of monomials mons, where a vector in the
    right nullspace of M corresponds to an interpolation polynomial $Q$, by the
    $i$'th element being the coefficient of the $i$'th monomial in mons of
    $Q$."""

    C = sum(map(lambda p: p[2] * (p[2] + 1) / 2, points))
    #the article says max_deg_Q = floor(sqrt(2*(k-1)*C) - (k-1)/2), which may 
    #cause M.nrows() >= M.ncols(), so I simply added 1.
    max_deg_Q = floor(sqrt(2 * weight_y * C) - weight_y / 2) + 1
    #max_deg_y = floor((1 + sqrt(1 + 8 * C / weight_y)) / 2) - 1

    #this print is for test purpose
    print 'C = %d, max_deg_Q = %d, max_deg_y = %d' % (C, max_deg_Q, max_deg_y)

    mons = gs_monomial_list(max_deg_Q, max_deg_y, weight_y)
    M = matrix(list(gs_interpol_matrix_by_mons(points, mons)))
    return (M, mons)

def gs_construct_Q_from_matrix(M, mons):
    """Given the interpolation matrix problem and the corresponding list of
    monomials, return a satisfactory Q polynomial."""

    #this print is for test purpose
    print "Rows = %d, Cols = %d" % (M.nrows(), M.ncols())

    if M.nrows() >= M.ncols():
        raise Exception("More rows than columns! Bailing")
    Sp = M.right_kernel()
    sol = Sp.random_element()
    #TODO: Option to pick out minimal element?
    while sol.is_zero():
        print "rat_construct_Q: Found zero as random element. Trying again."
        # Picking out e.g. element 1 directly seems to run into an infinite
        # loop for large matrices.
        sol = Sp.random_element()
    # Construct the Q polynomial
    PF.<x,y> = M.base_ring()[]
    Q = sum([ x^mons[i][0]*y^mons[i][1]*sol[i] for i in range(0, len(mons)) ])
    return Q

def gs_construct_Q(points, max_deg_y, weight_y):
    """Calculate an interpolation polynomial Q(x,y) for the parameters given.
    points is a list of tuples (xi, yi, m) such that Q(xi,yi) = 0 with multiplicity m.
    Shorthand for calling gs_construct_Q_from_matrix(*gs_interpol_matrix_problem(...))
    """
    return gs_construct_Q_from_matrix(
                *gs_interpol_matrix_problem(points, max_deg_y, weight_y))
