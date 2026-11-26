#!/usr/bin/env python3
"""Verify every number in the Course 27 final exam solutions, mostly by second routes.

Routes: an ODE for the thermal burst (1d); Little's law from a queue simulation count (2c);
golden-section minimization of energy per instruction (3b); numerical integration of a
Lambertian emitter (4a); a simulated ANC residual in the time domain (5a); a stepped EWMA (6b);
bit-by-bit worst-case stuffing (7a); integrated braking (7c); an executed ring all-reduce (8b-d,
12b); a numerical minimization of the lost fraction (9b); the LoRa payload by search (10c); and
an ODE for the supercapacitor discharge (11d).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("27-exam", ROOT / "exam" / "solutions.md")
rng = np.random.default_rng(27)

# ---------------------------------------------------------------- Q1
eta_ldo = 1.8 / 3.8
Pb = 1.2 / 0.9 + 0.6 / 0.85 + 0.15 / eta_ldo
v.check("X27.1a", Pb)
v.check("X27.1a1", 100 * 1.95 / Pb)
v.check("X27.1a2", Pb - 1.95)
v.check("X27.1a3", 100 * eta_ldo)
v.check("X27.1b", 0.9 * 15 / Pb)
Psus = (43 - 25) / 9
v.check("X27.1c", Psus)
# ODE: C dT/dt = P - (T - Ta)/theta with tau = theta C = 300 s
theta, tau = 9.0, 300.0
Cth = tau / theta
sol = integrate.solve_ivp(lambda t, T: [(6.0 - (T[0] - 25) / theta) / Cth], (0, 600), [25 + 1.0 * theta],
                          events=lambda t, T: T[0] - 43, rtol=1e-10, atol=1e-10)
v.check("X27.1d", sol.t_events[0][0])
v.check("X27.1d1", 100 * (Psus - 1.0) / (6.0 - 1.0))

# ---------------------------------------------------------------- Q2
beta = 64 / 8 * 8533e6
v.check("X27.2a", beta / 1e9)
v.check("X27.2a1", beta / (3e9 * 0.5))
v.check("X27.2b", 1 / ((1 - 0.4) + 0.4 / 10))
# Little's law by counting: requests issued at rate beta/64 per second, each held 120 ns
rate = beta / 64
t = np.sort(rng.uniform(0, 2e-5, int(rate * 2e-5)))
probe = np.linspace(2e-6, 1.8e-5, 200)
inflight = np.mean([np.sum((t <= p) & (t > p - 120e-9)) for p in probe])
v.assert_true(f"simulated lines in flight {inflight:.1f} near 128", abs(inflight - 128) < 6)
v.check("X27.2c", beta * 120e-9)
v.check("X27.2c1", beta * 120e-9 / 64)
dlnperf = (math.log((3.0 + 1e-6) ** (1 / 3)) - math.log((3.0 - 1e-6) ** (1 / 3))) / 2e-6  # numerical derivative
v.check("X27.2d", 100 * 0.3 * dlnperf)

# ---------------------------------------------------------------- Q3
c, V0, k, IPC, Ps = 1e-9, 0.5, 0.25e-9, 2, 0.1
E = lambda f: c * (V0 + k * f) ** 2 / IPC + Ps / (IPC * f)  # noqa: E731
v.check("X27.3a", 1e9 * E(1e9))
v.check("X27.3a1", 1e9 * E(3e9))
res = optimize.minimize_scalar(E, bounds=(1e8, 5e9), method="bounded", options={"xatol": 1e3})
v.check("X27.3b", res.x / 1e9)
v.check("X27.3c", 1e9 * res.fun)
dram = sum(d * (1 - h) for d, h in ((30, 0.4), (10, 0.2), (15, 0.6)))
v.check("X27.3d", dram)
v.check("X27.3d1", 9600e6 * 8 / 1e9)
v.check("X27.3d2", 100 * dram / 76.8)

# ---------------------------------------------------------------- Q4
flux, _ = integrate.dblquad(lambda th, ph: 400 * math.cos(th) * math.sin(th), 0, 2 * math.pi, 0, math.pi / 2)
Pd = flux * 9e-4 * 0.2 / 5
v.check("X27.4a", 1e3 * Pd)
Q = 2e-3 * 400e-6 + 5e-3 * 250e-6 + 6e-3 * 100e-6
v.check("X27.4b", 1e6 * Q)
v.check("X27.4b1", 1e6 * (3e-6 + Q / 0.1))
Eb = 0.300 * 3.85
v.check("X27.4c", Eb)
Eday = Pd * 2 + (0.020 + 0.003 + 0.005) * 24
v.check("X27.4c1", Eday)
v.check("X27.4c2", 24 * 0.9 * 0.9 * Eb / Eday)
v.check("X27.4d", 1e3 * (50 * 20e-6 + 50 * 2e-3 / 100))
v.check("X27.4d1", 1e3 * (50 * 20e-6 + 50 * 2e-3))

# ---------------------------------------------------------------- Q5 (time-domain residual)
def att_sim(f, tau=30e-6, g=1.0):
    fs = 2e6
    tt = np.arange(0, 0.2, 1 / fs)
    x = np.sin(2 * np.pi * f * tt)
    xd = np.sin(2 * np.pi * f * (tt - tau))
    r = x - g * xd
    return -20 * math.log10(np.sqrt(np.mean(r ** 2)) / np.sqrt(np.mean(x ** 2)))


v.check("X27.5a", att_sim(200))
v.check("X27.5a1", att_sim(1000))
v.check("X27.5b", optimize.brentq(lambda f: att_sim(f), 3000, 8000) / 1e3)
v.check("X27.5b1", optimize.brentq(lambda f: att_sim(f), 20000, 30000) / 1e3)
v.check("X27.5c", 200 * 0.012)
v.check("X27.5c1", optimize.brentq(lambda t: 200 * t - 1.0, 1e-4, 0.1) * 1e3)
Ebud = 55 * 3.85
v.check("X27.5d", Ebud * 0.85 / 18)
v.check("X27.5d1", 0.70 * 500 * 3.85 / (2 * Ebud))

# ---------------------------------------------------------------- Q6 (stepped EWMA)
Psoc = 0.6 * 0.5 + 0.3 * 3 + 0.1 * 15
v.check("X27.6a", Psoc)
v.check("X27.6a1", 60 / (Psoc + 2.5))
y, tt, dt = 5.0, 0.0, 1e-3
while y < 28.0:
    y += (55.0 - y) * dt / 28.0
    tt += dt
v.check("X27.6b", tt)
bw6 = 256 / 8 * 8000e6
v.check("X27.6c", bw6 / 1e9)
v.check("X27.6c1", bw6 / (14e9 * 0.5))
v.check("X27.6d", 2 * 14e9 * 4000 / (50e12 * 0.35))

# ---------------------------------------------------------------- Q7
def stuffed(nbytes):
    region = 34 + 8 * nbytes
    wire, last, run, stuff = 0, None, 0, 0
    for _ in range(region):
        bit = last if last is not None else 0
        if bit == last:
            run += 1
        else:
            run = 1
        last = bit
        wire += 1
        if run == 5:
            last = 1 - last
            stuff += 1
            run = 1
    return region + 13 + stuff


nb = stuffed(6)
v.check("X27.7a", nb)
v.check("X27.7a1", 1e6 * nb / 500e3)
v.check("X27.7b", 100 * optimize.brentq(lambda dc: 800 * (1 - dc) - 8, 0.5, 1.0))
v.check("X27.7b1", 800 * (1 - 0.98))
vv = 120 / 3.6
s = integrate.solve_ivp(lambda t, z: [z[1], -6.5 if t > 0.25 else 0.0], (0, 15), [0, vv],
                        events=lambda t, z: z[1], max_step=1e-3, rtol=1e-9, atol=1e-9)
v.check("X27.7c", s.y_events[0][0][0])
v.check("X27.7c1", vv * 0.25)
v.check("X27.7d", 100 * 300 / (300 + 150 * 50))

# ---------------------------------------------------------------- Q8 (executed ring)
def ring_steps(p):
    data = rng.integers(0, 100, size=(p, p))
    total = data.sum(axis=0)
    r = np.arange(p)
    steps = 0
    for kk in range(p - 1):
        cidx = (r - kk) % p
        pay = data[r, cidx].copy()
        data[(r + 1) % p, cidx] += pay
        steps += 1
    for kk in range(p - 1):
        cidx = (r + 1 - kk) % p
        pay = data[r, cidx].copy()
        data[(r + 1) % p, cidx] = pay
        steps += 1
    assert np.all(data == total)
    return steps


F = 6 * 70e9 * 2e12
v.check("X27.8a", F)
v.check("X27.8a1", F / (1024 * 1e15 * 0.4) / 86400)
ins = ring_steps(8) * (2e9 / 8) / 200e9
v.check("X27.8b", 1e3 * ins)
acr = ring_steps(128) * (2e9 / 8 / 128) / 50e9
v.check("X27.8c", 1e3 * acr)
v.check("X27.8c1", 1e3 * (ins + acr))
flat = ring_steps(1024) * (2e9 / 1024) / 50e9
v.check("X27.8d", 1e3 * flat)
v.check("X27.8d1", flat / (ins + acr))

# ---------------------------------------------------------------- Q9
M = 60000 / 20000 * 3600
v.check("X27.9a", M / 3600)
res9 = optimize.minimize_scalar(lambda tau_: 30 / tau_ + tau_ / (2 * M), bounds=(1, M), method="bounded",
                                options={"xatol": 1e-6})
v.check("X27.9b", res9.x)
lost = res9.fun + 300 / M
v.check("X27.9c", 100 * lost)
v.check("X27.9c1", 100 * (1 - lost))
step = (140e9 + 64 * 0.5e9) / (0.6 * 64e12)
v.check("X27.9d", 1e3 * step)
v.check("X27.9d1", 64 / step)
v.check("X27.9d2", 1 / step)
v.check("X27.9d3", 60e3 / (64 / step))

# ---------------------------------------------------------------- Q10
macs = sum(1 for _ in range(16 * 16 * 32)) * 9 * 16
v.check("X27.10a", macs)
v.check("X27.10b", 1e3 * macs / 100e6)
v.check("X27.10b1", 1e6 * macs / 100e6 * 10e-3)
tn = macs / (64 * 0.3 * 100e6)
v.check("X27.10b2", 1e3 * tn)
v.check("X27.10b3", 1e6 * tn * 15e-3)
Ts = 2 ** 8 / 125e3
need = 8 * 12 - 4 * 8 + 28 + 16
blocks = 0
while blocks * 4 * 8 < need:
    blocks += 1
nsym = 8 + 5 * blocks
toa = (8 + 4.25 + nsym) * Ts
v.check("X27.10c", 1e3 * Ts)
v.check("X27.10c1", nsym)
v.check("X27.10c2", 1e3 * toa)
v.check("X27.10c3", math.floor(36 / toa))
v.check("X27.10d", 1e3 * 8000 * 12 * 50e-9)
loc = 10 * tn * 15e-3 + 0.2e-3
v.check("X27.10d1", 1e3 * loc)
v.check("X27.10d2", 8000 * 12 * 50e-9 / loc)

# ---------------------------------------------------------------- Q11
Ee = 8000 / 105
P = Ee * 12e-4 * 0.18 * 0.8
v.check("X27.11a", Ee)
v.check("X27.11a1", 1e3 * P)
v.check("X27.11a2", P * 36000)
L = 0.5e-3 + 48 * 0.040 / 86400
v.check("X27.11b", 1e3 * L)
v.check("X27.11b1", L * 86400)
v.check("X27.11b2", P * 36000 / (L * 86400))
E72 = L * 72 * 3600
v.check("X27.11c", E72)
v.check("X27.11c1", 2 * E72 / (5.0 ** 2 - 2.5 ** 2))
s11 = integrate.solve_ivp(lambda t, V: [-L / (10.0 * V[0])], (0, 3e5), [5.0],
                          events=lambda t, V: V[0] - 2.5, rtol=1e-10, atol=1e-12)
v.check("X27.11d", s11.t_events[0][0])
v.check("X27.11d1", s11.t_events[0][0] / 3600)

# ---------------------------------------------------------------- Q12
st = ring_steps(72)
v.check("X27.12b", 1e3 * st * (4e9 / 72) / 900e9)
v.check("X27.12b1", 1e3 * st * 2e-6)
v.check("X27.12b2", 1e3 * st * ((4e9 / 72) / 900e9 + 2e-6))
cap = 3.6e6 / 4
en = 140 * 1.25 * 8760 * 0.07
tok = 1.2e5 * 0.5 * 8760 * 3600
v.check("X27.12c", cap)
v.check("X27.12c1", en)
v.check("X27.12c2", tok)
v.check("X27.12c3", (cap + en) / (tok / 1e6))
v.check("X27.12c4", 100 * en / (cap + en))

sys.exit(v.finish())
