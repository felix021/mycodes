#developing...

#Copyright Johan S. R. Nielsen
#This file is part of the Personal Sage Library of Johan S. R. Nielsen.
#This library is free software released under the GPL v3 or any later version as
#published by the Free Software Foundation.

"""Utilities for the Guruswami-Sudan algorithm"""
from sagelib.util import *
import sagelib.listdecoding

def gs_satisfiable(n,k,tau,s,l):
    """Returns whether the given parameters satisfy the governing equation of
    Guruswami-Sudan (e.g. jsrn thesis p. 36)"""
    return l > 0 and s > 0 and n*s*(s+1) < (l+1)*(2*s*(n-tau) - (k-1)*l)

def gs_params(n,k,tau):
    """"Calculate values of (s,l) like those given in the paper of
    Guruswami-Sudan"""
    if k==1:
        return (1,1)
    kk = k-1
    t = n-tau
    s = 1 + floor( (kk*n + sqrt(kk^2*n^2 + 4*(t^2-kk*n))) / (2*(t^2 - kk*n)) )
    l = floor((s*t - 1)/kk)
    assert gs_satisfiable(n,k,tau,s,l)
    return (s, l)

def gs_minimal_list(n,k,tau):
    """Calculate the minimal list size for the parameters along with a
    satisfiable multiplicity. Returns (l, s). This is slow (linear in the list
    size)."""
    # It is probably near the l given by the equations, so start here
    (firsts,firstl) = gs_params(n,k,tau)
    def try_l(l):
        (mins,maxs) = solve2deg_int(n, n-2*(l+1)*(n-tau), (k-1)*l*(l+1))
        if maxs > 0 and maxs >= mins:
            return max(1, mins) 
        else:
            return None
    l = find_minimal_satisfiable(try_l, firstl)
    s = try_l(l)
    assert gs_satisfiable(n,k,tau,s,l)
    return (s, l)

#####################################################
### CONSTRUCTING AN INTERPOLATION POLYNOMIAL
#####################################################

def gs_monomial_list(maxdeg, l, wy):
    """Return a list of the (x,y) powers of all monomials in F[x,y] whose
    (1,wy)-weighted degree is less than maxdeg and whose y-degree <= l."""
    mons = []
    for y in range(0, l+1):
        for x in range(0,  ceil(maxdeg - y*wy)):
            mons.append((x, y))
    return mons

def gs_interpol_matrix_by_mons(points, s, mons):
    """Return the interpolation matrix whose nullspace gives the coefficients
    for all interpolation polynomials, given the list of monomials allowed. The
    ith column will be the coefficients on the ith monomial in mons."""
    n = len(points)
    def eqs_affine(x0,y0):
        """Make equation for the affine point x0, y0. Return a list of
        equations, each equation being a list of coefficients corresponding to
        the monomials in mons."""
        eqs = []
        for i in range(0, s):
            for j in range(0, s-i):
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

def gs_interpol_matrix_problem(points, tau, s, l, wy):
    """Return the linear system of equations which Q should be a solution to.
    Returns a matrix M and a list of monomials mons, where a vector in the
    right nullspace of M corresponds to an interpolation polynomial $Q$, by the
    $i$'th element being the coefficient of the $i$'th monomial in mons of
    $Q$."""
    mons = gs_monomial_list((len(points)-tau)*s, l, wy)
    M = matrix(list(gs_interpol_matrix_by_mons(points, s, mons)))
    return (M, mons)

def gs_construct_Q_from_matrix(M, mons):
    """Given the interpolation matrix problem and the corresponding list of
    monomials, return a satisfactory Q polynomial."""
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

def gs_construct_Q(points, tau, s, l, wy):
    """Calculate an interpolation polynomial Q(x,y) for the parameters given.
    points is a list of tuples (xi,yi) such that Q(xi,yi) = 0 with multiplicity
    s.
    Shorthand for calling
    gs_construct_Q_from_matrix(*gs_interpol_matrix_problem(...))
    """
    return gs_construct_Q_from_matrix(
                *gs_interpol_matrix_problem(points, tau, s, l, wy))
