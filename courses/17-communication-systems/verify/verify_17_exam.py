#!/usr/bin/env python3
"""Verify every number in the Course 17 final-exam solutions.

Independent routes:
- the random-phase sinusoid's autocorrelation by averaging over a dense grid of phases; noise bandwidth and output
  variance by integrating |H|^2; the output correlation from the inverse transform of the output PSD;
- the Friis cascade stage by stage from noise powers (added noise referred to the input), not from the formula;
- Bessel spectra with scipy.special.jv, checked against an FFT of a sampled tone-FM waveform;
- ISI from the sampled step-difference response of a discretized RC channel, worst case by summing |cursors|;
- matched-filter and RC-filter SNRs by numerical convolution and noise integrals; error probabilities with
  scipy.stats.norm; the MAP threshold by root finding on the weighted likelihoods;
- entropy, and a Huffman code built with a heap; the Hamming code by enumerating all 2^7 error patterns with a
  syndrome decoder; RS burst length by brute force over burst start positions; Erlang B from its closed form;
- path loss from an exact two-ray field sum; fading BERs by numerical integration over the SNR densities; coherence
  correlation with scipy.special.j0; ICI from the exact Dirichlet kernel; MIMO capacity from numpy.linalg.svd;
- subnets with the standard-library ipaddress module; Ethernet bytes summed field by field.
"""
from __future__ import annotations

import heapq
import ipaddress
import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, special, stats
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("17-exam", ROOT / "exam" / "solutions.md")
C = 2.998e8
Qf = stats.norm.sf


def db(x):
    return 10 * math.log10(x)


# ---------------------------------------------------------------- Q1
A, f0 = 2.0, 1e3
th = np.linspace(0, 2 * np.pi, 20001)[:-1]
t0, tau = 0.37e-3, 0.11e-3
mean = np.mean(A * np.cos(2 * np.pi * f0 * t0 + th))
R = np.mean(A * np.cos(2 * np.pi * f0 * (t0 + tau) + th) * A * np.cos(2 * np.pi * f0 * t0 + th))
v.assert_true("Q1 mean zero", abs(mean) < 1e-9, f"{mean}")
v.assert_true("Q1 R = A^2/2 cos(2 pi f0 tau)", abs(R - A**2 / 2 * math.cos(2 * math.pi * f0 * tau)) < 1e-9)
R0 = np.mean((A * np.cos(th)) ** 2)
v.check("X17.1a", R0)
v.check("X17.1b", R0 / 2)  # half the power in each of the two lines
fc = 10e3
BN = integrate.quad(lambda f: 1 / (1 + (f / fc) ** 2), 0, np.inf)[0]
v.check("X17.1c", BN / 1e3)
N0 = 2e-8
var = integrate.quad(lambda f: N0 / 2 / (1 + (f / fc) ** 2), -np.inf, np.inf)[0]
v.check("X17.1d", var)
v.check("X17.1e", math.sqrt(var) * 1e3)


def rho(t):
    num = integrate.quad(lambda f: 1 / (1 + (f / fc) ** 2), 0, np.inf, weight="cos", wvar=2 * np.pi * t)[0]
    return num / BN


v.check("X17.1f", rho(20e-6))
v.check("X17.1g", brentq(lambda t: rho(t) - 0.1, 1e-6, 100e-6) * 1e6)

# ---------------------------------------------------------------- Q2 (noise powers, referred to the input)
k, T0 = 1.380649e-23, 290.0
stages = [(10 ** 1.5, 10 ** 0.15), (10 ** -0.8, 10 ** 0.8), (10**3, 10 ** 0.4)]


def cascade(st):
    """Output noise of the chain with a T0 source, divided by the noiseless-chain output noise."""
    n_out, gain = k * T0, 1.0  # per hertz
    for g, f in st:
        n_out = (n_out + k * T0 * (f - 1)) * g  # stage adds its own noise referred to its input
        gain *= g
    return n_out / (k * T0 * gain)


F = cascade(stages)
v.check("X17.2a", F)
v.check("X17.2b", db(F))
v.check("X17.2c", (stages[1][1] - 1) / stages[0][0])
v.check("X17.2d", (stages[2][1] - 1) / (stages[0][0] * stages[1][0]))
v.check("X17.2e", T0 * (F - 1))
v.check("X17.2f", db(cascade([(10 ** -0.2, 10 ** 0.2)] + stages)))
sens = -174 + db(20e6) + db(F) + 10
v.check("X17.2g", sens)
v.check("X17.2h", 10 - db(40e6 / 20e6))

