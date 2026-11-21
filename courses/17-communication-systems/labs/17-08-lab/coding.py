"""Channel coding toolkit for the 17-08 lab.

- GF(2) linear algebra: matrix products, rank, null space (generator from a parity-check matrix);
- linear block codes: Hamming codes in systematic form, weight distributions, syndrome decoding;
- CRCs by polynomial long division, with the NR generator polynomials of TS 38.212;
- bounded-distance block error rates on a binary symmetric channel and Reed-Solomon codeword error rates;
- rate-1/n convolutional codes: encoder, hard- and soft-decision Viterbi decoder, distance spectrum
  from the state diagram, and the union bound on bit-error rate;
- a regular LDPC code (Gallager construction) with a normalized min-sum decoder;
- polar codes: BEC polarization, encoder and successive-cancellation decoder.

Bits are numpy uint8 arrays. BPSK maps bit b to 1 - 2b, so a positive LLR favours 0.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.stats import binom, norm

Q = norm.sf


# ------------------------------------------------------------------ GF(2) linear algebra
def gf2_matmul(a, b):
    return (np.asarray(a, np.int64) @ np.asarray(b, np.int64)) % 2


def gf2_rref(m):
    """Reduced row-echelon form over GF(2); returns (matrix, pivot columns)."""
    a = np.array(m, np.uint8) % 2
    rows, cols = a.shape
    pivots, r = [], 0
    for c in range(cols):
        hits = np.flatnonzero(a[r:, c]) + r
        if len(hits) == 0:
            continue
        a[[r, hits[0]]] = a[[hits[0], r]]
        for i in np.flatnonzero(a[:, c]):
            if i != r:
                a[i] ^= a[r]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return a, pivots


def gf2_rank(m):
    return len(gf2_rref(m)[1])


def gf2_nullspace(h):
    """Basis (rows) of {x : H x = 0} over GF(2): a generator matrix for the code with parity checks H."""
    a, piv = gf2_rref(h)
    n = a.shape[1]
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        x = np.zeros(n, np.uint8)
        x[f] = 1
        for r, p in enumerate(piv):
            x[p] = a[r, f]
        basis.append(x)
    return np.array(basis, np.uint8)


# ------------------------------------------------------------------ block codes
def hamming(r):
    """Systematic Hamming code of length 2^r - 1: returns (G, H) with G = [I | P], H = [P^T | I]."""
    n, k = 2**r - 1, 2**r - 1 - r
    cols = [c for c in range(1, n + 1) if c & (c - 1)]  # non-powers of two: the data columns
    P = np.array([[(c >> (r - 1 - j)) & 1 for j in range(r)] for c in cols], np.uint8)  # k x r
    G = np.hstack([np.eye(k, dtype=np.uint8), P])
    H = np.hstack([P.T, np.eye(r, dtype=np.uint8)])
    return G, H


HAMMING_74_P = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]], np.uint8)


def hamming74():
    """The (7,4) code used in the chapter: p1 = d1+d2+d4, p2 = d1+d3+d4, p3 = d2+d3+d4."""
    G = np.hstack([np.eye(4, dtype=np.uint8), HAMMING_74_P])
    H = np.hstack([HAMMING_74_P.T, np.eye(3, dtype=np.uint8)])
    return G, H


def encode_block(msg, G):
    return gf2_matmul(np.atleast_2d(msg), G).astype(np.uint8)


def all_codewords(G):
    k = G.shape[0]
    msgs = ((np.arange(2**k)[:, None] >> np.arange(k - 1, -1, -1)) & 1).astype(np.uint8)
    return encode_block(msgs, G)


def weight_distribution(G):
    w = all_codewords(G).sum(axis=1)
    return np.bincount(w, minlength=G.shape[1] + 1)


def min_distance(G):
    w = all_codewords(G).sum(axis=1)
    return int(w[w > 0].min())


def syndrome(r, H):
    return gf2_matmul(np.atleast_2d(r), H.T).astype(np.uint8)


def syndrome_decode(r, H):
    """Single-error correction: flip the bit whose column of H equals the syndrome."""
    r = np.array(r, np.uint8).copy()
    s = syndrome(r, H)[0]
    if s.any():
        hit = np.flatnonzero((H.T == s).all(axis=1))
        if len(hit):
            r[hit[0]] ^= 1
    return r


def block_error_bsc(n, t, p):
    """Probability that more than t of n bits are in error (bounded-distance decoding failure)."""
    return float(binom.sf(t, n, p))


def rs_codeword_error(n, k, m, ber):
    """Reed-Solomon (n, k) over GF(2^m), t = (n - k)/2, with independent bit errors of rate ber."""
    t = (n - k) // 2
    q = -math.expm1(m * math.log1p(-ber))  # symbol error probability 1 - (1 - ber)^m
    return float(binom.sf(t, n, q))


def rs_burst_bits(t, m):
    """Longest bit burst that always touches at most t symbols of m bits (worst-case alignment)."""
    return (t - 1) * m + 1


# ------------------------------------------------------------------ CRC
NR_CRC = {  # TS 38.212 V19.4.0 clause 5.1: exponents of each generator polynomial
    "CRC24A": [24, 23, 18, 17, 14, 11, 10, 7, 6, 5, 4, 3, 1, 0],
    "CRC24B": [24, 23, 6, 5, 1, 0],
    "CRC24C": [24, 23, 21, 20, 17, 15, 13, 12, 8, 4, 2, 1, 0],
    "CRC16": [16, 12, 5, 0],
    "CRC11": [11, 10, 9, 5, 0],
    "CRC6": [6, 5, 0],
}


def poly_bits(exponents):
    """Coefficient bits, highest power first, from a list of exponents."""
    deg = max(exponents)
    b = np.zeros(deg + 1, np.uint8)
    for e in exponents:
        b[deg - e] = 1
    return b


def crc_remainder(msg, gen):
    """Remainder of msg(x) * x^r divided by gen(x) over GF(2); gen as bits, highest power first."""
    gen = np.array(gen, np.uint8)
    r = len(gen) - 1
    work = np.concatenate([np.array(msg, np.uint8), np.zeros(r, np.uint8)])
    for i in range(len(msg)):
        if work[i]:
            work[i : i + r + 1] ^= gen
    return work[-r:]


def crc_append(msg, gen):
    return np.concatenate([np.array(msg, np.uint8), crc_remainder(msg, gen)])


def crc_check(word, gen):
    """True if the whole word (message followed by check bits) divides evenly by gen."""
    gen = np.array(gen, np.uint8)
    r = len(gen) - 1
    work = np.array(word, np.uint8).copy()
    for i in range(len(work) - r):
        if work[i]:
            work[i : i + r + 1] ^= gen
    return not work[-r:].any()


# ------------------------------------------------------------------ convolutional codes
def _taps(gens_octal, K):
    return [int(str(g), 8) for g in gens_octal], K


def conv_encode(bits, gens_octal, K, terminate=True):
    """Rate-1/n feed-forward encoder; the generator's MSB taps the current input bit."""
    gens, _ = _taps(gens_octal, K)
    u = np.concatenate([np.array(bits, np.uint8), np.zeros(K - 1 if terminate else 0, np.uint8)])
    state, out = 0, []
    for b in u:
        reg = (int(b) << (K - 1)) | state
        out.extend(bin(reg & g).count("1") & 1 for g in gens)
        state = reg >> 1
    return np.array(out, np.uint8)


