#!/usr/bin/env python3
"""Verify chapter 17-07 (information theory and Shannon capacity): text, examples, problems and lab answers.

Routes:
- entropies directly and with scipy.stats.entropy; Huffman codes by the lab implementation and by an
  independent merge-depth computation, with prefix and round-trip checks;
- mutual information from joint tables, both from the definition and as H(Y) - H(Y|X);
- discrete channel capacities in closed form, by the lab's Blahut-Arimoto algorithm and by direct
  numerical maximization of I(X;Y) over the input distribution;
- Gaussian quantities by numerical integration of -f log2 f (differential entropy, BPSK-input capacity
  as h(Y) - h(Z) for the two-Gaussian mixture), cross-checked against the lab's Gauss-Hermite routine;
- thresholds by root finding; uncoded QAM from the square-QAM SER formula re-derived here;
- water-filling by a general constrained optimizer (SLSQP) against the lab's closed-form allocation;
- the practitioner comparisons from the logged values R-260, R-274 and R-276.
"""
from __future__ import annotations

import heapq
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import integrate, optimize
from scipy.stats import entropy as sp_entropy
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "17-07-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import infotheory as it  # noqa: E402

CH = ROOT / "chapters" / "17-07-information-theory-and-shannon.md"
v = Verifier.from_files("17-07", CH, ROOT / "solutions" / "17-07-solutions.md", LAB / "README.md")
Q, Qi = norm.sf, norm.isf
lg = math.log2


def db(x):
    return 10 * math.log10(x)


def un(d):
    return 10 ** (d / 10)


def H(ps):
    return float(sp_entropy(ps, base=2))


def h2(p):
    return H([p, 1 - p])


def huffman_lengths(ps):
    """Codeword lengths by repeated merging, tracking each symbol's depth (independent of the lab)."""
    heap = [(p, [i]) for i, p in enumerate(ps)]
    heapq.heapify(heap)
    depth = [0] * len(ps)
    while len(heap) > 1:
        p0, s0 = heapq.heappop(heap)
        p1, s1 = heapq.heappop(heap)
        for i in s0 + s1:
            depth[i] += 1
        heapq.heappush(heap, (p0 + p1, s0 + s1))
    return depth


def is_prefix_free(words):
    return not any(a != b and b.startswith(a) for a in words for b in words)


def mi_table(pxy):
    pxy = np.asarray(pxy, float)
    px, py = pxy.sum(1), pxy.sum(0)
    return sum(pxy[i, j] * lg(pxy[i, j] / (px[i] * py[j])) for i in range(pxy.shape[0]) for j in range(pxy.shape[1]) if pxy[i, j] > 0)


def mi_channel(p1, W):
    """I(X;Y) for binary input with P(X=1) = p1 and transition matrix W[x, y]."""
    px = np.array([1 - p1, p1])
    return mi_table(px[:, None] * np.asarray(W, float))


def capacity_by_search(W):
    res = optimize.minimize_scalar(lambda p: -mi_channel(p, W), bounds=(1e-9, 1 - 1e-9), method="bounded", options={"xatol": 1e-12})
    return -res.fun, res.x


def diff_entropy(f, lo, hi):
    """-int f log2 f over [lo, hi] by adaptive quadrature."""
    def g(x):
        fx = f(x)
        return -fx * lg(fx) if fx > 0 else 0.0
    val, _ = integrate.quad(g, lo, hi, limit=500, epsabs=1e-13, epsrel=1e-12)
    return val


def bpsk_soft_integral(es_n0):
    """BPSK-input capacity per real use as h(Y) - h(Z), Y a two-Gaussian mixture (Es = 1)."""
    s = math.sqrt(1 / (2 * es_n0))
    f = lambda y: 0.5 * (norm.pdf(y, 1, s) + norm.pdf(y, -1, s))  # noqa: E731
    hy = diff_entropy(f, -1 - 14 * s, 1 + 14 * s)
    return hy - 0.5 * lg(2 * math.pi * math.e * s * s)


def bpsk_hard(es_n0):
    return 1 - h2(Q(math.sqrt(2 * es_n0)))


def gauss_real(es_n0):
    return 0.5 * lg(1 + 2 * es_n0)


