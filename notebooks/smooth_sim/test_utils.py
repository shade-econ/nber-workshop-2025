import numpy as np
import pytest
from scipy.integrate import quad

from utils import integrate_normal_interval, integrate_lognormal_interval, normal_pdf, smooth_weight


"""Test integrate_normal_interval"""

def _reference_normal_integral(f, mu, sigma, x_l, x_h):
    """High-precision ground-truth using scipy.quad."""
    # quad accepts ±np.inf directly
    val, _err = quad(lambda t: f(t) * normal_pdf(t, mu, sigma), x_l, x_h)
    return val

intervals = [
    (0.0, 1.0, -np.inf, np.inf),          # full line
    (0.0, 1.0, -np.inf,  0.8),            # upper tail
    (0.0, 1.0, -0.8,     np.inf),         # lower tail
    (0.0, 1.0, -1.2,     2.1),            # finite
    (2.0, 3.0, -np.inf,  np.inf),         # non-standard μ,σ
]

functions = [
    ("cubic",   lambda z: z**3 - 2*z + 1.3),
    ("quintic", lambda z: z**5 - 3*z**3 + 2*z),
    ("cosine",  lambda z: np.cos(0.3 * z)),      # can't oscillate too much or need more Legendre points
    ("constant",lambda z: 0.*z + 1.0),           # keep a trivial case for sanity
]

@pytest.mark.parametrize("mu, sigma, x_l, x_h", intervals,
                         ids=[f"mu={mu},sigma={s},[{l},{h}]" for mu,s,l,h in intervals])
@pytest.mark.parametrize("fname, func", functions,
                         ids=[f[0] for f in functions])
def test_integral_accuracy(mu, sigma, x_l, x_h, fname, func):
    """Check ∫ f(x) ϕ(x) 1[x∈(x_l,x_h)] dx against SciPy."""
    w, x = integrate_normal_interval(mu, sigma, x_l, x_h)
    approx = np.dot(w, func(x))           # quadrature estimate
    exact  = _reference_normal_integral(func, mu, sigma, x_l, x_h)
    np.testing.assert_allclose(approx, exact, atol=1E-7,
                               err_msg=f"{fname} on interval [{x_l},{x_h}]")


"""Test integrate_lognormal_interval"""

def _reference_lognormal_integral(f, a, mu, sigma, x_l, x_h):
    if x_h <= a:
        return 0.0

    # transform bounds exactly as the implementation does
    z_l = -np.inf if x_l <= a else np.log(x_l - a)
    z_h =  np.inf if np.isinf(x_h) else np.log(x_h - a)

    # --- match integrate_normal_interval’s hard cut-off -------------------
    z_l_clip = max(z_l, mu - 8.0 * sigma)
    z_h_clip = min(z_h, mu + 8.0 * sigma)
    if z_h_clip <= z_l_clip:           # window vanishes
        return 0.0

    val, _ = quad(lambda z: f(a + np.exp(z)) * normal_pdf(z, mu, sigma),
                  z_l_clip, z_h_clip)
    return val


intervals = [
    # (a, mu, sigma, x_l, x_h)
    (0.0, 0.0, 1.0, -np.inf, np.inf),       # whole support
    (0.0, 0.0, 1.0, 1.0,     np.inf),       # lower tail
    (0.0, 0.0, 1.0, -np.inf, 2.0),          # upper tail
    (0.0, 0.0, 1.0, 0.5,     4.0),          # finite
    (1.7, 0.3, 0.8, 1.7,     20.0),         # shifted 'a', full tail
    (1.7, 0.3, 0.8, 4.0,     15.0),         # shifted finite interval
]

functions = [
    ("cubic",      lambda x: x**3 - 2*x + 1.0),
    ("quintic",    lambda x: x**5 - 3*x**3 + 2*x),
    ("reciprocal", lambda x: 1.0 / (x + 1.0)),
    ("constant",   lambda x: 0.*x + 1.0),
]

# ----- master accuracy test -------------------------------------------------
@pytest.mark.parametrize("a, mu, sigma, x_l, x_h", intervals,
                         ids=[f"a={a}|μ={mu},σ={s}|[{l},{h}]"
                              for a,mu,s,l,h in intervals])
@pytest.mark.parametrize("fname, func", functions,
                         ids=[f[0] for f in functions])
def test_lognormal_integral_accuracy(a, mu, sigma, x_l, x_h, fname, func):
    w, x = integrate_lognormal_interval(a, mu, sigma, x_l, x_h)
    approx = np.dot(w, func(x))
    exact  = _reference_lognormal_integral(func, a, mu, sigma, x_l, x_h)
    np.testing.assert_allclose(approx, exact,
                               rtol=1e-9, atol=1e-11,
                               err_msg=f"{fname} on interval [{x_l},{x_h}]")


"""Test smooth_weight"""

@pytest.mark.parametrize("M, n", [(10.0, 201), (7.3, 97)])   # two grid shapes
def test_smooth_weight(M, n):
    x = np.linspace(0.0, M, n)
    w = smooth_weight(x)

    # 1) range and monotonicity
    assert np.all((0.0 <= w) & (w <= 1.0))
    assert np.all(np.diff(w) >= 0.0)

    # 2) flat 0 until M/2  (allow float tol)
    mid_idx = np.searchsorted(x, M/2)
    assert np.allclose(w[:mid_idx], 0.0, atol=0.0)

    # 3) exactly 1 at the right edge
    assert w[-1] == 1.0

    # 4) cubic shape at a single interior point: t=0.3 ⇒ 3t²−2t³
    t = 0.3
    x_test = M/2 + t*(M/2)
    idx = np.searchsorted(x, x_test)
    x_test = x[idx]
    t = (x_test - M/2) / (M/2)
    expected = 3*t**2 - 2*t**3
    np.testing.assert_allclose(w[idx], expected, rtol=1e-12, atol=1e-12)
