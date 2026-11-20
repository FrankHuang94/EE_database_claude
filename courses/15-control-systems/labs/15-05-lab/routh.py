"""Lab 15-05 helpers: the Routh array, with both special cases, and stability counts.

    routh(coeffs, eps=1e-9)   Routh array rows and notes on special cases
    rhp_count(coeffs)         number of right-half-plane roots from the first column's sign changes
    jw_roots(coeffs)          imaginary-axis roots found through an auxiliary polynomial (if any)
    gain_range(char_of_K, ...) the interval of K for which a characteristic polynomial is stable (by scanning)

Coefficients are highest power first. The array is built exactly as in the chapter (section 3.3):
  row k+2 entry j = (r1[0] * r0[j+1] - r0[0] * r1[j+1]) / r1[0]
A zero first element is replaced by a small positive eps (special case 1); an all-zero row is replaced by the
derivative of the auxiliary polynomial formed from the row above it (special case 2).
"""
from __future__ import annotations

import numpy as np


def routh(coeffs, eps=1e-9):
    c = np.trim_zeros(np.asarray(coeffs, dtype=float), "f")
    n = len(c) - 1
    width = n // 2 + 1
    rows = [np.zeros(width), np.zeros(width)]
    rows[0][: len(c[0::2])] = c[0::2]
    rows[1][: len(c[1::2])] = c[1::2]
    notes = []
    aux = None
    for k in range(2, n + 1):
        r0, r1 = rows[k - 2], rows[k - 1]
        if np.all(np.abs(r1) < 1e-12):
            # special case 2: auxiliary polynomial from r0 (power n-k+2, even/odd powers stepping by 2)
            p = n - k + 2
            aux_c = np.zeros(p + 1)
            aux_c[0::2] = r0[: p // 2 + 1]
            aux = aux_c
            der = np.polyder(aux_c)
            r1 = np.zeros(width)
            r1[: len(der[0::2])] = der[0::2]
            rows[k - 1] = r1
            notes.append(f"row s^{n - k + 1} was all zero: replaced by d/ds of auxiliary {np.round(aux_c, 6).tolist()}")
        if abs(r1[0]) < 1e-12:
            r1 = r1.copy()
            r1[0] = eps
            rows[k - 1] = r1
            notes.append(f"row s^{n - k + 1} had a zero first element: replaced by eps")
        new = np.zeros(width)
        for j in range(width - 1):
            new[j] = (r1[0] * r0[j + 1] - r0[0] * r1[j + 1]) / r1[0]
        rows.append(new)
    if abs(rows[n][0]) < 1e-12 and n >= 1:
        notes.append("last row is zero")
    return rows, notes, aux


def first_column(coeffs, eps=1e-9):
    rows, _, _ = routh(coeffs, eps)
    return np.array([r[0] for r in rows])


def rhp_count(coeffs, eps=1e-9):
    """Sign changes in the first column = number of roots with positive real part."""
    col = first_column(coeffs, eps)
    signs = np.sign(col)
    return int(np.sum(signs[1:] * signs[:-1] < 0))


def jw_roots(coeffs, eps=1e-9):
    """Roots of the auxiliary polynomial (on the imaginary axis when the array has no further sign changes)."""
    _, _, aux = routh(coeffs, eps)
    return None if aux is None else np.roots(aux)


def is_stable(coeffs):
    """Routh test: stable iff every first-column entry is strictly positive and no special case occurred."""
    rows, notes, _ = routh(coeffs)
    col = np.array([r[0] for r in rows])
    return bool(not notes and np.all(col > 0))


def gain_range(char_of_K, K_lo, K_hi, n=20001):
    """Scan K over [K_lo, K_hi] and return (first stable K, last stable K) of the first stable interval."""
    Ks = np.linspace(K_lo, K_hi, n)
    ok = [bool(np.all(np.roots(char_of_K(K)).real < 0)) for K in Ks]
    idx = np.flatnonzero(ok)
    return (Ks[idx[0]], Ks[idx[-1]]) if idx.size else None
