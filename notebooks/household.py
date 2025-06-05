"""Placeholder default household block that we'll use for our internal code"""

import numpy as np
import json

import sequence_jacobian as sj

# household block (TODO: clean up notation to agree with lecture notes)
@sj.het(exogenous='Pi', policy='a', backward='Va', backward_init=sj.hetblocks.hh_sim.hh_init)
def hh(Va_p, a_grid, y, r, beta, eis):
    """Household block. Slightly modify sequence_jacobian.hetblocks.hh_sim.hh to allow for beta vector"""
    uc_nextgrid = beta[:, np.newaxis] * Va_p # beta now vector, multiply Va_prime by row (e state)
    c_nextgrid = uc_nextgrid ** (-eis)
    coh = (1 + r) * a_grid[np.newaxis, :] + y[:, np.newaxis]
    a = sj.interpolate.interpolate_y(c_nextgrid + a_grid, coh, a_grid)
    sj.misc.setmin(a, a_grid[0])
    c = coh - a 
    Va = (1 + r) * c ** (-1 / eis)
    return Va, a, c

# asset grid
a_grid = sj.grids.asset_grid(amin=0, amax=4000, n=400)

# prespecify endowment process
rho_e = 0.91**(1/4)     # annual rho=0.91 from IKC
sd_e = 0.92             # cross-sectional sd from IKC  
e_grid, pi_e, Pi_e = sj.utilities.discretize.markov_rouwenhorst(rho_e, sd_e, 11)

# prespecify beta process (but not betas themselves)
q = 0.01        # draw new beta every 25 years
pi_b = np.array([1/4, 1/4, 1/4, 1/4])
Pi_b = (1-q)*np.eye(4) + q*np.outer(np.ones(4), pi_b)

Pi = np.kron(Pi_b, Pi_e)
pi = np.kron(pi_b, pi_e)
e_grid = np.kron(np.ones(4), e_grid)

# hetinputs and full hetblock
def income(Z, e_grid):
    y = Z * e_grid
    return y

def make_beta(beta_hi, dbeta):
    beta = np.kron(np.array([beta_hi-3*dbeta, beta_hi-2*dbeta, beta_hi-dbeta, beta_hi]), np.ones(len(pi_e)))
    return beta

hh = hh.add_hetinputs([income, make_beta])

# basic calibration
calibration = dict(r=0.02/4, Z=0.7, eis=1, Pi=Pi, a_grid=a_grid, e_grid=e_grid)

# get betas 
try:
    with open('betas.json') as f:
        beta_dict = json.load(f)
except:
    # temporarily hardcode in here
    beta_dict = {
        "beta_hi": 1.0022891146652246,
        "dbeta": 0.019263625332690423
    }
calibration |= beta_dict

