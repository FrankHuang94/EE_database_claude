#!/usr/bin/env python3
"""Verify every number in the Course 23 final-exam solutions.

About half the values are recomputed by a second route; the rest are closed-form re-evaluations:
- Question 2(c): the margin by root finding on the exact array yield (1 - Q(k))^N;
- Questions 3(a) and 11(a): charge sharing from conservation of charge solved as a linear system;
- Question 4(c): far-end voltages by summing a lattice diagram; 4(d): cursors by integrating the step response;
- Question 5(c): stack temperatures by solving the thermal ladder's nodal equations;
- Questions 6(c), 8(a) and 8(b): tails by direct summation, limits by root finding;
- Questions 7(b), 7(c) and 11(c): the FIFO fixed point by iteration, checked against Lambert W;
- Question 8(c): the hold-up capacitance by integrating the bank's discharge;
- Question 9(c): the PCM pulse by integrating the thermal ODE;
- Question 10: the crossbar by per-cell summation, the Amdahl fraction by root finding.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, special, stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("23-exam", ROOT / "exam" / "solutions.md")
QE = 1.602176634e-19
KB_EV = 8.617333262e-5
YEAR = 365.25 * 86400


def u_iter(alpha):
    u = 0.5
    for _ in range(10000):
        u = math.exp(-alpha * (1 - u))
    return u


def wa_lambert(alpha):
    return alpha / (alpha + special.lambertw(-alpha * math.exp(-alpha), 0).real)


def share(cs, vcell, cbl, vpre):
    """Solve total charge conservation for the common voltage."""
    vfin = np.linalg.solve(np.array([[cs + cbl]]), np.array([cs * vcell + cbl * vpre]))[0]
    return vfin - vpre


def tail_sum(t, n, p):
    k = np.arange(t + 1, n + 1)
    logs = (special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)
            + k * math.log(p) + (n - k) * math.log1p(-p))
    m = logs.max()
    return math.exp(m) * np.exp(logs - m).sum()


def cap(p):
    return 1 + p * math.log2(p) + (1 - p) * math.log2(1 - p)


# ---------------------------------------------------------------- Q1
v.check("X23.1a", 80 / (5.5e-12 * 8) / 1e12)
v.check("X23.1a1", 6e12 * 8 * 5.5e-12)
v.check("X23.1b", 1024 * 8e9 / 8 / 1e9)
v.check("X23.1b1", 6 * 1024 * 8e9 / 8 / 1e12)
v.check("X23.1c", 6e12 * 500e-9 / 1e6)
v.check("X23.1c1", 6e12 * 500e-9 / 64)
v.check("X23.1d", 3e15 / 6e12)
v.check("X23.1d1", 2 / (3e15 / 6e12) * 100)

# ---------------------------------------------------------------- Q2
raw = 1 / 0.024
v.check("X23.2a", raw)
v.check("X23.2a2", raw)
v.check("X23.2a1", 30 / raw * 100)
new = 0.35 + 0.65 / 1.5
v.check("X23.2b", new * 100)
v.check("X23.2b3", new)
v.check("X23.2b1", 0.35 / new * 100)
v.check("X23.2b2", 1 / new)
N2 = 2 ** 25
v.check("X23.2c0", -math.log(0.99) / N2)
k2 = optimize.brentq(lambda k: N2 * math.log1p(-stats.norm.sf(k)) - math.log(0.99), 3, 10, xtol=1e-12)
v.check("X23.2c", k2)
i2 = 2 ** 27 * 4e-12
v.check("X23.2d", i2 * 1e3)
v.check("X23.2d1", i2 * 0.75 * 1e3)
f2 = 0.5 ** ((0.75 - 0.45) / 0.1)
v.check("X23.2d2", f2)
v.check("X23.2d3", i2 * f2 * 0.45 * 1e3)
v.check("X23.2d4", (i2 * 0.75) / (i2 * f2 * 0.45))

# ---------------------------------------------------------------- Q3
v.check("X23.3a", share(6e-15, 1.1, 36e-15, 0.55) * 1e3)
cbl = optimize.brentq(lambda c: 0.45 * 6 / (6 + c) - 0.07, 0, 1000)
v.check("X23.3b", cbl)
v.check("X23.3b1", cbl)
nmax = (cbl - 3) / 0.07
v.check("X23.3b2", math.floor(nmax))
v.check("X23.3b3", max(2 ** k for k in range(20) if 2 ** k <= nmax))
v.check("X23.3c", 410 / 7812.5 * 100)
v.check("X23.3c1", 410 / 3906.25 * 100)
v.check("X23.3d", 0.8 * 0.5 ** 4 * 1e3)
v.check("X23.3d1", 0.8 * 0.5 ** 5 * 1e3)
v.assert_true("weak cell fails both windows", 0.8 * 0.5 ** 4 < 0.064 and 0.8 * 0.5 ** 5 < 0.032)

# ---------------------------------------------------------------- Q4
v.check("X23.4a", 16 * 16 / 8)
v.check("X23.4a1", 8e9 * 16 / 8 / 1e9)
i4 = 1.1 / 88
v.check("X23.4b", i4 * 1e3)
v.check("X23.4b1", 1.1 * 40 / 88)  # divider: the driver's 40 ohm to ground against 48 ohm to VDDQ
v.check("X23.4b2", 1.1 * i4 * 1e3)
v.check("X23.4b3", 1.1 * i4 / 8e9 * 0.5 * 1e12)
gl, gs = (60 - 40) / 100, (30 - 40) / 70
v.check("X23.4c", gl)
v.check("X23.4c1", gs)
v.check("X23.4c8", gs)
vp = 40 / 70
v.check("X23.4c2", vp)
v.check("X23.4c6", vp)
arrivals, vfar, wave = [], 0.0, vp
for _ in range(200):
    vfar += wave * (1 + gl)
    arrivals.append(vfar)
    wave *= gl * gs
v.check("X23.4c3", arrivals[0])
v.check("X23.4c7", arrivals[0])
v.check("X23.4c4", arrivals[1])
v.check("X23.4c5", arrivals[-1])
v.assert_true("lattice converges to the DC divider", abs(arrivals[-1] - 60 / 90) < 1e-12)
tau = 0.8
step = lambda t: 1 - math.exp(-t / tau) if t > 0 else 0.0  # noqa: E731
h = [step(k + 1) - step(k) for k in range(60)]  # one-UI pulse sampled at the end of each UI
a4 = math.exp(-1 / tau)
v.check("X23.4d", a4)
v.check("X23.4d1", h[0])
v.check("X23.4d2", h[1])
v.check("X23.4d3", h[0] - sum(h[1:]))
v.check("X23.4d4", h[0] - sum(h[2:]))

# ---------------------------------------------------------------- Q5
v.check("X23.5a", 2048 * 10e9 / 8 / 1e12)
v.check("X23.5a1", 8 * 2048 * 10e9 / 8 / 1e12)
v.check("X23.5a2", 12 * 24 / 8)
e5 = 0.25 * 0.8e-12 * 0.4 ** 2
v.check("X23.5b", e5 * 1e12)
v.check("X23.5b1", 2048 * 10e9 * e5)
# nodal thermal ladder: node 0 is the top (heat sink, 0 K); layer j sits between nodes; base die is the bottom node
n5, rl = 16, 0.03
g = 1 / rl
A = np.zeros((n5, n5))
b = np.zeros(n5)
for j in range(n5):  # node j = die j from the top (j = n5-1 is the base die)
    A[j, j] += g
    if j > 0:
        A[j, j - 1] -= g
        A[j - 1, j] -= g
        A[j - 1, j - 1] += g
    b[j] = 12 if j == n5 - 1 else 1.2
temps = np.linalg.solve(A, b)
v.check("X23.5c", temps[-1])
v.check("X23.5d", 0.995 ** 16 * 100)
v.check("X23.5d1", math.exp(math.log(0.9) / 16) * 100)

# ---------------------------------------------------------------- Q6
dv6 = QE / 18e-18
v.check("X23.6a", dv6 * 1e3)
v.check("X23.6a4", dv6 * 1e3)
gap = 5.8 / 15
v.check("X23.6a1", gap)
v.check("X23.6a3", gap)
v.check("X23.6a2", gap / dv6)
n_p, vt = 0, -1.8
while vt < 4.2 - 1e-9:
    vt += 0.2
    n_p += 1
v.check("X23.6b", n_p)
v.check("X23.6b1", n_p * 22)
v.check("X23.6c", gap / 0.14)
v.check("X23.6c1", gap / 0.14)
centres = np.linspace(0, 5.8, 16)
edges = np.concatenate(([-np.inf], (centres[:-1] + centres[1:]) / 2, [np.inf]))
gray = [i ^ (i >> 1) for i in range(16)]
tot = 0.0
for i, c in enumerate(centres):
    for j in range(16):
        if i != j:
            pij = stats.norm.cdf(edges[j + 1], c, 0.07) - stats.norm.cdf(edges[j], c, 0.07)
            tot += pij * bin(gray[i] ^ gray[j]).count("1")
v.check("X23.6c2", tot / 16 / 4)
af = math.exp(-1.0 / (KB_EV * 398.15)) / math.exp(-1.0 / (KB_EV * 313.15))
v.check("X23.6d", af)
v.check("X23.6d2", YEAR / 3600)
v.check("X23.6d1", YEAR / 3600 / af)

# ---------------------------------------------------------------- Q7
v.check("X23.7a", 15.36e12 // 4096 * 4 / 1e9)
v.check("X23.7a1", 15.36e12 // 16384 * 4 / 1e9)
u12 = u_iter(1.12)
v.check("X23.7b", u12)
v.check("X23.7b1", 1 / (1 - u12))
v.assert_true("iteration matches Lambert W", abs(1 / (1 - u12) - wa_lambert(1.12)) < 1e-9)
v.check("X23.7b2", 1 / (1 - u_iter(1.25)))
a7 = 17.2 / 15.36
A7 = 1 / (1 - u_iter(a7))
v.check("X23.7c", (a7 - 1) * 100)
v.check("X23.7c1", A7)
v.check("X23.7c4", A7)
tbw = 17.2 * 3000 / A7
v.check("X23.7c2", tbw)
v.check("X23.7c3", tbw / (15.36 * 1825))
v.check("X23.7d", 3.2e6 * 90e-6)
v.check("X23.7d1", 3.2e6 * 4096 / 1e9)
v.check("X23.7d2", 1 / 90e-6)

# ---------------------------------------------------------------- Q8
n8 = 8192 + 13 * 48
v.check("X23.8a", 13 * 48)
v.check("X23.8a1", n8)
v.check("X23.8a2", n8 * 2e-3)
v.check("X23.8a3", tail_sum(48, n8, 2e-3))
lam = n8 * 2e-3
v.check("X23.8a4", 1 - sum(math.exp(-lam) * lam ** k / math.factorial(k) for k in range(49)))
r8 = 16 / 18.5
v.check("X23.8b", r8)
v.check("X23.8b1", cap(0.01))
v.check("X23.8b2", optimize.brentq(lambda p: cap(p) - r8, 1e-4, 0.2) * 100)
e8 = 25 * 0.03 / 0.9
v.check("X23.8c", e8)
v.check("X23.8c2", e8)


def hold(c):
    sol = integrate.solve_ivp(lambda t, y: [-25 / 0.9 / (c * y[0])], (0, 1), [36.0],
                              events=lambda t, y: y[0] - 12, rtol=1e-10, atol=1e-12)
    return sol.t_events[0][0]


v.check("X23.8c1", optimize.brentq(lambda c: hold(c) - 0.03, 1e-4, 1e-2, xtol=1e-12) * 1e3)

# ---------------------------------------------------------------- Q9
rap = 5e3 * (1 + 1.2)
ip, iap = 0.12 / (5e3 + 2.5e3), 0.12 / (rap + 2.5e3)
v.check("X23.9a", rap / 1e3)
v.check("X23.9a1", ip * 1e6)
v.check("X23.9a2", iap * 1e6)
v.check("X23.9a4", iap * 1e6)
v.check("X23.9a3", (ip / iap - 1) * 100)
d9 = optimize.brentq(lambda d: 2 ** 27 * 10 * YEAR * 1e9 * math.exp(-d) - 1, 10, 200, xtol=1e-12)
v.check("X23.9b", d9)
v.check("X23.9b1", d9 * KB_EV * 378.15 / (KB_EV * 298.15))
p9 = (250e-6) ** 2 * 1.6e3
v.check("X23.9c", p9 * 1e6)
rth = 620 / p9
v.check("X23.9c1", rth / 1e6)
v.check("X23.9c2", p9 * 40e-9 * 1e12)
cth = 1.5e-9 / rth
ev = lambda t, y: y[0] - 140  # noqa: E731
ev.terminal = True
sol9 = integrate.solve_ivp(lambda t, y: [-y[0] / rth / cth], (0, 1e-7), [620.0], events=ev, rtol=1e-11, atol=1e-10)
v.check("X23.9c3", sol9.t_events[0][0] * 1e9)
v.check("X23.9d", math.exp(0.08 * math.log(YEAR)))
v.check("X23.9d1", math.exp(math.log(1.5) / 0.08))

# ---------------------------------------------------------------- Q10
x10 = [0.5, 1.5, 1.0]
W10 = [[2, -1], [-1, 3], [1, 1]]
cur = {}
for j in range(2):
    for sgn in ("p", "n"):
        tot = 0.0
        for i in range(3):
            w = W10[i][j]
            g = 8e-6 * (max(w, 0) if sgn == "p" else max(-w, 0)) + 0.5e-6
            tot += 0.1 * x10[i] * g
        cur[(j, sgn)] = tot
v.check("X23.10a", cur[(0, "p")] * 1e6)
v.check("X23.10a1", cur[(0, "n")] * 1e6)
v.check("X23.10a2", cur[(1, "p")] * 1e6)
v.check("X23.10a3", cur[(1, "n")] * 1e6)
v.check("X23.10a4", (cur[(0, "p")] - cur[(0, "n")]) * 1e6)
v.check("X23.10a5", (cur[(1, "p")] - cur[(1, "n")]) * 1e6)
v.check("X23.10a6", sum(x10[i] * W10[i][0] for i in range(3)))
v.check("X23.10a7", sum(x10[i] * W10[i][1] for i in range(3)))
v.check("X23.10a8", 0.1 * 8e-6 * 1e6)
snr10 = 10 * math.log10(1 / 0.03 ** 2)
v.check("X23.10b", snr10)
v.check("X23.10b2", snr10)
v.check("X23.10b1", (snr10 - 1.76) / 6.02)
e10 = 3e-15 * 2 ** 8 * 16 / 256
v.check("X23.10c", e10 * 1e15)
v.check("X23.10c1", 2 / e10 / 1e12)
v.check("X23.10d", 1 / (0.3 + 0.7 / 6))
v.check("X23.10d1", optimize.brentq(lambda f: 1 / ((1 - f) + f / 6) - 2.5, 0, 1, xtol=1e-14))

# ---------------------------------------------------------------- Q11
v.check("X23.11a", 7 / 42)
v.check("X23.11a1", share(7e-15, 1.05, 35e-15, 0.525) * 1e3)
v.check("X23.11b", 18e-18 * 0.25 / QE)
u11 = u_iter(1.2)
v.check("X23.11c", u11)
v.check("X23.11c1", 1 / (1 - u11))
v.check("X23.11c2", math.exp(-1.2 * (1 - u11)))
v.check("X23.11c3", 1 - u11)
v.check("X23.11d", 10 * math.log10(1 / 0.04 ** 2))
v.check("X23.11d1", 10 * math.log10(128 / 0.04 ** 2))

# ---------------------------------------------------------------- Q12
bw12 = 8 * 614e9
m12 = 70e9 * 4 / 8
v.check("X23.12a", bw12 / 1e12)
v.check("X23.12a1", m12 / 1e9)
v.check("X23.12a2", bw12 / m12)
base = 8 * 76.8e9 / m12
v.check("X23.12a3", base)
v.check("X23.12a4", base)
sp = 1 / (0.2 + 0.8 / 8)
v.check("X23.12b", sp)
v.check("X23.12b1", base * sp)
kv = 2 * 80 * 8 * 128 * 1
v.check("X23.12c", kv)
v.check("X23.12c1", kv * 32768 / 1e9)
v.check("X23.12c3", kv * 32768 / 1e9)
v.check("X23.12c2", math.floor((128e9 - m12) / (kv * 32768)))
v.check("X23.12d", 8e12 / m12)
v.check("X23.12d1", (8e12 / m12) / (base * sp))

sys.exit(v.finish())
