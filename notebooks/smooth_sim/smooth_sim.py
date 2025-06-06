import numpy as np
from numba import njit
from scipy import interpolate

from . import spline, utils

# TODO: can make code more efficient, e.g. by replacing Gauss-Legendre with Gauss-Hermite in unbounded case
# or by feeding query points more intelligently to spline.val_monotonic

"""Backward iteration and steady-state policy and value function"""

@njit
def backward_iteration(Va, Pi, a_grid, y, r, beta, eis, sigma, share):
    # Part 1: standard dicounting and expectation step
    Wa = beta * Pi @ Va

    # Part 2: mapping from endogenous coh grid to consumption (constrained below coh_endog[0])
    c_endog = Wa**(-eis)
    coh_endog = c_endog + a_grid
    
    q = np.empty_like(Va)
    for s in range(len(y)):
        q[s] = spline.interp(coh_endog[s], c_endog[s])

    # Part 3: integrate over lognormal part of income to get Va(s, a)
    coh_certain, coh_lognormal_mu = coh_components(a_grid, y, r, sigma, share)

    Va = np.empty_like(Va)
    for s in range(len(y)):
        for a in range(len(a_grid)):
            Va[s, a] = expectation_lognormal_coh(coh_certain[s, a], 
                            coh_endog[s], q[s], coh_lognormal_mu[s], sigma, eis)
        
    # Scale by 1+r to reflect returns
    Va *= (1+r)

    return Va, (q, coh_endog)


@njit
def coh_components(a_grid, y, r, sigma, share):
    coh_certain = (1+r)*a_grid + (1-share)*y[:, np.newaxis] # not including lognormal part
    coh_lognormal_mu = -sigma**2/2 + np.log(share*y)        # mean of log coh above coh_certain
    return coh_certain, coh_lognormal_mu


@njit
def expectation_lognormal_coh(coh_certain, coh_grid, q, mu, sigma, eis):
    """Take expectations of marg utility at coh_certain over lognormal part
    of cash-on-hand, given spline q on coh_grid for unconstrained consumption"""
    # constrained part: marginal utility is coh**(-1/eis)
    w, x = utils.integrate_lognormal_interval(coh_certain, mu, sigma, 0, coh_grid[0])
    constrained_part = w @ x**(-1/eis)

    # unconstrained part: marginal utility is q(coh)**(-1/eis)
    w, x = utils.integrate_lognormal_interval(coh_certain, mu, sigma, coh_grid[0], np.inf)
    unconstrained_part = w @ spline.val_monotonic(q, coh_grid, x)**(-1/eis)

    return constrained_part + unconstrained_part


def policy_ss(Pi, a_grid, y, r, beta, eis, sigma, share, tol=1E-9, Va_shock=0):
    # arbitrary initial guess for consumption, use standard
    c_init = 0.05 * (y[:, np.newaxis] + a_grid)
    Va = c_init**(-1/eis)

    # iterate until maximum distance between two iterations, as measured by coh_endog, falls below tol
    for it in range(10_000):
        Va, (q, coh_endog) = backward_iteration(Va + Va_shock, Pi, a_grid, y, r, beta, eis, sigma, share)
        if it > 0 and np.max(np.abs(coh_endog - coh_endog_old)) < tol:
            break
        coh_endog_old = coh_endog
    else:
        raise ValueError(f"Policy failed to converge after {it} iterations")
    return Va, (q, coh_endog)


"""Forward iteration and steady-state distribution"""

def forward_iteration(F, coh_endog, Pi_F, a_grid, y, r, sigma, share):
    return Pi_F @ forward_policy(F, coh_endog, a_grid, y, r, sigma, share)


@njit
def forward_policy(F, coh_endog, a_grid, y, r, sigma, share):
    coh_certain, coh_lognormal_mu = coh_components(a_grid, y, r, sigma, share)

    Fnew = np.empty_like(F)
    for s in range(len(y)):
        qF = spline.interp(a_grid, F[s])
        # get CDF on coh_endog, which maps directly to CDF on assets
        Fnew[s] = iteration_lognormal_coh(qF, coh_certain[s], coh_endog[s], coh_lognormal_mu[s], sigma)

    # ensure that near the top of the distribution, we have exactly 1
    w = utils.smooth_weight(a_grid)
    Fnew = (1-w)*Fnew + w
        
    return Fnew


@njit
def iteration_lognormal_coh(qF, coh_certain, coh_endog, mu, sigma):
    """Iterate forward distribution from CDF spline qF on coh_certain,
    integrating over lognormal part of cash-on-hand to get CDF on coh_endog"""
    Fnew = np.zeros_like(coh_endog)
    for i, coh in enumerate(coh_endog):
        if coh >= coh_certain[0]:
            w, x = utils.integrate_lognormal_interval(coh_certain[0], mu, sigma, coh_certain[0], coh)
            Fvals = spline.val_monotonic(qF, coh_certain, (coh + coh_certain[0] - x)[::-1])[::-1].copy()
            Fnew[i] = w @ Fvals

    return Fnew


def distribution_ss(coh_endog, Pi, a_grid, y, r, sigma, share, tol=1E-11, maxit=10_000):
    F = np.ones_like(coh_endog)     # initialize to everyone at constraint
    Pi_F = utils.get_Pi_F(Pi)       # transition matrix for conditional CDFs
    
    # iterate until maximum distance between two iterations falls below tol
    for it in range(maxit):
        Fnew = forward_iteration(F, coh_endog, Pi_F, a_grid, y, r, sigma, share)
        if it > 0 and np.max(np.abs(Fnew - F)) < tol:
            break
        F = Fnew
    else:
        raise ValueError(f"Distribution failed to converge after {it} iterations")
    return F


def aggregate_assets_by_state(F, a_grid):
    """What are aggregate assets for each state s, given CDF F on a_grid?"""
    return np.array([interpolate.CubicSpline(a_grid, 1-F[yi])
                        .integrate(0, a_grid[-1]) for yi in range(F.shape[0])])


"""High-level convenience functions"""

def steady_state(Pi, a_grid, y, r, beta, eis, sigma, share, backward_tol=1E-9, forward_tol=1E-11, Va_shock=0):
    Va, (q, coh_endog) = policy_ss(Pi, a_grid, y, r, beta, eis, sigma, share, tol=backward_tol, Va_shock=Va_shock)
    
    F = distribution_ss(coh_endog, Pi, a_grid, y, r, sigma, share, tol=forward_tol)

    pi = utils.stationary_markov(Pi)
    As = aggregate_assets_by_state(F, a_grid)
    Cs = r * As + y
    A, C = pi @ As, pi @ Cs
    return dict(Va=Va, q_policy=q, coh_endog=coh_endog, pi=pi, F=F, A=A, C=C)


def get_policies(q, coh_endog):
    """Return consumption and assets as functions of state s and cash-on-hand coh"""
    def c(s, coh):
        return (coh > coh_endog[s, 0])*spline.val_monotonic(q[s], coh_endog[s], coh) + (coh <= coh_endog[s, 0])*coh
    def a(s, coh):
        return (coh > coh_endog[s, 0])*(coh - spline.val_monotonic(q[s], coh_endog[s], coh))
    return c, a