def ser_square_qam(m, es_n0):
    """Square M-QAM symbol-error rate: two independent sqrt(M)-PAM decisions."""
    pam = 2 * (1 - 1 / math.sqrt(m)) * Q(math.sqrt(3 * es_n0 / (m - 1)))
    return 1 - (1 - pam) ** 2


def uncoded_ebn0_db(m, ber=1e-5):
    if m == 4:
        return db(Qi(ber) ** 2 / 2)
    k = lg(m)
    return optimize.brentq(lambda x: ser_square_qam(m, k * un(x)) / k - ber, 0, 40, xtol=1e-12)


def waterfill_numeric(g, P):
    """Maximize sum log2(1 + g p) subject to sum p = P, p >= 0, with SLSQP."""
    g = np.asarray(g, float)
    n = len(g)
    res = optimize.minimize(
        lambda p: -np.sum(np.log2(1 + g * p)),
        np.full(n, P / n),
        jac=lambda p: -g / ((1 + g * p) * math.log(2)),
        bounds=[(0, P)] * n,
        constraints=[{"type": "eq", "fun": lambda p: np.sum(p) - P, "jac": lambda p: np.ones(n)}],
        method="SLSQP",
        options={"ftol": 1e-14, "maxiter": 1000},
    )
    assert res.success, res.message
    return res.x, -res.fun


def rate_half_es_db(fn):
    return optimize.brentq(lambda x: fn(un(x)) - 0.5, -10, 10, xtol=1e-12)


# ------------------------------------------------------------------ text
v.check("Txt 17-07.a", h2(0.1))
v.check("Txt 17-07.b", 1 - h2(0.01))
v.check("Txt 17-07.c", 1 - h2(0.11))
v.check("Txt 17-07.d", 1 / math.log(2))
v.check("Txt 17-07.e", db(math.log(2)))
v.check("Txt 17-07.f", db((2**2 - 1) / 2))
v.check("Txt 17-07.g", db((2**6 - 1) / 6))
v.check("Txt 17-07.h", uncoded_ebn0_db(4) - db(1.5))
es_soft, es_hard = rate_half_es_db(bpsk_soft_integral), rate_half_es_db(bpsk_hard)
v.check("Txt 17-07.i", es_hard - es_soft)
v.check("Txt 17-07.j", 20e6 * lg(1 + 100) / 1e6)

# entropy bounds and the ln x <= x - 1 inequality behind them
rng = np.random.default_rng(1707)
for _ in range(200):
    p = rng.dirichlet(np.ones(6))
    assert 0 <= H(p) <= lg(6) + 1e-12
v.assert_true("0 <= H <= log2 M on 200 random distributions; uniform attains log2 M", abs(H(np.ones(6) / 6) - lg(6)) < 1e-12)
v.assert_true("information in nats is smaller by ln 2 = 0.693", abs(math.log(2) - 0.693) < 5e-4)
v.assert_true("10 bits for one of 1024 outcomes; log2(1/8) = -3", lg(1024) == 10 and lg(1 / 8) == -3)

# mutual information: symmetric, zero for independence; the three forms agree
pxy = rng.dirichlet(np.ones(6)).reshape(2, 3)
px, py = pxy.sum(1), pxy.sum(0)
hyx = sum(px[i] * H(pxy[i] / px[i]) for i in range(2))
hxy = sum(py[j] * H(pxy[:, j] / py[j]) for j in range(3))
v.assert_true("I = H(Y) - H(Y|X) = H(X) - H(X|Y) = definition", abs(mi_table(pxy) - (H(py) - hyx)) < 1e-12 and abs(mi_table(pxy) - (H(px) - hxy)) < 1e-12)
v.assert_true("I = 0 for independent X, Y; lab mutual_info agrees", abs(mi_table(np.outer(px, py))) < 1e-12 and abs(it.mutual_info(pxy) - mi_table(pxy)) < 1e-12)
v.assert_true("chain rule H(X,Y) = H(X) + H(Y|X)", abs(H(pxy.ravel()) - (H(px) + hyx)) < 1e-12)

