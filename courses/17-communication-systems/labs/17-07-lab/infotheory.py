"""Information theory toolkit for the 17-07 lab.

- entropy of a distribution and of a sample, the binary entropy function;
- Huffman coding (build, encode, decode) and the Kraft sum;
- mutual information from a joint probability table;
- the Blahut-Arimoto algorithm for the capacity of any discrete memoryless channel;
- closed-form BSC, BEC and Z-channel capacities;
- AWGN capacity (real and complex), BPSK-input soft-decision and hard-decision capacities;
- the Shannon limit on Eb/N0 at a given spectral efficiency;
- water-filling over parallel Gaussian channels.

All logarithms are base 2 unless a name says otherwise.
"""
from __future__ import annotations

import heapq
import math
import re
from collections import Counter

import numpy as np
from scipy import optimize
from scipy.stats import norm


# A short original paragraph used in the lab's compression exercise.
SAMPLE_TEXT = (
    "a channel is any path that carries a message from one place to another and every real "
    "channel adds some noise. the surprising result of information theory is that noise does not "
    "force errors on us. as long as we send information more slowly than the capacity of the "
    "channel we can make the error rate as small as we like by coding long blocks of data. the "
    "price is delay and complexity in the encoder and the decoder, and engineers spend their "
    "careers trading those costs against power and bandwidth. a radio that works near the limit "
    "uses a strong code, a receiver that keeps soft information about every bit, and a clever "
    "choice of how to spread its power over the frequencies that the channel passes best."
)


def letters_only(text):
    """Lower-case letters and single spaces only (punctuation removed)."""
    t = re.sub(r"[^a-z ]", "", text.lower())
    return re.sub(r" +", " ", t)


# ------------------------------------------------------------------ entropy
def entropy(p):
    """H(p) in bits for a probability vector (zeros allowed)."""
    p = np.asarray(p, float)
    p = p[p > 0]
    return float(-np.sum(p * np.log2(p)))


def binary_entropy(p):
    """h(p) = -p log2 p - (1-p) log2(1-p), with h(0) = h(1) = 0."""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def empirical_entropy(seq):
    """Entropy of the symbol frequencies in a sequence, and the frequency table."""
    counts = Counter(seq)
    n = sum(counts.values())
    probs = {s: c / n for s, c in counts.items()}
    return entropy(list(probs.values())), probs


# ------------------------------------------------------------------ source coding
def huffman(probs):
    """Huffman code for a dict {symbol: probability}; returns {symbol: codeword string}."""
    if len(probs) == 1:
        return {next(iter(probs)): "0"}
    heap = [(p, i, {s: ""}) for i, (s, p) in enumerate(probs.items())]
    heapq.heapify(heap)
    tie = len(heap)
    while len(heap) > 1:
        p0, _, c0 = heapq.heappop(heap)
        p1, _, c1 = heapq.heappop(heap)
        merged = {s: "0" + w for s, w in c0.items()}
        merged.update({s: "1" + w for s, w in c1.items()})
        heapq.heappush(heap, (p0 + p1, tie, merged))
        tie += 1
    return heap[0][2]


def average_length(code, probs):
    return sum(probs[s] * len(w) for s, w in code.items())


def kraft(lengths):
    """Kraft sum: a prefix code with these lengths exists iff the sum is <= 1."""
    return sum(2.0 ** -l for l in lengths)


def encode(seq, code):
    return "".join(code[s] for s in seq)


def decode(bits, code):
    inverse = {w: s for s, w in code.items()}
    out, word = [], ""
    for b in bits:
        word += b
        if word in inverse:
            out.append(inverse[word])
            word = ""
    if word:
        raise ValueError("bit string ends inside a codeword")
    return out


# ------------------------------------------------------------------ mutual information and capacity
def mutual_info(joint):
    """I(X;Y) in bits from a joint table joint[x, y] (rows: inputs)."""
    pxy = np.asarray(joint, float)
    pxy = pxy / pxy.sum()
    px = pxy.sum(axis=1, keepdims=True)
    py = pxy.sum(axis=0, keepdims=True)
    mask = pxy > 0
    return float(np.sum(pxy[mask] * np.log2(pxy[mask] / (px @ py)[mask])))