# ---------------------------------------------------------------- Q3
beta = 40 / 10
v.check("X17.3a", beta)
v.check("X17.3b", 2 * (40 + 10))
Jn = special.jv(np.arange(0, 6), beta)
v.check("X17.3c", Jn[0] ** 2)
frac = Jn[0] ** 2 + 2 * np.sum(Jn[1:] ** 2)
v.check("X17.3d", frac)
# FFT check of the tone-FM spectrum
fs, fm, N = 2.56e6, 10e3, 2**16
tt = np.arange(N) / fs
x = np.exp(1j * beta * np.sin(2 * np.pi * fm * tt))
X = np.fft.fft(x) / N
fr = np.fft.fftfreq(N, 1 / fs)
inband = np.sum(np.abs(X[np.abs(fr) <= 50e3 + 1]) ** 2)
v.assert_true("Q3 FFT in-band fraction", abs(inband - frac) < 1e-6, f"{inband} vs {frac}")
v.check("X17.3e", 1.5 * beta**2)
v.check("X17.3f", db(1.5 * beta**2))
ka2Pm = 0.5**2 * np.mean(np.sin(th) ** 2)
eta = ka2Pm / (1 + ka2Pm)
v.check("X17.3g", eta)
v.check("X17.3h", db(eta))

# ---------------------------------------------------------------- Q4 (discretized RC channel)
v.check("X17.4a", 1.3 * 28 / 2)
tauc = 1 / (2 * math.pi * 12e9)
v.check("X17.4b", tauc * 1e12)


def cursors(T, n=40, steps=4000):
    """Sampled pulse response at t = (k+1)T of an RC driven by a unit pulse of width T (exact exponential update)."""
    dt = T / steps
    a = math.exp(-dt / tauc)
    y, out = 0.0, []
    for kk in range(n):
        u = 1.0 if kk == 0 else 0.0
        for _ in range(steps):
            y = a * y + (1 - a) * u
        out.append(y)
    return np.array(out)


hN = cursors(1 / 56e9)
hP = cursors(1 / 28e9)
rN, rP = 1 - hN[0], 1 - hP[0]
v.check("X17.4c", rN)
v.check("X17.4e", rP)
eyeN = (2 * hN[0] - 2 * np.sum(np.abs(hN[1:]))) / 2
eyeP = (2 / 3 * hP[0] - 2 * np.sum(np.abs(hP[1:]))) / 2
v.check("X17.4d", eyeN)
v.check("X17.4f", eyeP)
v.check("X17.4g", 20 * math.log10(eyeN / eyeP))
v.check("X17.4h", 20 * math.log10(2 / (2 / 3)))

# ---------------------------------------------------------------- Q5
Amp, T, N0 = 2e-3, 0.5e-6, 2e-14
tg = np.linspace(0, T, 200001)
E = integrate.trapezoid(np.full_like(tg, Amp**2), tg)
v.check("X17.5a", E)
snr_mf = 2 * E / N0
v.check("X17.5b", snr_mf)
v.check("X17.5c", db(snr_mf))
tau_rc = 2 * T
sig = integrate.quad(lambda s: Amp * math.exp(-(T - s) / tau_rc) / tau_rc, 0, T)[0]
# substitute s = u tau: the integral of h^2 is (1/tau) * integral of exp(-2u) du
nvar = N0 / 2 / tau_rc * integrate.quad(lambda u: math.exp(-2 * u), 0, 60)[0]
snr_rc = sig**2 / nvar
v.check("X17.5d", snr_rc / snr_mf)
v.check("X17.5e", snr_rc)
v.check("X17.5f", db(snr_rc))
v.check("X17.5g", db(snr_mf / snr_rc))
g9 = 10**0.9
v.check("X17.5h", Qf(math.sqrt(2 * g9)))
v.check("X17.5i", Qf(math.sqrt(g9)))
s5 = math.sqrt(0.8 / 2)
pp, pm = 0.7, 0.3
thr = brentq(lambda r: pp * stats.norm.pdf(r, 1, s5) - pm * stats.norm.pdf(r, -1, s5), -1, 1)
v.check("X17.5j", thr)
e_plus = stats.norm.cdf(thr, 1, s5)
e_minus = stats.norm.sf(thr, -1, s5)
v.check("X17.5k", e_plus)
v.check("X17.5l", e_minus)
v.check("X17.5m", pp * e_plus + pm * e_minus)
v.check("X17.5n", stats.norm.cdf(0, 1, s5))

