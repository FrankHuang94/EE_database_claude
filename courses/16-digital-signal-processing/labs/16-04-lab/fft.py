"""FFT toolkit for Lab 16-04: radix-2 FFTs written out butterfly by butterfly, with operation counters.

Functions
- bit_reverse(n, bits)          the bit-reversed index
- fft_recursive(x)              decimation in time, written as the recursion of section 3.2
- fft_dit(x, count=None)        iterative in-place radix-2 DIT: bit-reversed input, natural-order output
- fft_dif(x)                    iterative in-place radix-2 DIF: natural input, bit-reversed output (then reordered)
- ifft_via_fft(X)               inverse FFT by conjugation: conj(FFT(conj(X)))/N
- two_real_ffts(a, b)           FFTs of two real sequences with one complex FFT
- twiddle_counts(N)             butterflies, all twiddle multiplies, and non-trivial ones (not 1 or -j)
- fft8_fixed(x)                 the 8-point Q1.15 fixed-point FFT of fft8.v, bit-exact (scaled by 1/2 per stage)

`count`, if given, is a dict whose keys 'butterflies', 'cmul', 'cmul_nontrivial' are incremented.
"""
from __future__ import annotations

import math

import numpy as np


def bit_reverse(n, bits):
    r = 0
    for _ in range(bits):
        r = (r << 1) | (n & 1)
        n >>= 1
    return r


