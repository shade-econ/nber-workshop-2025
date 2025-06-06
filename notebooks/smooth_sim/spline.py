"""Simple Numba-compatible cubic spline interpolation and evaluation"""
import numpy as np
from numba import njit


"""Convenience routines for higher-level use"""

@njit
def val(q, xgrid, xs):
    """Given cubic spline coefficients q and original grid xgrid, evaluate spline at all xs in array.
    Robust option that searches for each x separately, requires no structure."""
    t = make_knots(xgrid)
    ys = np.empty_like(xs)
    for i in range(len(xs)):
        ys[i] = val_scalar(q, t, xs[i])
    return ys

@njit
def val_monotonic(q, xgrid, xs):
    """Similar to val, but assumes that xs are also monotonic, so that search can be monotonic,
    best when xs and xgrid have similar length."""
    t = make_knots(xgrid)
    nx = len(xs)
    nt = len(t)
    ys = np.empty_like(xs)

    ti = 3
    for xi in range(nx):
        x_cur = xs[xi]
        while ti < nt - 5:
            if t[ti+1] >= x_cur:
                break
            ti += 1
        
        ys[xi] = val_scalar_known_i(q, t, ti, x_cur)
    return ys

@njit
def val_scalar(q, t, x):
    return val_scalar_known_i(q, t, locate(t, x), x)

@njit
def val_scalar_with_der(q, t, x):
    return val_scalar_with_der_known_i(q, t, locate(t, x), x)

@njit
def make_knots(x):
    """Given a sorted array x, return the knots t needed to interpolate it with a cubic spline,
    assuming standard not-a-knot for second and second-to-last xs."""
    n = len(x)
    t = np.empty(n+4)
    t[4:-4] = x[2:-2]
    t[:4] = x[0]
    t[-4:] = x[-1]
    return t

@njit
def locate(t, x):
    i = np.searchsorted(t, x) - 1
    i = np.maximum(i, 3)
    i = np.minimum(i, len(t)-5)
    return i

"""Core spline scalar evaluation for known i routines"""

@njit
def val_scalar_known_i(q, t, i, x):
    """Given n cubic spline coefficients q, knots t, and some x lying between knots t[i]
     and t[i+1], evaluate spline at x."""
    alpha0 = (t[i+1]-x)/(t[i+1]-t[i-2])
    alpha1 = (t[i+2]-x)/(t[i+2]-t[i-1])
    alpha2 = (t[i+3]-x)/(t[i+3]-t[i])
    m0 = alpha0*q[i-3] + (1-alpha0)*q[i-2]
    m1 = alpha1*q[i-2] + (1-alpha1)*q[i-1]
    m2 = alpha2*q[i-1] + (1-alpha2)*q[i]
    beta0 = (t[i+1]-x)/(t[i+1]-t[i-1])
    beta1 = (t[i+2]-x)/(t[i+2]-t[i])
    n0 = beta0*m0 + (1-beta0)*m1
    n1 = beta1*m1 + (1-beta1)*m2
    gamma = (t[i+1]-x)/(t[i+1]-t[i])
    return gamma*n0 + (1-gamma)*n1


@njit
def val_scalar_with_der_known_i(q, t, i, x):
    """Same as eval_scalar, but also return derivative of spline at x."""
    alpha0 = (t[i+1]-x)/(t[i+1]-t[i-2])
    alpha1 = (t[i+2]-x)/(t[i+2]-t[i-1])
    alpha2 = (t[i+3]-x)/(t[i+3]-t[i])
    m0 = alpha0*q[i-3] + (1-alpha0)*q[i-2]
    m1 = alpha1*q[i-2] + (1-alpha1)*q[i-1]
    m2 = alpha2*q[i-1] + (1-alpha2)*q[i]
    dm0 = (q[i-2]-q[i-3])/(t[i+1]-t[i-2])
    dm1 = (q[i-1]-q[i-2])/(t[i+2]-t[i-1])
    dm2 = (q[i]-q[i-1])/(t[i+3]-t[i])
    beta0 = (t[i+1]-x)/(t[i+1]-t[i-1])
    beta1 = (t[i+2]-x)/(t[i+2]-t[i])
    n0 = beta0*m0 + (1-beta0)*m1
    n1 = beta1*m1 + (1-beta1)*m2
    dn0 = (m1-m0)/(t[i+1]-t[i-1]) + beta0*dm0 + (1-beta0)*dm1
    dn1 = (m2-m1)/(t[i+2]-t[i]) + beta1*dm1 + (1-beta1)*dm2
    gamma = (t[i+1]-x)/(t[i+1]-t[i])
    out = gamma*n0 + (1-gamma)*n1
    dout = gamma*dn0 + (1-gamma)*dn1 + (n1-n0)/(t[i+1]-t[i])
    return out, dout