def _trellis(gens_octal, K):
    gens, _ = _taps(gens_octal, K)
    S = 2 ** (K - 1)
    n = len(gens)
    # for each next state: the two predecessor states, the input bit, and the branch outputs
    pred = np.zeros((S, 2), np.int64)
    outs = np.zeros((S, 2, n), np.uint8)
    for ns in range(S):
        u = ns >> (K - 2) if K > 1 else 0
        for b in range(2):
            ps = ((ns << 1) & (S - 1)) | b
            reg = (u << (K - 1)) | ps
            pred[ns, b] = ps
            outs[ns, b] = [bin(reg & g).count("1") & 1 for g in gens]
    return pred, outs, S, n


def viterbi(rx, gens_octal, K, soft=True, terminated=True):
    """Maximum-likelihood sequence decoding.

    rx: soft values (BPSK 1 - 2c plus noise) if soft, else hard bits. Returns the decoded
    information bits (tail removed when terminated).
    """
    pred, outs, S, n = _trellis(gens_octal, K)
    rx = np.asarray(rx, float).reshape(-1, n)
    T = rx.shape[0]
    sym = 1.0 - 2.0 * outs  # S x 2 x n, BPSK images of the branch outputs
    metric = np.full(S, np.inf)
    metric[0] = 0.0
    choice = np.zeros((T, S), np.uint8)
    for t in range(T):
        if soft:
            bm = -(sym * rx[t]).sum(axis=2)  # negative correlation: smaller is better
        else:
            bm = (outs != rx[t].astype(np.uint8)).sum(axis=2).astype(float)
        cand = metric[pred] + bm  # S x 2
        choice[t] = np.argmin(cand, axis=1)
        metric = cand[np.arange(S), choice[t]]
    state = 0 if terminated else int(np.argmin(metric))
    bits = np.zeros(T, np.uint8)
    for t in range(T - 1, -1, -1):
        bits[t] = state >> (K - 2)
        state = pred[state, choice[t, state]]
    return bits[: T - (K - 1)] if terminated else bits