# ---------------------------------------------------------------- Q6
v.check("X17.6a", 2 * 25 / (1.2 * 25))
v.check("X17.6b", Qf(math.sqrt(2 * 10**0.7)))
Es = 4 * 10**1.4
# 16-QAM SER from the per-dimension 4-PAM error probability (inner points err two ways, outer one way)
d = math.sqrt(3 * Es / 15)  # half-distance over sigma, in units where sigma = 1
p_inner, p_outer = 2 * Qf(d), Qf(d)
p_dim = 0.5 * p_inner + 0.5 * p_outer
Ps = 1 - (1 - p_dim) ** 2
v.check("X17.6c", Ps)
v.check("X17.6d", Ps / 4)
v.check("X17.6e", -20 * math.log10(0.045))
v.check("X17.6f", -20 * math.log10(0.08))
snr_eff = 1 / (10**-2.5 + 0.05**2)
v.check("X17.6g", snr_eff)
v.check("X17.6h", db(snr_eff))

# ---------------------------------------------------------------- Q7
P = [0.35, 0.25, 0.20, 0.12, 0.08]
H = -sum(p * math.log2(p) for p in P)
v.check("X17.7a", H)
heap = [(p, i, {i: 0}) for i, p in enumerate(P)]
heapq.heapify(heap)
cnt = len(P)
while len(heap) > 1:
    p1, _, a1 = heapq.heappop(heap)
    p2, _, a2 = heapq.heappop(heap)
    merged = {s: L + 1 for s, L in {**a1, **a2}.items()}
    heapq.heappush(heap, (p1 + p2, cnt, merged))
    cnt += 1
lengths = heap[0][2]
Lbar = sum(P[s] * L for s, L in lengths.items())
v.check("X17.7b", Lbar)
v.check("X17.7c", H / Lbar)
pb = 0.05
v.check("X17.7d", 1 + pb * math.log2(pb) + (1 - pb) * math.log2(1 - pb))
v.check("X17.7e", 10e6 * math.log2(1 + 10**1.5) / 1e6)
v.check("X17.7f", db(brentq(lambda e: math.log2(1 + 3 * e) - 3, 0.1, 100)))
v.check("X17.7g", db(brentq(lambda e: math.log2(1 + 1e-7 * e) - 1e-7, 0.1, 10)))

# ---------------------------------------------------------------- Q8
v.check("X17.8a", 4 / 7)
Hm = np.array([[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]])
pbsc, pfail = 0.01, 0.0
for e in itertools.product([0, 1], repeat=7):
    e = np.array(e)
    syn = Hm @ e % 2
    pos = syn[0] + 2 * syn[1] + 4 * syn[2]
    corr = e.copy()
    if pos:
        corr[pos - 1] ^= 1
    if corr.any():
        w = int(e.sum())
        pfail += pbsc**w * (1 - pbsc) ** (7 - w)