# BSC/BEC capacity claims
bsc = lambda p: np.array([[1 - p, p], [p, 1 - p]])  # noqa: E731
v.assert_true("BSC capacity 1 - h(p) equals the maximized I(X;Y) at p = 0.01 (uniform input)", abs(capacity_by_search(bsc(0.01))[0] - (1 - h2(0.01))) < 1e-9 and abs(capacity_by_search(bsc(0.01))[1] - 0.5) < 1e-4)
bec = lambda e: np.array([[1 - e, e, 0], [0, e, 1 - e]])  # noqa: E731
v.assert_true("BEC capacity 1 - eps by Blahut-Arimoto (eps = 0.3)", abs(it.blahut_arimoto(bec(0.3))[0] - 0.7) < 1e-9)

# Gaussian channel: differential entropy and capacity per real sample
for s in (0.5, 1.0, 3.0):
    hnum = diff_entropy(lambda x: norm.pdf(x, 0, s), -15 * s, 15 * s)
    assert abs(hnum - 0.5 * lg(2 * math.pi * math.e * s * s)) < 1e-9
v.assert_true("h(N(0, s^2)) = 0.5 log2(2 pi e s^2) by integration (s = 0.5, 1, 3)", True)
lap = 1 / math.sqrt(2)  # Laplace scale giving unit variance
h_lap = diff_entropy(lambda x: math.exp(-abs(x) / lap) / (2 * lap), -40, 40)
uni = math.sqrt(3)  # uniform on [-sqrt3, sqrt3] has unit variance
v.assert_true("maximum entropy: unit-variance Laplace and uniform have less entropy than the Gaussian", h_lap < 0.5 * lg(2 * math.pi * math.e) and lg(2 * uni) < 0.5 * lg(2 * math.pi * math.e))
P, sig2 = 3.0, 1.0
hy = diff_entropy(lambda y: norm.pdf(y, 0, math.sqrt(P + sig2)), -40, 40)
v.assert_true("I(X;Y) = h(Y) - h(Z) = 0.5 log2(1 + P/sigma^2) for Gaussian input (P/sigma^2 = 3)", abs(hy - 0.5 * lg(2 * math.pi * math.e * sig2) - 0.5 * lg(1 + P / sig2)) < 1e-9)
# samples to seconds: 2B samples of 0.5 log2(1 + S/(N0 B)) = B log2(1 + S/(N0 B))
B, S, N0 = 1e6, 2e-9, 1e-15
v.assert_true("2B x 0.5 log2(1 + P/sigma^2) with P = S/2B, sigma^2 = N0/2 equals Shannon-Hartley", abs(2 * B * 0.5 * lg(1 + (S / (2 * B)) / (N0 / 2)) - B * lg(1 + S / (N0 * B))) < 1e-6)
v.assert_true("20 MHz at 30 dB = 199.3 Mb/s", abs(20 * lg(1001) - 199.3) < 0.05)
v.assert_true("high SNR: about 3 dB per extra b/s/Hz", abs(db(2**11 - 1) - db(2**10 - 1) - 3.01) < 0.01)
v.assert_true("C_inf = S/(N0 ln 2): capacity_from_sn0 tends to it", abs(it.capacity_from_sn0(1e12, 1e6) / (1e6 / math.log(2)) - 1) < 1e-5)
v.assert_true("Shannon limit tends to ln 2 as eta -> 0; limit at 4 b/s/Hz is 5.74 dB", abs((2**1e-7 - 1) / 1e-7 - math.log(2)) < 1e-6 and abs(db(15 / 4) - 5.74) < 0.005)
v.assert_true("uncoded QPSK needs 9.59 dB at 1e-5 and sits 7.83 dB above the 2 b/s/Hz limit", abs(uncoded_ebn0_db(4) - 9.59) < 0.005)
v.assert_true("rate-1/2 bounds: unconstrained 0 dB, soft 0.19 dB, hard 1.77 dB", abs(db(2 * un(rate_half_es_db(gauss_real)))) < 1e-9 and abs(es_soft + db(2) - 0.19) < 0.005 and abs(es_hard + db(2) - 1.77) < 0.005)
v.assert_true("BPSK-input capacity never exceeds 1 bit and approaches the Gaussian bound at low SNR", bpsk_soft_integral(un(15)) <= 1 and bpsk_soft_integral(un(15)) > 0.999 and abs(bpsk_soft_integral(un(-15)) / gauss_real(un(-15)) - 1) < 0.02)