def path_metric_hard(rx, gens_octal, K):
    """Hamming distance between rx and the codeword chosen by hard-decision Viterbi."""
    dec = viterbi(rx, gens_octal, K, soft=False)
    return int(np.sum(conv_encode(dec, gens_octal, K) != np.asarray(rx, np.uint8)))


def distance_spectrum(gens_octal, K, dmax):
    """Paths that leave the zero state and first return to it, by output weight d <= dmax.

    Returns {d: (A_d, B_d)}: the number of such paths and their total information weight.
    """
    gens, _ = _taps(gens_octal, K)
    S = 2 ** (K - 1)
    count = np.zeros((S, dmax + 1))
    infow = np.zeros((S, dmax + 1))
    reg = 1 << (K - 1)
    w0 = sum(bin(reg & g).count("1") & 1 for g in gens)
    count[reg >> 1, w0] = 1
    infow[reg >> 1, w0] = 1
    A = np.zeros(dmax + 1)
    B = np.zeros(dmax + 1)
    for _ in range(50 * dmax * K):
        if not count.any():
            break
        nc = np.zeros_like(count)
        ni = np.zeros_like(infow)
        for s in np.flatnonzero(count.any(axis=1)):
            for u in (0, 1):
                reg = (u << (K - 1)) | int(s)
                ns = reg >> 1
                w = sum(bin(reg & g).count("1") & 1 for g in gens)
                if w > dmax:
                    continue
                c = count[s, : dmax + 1 - w]
                iw = infow[s, : dmax + 1 - w] + u * c
                if ns == 0:
                    A[w:] += c
                    B[w:] += iw
                else:
                    nc[ns, w:] += c
                    ni[ns, w:] += iw
        count, infow = nc, ni
    return {d: (int(A[d]), int(B[d])) for d in range(dmax + 1) if A[d] > 0}


def free_distance(gens_octal, K, dmax=40):
    return min(distance_spectrum(gens_octal, K, dmax))


def union_bound_ber(spectrum, rate, ebn0, k=1):
    """Soft-decision union bound: Pb <= (1/k) sum_d B_d Q(sqrt(2 R d Eb/N0))."""
    return sum(b * Q(math.sqrt(2 * rate * d * ebn0)) for d, (a, b) in spectrum.items()) / k


# ------------------------------------------------------------------ LDPC
def gallager_ldpc(n, wc, wr, rng):
    """Regular (wc, wr) parity-check matrix by Gallager's construction (n divisible by wr)."""
    m1 = n // wr
    base = np.zeros((m1, n), np.uint8)
    for i in range(m1):
        base[i, i * wr : (i + 1) * wr] = 1
    blocks = [base] + [base[:, rng.permutation(n)] for _ in range(wc - 1)]
    return np.vstack(blocks)


