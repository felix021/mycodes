//  Percy++
//  Copyright 2007 Ian Goldberg <iang@cs.uwaterloo.ca>
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of version 2 of the GNU General Public License as
//  published by the Free Software Foundation.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  There is a copy of the GNU General Public License in the COPYING file
//  packaged with this plugin; if you cannot find it, write to the Free
//  Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
//  02111-1307  USA

#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <math.h>
#include <NTL/mat_ZZ_p.h>
#include <NTL/ZZ_pX.h>
#include <NTL/GF2EX.h>
#include "rr_roots.h"
#include "recover.h"
#include "ZZ_pXY.h"

NTL_CLIENT

static ZZ_p C(unsigned int n, unsigned int k)
{
    ZZ_p num, dem;
    num = 1;
    dem = 1;
    unsigned int i;

    for (i=0;i<k;++i) {
        num *= (n-i);
        dem *= (k-i);
    }

    return num/dem;
}

// Return the index of the first non-zero entry in this row, or -1 if
// it's all zeros.
static long first_non_zero(const vec_ZZ_p& R)
{
    long len = R.length();
    for (long i=0; i<len; ++i) {
        if (!IsZero(R[i])) {
            return i;
        }
    }
    return -1;
}

static vec_ZZ_p solvemat(mat_ZZ_p& M) 
{
    // Do Gaussian elimination on M.
    gauss(M);

    // Build a non-zero solution.  First find the last row that isn't
    // all zeros.
    long numrows = M.NumRows();
    long numcols = M[0].length();
    long lastnonzerorow = -1;
    for (long i=numrows-1; i>=0; --i) {
        if (!IsZero(M[i])) {
            lastnonzerorow = i;
            break;
        }
    }

    // Initialize the solution vector to all 0's
    vec_ZZ_p soln;
    soln.SetLength(numcols);

    // We want a non-zero solution, so find the leftmost column that
    // does not contain a leading 1.
    long lastlead = -1;
    int found = 0;
    for (long i=0; i<numrows; ++i) {
        long leadingidx = first_non_zero(M[i]);
        if (leadingidx < 0 || leadingidx > lastlead + 1) {
            soln[lastlead+1] = 1;
            found = 1;
            break;
        }
        lastlead = leadingidx;
    }
    if (!found && lastlead < numcols - 1) {
        soln[lastlead+1] = 1;
    }

    // Do the back substitution
    for (long i=lastnonzerorow; i>=0; --i) {
        // Find the first non-zero entry
        long leadingidx = first_non_zero(M[i]);
        ZZ_p newval;
        InnerProduct(newval, M[i], soln);
        soln[leadingidx] = -newval / M[i][leadingidx];
    }

    return soln;
}

struct RecoveryPoly {
    RecoveryPoly(vector<unsigned short> G, ZZ_pX phi) : G(G), phi(phi) {}
    vector<unsigned short> G;
    ZZ_pX phi;
};