# ------------------------------------------------------------------ examples
ps1 = [0.5, 0.25, 0.125, 0.125]
v.check("Ex 17-07.1a", H(ps1))
code1 = it.huffman(dict(zip("ABCD", ps1)))
L1 = it.average_length(code1, dict(zip("ABCD", ps1)))
v.assert_true("Example 1: lab Huffman lengths 1, 2, 3, 3 match the independent merge depths", sorted(len(w) for w in code1.values()) == sorted(huffman_lengths(ps1)) == [1, 2, 3, 3])
v.check("Ex 17-07.1b", sum(p * l for p, l in zip(ps1, huffman_lengths(ps1))))
v.check("Ex 17-07.1c", math.ceil(lg(4)))
v.assert_true("Example 1: Kraft sum exactly 1; code prefix-free; lab average equals entropy", it.kraft([1, 2, 3, 3]) == 1 and is_prefix_free(list(code1.values())) and abs(L1 - 1.75) < 1e-12)

v.check("Ex 17-07.2a", capacity_by_search(bsc(0.01))[0])
p_half = optimize.brentq(lambda p: h2(p) - 0.5, 1e-6, 0.5, xtol=1e-14)
v.check("Ex 17-07.2b", p_half)
v.assert_true("Example 2: h(0.01) = 0.0808 (8.1% redundancy); C = 0.500 at p = 0.11", abs(h2(0.01) - 0.0808) < 5e-5 and abs(1 - h2(0.11) - 0.500) < 5e-4)
v.assert_true("Example 2 sanity: C = 0 at p = 0.5 and C = 1 at p = 1 (Blahut-Arimoto)", abs(it.blahut_arimoto(bsc(0.5))[0]) < 1e-9 and abs(it.blahut_arimoto(bsc(1.0))[0] - 1) < 1e-9)

for key, snr_db in (("Ex 17-07.3a", 0), ("Ex 17-07.3b", 20), ("Ex 17-07.3c", 30)):
    v.check(key, it.shannon_hartley(20e6, un(snr_db)) / 1e6)
sn0 = un(20) * 20e6  # S/N0 that gives 20 dB in 20 MHz
v.check("Ex 17-07.3d", it.capacity_from_sn0(40e6, sn0) / 1e6)
v.check("Ex 17-07.3e", sn0 / math.log(2) / 1e6)
v.assert_true("Example 3: from 20 to 30 dB capacity grows by about 50%", abs(20 * lg(1001) / (20 * lg(101)) - 1.5) < 0.005)

for key, eta in (("Ex 17-07.4a", 2), ("Ex 17-07.4b", 4), ("Ex 17-07.4c", 6)):
    v.check(key, it.shannon_limit_db(eta))
unc = {m: uncoded_ebn0_db(m) for m in (4, 16, 64)}
v.check("Ex 17-07.4d", unc[4])
v.check("Ex 17-07.4e", unc[16])
v.check("Ex 17-07.4f", unc[64])
v.check("Ex 17-07.4g", unc[4] - db(3 / 2))
v.check("Ex 17-07.4h", unc[16] - db(15 / 4))
v.check("Ex 17-07.4i", unc[64] - db(63 / 6))
v.assert_true("Example 4: every gap between 7.5 and 8 dB", all(7.5 < unc[m] - it.shannon_limit_db(lg(m)) < 8 for m in unc))

v.check("Ex 17-07.5a", es_soft)
v.check("Ex 17-07.5b", es_soft + db(2))
v.check("Ex 17-07.5c", es_hard)
v.check("Ex 17-07.5d", es_hard + db(2))
v.check("Ex 17-07.5e", es_hard - es_soft)
v.check("Ex 17-07.5f", db(2 * un(rate_half_es_db(gauss_real))))
v.assert_true("Example 5: lab Gauss-Hermite BPSK capacity matches the h(Y) - h(Z) integral", all(abs(it.bpsk_soft_capacity(un(x)) - bpsk_soft_integral(un(x))) < 1e-6 for x in (-10, -2.82, 0, 5)))
v.assert_true("Example 5: lab root finder gives the same soft and hard thresholds", abs(it.required_es_n0_db(it.bpsk_soft_capacity, 0.5) - es_soft) < 1e-8 and abs(it.required_es_n0_db(it.bpsk_hard_capacity, 0.5) - es_hard) < 1e-8)