@njit
def val_bsplines_scalar_known_i(t, i, x):
    """Given knots t and some x lying between knots t[i] and t[i+1], evaluate the
    cubic B-splines i-3 through i (the only nonnegative ones) at x."""
    # essentially the transpose calculation of eval_scalar, not evaluated at q
    gamma = (t[i+1]-x)/(t[i+1]-t[i])
    n0 = gamma
    n1 = 1-gamma
    beta0 = (t[i+1]-x)/(t[i+1]-t[i-1])
    beta1 = (t[i+2]-x)/(t[i+2]-t[i])
    m0 = beta0*n0
    m1 = (1-beta0)*n0 + beta1*n1
    m2 = (1-beta1)*n1
    alpha0 = (t[i+1]-x)/(t[i+1]-t[i-2])
    alpha1 = (t[i+2]-x)/(t[i+2]-t[i-1])
    alpha2 = (t[i+3]-x)/(t[i+3]-t[i])
    out0 = alpha0*m0
    out1 = (1-alpha0)*m0 + alpha1*m1
    out2 = (1-alpha1)*m1 + alpha2*m2
    out3 = (1-alpha2)*m2
    return out0, out1, out2, out3


"""Obtaining spline coefficients"""

@njit
def interp(x, y):
    """Return B-spline coefficients of cubic spline interpolating (x, y) pairs."""
    t = make_knots(x)
    n = len(x)
    q = np.empty(n)

    # first and last coefficients equal first and last datapoints
    q[0] = y[0]
    q[-1] = y[-1]

    # non-boundary knots start at i=4 and end at i=n, evaluate B-splines i-3 through i-1 for each
    # note that all rows of Xs should sum to 1!
    Xtri = np.empty((n-4, 3))
    for i in range(4, n):
        Xtri[i-4] = val_bsplines_scalar_known_i(t, i, t[i])[:3]
    
    ytri = y[2:-2].copy()

    # also need to evaluate B-splines 0, 1, 2, 3 for second x, and n-4, n-3, n-2, n-1 for second-to-last
    b0, b1, b2, b3 = val_bsplines_scalar_known_i(t, 3, x[1])
    e0, e1, e2, e3 = val_bsplines_scalar_known_i(t, n-1, x[-2])

    # reduce system so these rows aren't there, subtracting them from first and last of tridiagonal
    # first get residual after taking out first and last B-splines...
    by = y[1] - b0*y[0]
    ey = y[-2] - e3*y[-1]

    # now subtract first row to kill first element of first row in Xtri, similarly for last row
    bratio = Xtri[0, 0] / b1
    eratio = Xtri[-1, -1] / e2
    Xtri[0, 1] -= bratio*b2
    Xtri[0, 2] -= bratio*b3
    ytri[0] -= bratio*by
    Xtri[-1, 0] -= eratio*e0
    Xtri[-1, 1] -= eratio*e1
    ytri[-1] -= eratio*ey

    # now inner tridiagonal system ready to be solved
    q[2:-2] = tridiagonal_solve(Xtri.T, ytri, overwrite=True)

    # finally, back out second and second-to-last coefficients
    q[1] = (by - b2*q[2] - b3*q[3])/b1
    q[-2] = (ey - e0*q[-4] - e1*q[-3])/e2
    
    return q


@njit
def tridiagonal_solve(abc, d, overwrite=False):
    """See Wikipedia https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm
    in the second description of Thomas algorithm with 'less bookkeeping'.
    To solve an n=100 tridiagonal system takes about 2.5 microseconds on my CPU."""

    n = len(d)
    a, b, c = abc
    if not overwrite:
        b = b.copy()
        d = d.copy()

    for i in range(1, n):
        w = a[i]/b[i-1]
        b[i] = b[i] - w*c[i-1] 
        d[i] = d[i] - w*d[i-1]
        	    
    x = b
    x[-1] = d[-1]/b[-1]

    for i in range(n-2, -1, -1):
        x[i] = (d[i] - c[i]*x[i+1])/b[i]

    return x