// Find all polynomials of degree at most k that agree with the given
// (index,share) pairs at at least t of the n points.  The notation is
// from Venkatesan Guruswami and Madhu Sudan, "Improved Decoding of
// Reed-Solomon and Algebraic-Geometry Codes".
static vector<RecoveryPoly> findpolys(unsigned int n, unsigned int k, unsigned int t,
        const vec_ZZ_p& X, const vec_ZZ_p& Y)
{
    // Compute the r and l parameters
    unsigned int r = 1 + (unsigned int)(floor( (k*n + sqrt(k*k*n*n+4*(t*t-k*n)))/(2*(t*t-k*n)) ));
    unsigned int l = r*t - 1;
    cerr << "r = " << r << ", l = " << l << endl;

    typedef pair<unsigned int, unsigned int> pairint;
    map<pairint, unsigned int> Qmap;
    map<unsigned int, pairint> Qinv;

    // Make a mapping from <xdegree, ydegree> to a single index.
    // Also make the inverse mapping.
    unsigned int c = 0;
    unsigned int i,j,j1,j2,j1p,j2p;
    for(j=0; j <= l/k; ++j) {
        for (i=0; i <= l-j*k; ++i) {
            pairint ij(i,j);
            Qmap[ij] = c;
            Qinv[c] = ij;
            ++c;
        }
    }

    // We're going to build a large matrix A and find a non-zero
    // solution to A.v = 0.
    mat_ZZ_p A;

    A.SetDims(n * r * (r+1) / 2, c);

    std::cerr << "Generating " << n * r * (r+1) / 2 << " x " << c << " matrix...\n";

    // This is the part you need to read the paper for
    unsigned int Arow = 0;
    for (i=0; i<n; ++i) {
        for (j1=0; j1<r; ++j1) {
            // std::cerr << i << ", " << j1 << " / " << n << ", " << r << "\n";
            for (j2=0; j2 < r - j1; ++j2) {
                for (j2p = j2; j2p <= l/k; ++j2p) {
                    for (j1p = j1; j1p <= l - k*j2p; ++j1p) {
                        pairint j1pj2p(j1p, j2p);
                        A[Arow][Qmap[j1pj2p]] = C(j1p,j1) * C(j2p,j2) *
                            power(X[i], j1p-j1) *
                            power(Y[i], j2p-j2);
                    }
                }
                ++Arow;
            }
        }
    }

    std::cerr << "Solving matrix...\n";

    vec_ZZ_p soln = solvemat(A);

    // The soln vector now consists of coefficients for a bivariate
    // polynomial P(x,y).
    ZZ_pXY P;
    P.SetMaxLength(l/k + 1);   // The y-degree of P

    for(unsigned int i=0; i<c; ++i) {
        if (soln[i] != 0) {
            SetCoeff(P, Qinv[i].second, Qinv[i].first, soln[i]);
        }
    }

    std::cerr << "Factoring resulting polynomial...\n";
    cerr << P << endl;

    // It turns out that any polynomial phi(x) that we should be
    // returning (since phi is of degree at most k and agrees with the
    // input data on at least t points) is such that (y - phi(x)) is a
    // factor of P(x,y).  So we first find all roots for y of P(x,y)
    // which are polynomials of degree at most k.
    vec_ZZ_pX roots = rr_findroots(P, k);

    // For each of these roots, check how many input points it agrees
    // with.  If it's at least t, add it to the list of polys to return.
    vector<RecoveryPoly> polys;
    unsigned int numroots = roots.length();
    for (unsigned int i=0; i<numroots; ++i) {
        if (deg(roots[i]) > (long)k) 
            continue;
        vector<unsigned short> vecagree;
        unsigned short numagree = 0;
        for (i = 0; i < n; i++) {
            ZZ_p phival;
            eval(phival, roots[i], X[i]);
            if (phival == Y[i]) {
                ++numagree;
                vecagree.push_back(i);
            }
        }
        if (numagree >= t) {
            RecoveryPoly n(vecagree, roots[i]);
            polys.push_back(n);
        }
    }
    return polys;
}

#ifndef TEST_RR

int main(int argc, char *argv[])
{
    /*
    ZZ modulus;
    modulus = 8; //define GF(8)
    ZZ_p::init(modulus);
    */

    unsigned n = 7, k = 5, t = n - 1 - (int)sqrt(n * (k - 1));
    cerr << "n = " << n << ", k = " << k << ", t = " << t << endl;

    stringstream ss(stringstream::in | stringstream::out);

    GF2X generator_polynomial;
    generator_polynomial = 13;
    GF2E::init(generator_polynomial);

    GF2E a;
    a = 2;

    cout << a << endl;

    /*
    GF2EX P;
    GF2EXModulus modulus;
    modulus = 8;
    ss << "[1 2]";
    ss >> P;

    cout << P << endl;

    GF2E x, y;
    //ZZ_p x, y;
    for (int i = 0; i < n; i++) {
        conv(x, i);
        eval(y, P, x);
        cout << y << endl;
    }
    */

    /*
    ZZ_pX msg;
    u.SetLength(n);
    ss << "[0 1 2 3 4 5 6 7]";
    ss >> F;
    ss << "[0 5 7 5 4]";
    ss >> msg;
    for (int i = 0; i < n + 1; i++) {
        ZZ_p x;
        x = i;
        eval(u[i], msg, x);
        cerr << x << ", " << u[i] << endl;
    }
    */
    //cout << F << ", " << u << endl;

//findpolys(unsigned int n, unsigned int k, unsigned int t, const vec_ZZ_p& X, const vec_ZZ_p& Y)
    /*
    vector<RecoveryPoly> polys = findpolys(n, k, t, F, u);

    cout << polys.size() << endl;

    vector<RecoveryPoly>::const_iterator Piter;

    for (Piter = polys.begin(); Piter != polys.end(); ++Piter) {
        // Find the secret determined by this poly
        ZZ_p wz;
        eval(wz, Piter->phi, ZZ_p::zero());
        cout << wz << endl;
    }
    */


    /*
    ss << "[[4 12 5 11 8 13] [14 14 9 16 8] [14 13 1] [2 11 1] [17]] ";
    ss >> P;

    vec_ZZ_pX roots = rr_findroots(P, 1);
    cout << "\nRoots found = " << roots << "\n";
    */

    return 0;
}

#endif
