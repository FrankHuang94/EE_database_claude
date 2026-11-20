"""Lab 15-10 helpers: state-space analysis and design with plain numpy/scipy.

    ctrb(A, B), obsv(A, C)           controllability and observability matrices
    acker(A, B, poles)               state-feedback gain K (single input) by Ackermann's formula
    observer_gain(A, C, poles)       observer gain L (single output), by duality with acker
    tf_of(A, B, C, D=0)              (num, den) of C (sI - A)^-1 B + D
    augment_integral(A, B, C)        plant augmented with the integral of the tracking error
    closed_loop_response(...)        response of a closed-loop state model (state feedback, observer, augmentation)
                                     to a reference step from an initial state, by the matrix exponential

Everything is linear, so simulations use the exact discretization x[k+1] = Ad x[k] + Bd u[k] for piecewise-constant
inputs, or the matrix exponential of the whole closed-loop system.
"""
from __future__ import annotations

import numpy as np
from scipy import signal
from scipy.linalg import expm


def ctrb(A, B):
    A, B = np.atleast_2d(A), np.atleast_2d(B).reshape(len(A), -1)
    cols = [B]
    for _ in range(len(A) - 1):
        cols.append(A @ cols[-1])
    return np.hstack(cols)


def obsv(A, C):
    return ctrb(np.atleast_2d(A).T, np.atleast_2d(C).T).T


def acker(A, B, poles):
    """K such that eig(A - B K) = poles, for a single-input controllable pair (Ackermann's formula)."""
    A = np.atleast_2d(np.asarray(A, float))
    n = len(A)
    Wc = ctrb(A, B)
    coeffs = np.real(np.poly(poles))           # desired characteristic polynomial
    phiA = np.zeros_like(A)
    for c in coeffs:
        phiA = phiA @ A + c * np.eye(n)          # Horner evaluation of phi(A)
    e = np.zeros((1, n))
    e[0, -1] = 1.0
    return e @ np.linalg.solve(Wc, phiA)


def observer_gain(A, C, poles):
    """L such that eig(A - L C) = poles (duality: acker on (A^T, C^T))."""
    return acker(np.asarray(A, float).T, np.asarray(C, float).reshape(-1, 1), poles).T


def tf_of(A, B, C, D=0.0):
    num, den = signal.ss2tf(np.asarray(A, float), np.asarray(B, float).reshape(len(A), -1),
                            np.asarray(C, float).reshape(1, -1), np.atleast_2d(D))
    return np.trim_zeros(num[0], "f"), den


def augment_integral(A, B, C):
    """States [x; xi] with xi' = r - C x: returns (Aa, Ba, Br) so that d/dt [x; xi] = Aa [x; xi] + Ba u + Br r."""
    A, B, C = np.atleast_2d(A), np.asarray(B, float).reshape(-1, 1), np.asarray(C, float).reshape(1, -1)
    n = len(A)
    Aa = np.block([[A, np.zeros((n, 1))], [-C, np.zeros((1, 1))]])
    Ba = np.vstack([B, [[0.0]]])
    Br = np.vstack([np.zeros((n, 1)), [[1.0]]])
    return Aa, Ba, Br


def closed_loop_response(Acl, Bcl, Ccl, x0, t, r=1.0):
    """y(t) of x' = Acl x + Bcl r (constant r) from x0, exactly, on the time grid t."""
    n = len(Acl)
    M = np.zeros((n + 1, n + 1))
    M[:n, :n] = Acl
    M[:n, n:] = np.asarray(Bcl, float).reshape(-1, 1) * r
    z0 = np.concatenate([np.asarray(x0, float), [1.0]])
    ys, xs = [], []
    for tk in t:
        z = expm(M * tk) @ z0
        xs.append(z[:n])
        ys.append(float((np.asarray(Ccl, float).reshape(1, -1) @ z[:n])[0]))
    return np.array(ys), np.array(xs)