def blahut_arimoto(W, tol=1e-12, max_iter=100000):
    """Capacity (bits/use) and optimal input of a DMC with W[x, y] = p(y|x).

    Returns (capacity, input distribution, number of iterations). The bounds
    log2(sum_x p(x) 2^D(x)) and max_x D(x) bracket C and stop the loop.
    """
    W = np.asarray(W, float)
    nx = W.shape[0]
    p = np.full(nx, 1.0 / nx)
    for it in range(1, max_iter + 1):
        q = p @ W  # output distribution
        with np.errstate(divide="ignore", invalid="ignore"):
            d = np.where(W > 0, W * np.log2(W / q), 0.0).sum(axis=1)  # D(W(.|x) || q)
        lower = math.log2(np.sum(p * 2.0 ** d))
        upper = float(np.max(d))
        if upper - lower < tol:
            return lower, p, it
        p = p * 2.0 ** d
        p /= p.sum()
    return lower, p, max_iter


def bsc_capacity(p):
    return 1 - binary_entropy(p)


def bec_capacity(eps):
    return 1 - eps


def z_capacity(q):
    """Z-channel: 0 -> 0 always; 1 -> 0 with probability q. Returns (C, optimal P(X=1))."""
    c = math.log2(1 + (1 - q) * q ** (q / (1 - q)))
    p1 = 1 / ((1 - q) * (1 + 2 ** (binary_entropy(q) / (1 - q))))
    return c, p1


# ------------------------------------------------------------------ Gaussian channels
def gaussian_diff_entropy(sigma):
    """Differential entropy of N(0, sigma^2) in bits."""
    return 0.5 * math.log2(2 * math.pi * math.e * sigma**2)


def awgn_real(snr):
    """Capacity per real sample, 0.5 log2(1 + P/sigma^2)."""
    return 0.5 * math.log2(1 + snr)


def shannon_hartley(bandwidth, snr):
    """Capacity in b/s of a channel of bandwidth B (Hz) at SNR (linear)."""
    return bandwidth * math.log2(1 + snr)


def capacity_from_sn0(bandwidth, s_n0):
    """Capacity with fixed received S/N0 (Hz): noise grows with bandwidth."""
    return bandwidth * math.log2(1 + s_n0 / bandwidth)


_GH_X, _GH_W = np.polynomial.hermite.hermgauss(120)


def bpsk_soft_capacity(es_n0):
    """Capacity per use of a real AWGN channel with equiprobable +/-sqrt(Es) input.

    C = 1 - E[log2(1 + exp(-2 y sqrt(Es)/sigma^2))], y ~ N(sqrt(Es), sigma^2),
    sigma^2 = N0/2, evaluated by Gauss-Hermite quadrature with Es = 1.
    """
    sigma = math.sqrt(1 / (2 * es_n0))
    y = 1 + math.sqrt(2) * sigma * _GH_X
    llr = 2 * y / sigma**2
    vals = np.logaddexp(0, -llr) / math.log(2)
    return 1 - float(np.sum(_GH_W * vals) / math.sqrt(math.pi))


def bpsk_hard_capacity(es_n0):
    """Hard-decision BPSK: a BSC with p = Q(sqrt(2 Es/N0))."""
    return bsc_capacity(norm.sf(math.sqrt(2 * es_n0)))


def gaussian_real_capacity(es_n0):
    """Gaussian input on the real channel, per use: 0.5 log2(1 + 2 Es/N0)."""
    return awgn_real(2 * es_n0)


def required_es_n0_db(cap_fn, rate, lo=-20.0, hi=20.0):
    """Es/N0 (dB) at which cap_fn reaches the given rate (bits per use)."""
    return optimize.brentq(lambda x: cap_fn(10 ** (x / 10)) - rate, lo, hi, xtol=1e-12)


def shannon_limit_db(eta):
    """Minimum Eb/N0 (dB) at spectral efficiency eta (b/s/Hz); eta -> 0 gives -1.59 dB."""
    if eta == 0:
        return 10 * math.log10(math.log(2))
    return 10 * math.log10((2**eta - 1) / eta)


# ------------------------------------------------------------------ water-filling
def waterfill(gains, total_power):
    """Water-filling over parallel channels with noise-normalized gains g_k.

    Returns (powers, water level mu, capacity in b/s/Hz) with p_k = max(0, mu - 1/g_k).
    """
    g = np.asarray(gains, float)
    floors = 1 / g
    order = np.argsort(floors)
    for k in range(len(g), 0, -1):
        used = order[:k]
        mu = (total_power + floors[used].sum()) / k
        if mu > floors[used].max():
            p = np.zeros_like(g)
            p[used] = mu - floors[used]
            return p, mu, float(np.sum(np.log2(1 + g * p)))
    raise ValueError("no feasible allocation")


def equal_power_capacity(gains, total_power):
    g = np.asarray(gains, float)
    return float(np.sum(np.log2(1 + g * total_power / len(g))))