p2, c2 = waterfill_numeric([1, 0.25], 2)
p6, c6 = waterfill_numeric([1, 0.25], 6)
v.check("Ex 17-07.6a", c2)
v.check("Ex 17-07.6b", it.equal_power_capacity([1, 0.25], 2))
v.check("Ex 17-07.6c", p6[0])
v.check("Ex 17-07.6d", p6[1])
v.check("Ex 17-07.6e", c6)
v.check("Ex 17-07.6f", it.equal_power_capacity([1, 0.25], 6))
lp2, mu2, lc2 = it.waterfill([1, 0.25], 2)
lp6, mu6, lc6 = it.waterfill([1, 0.25], 6)
v.assert_true("Example 6: P = 2 uses only channel 1; lab closed form matches SLSQP; mu = 5.5 at P = 6", abs(p2[1]) < 1e-6 and np.allclose(lp2, p2, atol=1e-6) and np.allclose(lp6, p6, atol=1e-6) and abs(mu6 - 5.5) < 1e-12)
v.assert_true("Example 6: gain over equal power falls from 0.26 to 0.11 b/s/Hz", abs(c2 - 1.3219 - 0.26) < 0.005 and abs(c6 - it.equal_power_capacity([1, 0.25], 6) - 0.11) < 0.005)

# ------------------------------------------------------------------ practitioner lens and concept checks
for es, eta, gap in ((1.00, 0.988858, 1.07), (16.05, 4.453027, 2.85)):  # R-276 Table 13
    assert abs((es - db(eta)) - it.shannon_limit_db(eta) - gap) < 0.005
v.assert_true("DVB-S2 QPSK 1/2 and 32APSK 9/10 sit 1.07 and 2.85 dB from Shannon (R-276)", True)
eta_nr = 2 / 3  # QPSK, rate 1/3 (R-260)
v.assert_true("NR: Shannon SNR at 0.667 b/s/Hz is -2.31 dB, 1.31 dB below the assumed -1 dB", abs(db(2**eta_nr - 1) + 2.31) < 0.005 and abs(-1 - db(2**eta_nr - 1) - 1.31) < 0.005)
ebn0_lora = -20 + db(125e3 / 293)  # R-274
v.assert_true("LoRa SF12: eta = 0.0023, Eb/N0 = 6.3 dB, 7.9 dB above -1.59 dB", abs(293 / 125e3 - 0.0023) < 5e-5 and abs(ebn0_lora - 6.3) < 0.05 and abs(ebn0_lora - db(math.log(2)) - 7.9) < 0.05)
v.assert_true("1 -> 10 b/s/Hz: required SNR 0 -> 30 dB; 4 -> 40 b/s/Hz: more than 100 dB more", abs(db(2**1 - 1)) < 1e-12 and abs(db(2**10 - 1) - 30.1) < 0.05 and db(2**40 - 1) - db(2**4 - 1) > 100)
v.assert_true("Q1: 8 equiprobable symbols carry 3 bits", H(np.ones(8) / 8) == 3)
v.assert_true("Q3: 9.97B -> 17.9B (1.8x) at 30 dB; 0.1375B -> 0.1408B at -10 dB", abs(lg(1001) - 9.97) < 0.005 and abs(2 * lg(501) - 17.9) < 0.05 and abs(lg(1.1) - 0.1375) < 5e-5 and abs(2 * lg(1.05) - 0.1408) < 5e-5)