def min_sum_decode(llr, H, iters=50, alpha=0.75):
    """Normalized min-sum belief propagation. Returns (hard decisions, iterations used, success)."""
    H = np.asarray(H, bool)
    llr = np.asarray(llr, float)
    Qm = np.where(H, llr, 0.0)
    total = llr.copy()
    for it in range(1, iters + 1):
        mag = np.where(H, np.abs(Qm), np.inf)
        sgn = np.where(H & (Qm < 0), -1.0, 1.0)
        row_sign = np.prod(sgn, axis=1, keepdims=True)
        idx = np.argmin(mag, axis=1)
        min1 = mag[np.arange(H.shape[0]), idx]
        mag2 = mag.copy()
        mag2[np.arange(H.shape[0]), idx] = np.inf
        min2 = mag2.min(axis=1)
        mins = np.where(np.arange(H.shape[1])[None, :] == idx[:, None], min2[:, None], min1[:, None])
        R = np.where(H, alpha * row_sign * sgn * mins, 0.0)
        total = llr + R.sum(axis=0)
        hard = (total < 0).astype(np.uint8)
        if not (gf2_matmul(H.astype(np.uint8), hard) % 2).any():
            return hard, it, True
        Qm = np.where(H, total[None, :] - R, 0.0)
    return (total < 0).astype(np.uint8), iters, False


# ------------------------------------------------------------------ polar codes
def bec_polarize(eps, n_levels):
    """Erasure probabilities of the 2^n synthesized channels, natural index order (MSB = first split)."""
    # index bits, read MSB first, select the worse (0: 2z - z^2) or better (1: z^2) channel at each split
    N = 2**n_levels
    out = np.empty(N)
    for i in range(N):
        zi = eps
        for lvl in range(n_levels - 1, -1, -1):
            zi = 2 * zi - zi * zi if not (i >> lvl) & 1 else zi * zi
        out[i] = zi
    return out


def polar_encode(u):
    """x = u F^{(x)n} with F = [[1, 0], [1, 1]] (natural order): x = [(u1 + u2) G, u2 G]."""
    u = np.array(u, np.uint8)
    if len(u) == 1:
        return u
    h = len(u) // 2
    return np.concatenate([polar_encode(u[:h] ^ u[h:]), polar_encode(u[h:])])


def _f(a, b):
    t = np.tanh(np.clip(a, -40, 40) / 2) * np.tanh(np.clip(b, -40, 40) / 2)
    return 2 * np.arctanh(np.clip(t, -1 + 1e-15, 1 - 1e-15))


def polar_sc_decode(llr, frozen):
    """Successive-cancellation decoding; frozen is a boolean mask (frozen bits are 0).

    Returns (u_hat, x_hat) where x_hat = polar_encode(u_hat).
    """
    llr = np.asarray(llr, float)
    if len(llr) == 1:
        u = np.array([0 if frozen[0] else int(llr[0] < 0)], np.uint8)
        return u, u.copy()
    h = len(llr) // 2
    a, b = llr[:h], llr[h:]
    u1, v1 = polar_sc_decode(_f(a, b), frozen[:h])  # a xor b carries G(u1); v1 = G(u1)
    u2, v2 = polar_sc_decode(b + (1 - 2 * v1.astype(float)) * a, frozen[h:])  # b and a xor v1 both carry G(u2)
    return np.concatenate([u1, u2]), np.concatenate([v1 ^ v2, v2])


def polar_design(N, K, eps=0.5):
    """Frozen mask choosing the K most reliable synthesized channels by BEC polarization."""
    z = bec_polarize(eps, int(math.log2(N)))
    frozen = np.ones(N, bool)
    frozen[np.argsort(z)[:K]] = False
    return frozen


# ------------------------------------------------------------------ channels
def bpsk_awgn(bits, ebn0_db, rate, rng):
    """BPSK symbols 1 - 2b with noise for Eb/N0 (dB) at code rate R; returns (received, channel LLRs)."""
    es_n0 = rate * 10 ** (ebn0_db / 10)
    sigma = math.sqrt(1 / (2 * es_n0))
    y = 1.0 - 2.0 * np.asarray(bits, float) + sigma * rng.standard_normal(len(bits))
    return y, 2 * y / sigma**2