def fft_recursive(x):
    x = np.asarray(x, complex)
    N = len(x)
    if N == 1:
        return x.copy()
    if N % 2:
        raise ValueError("length must be a power of 2")
    G = fft_recursive(x[0::2])
    H = fft_recursive(x[1::2])
    W = np.exp(-2j * np.pi * np.arange(N // 2) / N)
    return np.concatenate([G + W * H, G - W * H])


def _is_trivial(k, N):
    """W_N^k equal to 1 or -j (multiplying by these costs no real multiply)."""
    return k % N == 0 or (4 * k) % N == 0 and (4 * k) // N % 4 == 1


def fft_dit(x, count=None):
    x = np.asarray(x, complex)
    N = len(x)
    m = int(round(math.log2(N)))
    if 1 << m != N:
        raise ValueError("length must be a power of 2")
    a = np.array([x[bit_reverse(i, m)] for i in range(N)])
    size = 2
    while size <= N:
        half = size // 2
        for start in range(0, N, size):
            for j in range(half):
                k = j * (N // size)                 # twiddle W_N^k = W_size^j
                w = np.exp(-2j * np.pi * k / N)
                t = w * a[start + j + half]
                u = a[start + j]
                a[start + j] = u + t
                a[start + j + half] = u - t
                if count is not None:
                    count["butterflies"] = count.get("butterflies", 0) + 1
                    count["cmul"] = count.get("cmul", 0) + 1
                    if not _is_trivial(k, N):
                        count["cmul_nontrivial"] = count.get("cmul_nontrivial", 0) + 1
        size *= 2
    return a


def fft_dif(x):
    a = np.asarray(x, complex).copy()
    N = len(a)
    m = int(round(math.log2(N)))
    size = N
    while size >= 2:
        half = size // 2
        for start in range(0, N, size):
            for j in range(half):
                w = np.exp(-2j * np.pi * j / size)
                u, v = a[start + j], a[start + j + half]
                a[start + j] = u + v
                a[start + j + half] = (u - v) * w
        size //= 2
    return np.array([a[bit_reverse(i, m)] for i in range(N)])


def ifft_via_fft(X):
    X = np.asarray(X, complex)
    return np.conj(fft_dit(np.conj(X))) / len(X)


def two_real_ffts(a, b):
    """With z = a + jb: A[k] = (Z[k] + Z*[N-k])/2 and B[k] = (Z[k] - Z*[N-k])/(2j)."""
    z = np.asarray(a, float) + 1j * np.asarray(b, float)
    Z = fft_dit(z)
    N = len(Z)
    Zr = np.conj(Z[(-np.arange(N)) % N])
    return (Z + Zr) / 2, (Z - Zr) / 2j


def twiddle_counts(N):
    c = {}
    fft_dit(np.zeros(N), count=c)
    return c.get("butterflies", 0), c.get("cmul", 0), c.get("cmul_nontrivial", 0)


# ------------------------------------------------------------------------- fixed point (matches fft8.v)
Q = 15
TW8 = [(round(math.cos(2 * math.pi * k / 8) * (1 << Q)), round(-math.sin(2 * math.pi * k / 8) * (1 << Q))) for k in range(4)]
TW8 = [(min(v, (1 << Q) - 1), min(w, (1 << Q) - 1)) for v, w in TW8]   # 1.0 is not representable in Q1.15


def _sat16(v):
    return max(-32768, min(32767, v))


def _cmul_q15(br, bi, wr, wi):
    """(br + j bi)(wr + j wi) with 32-bit products, rounded back to Q1.15 by adding 2^14 and shifting right 15."""
    pr = br * wr - bi * wi
    pi = br * wi + bi * wr
    return (pr + (1 << (Q - 1))) >> Q, (pi + (1 << (Q - 1))) >> Q


SAT_EVENTS = [0]     # incremented whenever a butterfly output saturates (for the lab and the test vectors)
SAT_POS = [0]        # ... at +32767
SAT_NEG = [0]        # ... at -32768


def _sat_count(v):
    if v > 32767 or v < -32768:
        SAT_EVENTS[0] += 1
        if v > 32767:
            SAT_POS[0] += 1
        else:
            SAT_NEG[0] += 1
    return _sat16(v)


def _bfly(ar, ai, br, bi, k):
    wr, wi = TW8[k]
    tr, ti = _cmul_q15(br, bi, wr, wi)
    # sum and difference in 19 bits, scale by 1/2 (arithmetic shift: floor), saturate to 16 bits; saturation is
    # needed because a component can grow by 1 + sqrt(2) in one stage, more than the factor of 2 the shift removes
    return _sat_count((ar + tr) >> 1), _sat_count((ai + ti) >> 1), _sat_count((ar - tr) >> 1), _sat_count((ai - ti) >> 1)


def fft_fixed(x, bits=16):
    """Radix-2 DIT FFT in bits-bit fixed point with 1/2 scaling per stage (no saturation), returning X/N as floats.

    Same arithmetic as fft8_fixed for any power-of-two N: Q1.(bits-1) twiddles rounded (1.0 clamped to the largest
    code), each twiddle product rounded (add half an LSB, floor-shift), each butterfly output floor-shifted by one.
    Inputs must keep every component inside the representable range (no saturation is modelled)."""
    x = np.asarray(x, dtype=complex)
    N = len(x)
    m = int(round(math.log2(N)))
    S = 2 ** (bits - 1)
    order = [bit_reverse(i, m) for i in range(N)]
    ar = np.round(x.real * S).astype(np.int64)[order]
    ai = np.round(x.imag * S).astype(np.int64)[order]
    for s in range(1, m + 1):
        size, half = 2**s, 2 ** (s - 1)
        k = np.arange(half)
        wr = np.minimum(np.round(np.cos(2 * np.pi * k / size) * S).astype(np.int64), S - 1)
        wi = np.round(-np.sin(2 * np.pi * k / size) * S).astype(np.int64)
        ar, ai = ar.reshape(-1, size), ai.reshape(-1, size)
        br, bi = ar[:, half:], ai[:, half:]
        tr = (br * wr - bi * wi + S // 2) // S
        ti = (br * wi + bi * wr + S // 2) // S
        nr = np.concatenate([(ar[:, :half] + tr) >> 1, (ar[:, :half] - tr) >> 1], axis=1)
        ni = np.concatenate([(ai[:, :half] + ti) >> 1, (ai[:, :half] - ti) >> 1], axis=1)
        ar, ai = nr.reshape(-1), ni.reshape(-1)
    return (ar + 1j * ai) / S


def fft8_fixed(xr, xi):
    """Bit-exact model of fft8.v: 16-bit signed real and imaginary inputs, three radix-2 DIT stages, each output
    scaled by 1/2, so the result approximates DFT/8. Returns (Xr, Xi) lists in natural order."""
    order = [bit_reverse(i, 3) for i in range(8)]
    ar = [xr[i] for i in order]
    ai = [xi[i] for i in order]
    for size in (2, 4, 8):
        half = size // 2
        nr, ni = ar[:], ai[:]
        for start in range(0, 8, size):
            for j in range(half):
                k = j * (8 // size)
                p, q = start + j, start + j + half
                nr[p], ni[p], nr[q], ni[q] = _bfly(ar[p], ai[p], ar[q], ai[q], k)
        ar, ai = nr, ni
    return ar, ai