# ------------------------------------------------------------------ problems
v.check("17-07.1a", H(np.ones(6) / 6))
v.check("17-07.1b", h2(0.9))
ps4 = [0.4, 0.3, 0.2, 0.1]
v.check("17-07.1c", H(ps4))
v.assert_true("Solution 1: -log2 of 0.4, 0.3, 0.2, 0.1 = 1.322, 1.737, 2.322, 3.322", all(abs(-lg(p) - x) < 5e-4 for p, x in zip(ps4, (1.322, 1.737, 2.322, 3.322))))
len4 = huffman_lengths(ps4)
code4 = it.huffman(dict(zip("abcd", ps4)))
v.check("17-07.2a", sum(p * l for p, l in zip(ps4, len4)))
v.check("17-07.2b", H(ps4) / sum(p * l for p, l in zip(ps4, len4)))
v.assert_true("Solution 2: lengths 1, 2, 3, 3 from both implementations; lab code decodes a random message", len4 == [1, 2, 3, 3] and [len(code4[s]) for s in "abcd"] == [1, 2, 3, 3] and it.decode(it.encode(list("abcdcbaadd"), code4), code4) == list("abcdcbaadd"))
v.check("17-07.3a", float(sum(Fraction(1, 2**l) for l in (1, 2, 2, 3))))
v.assert_true("Solution 3: lengths 1, 2, 3, 3 give a Kraft sum of exactly 1 and the code 0, 10, 110, 111 is prefix-free", sum(Fraction(1, 2**l) for l in (1, 2, 3, 3)) == 1 and is_prefix_free(["0", "10", "110", "111"]))
j4 = np.array([[0.4, 0.1], [0.1, 0.4]])
v.check("17-07.4a", mi_table(j4))
v.assert_true("Solution 4: H(X) = 1, H(Y|X) = h(0.2) = 0.722, I = H(Y) - H(Y|X)", abs(H(j4.sum(1)) - 1) < 1e-12 and abs(h2(0.2) - 0.722) < 5e-4 and abs(mi_table(j4) - (1 - h2(0.2))) < 1e-12)
v.check("17-07.5a", it.blahut_arimoto(bec(0.2))[0])
v.check("17-07.5b", capacity_by_search(bsc(0.2))[0])
Z = np.array([[1, 0], [0.5, 0.5]])
cz, pz = capacity_by_search(Z)
v.check("17-07.6a", cz)
v.check("17-07.6b", pz)
v.assert_true("Solution 6: closed form, Blahut-Arimoto and direct search agree", abs(it.z_capacity(0.5)[0] - cz) < 1e-9 and abs(it.blahut_arimoto(Z)[0] - cz) < 1e-9 and abs(it.blahut_arimoto(Z)[1][1] - 0.4) < 1e-5)
v.check("17-07.7a", 1e6 * lg(1 + un(10)) / 1e6)
v.check("17-07.7b", db(2**10 - 1))
b70 = optimize.brentq(lambda b: it.capacity_from_sn0(b, un(70)) - 1e7, 1e5, 1e9, xtol=1e-6)
b73 = optimize.brentq(lambda b: it.capacity_from_sn0(b, un(73)) - 1e7, 1e5, 1e9, xtol=1e-6)
v.check("17-07.8a", b70 / 1e6)
v.check("17-07.8b", b73 / 1e6)
v.assert_true("Solution 8: at the minimum bandwidth, Eb/N0 = (S/N0)/Rb = 0 dB = limit at eta = 1", abs(db(un(70) / 1e7)) < 1e-12 and abs(it.shannon_limit_db(1.0)) < 1e-12)
v.check("17-07.9a", it.shannon_limit_db(1.5))
v.assert_true("Solution 9: (2^1.5 - 1)/1.5 = 1.219", abs((2**1.5 - 1) / 1.5 - 1.219) < 5e-4)
v.check("17-07.10a", it.capacity_from_sn0(1e15, un(60)) / 1e6)
v.check("17-07.10b", it.capacity_from_sn0(1e6, un(60)) / 1e6)
v.check("17-07.10c", it.capacity_from_sn0(1e7, un(60)) / 1e6)
v.assert_true("Solution 10: ten times the bandwidth gains 37.5%", abs(it.capacity_from_sn0(1e7, un(60)) / it.capacity_from_sn0(1e6, un(60)) - 1.375) < 5e-4)
v.check("17-07.11a", diff_entropy(norm.pdf, -40, 40))
v.assert_true("Solution 11: lab gaussian_diff_entropy agrees with the integral", abs(it.gaussian_diff_entropy(1.0) - diff_entropy(norm.pdf, -40, 40)) < 1e-9)
# Problem 12: real-valued lengths minimizing sum p l subject to Kraft equality give H
res = optimize.minimize(lambda l: np.dot(ps4, l), np.full(4, 2.0), constraints=[{"type": "eq", "fun": lambda l: np.sum(2.0 ** -l) - 1}], method="SLSQP", options={"ftol": 1e-14})
ceil_len = [math.ceil(-lg(p)) for p in ps4]
v.assert_true("Problem 12: optimum of the relaxed problem is H at l = -log2 p; ceiling lengths satisfy Kraft and average < H + 1", abs(res.fun - H(ps4)) < 1e-7 and np.allclose(res.x, -np.log2(ps4), atol=1e-4) and it.kraft(ceil_len) <= 1 and np.dot(ps4, ceil_len) < H(ps4) + 1)
g13 = [2, 1, 0.2]
p13, c13 = waterfill_numeric(g13, 1)
lp13, mu13, lc13 = it.waterfill(g13, 1)
v.check("17-07.13a", mu13)
v.check("17-07.13b", p13[0])
v.check("17-07.13c", p13[1])
v.check("17-07.13d", c13)
v.check("17-07.13e", it.equal_power_capacity(g13, 1))
v.assert_true("Solution 13: third channel gets nothing; all-three level 2.5 lies below its floor 5; lab = SLSQP; +32%", abs(p13[2]) < 1e-6 and (1 + 0.5 + 1 + 5) / 3 < 5 and np.allclose(lp13, p13, atol=1e-6) and abs(c13 / it.equal_power_capacity(g13, 1) - 1.32) < 0.005)
v.check("17-07.14a", gauss_real(1.0))
v.check("17-07.14b", bpsk_soft_integral(1.0))
v.check("17-07.14c", 1 - h2(Q(math.sqrt(2))))
v.assert_true("Solution 14: Q(sqrt 2) = 0.0786; fractions 91% and 76% of the Gaussian capacity", abs(Q(math.sqrt(2)) - 0.0786) < 5e-5 and round(100 * bpsk_soft_integral(1.0) / gauss_real(1.0)) == 91 and round(100 * bpsk_hard(1.0) / gauss_real(1.0)) == 76)
v.assert_true("Solution 14: hard capacity also from Blahut-Arimoto on the BSC", abs(it.blahut_arimoto(bsc(Q(math.sqrt(2))))[0] - bpsk_hard(1.0)) < 1e-9)

