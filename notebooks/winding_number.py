import numpy as np
import matplotlib.pyplot as plt
from numba import njit


def winding_number(j, K=8192, plot=False, **kwargs):
    """Convenience routine for notebook"""
    e = sample_values_simple(j, K)
    if plot:
        plt.plot(e.real, e.imag, color='C0', **kwargs)
        # add arrows at beginning and middle to show direction
        for i in (0, K//2):
            rdir, idir = e.real[i + 1] - e.real[i], e.imag[i + 1] - e.imag[i]
            rdir, idir = rdir / np.hypot(rdir, idir) * 0.01, idir / np.hypot(rdir, idir) * 0.01
            plt.arrow(e.real[i]-rdir, e.imag[i]-idir, 2*rdir, 2*idir,
                        head_width=0.05, head_length=0.2, fc='C0', ec='C0', zorder=10)
        plt.plot([0], [0], marker='o', markersize=5, color="red")
    return winding_number_of_path(e.real, e.imag)


def sample_values_simple(j, K=8192):
    """Evaluate Laurent polynomial j(z) (with equally many
    positive and negative powers) counterclockwise at K evenly
    spaced roots of unity z, wrapping back around to z=1"""
    # j is (2*T-1,) array of Laurent coeffs (powers from -(T-1) to T-1)
    assert (K % 2 == 0) and (len(j) % 2 == 1) and (K > len(j))
    T = len(j) // 2 + 1

    # center j(z) at K/2, fill rest with zeros
    jhat = np.zeros(K)
    jhat[(K//2 - (T - 1)):(K//2 + T)] = j

    # take FFT of jhat to evaluate z^(K/2)*j(z) at clockwise roots of unity
    x = np.fft.fft(jhat)

    # divide by z^(K/2), which is alternating 1, -1 at roots of unity
    alt = np.tile([1, -1], K//2)
    x *= alt

    # return wrapped back to z=1, reversed to make counterclockwise
    return np.concatenate((x, [x[0]]))[::-1]


def sample_values(j, K=8192):
    """Like sample_values_simple, but evaluating det j(z) for block j,
    also using conjugate symmetry for efficiency"""
    # j is 2*T-1 or (2*T-1, n, n) array of Laurent polynomial coefficients
    assert (K % 2 == 0) and (len(j) % 2 == 1) and (K > len(j))
    T = len(j) // 2 + 1
    if j.ndim == 3: assert j.shape[1] == j.shape[2]

    # center j(z) at K/2, fill rest with zeros
    jhat = np.zeros((K, *j.shape[1:])) if j.ndim == 3 else np.zeros(K)
    jhat[(K//2 - (T - 1)):(K//2 + T)] = j

    # take FFT to evaluate z^(K/2)*j(z) at clockwise roots of unity
    # rfft only computes for K/2+1 roots with non-positive imag part
    x = np.fft.rfft(jhat, axis=0)

    # divide by z^(K/2), which is alternating 1, -1 at roots of unity
    alt = np.tile([1, -1], K//2+1)[:K//2+1]
    if j.ndim == 3:
        x = np.linalg.det(x*alt[:, np.newaxis, np.newaxis])
    else:
        x *= alt

    # use conjugate symmetry to fill in roots, go counterclockwise
    return np.concatenate((x.conj(), x[:-1][::-1]))


@njit
def winding_number_of_path(x, y):
    """Compute winding number around origin of (x,y) coordinates that make closed path by
    counting number of counterclockwise crossings of ray from (0,0) -> (infty,0) on x axis"""
    assert x[-1] == x[0] and y[-1] == y[0]  # path must be closed
    w = 0                                   # winding number
    s = (y[0] >= 0)                         # current sign of y

    for k in range(1, len(x)):
        if (y[k] >= 0) != s:
            # s changed, so moved across x-axis, possible crossing of ray
            s = (y[k] >= 0)

            if x[k] > 0 and x[k - 1] > 0:
                # definite crossing, increment w if s increased and vice versa
                w += 2 * s - 1
            elif not (x[k] <= 0 and x[k - 1] <= 0):
                # ruled out x_k, x_(k-1) <= 0, where there is no crossing
                # ambiguous case, analytically check if segment crosses right or left of origin
                crossed_on_right = (x[k - 1] * y[k] - x[k] * y[k - 1]) / (y[k] - y[k - 1])
                if crossed_on_right > 0:
                    w += 2 * s - 1
    return w
