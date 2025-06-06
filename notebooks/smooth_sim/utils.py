import numpy as np
from numba import njit

import math
from numpy.polynomial import legendre


"""1. Specific tools needed for smooth model"""

@njit
def integrate_lognormal_interval(a, mu, sigma, x_l, x_h):
    """Give weights w and points x such that evaluating w @ F(x) numerically 
     integrates F(x)*1(x in [x_l, x_h]) if x=y+a, where log y ~ N(mu, sigma^2)"""
    if x_h <= a:
        return np.empty(0), np.empty(0)

    logy_l, logy_h = log_with_inf(x_l - a), log_with_inf(x_h - a)
    w, logy = integrate_normal_interval(mu, sigma, logy_l, logy_h)
    x = a + np.exp(logy)
    return w, x


@njit
def integrate_normal_interval(mu, sigma, x_l, x_h):
    """Give weights w and points x such that evaluating w @ F(x) numerically 
     integrates F(x)*1(x in [x_l, x_h]) if x ~ N(mu, sigma^2)"""
    aquad = max(mu - 8*sigma, x_l)
    bquad = min(mu + 8*sigma, x_h)
    if aquad >= bquad:
        return np.empty(0), np.empty(0)
    else:
        w, x = leg_interval(Leg, aquad, bquad)
        return w * normal_pdf(x, mu, sigma), x
    

@njit
def log_with_inf(x):
    return np.log(x) if x > 0 else -np.inf


@njit
def normal_pdf(x, mu, sigma):
    return np.exp(-((x-mu)/sigma)**2/2)/np.sqrt(2*np.pi)/sigma


@njit
def normal_cdf(x, mu, sigma):
    # can only take scalars
    return 0.5*(1 + math.erf((x-mu)/sigma/np.sqrt(2)))


@njit
def smooth_weight(x_grid):
    """Smooth weights that go from 0 to 1 over grid, flat at 0 until reaching x_grid[-1]/2"""
    M = x_grid[-1]
    w = np.zeros_like(x_grid)
    imid = np.searchsorted(x_grid, M/2)
    t = (x_grid[imid:] - M/2) / (M/2)
    w[imid:] = 3 * t**2 - 2 * t**3
    return w


def get_Pi_F(Pi):
    """Get transition matrix for conditional CDFs from Markov transition matrix Pi"""
    pi = stationary_markov(Pi)

    # since CDFs are conditional on first state, need to normalize
    return Pi.T * pi / pi[:, np.newaxis]


"""2. Standard discretization tools"""

def discretize_assets(amin, amax, n_a):
    # find maximum ubar of uniform grid corresponding to desired maximum amax of asset grid
    ubar = np.log(1 + np.log(1 + amax - amin))
    
    # make uniform grid
    u_grid = np.linspace(0, ubar, n_a)
    
    # double-exponentiate uniform grid and add amin to get grid from amin to amax
    return amin + np.exp(np.exp(u_grid) - 1) - 1


def rouwenhorst_Pi(N, p):
    # base case Pi_2
    Pi = np.array([[p, 1 - p],
                   [1 - p, p]])
    
    # recursion to build up from Pi_2 to Pi_N
    for n in range(3, N + 1):
        Pi_old = Pi
        Pi = np.zeros((n, n))
        
        Pi[:-1, :-1] += p * Pi_old
        Pi[:-1, 1:] += (1 - p) * Pi_old
        Pi[1:, :-1] += (1 - p) * Pi_old
        Pi[1:, 1:] += p * Pi_old
        Pi[1:-1, :] /= 2
        
    return Pi


def stationary_markov(Pi, tol=1E-14):
    # start with uniform distribution over all states
    n = Pi.shape[0]
    pi = np.full(n, 1/n)
    
    # update distribution using Pi until successive iterations differ by less than tol
    for _ in range(10_000):
        pi_new = Pi.T @ pi
        if np.max(np.abs(pi_new - pi)) < tol:
            return pi_new
        pi = pi_new


def discretize_income(rho, sigma, n_e):
    # choose inner-switching probability p to match persistence rho
    p = (1+rho)/2
    
    # start with states from 0 to n_e-1, scale by alpha to match standard deviation sigma
    e = np.arange(n_e)
    alpha = 2*sigma/np.sqrt(n_e-1)
    e = alpha*e
    
    # obtain Markov transition matrix Pi and its stationary distribution
    Pi = rouwenhorst_Pi(n_e, p)
    pi = stationary_markov(Pi)
    
    # e is log income, get income y and scale so that mean is 1
    y = np.exp(e)
    y /= np.vdot(pi, y)
    
    return y, pi, Pi


"""3. Tools for Gauss-Legendre quadrature"""

def leg_start(n):
    return legendre.leggauss(n)

@njit
def leg_interval(S, a, b):
    z, wnorm = S
    x = _demap(z, a, b)
    w = (b-a)/2*wnorm
    return w, x
    
@njit
def _demap(z, a, b):
    """Map z in [-1,1] to x in [a,b]"""
    return (b-a)/2*(z+1) + a

# here, precalculate a single baseline set of nodes and weights
Leg = leg_start(40)