v.check("X17.8b", pfail)
v.check("X17.8c", 1 - (1 - pbsc) ** 4)
v.check("X17.8d", 2.0**-16)
v.check("X17.8e", db(0.5 * 12))
v.check("X17.8f", db(0.5 * ((12 - 1) // 2 + 1)))
v.check("X17.8g", (255 - 223) // 2)
v.check("X17.8h", (255 / 223 - 1) * 100)
best = 0
for b in range(1, 200):
    worst = max(len({(s + i) // 8 for i in range(b)}) for s in range(8))
    if worst <= 16:
        best = b
v.check("X17.8i", best)

# ---------------------------------------------------------------- Q9
lam9 = C / 915e6
v.check("X17.9a", 20 * math.log10(4 * math.pi * 300 / lam9))
v.check("X17.9b", 20 - 20 * math.log10(4 * math.pi * 300 / lam9))
lam = C / 2.4e9
ht, hr = 10.0, 1.5
v.check("X17.9c", 4 * ht * hr / lam)
dd = 2000.0
d1, d2 = math.hypot(dd, ht - hr), math.hypot(dd, ht + hr)
field = abs(np.exp(-2j * np.pi * d1 / lam) / d1 - np.exp(-2j * np.pi * d2 / lam) / d2) * lam / (4 * math.pi)
v.check("X17.9d", 40 * math.log10(dd) - 20 * math.log10(ht * hr))
v.check("X17.9d2", -20 * math.log10(field))
fD = 25 * 2.6e9 / C
v.check("X17.9e", fD)
v.check("X17.9f", brentq(lambda t: special.j0(2 * math.pi * fD * t) - 0.5, 1e-5, 2e-3) * 1e3)
v.check("X17.9g", special.j0(2 * math.pi * fD * 0.5e-3))
gb = 10 ** 2.5
p1 = integrate.quad(lambda g: Qf(math.sqrt(2 * g)) * math.exp(-g / gb) / gb, 0, 50 * gb, points=[1, 10, 100])[0]
v.check("X17.9h", p1)
v.check("X17.9i", 1 / (4 * gb))
p2 = integrate.quad(lambda g: Qf(math.sqrt(2 * g)) * g * math.exp(-g / gb) / gb**2, 0, 60 * gb, points=[1, 10, 100])[0]
v.check("X17.9j", p2)
v.check("X17.9k", math.comb(3, 2) / (4 * gb) ** 2)

# ---------------------------------------------------------------- Q10
Tu = 1 / 15e3
Tcp = 144 / 2048 * Tu
v.check("X17.10a", Tu * 1e6)
v.check("X17.10b", Tcp * 1e6)
v.check("X17.10c", Tcp / (Tu + Tcp) * 100)
v.check("X17.10d", C * Tcp / 1e3)
df = 0.2e-6 * 2.6e9
v.check("X17.10e", df)
eps = df / 30e3
v.check("X17.10f", eps)
Nfft = 4096
ici = 1 - abs(math.sin(math.pi * eps) / (Nfft * math.sin(math.pi * eps / Nfft))) ** 2
v.check("X17.10g", db(ici))
Hmat = np.array([[1, 0.5], [0.5, 1]])
sv2 = np.linalg.svd(Hmat, compute_uv=False) ** 2
cap = np.log2(np.linalg.det(np.eye(2) + 100 / 2 * Hmat @ Hmat.T))
v.assert_true("Q10 det form = SVD form", abs(cap - np.sum(np.log2(1 + 50 * sv2))) < 1e-12)
v.check("X17.10h", cap)
v.check("X17.10i", math.log2(101))
v.check("X17.10j", db((1.2 + 0.6) * 10))
v.check("X17.10k", db((1.2 + 0.6) * 10 / 2))

# ---------------------------------------------------------------- Q11
v.check("X17.11a", 0.75 * math.exp(-0.75))
v.check("X17.11b", 0.75 * math.exp(-1.5))


def erlang_b(a, c):
    return (a**c / math.factorial(c)) / sum(a**kk / math.factorial(kk) for kk in range(c + 1))


v.check("X17.11c", erlang_b(3, 8) * 100)
v.check("X17.11d", next(c for c in range(1, 60) if erlang_b(10, c) <= 0.01))
v.check("X17.11e", db(math.sqrt(9) ** 3.5 / 6))
v.check("X17.11f", db(math.sqrt(12) ** 3.5 / 6))
v.assert_true("Q11 N = 3 fails and N = 4 passes 10 dB", db(3**3.5 / 6) < 10 < db(12**1.75 / 6))
_ph, _mh = 0.2, 3
_tx = sum(_ph ** (k - 1) for k in range(1, _mh + 1))  # attempt k happens if the first k - 1 failed
v.check("X17.11g", _tx)
v.check("X17.11g2", (1 - _ph ** _mh) / _tx)
v.check("X17.11h", _ph ** _mh)

# ---------------------------------------------------------------- Q12
fields = {"preamble+SFD": 8, "MAC header": 14, "IPv4": 20, "UDP": 8, "payload": 200, "FCS": 4, "IFG": 12}
wire = sum(fields.values())
v.check("X17.12a", wire)
v.check("X17.12b", 200 / wire * 100)
plen = next(p for p in range(30, 0, -1) if ipaddress.ip_network(f"10.0.0.0/{p}").num_addresses - 2 >= 100)
v.check("X17.12c", plen)
v.check("X17.12d", len(list(ipaddress.ip_network("172.16.0.0/20").subnets(new_prefix=plen))))
v.check("X17.12e", 8 * 65535 / 0.08 / 1e6)
bdp = 2.5e9 * 0.08 / 8
v.check("X17.12f", bdp / 1e6)
v.check("X17.12g", next(s for s in range(15) if 65535 * 2**s >= bdp))
v.check("X17.12l", ipaddress.ip_network(f"10.0.0.0/{plen}").num_addresses - 2)
_G = {"P": {"Q": 3, "R": 1}, "Q": {"P": 3, "R": 1, "S": 2}, "R": {"P": 1, "Q": 1, "S": 6, "T": 5},
      "S": {"Q": 2, "R": 6, "T": 1}, "T": {"R": 5, "S": 1}}


def _all_paths(u, dst, seen):
    if u == dst:
        yield [u]
        return
    for w in _G[u]:
        if w not in seen:
            for rest in _all_paths(w, dst, seen | {w}):
                yield [u] + rest


def _dist(dst):
    return min(sum(_G[a][b] for a, b in zip(pth, pth[1:])) for pth in _all_paths("P", dst, {"P"}))


for key, node in (("X17.12h", "Q"), ("X17.12i", "R"), ("X17.12j", "S"), ("X17.12k", "T")):
    v.check(key, _dist(node))
_best = min(_all_paths("P", "T", {"P"}), key=lambda pth: sum(_G[a][b] for a, b in zip(pth, pth[1:])))
v.assert_true("shortest path to T is P-R-Q-S-T (brute-force enumeration)", _best == ["P", "R", "Q", "S", "T"])

# ---------------------------------------------------------------- Q14
N0dbm = -174 + 6
ebn0 = -137 - N0dbm - 60
v.check("X17.14a", ebn0)
v.check("X17.14b", db(math.log(2)) - ebn0)
cn0 = 10 ** ((-137 - N0dbm) / 10)
v.check("X17.14c", cn0)
v.check("X17.14d", cn0 / math.log(2))
v.check("X17.14e", cn0 / 10**0.5)
lam8 = C / 868e6


def two_ray_range(budget_db, h1=15.0, h2=1.0):
    def loss(dist):
        a, b = math.hypot(dist, h1 - h2), math.hypot(dist, h1 + h2)
        fld = abs(np.exp(-2j * np.pi * a / lam8) / a - np.exp(-2j * np.pi * b / lam8) / b) * lam8 / (4 * math.pi)
        return -20 * math.log10(fld)

    return brentq(lambda dist: loss(dist) - budget_db, 1e3, 2e5)


v.check("X17.14f", lam8 / (4 * math.pi) * 10 ** (151 / 20) / 1e3)
v.check("X17.14g", two_ray_range(151) / 1e3)
v.check("X17.14h", two_ray_range(141) / 1e3)
s1m = -174 + 6 + 60 + 5
v.check("X17.14i", s1m)
v.check("X17.14j", two_ray_range(14 - s1m) / 1e3)
v.assert_true("Q14 breakpoint well inside the ranges", 4 * 15 * 1 / lam8 < 1000)

# requested intermediate answers and quoted ratios
v.check("X17.3i", 2 * (40 + 10))
v.check("X17.3j", 2 * 10)
v.check("X17.4i", 56)
v.check("X17.4j", 56 / 2)
v.check("X17.4k", 56 / 2)
v.check("X17.4l", 28 / 2)
v.check("X17.5o", Qf(math.sqrt(g9)) / Qf(math.sqrt(2 * g9)))
v.check("X17.6i", 2 * 25)
v.check("X17.6j", 1.2 * 25)
v.check("X17.8j", (1 - (1 - pbsc) ** 4) / pfail)
v.check("X17.9l", p1 / p2)
v.check("X17.10l", 100 * (cap / math.log2(101) - 1))
v.check("X17.14k", 4 * 15 * 1 / lam8)
v.check("X17.14l", 14 - s1m)
v.check("X17.14m", two_ray_range(14 - s1m - 10) / 1e3)

sys.exit(v.finish())