# ------------------------------------------------------------------ lab
text = it.letters_only(it.SAMPLE_TEXT)
counts = Counter(text)
freq = np.array(list(counts.values())) / len(text)
v.check("Lab 17-07.a", H(freq))
lab_code = it.huffman({s: c / len(text) for s, c in counts.items()})
dep = huffman_lengths(list(freq))
v.check("Lab 17-07.b", float(np.dot(freq, dep)))
v.assert_true("Lab part 1: 25 symbols; lab Huffman average equals independent; round trip exact; within 0.04 bits of H", len(counts) == 25 and abs(it.average_length(lab_code, {s: c / len(text) for s, c in counts.items()}) - np.dot(freq, dep)) < 1e-12 and "".join(it.decode(it.encode(text, lab_code), lab_code)) == text and np.dot(freq, dep) - H(freq) < 0.04)
v.check("Lab 17-07.c", it.blahut_arimoto(bsc(0.1))[0])
v.assert_true("Lab part 2: BA gives a uniform input for the BSC", np.allclose(it.blahut_arimoto(bsc(0.1))[1], 0.5))
v.check("Lab 17-07.d", 2 * lg(1 + un(30) / 2) / lg(1 + un(30)))
v.check("Lab 17-07.e", 2 * lg(1 + un(-10) / 2) / lg(1 + un(-10)))
k = np.arange(64)
g64 = np.abs(1 + 0.9 * np.exp(-2j * np.pi * k / 64)) ** 2
p64, c64 = waterfill_numeric(g64, 64)
lp64, mu64, lc64 = it.waterfill(g64, 64)
off = np.flatnonzero(lp64 == 0)
v.check("Lab 17-07.f", len(off))
v.check("Lab 17-07.g", c64 / 64)
v.check("Lab 17-07.h", it.equal_power_capacity(g64, 64) / 64)
v.assert_true("Lab part 5: lab allocation matches SLSQP; the switched-off subcarriers are contiguous around k = 32", np.allclose(lp64, p64, atol=1e-5) and abs(lc64 - c64) < 1e-9 and np.array_equal(off, np.arange(off[0], off[-1] + 1)) and off[0] + off[-1] == 64)
v.assert_true("Lab part 5: water-filling beats equal power by about 0.17 b/s/Hz per subcarrier", abs((c64 - it.equal_power_capacity(g64, 64)) / 64 - 0.17) < 0.006)

sys.exit(v.finish())
