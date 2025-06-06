import numpy as np

import smooth_sim as sm
import utils

def test_basic_calibration():
    # placeholder test to ensure basic functionality remains same, results don't change
    a_grid = utils.discretize_assets(0, 10_000, 200)
    y, pi, Pi = utils.discretize_income(0.92, 0.8, 11)
    beta = 0.95
    r = 0.02
    eis = 1
    sigma = 0.3
    share = 0.8
    ss = sm.steady_state(Pi, a_grid, y, r, beta, eis, sigma, share)
    
    assert np.isclose(ss['A'], 2.7895312553338143)
    assert np.isclose(ss['C'], r*ss['A'] + pi @ y)

