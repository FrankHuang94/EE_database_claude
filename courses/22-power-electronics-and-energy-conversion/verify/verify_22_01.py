#!/usr/bin/env python3
"""Verify every number in chapter 22-01 (power conversion principles), its problems and its lab.

Independent routes (the lab module power.py uses closed forms and matrix exponentials):
- capacitor-charging and charge-sharing losses come from integrating i^2 R along numerical ODE solutions;
- the buck's ripple comes from brute-force time stepping of the switched ODE until periodic steady state,
  and from a Fourier sum over 400 harmonics through the loaded LC filter;
- switch-node harmonic amplitudes come from an FFT of a sampled rectangular wave;
- the peak-efficiency load and the phase-shedding thresholds come from numerical minimization and root finding;
- the hold-up capacitance comes from integrating C v dv/dt = -P at constant power and solving for C;
- the chain losses are computed by stepping forward from the source instead of back from the load;
- volumes use 25.4 mm per inch directly.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-01-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-01", ROOT / "chapters" / "22-01-power-conversion-principles.md",
                        ROOT / "solutions" / "22-01-solutions.md", LAB / "README.md")
IN3_MM3 = 25.4 ** 3


def loss(p_out, eta):
    """Loss as input minus output (input computed first)."""
    p_in = p_out / eta
    return p_in - p_out


def rc_charge_loss(c, r, v_from, v_to, v_cap0):
    """Integrate i^2 R for a capacitor at v_cap0 connected through r to a source stepped to v_to."""
    tau = r * c

    def rhs(t, y):
        vc, e = y
        i = (v_to - vc) / r
        return [i / c, i * i * r]

    sol = integrate.solve_ivp(rhs, (0, 40 * tau), [v_cap0, 0.0], rtol=1e-11, atol=1e-16, method="LSODA")
    return sol.y[1, -1]


def share_ode(c1, v1, c2, v2, r=1.0):
    def rhs(t, y):
        a, b, e = y
        i = (a - b) / r
        return [-i / c1, i / c2, i * i * r]

    tau = r * c1 * c2 / (c1 + c2)
    sol = integrate.solve_ivp(rhs, (0, 40 * tau), [v1, v2, 0.0], rtol=1e-11, atol=1e-18, method="LSODA")
    return sol.y[2, -1]


def buck_bruteforce(v_in, d, fs, ind, cap, r, periods=600, pts=4000):
    """Time-step the switched buck from rest until periodic steady state; return (avg, p-p, i_in avg)."""
    t_s = 1 / fs
    x = np.array([0.0, 0.0])

    def make_rhs(vs):
        return lambda t, y: [(vs - y[1]) / ind, y[0] / cap - y[1] / (r * cap)]

    on, off = make_rhs(v_in), make_rhs(0.0)
    for _ in range(periods):
        s1 = integrate.solve_ivp(on, (0, d * t_s), x, rtol=1e-10, atol=1e-13)
        s2 = integrate.solve_ivp(off, (0, (1 - d) * t_s), s1.y[:, -1], rtol=1e-10, atol=1e-13)
        x = s2.y[:, -1]
    t1 = np.linspace(0, d * t_s, pts)
    t2 = np.linspace(0, (1 - d) * t_s, pts)
    s1 = integrate.solve_ivp(on, (0, d * t_s), x, t_eval=t1, rtol=1e-11, atol=1e-14)
    s2 = integrate.solve_ivp(off, (0, (1 - d) * t_s), s1.y[:, -1], t_eval=t2, rtol=1e-11, atol=1e-14)
    vo = np.concatenate([s1.y[1], s2.y[1]])
    tt = np.concatenate([t1, d * t_s + t2])
    avg = np.trapezoid(vo, tt) / t_s
    i_in = np.trapezoid(s1.y[0], t1) / t_s
    return avg, vo.max() - vo.min(), i_in


def fourier_ripple(v_in, d, fs, ind, cap, r, nmax=400):
    w = 2 * math.pi * fs
    t = np.linspace(0, 1 / fs, 8001)
    vo = np.full_like(t, d * v_in)
    for n in range(1, nmax + 1):
        cn = v_in / (1j * 2 * math.pi * n) * (1 - np.exp(-1j * 2 * math.pi * n * d))
        wn = n * w
        h = 1 / (1 - wn * wn * ind * cap + 1j * wn * ind / r)
        vo = vo + 2 * np.real(cn * h * np.exp(1j * wn * t))
    return vo.max() - vo.min()


def fft_harmonic(v_in, d, n, samples=1 << 16):
    x = np.where(np.arange(samples) < d * samples, v_in, 0.0)
    return 2 * abs(np.fft.rfft(x)[n]) / samples


def holdup_c(p, t_hold, v1, v2):
    """Solve for C such that a constant-power discharge from v1 reaches v2 at t_hold (ODE route)."""
    def t_reach(c):
        ev = lambda t, y: y[0] - v2  # noqa: E731
        ev.terminal = True
        sol = integrate.solve_ivp(lambda t, y: [-p / (c * y[0])], (0, 10), [v1], events=ev, rtol=1e-11,
                                  atol=1e-12)
        return sol.t_events[0][0]

    return optimize.brentq(lambda c: t_reach(c) - t_hold, 1e-5, 1e-1, xtol=1e-12)


def peak_current(p0, a, r):
    res = optimize.minimize_scalar(lambda i: (p0 + a * i + r * i * i) / i, bounds=(1e-3, 1e3), method="bounded",
                                   options={"xatol": 1e-10})
    return res.x


def shed_point(n, p0, r):
    f = lambda i: (n * p0 + r * i * i / n) - ((n + 1) * p0 + r * i * i / (n + 1))  # noqa: E731
    return optimize.brentq(f, 1e-3, 1e4, xtol=1e-12)


def chain_forward(p_in, etas):
    losses = []
    p = p_in
    for e in etas:
        losses.append(p * (1 - e))
        p *= e
    return losses, p


def chain_input(p_load, etas):
    return optimize.brentq(lambda pin: chain_forward(pin, etas)[1] - p_load, p_load, 10 * p_load, xtol=1e-12)


# ---------------------------------------------------------------- Example 22-01.1
print("Example 22-01.1")
v.check("Ex 22-01.1a", loss(1000, 0.96))
v.check("Ex 22-01.1b", loss(1000, 0.965))
v.check("Ex 22-01.1c", (1 - loss(1, 0.965) / loss(1, 0.96)) * 100)
v.check("Ex 22-01.1d", loss(16500, 0.96) - loss(16500, 0.965))
v.check("Ex 22-01.1e", (loss(16500, 0.96) - loss(16500, 0.965)) * 8760 / 1000)
v.check("Ex 22-01.1f", 0.005 * 16500 / 0.96)
v.check("Ex 22-01.1g", loss(16500, 0.96))
v.check("Ex 22-01.1h", loss(16500, 0.965))

# ---------------------------------------------------------------- Example 22-01.2
print("Example 22-01.2")
VB, VO, IQ = 3.6, 1.8, 25e-9
for key, i in (("a", 10e-3), ("c", 1e-6)):
    pin = VB * (i + IQ)
    v.check(f"Ex 22-01.2{key}", VO * i / pin * 100)
v.check("Ex 22-01.2b", (VB * (10e-3 + IQ) - VO * 10e-3) * 1e3)
v.check("Ex 22-01.2d", (VB * (1e-6 + IQ) - VO * 1e-6) * 1e6)
ib = VO * 1e-6 / 0.8 / VB
v.check("Ex 22-01.2e", ib * 1e6)
v.check("Ex 22-01.2f", (1e-6 + IQ) / ib)
v.check("Ex 22-01.2g", IQ / 1e-6 * 100)

# ---------------------------------------------------------------- Example 22-01.3
print("Example 22-01.3")
e1 = rc_charge_loss(10e-6, 1.0, 0, 5.0, 0.0)
e100 = rc_charge_loss(10e-6, 100.0, 0, 5.0, 0.0)
v.assert_true("charging loss independent of R (1 ohm vs 100 ohm)", abs(e1 - e100) / e1 < 1e-6)
v.check("Ex 22-01.3a", e1 * 1e6)
estep = sum(rc_charge_loss(10e-6, 1.0, 0, 1.25 * k, 1.25 * (k - 1)) for k in range(1, 5))
v.check("Ex 22-01.3b", estep * 1e6)
es = share_ode(1e-6, 5.0, 1e-6, 4.8)
v.check("Ex 22-01.3c", es * 1e9)
v.check("Ex 22-01.3d", es * 1e6 * 1e3)
v.check("Ex 22-01.3e", 10e-6 * 5.0 * 5.0 * 1e6)   # charge C V times voltage V

# ---------------------------------------------------------------- Example 22-01.4
print("Example 22-01.4")
VIN, FS, LL, CC, RL = 12.0, 500e3, 10e-6, 1e-6, 3.3
D = 3.3 / VIN
v.check("Ex 22-01.4a", D)
avg, vpp, iin = buck_bruteforce(VIN, D, FS, LL, CC, RL)
v.assert_true("brute-force buck average equals D Vin", abs(avg - 3.3) < 1e-6)
v.check("Ex 22-01.4b", iin)
f0 = 1 / (2 * math.pi * math.sqrt(LL * CC))
v.check("Ex 22-01.4c", f0 / 1e3)
a1 = fft_harmonic(VIN, D, 1)
v.check("Ex 22-01.4d", a1)
att = abs(1 - (FS / f0) ** 2)
v.check("Ex 22-01.4k", att)
v.check("Ex 22-01.4e", 2 * a1 / att * 1e3)
v.check("Ex 22-01.4f", vpp * 1e3)
v.assert_true("Fourier-sum ripple matches the time-domain ripple", abs(fourier_ripple(VIN, D, FS, LL, CC, RL) - vpp) < 1e-5)
_, vpp2, _ = buck_bruteforce(VIN, D, 2 * FS, LL / 2, CC / 2, RL, periods=600)
v.assert_true("halving L and C at twice f_s leaves the ripple unchanged", abs(vpp2 - vpp) < 1e-6)
v.check("Ex 22-01.4g", LL / 2 * 1e6)
v.check("Ex 22-01.4h", CC / 2 * 1e6)
v.check("Ex 22-01.4i", (1 - (2 * a1 / att) / vpp) * 100)
v.check("Ex 22-01.4j", vpp / 3.3 * 100)

# ---------------------------------------------------------------- Example 22-01.5
print("Example 22-01.5")
P0, A, R = 0.150, 0.030, 0.003
eta = lambda i, p0=P0: i / (i + p0 + A * i + R * i * i)  # noqa: E731
ip = peak_current(P0, A, R)
v.check("Ex 22-01.5a", ip)
v.check("Ex 22-01.5b", eta(ip) * 100)
for key, i in (("c", 20.0), ("d", 1.0), ("e", 0.1)):
    v.check(f"Ex 22-01.5{key}", eta(i) * 100)
v.check("Ex 22-01.5f", eta(0.1, 0.015) * 100)
v.check("Ex 22-01.5g", shed_point(1, P0, R))
v.check("Ex 22-01.5h", shed_point(2, P0, R))
v.check("Ex 22-01.5i", 25 * (P0 + A * 20 + R * 400))
v.check("Ex 22-01.5j", 2 * P0 + A * 20 + R * 400 / 2)
v.check("Ex 22-01.5k", P0 + A * ip + R * ip * ip)
for key, i, p0 in (("l", 20.0, P0), ("m", 1.0, P0), ("n", 0.1, P0), ("o", 0.1, 0.015)):
    v.check(f"Ex 22-01.5{key}", p0 + A * i + R * i * i)

# ---------------------------------------------------------------- Example 22-01.6
print("Example 22-01.6")
vol18 = 104 * 710 * 40
v.check("Ex 22-01.6g", vol18 / 1e6)
v.check("Ex 22-01.6a", vol18 / IN3_MM3)
v.check("Ex 22-01.6b", 18e3 / (vol18 / IN3_MM3))
vol55 = 640 * 73.5 * 40
v.check("Ex 22-01.6h", vol55 / 1e6)
v.check("Ex 22-01.6i", vol55 / IN3_MM3)
v.check("Ex 22-01.6c", 5.5e3 / (vol55 / IN3_MM3))
for key, e in (("d", 0.95), ("e", 0.975), ("f", 0.99)):
    # largest output whose loss fits q = 3 W/in^3 in one cubic inch
    v.check(f"Ex 22-01.6{key}", optimize.brentq(lambda p, e=e: loss(p, e) - 3.0, 1e-3, 1e5, xtol=1e-12))

# ---------------------------------------------------------------- Example 22-01.7
print("Example 22-01.7")
pb = 5500 / 0.985
v.check("Ex 22-01.7a", pb)
c320 = holdup_c(pb, 0.020, 400, 320)
v.check("Ex 22-01.7b", c320 * 1e3)
v.check("Ex 22-01.7c", 0.5 * c320 * 400 ** 2)
c300 = holdup_c(pb, 0.020, 400, 300)
v.check("Ex 22-01.7d", c300 * 1e3)
v.check("Ex 22-01.7e", (1 - c300 / c320) * 100)
v.check("Ex 22-01.7f", 0.5 * c320 * (400 ** 2 - 320 ** 2))
v.check("Ex 22-01.7g", (400 ** 2 - 320 ** 2) / 400 ** 2 * 100)

# ---------------------------------------------------------------- Example 22-01.8
print("Example 22-01.8")
CH = [0.97, 0.975, 0.977, 0.90]
pin = chain_input(1000, CH)
ls, _ = chain_forward(pin, CH)
v.check("Ex 22-01.8a", 1000 / pin * 100)
v.check("Ex 22-01.8b", pin - 1000)
v.check("Ex 22-01.8c", ls[3])
v.check("Ex 22-01.8d", ls[0])
v.check("Ex 22-01.8i", ls[1])
v.check("Ex 22-01.8h", ls[2])
v.check("Ex 22-01.8g", ls[3] / (pin - 1000) * 100)
pin92 = chain_input(1000, CH[:3] + [0.92])
v.check("Ex 22-01.8k", pin92 - 1000)
v.check("Ex 22-01.8e", pin - pin92)
v.check("Ex 22-01.8f", pin - chain_input(1000, [0.98] + CH[1:]))
v.check("Ex 22-01.8j", chain_input(1, CH[:3]))

# ---------------------------------------------------------------- text
print("Text")
v.check("Txt 22-01.e", loss(1000, 0.90))
v.check("Txt 22-01.f", loss(1000, 0.91))
v.check("Txt 22-01.a", loss(1000, 0.90) - loss(1000, 0.91))
v.check("Txt 22-01.b", (1 - loss(1, 0.91) / loss(1, 0.90)) * 100)
v.check("Txt 22-01.g", loss(1000, 0.98))
v.check("Txt 22-01.h", loss(1000, 0.99))
v.check("Txt 22-01.c", loss(1000, 0.98) - loss(1000, 0.99))
v.check("Txt 22-01.d", (1 - loss(1, 0.99) / loss(1, 0.98)) * 100)
v.check("Txt 22-01.i", 1 / loss(1, 0.95))
v.check("Txt 22-01.j", 1 / loss(1, 0.99))
v.check("Txt 22-01.k", chain_forward(100, [0.97] * 4)[1])
v.check("Txt 22-01.l", chain_forward(100, [0.99, 0.98])[1])

# ---------------------------------------------------------------- problems
print("Problems")
for key, e in zip("abcd", (0.80, 0.85, 0.97, 0.98)):
    v.check(f"22-01.1{key}", loss(2000, e))
v.check("22-01.1e", loss(2000, 0.80) - loss(2000, 0.85))
v.check("22-01.1f", loss(2000, 0.97) - loss(2000, 0.98))
v.check("22-01.1g", (1 - loss(1, 0.85) / loss(1, 0.80)) * 100)
v.check("22-01.1h", (1 - loss(1, 0.98) / loss(1, 0.97)) * 100)

C2 = [0.98, 0.95, 0.92]
pin2 = chain_input(50, C2)
ls2, _ = chain_forward(pin2, C2)
v.check("22-01.2a", 50 / pin2 * 100)
v.check("22-01.2b", pin2)
v.check("22-01.2c", ls2[2])
v.check("22-01.2d", ls2[1])
v.check("22-01.2e", ls2[0])
v.check("22-01.2f", ls2[2] / sum(ls2) * 100)

pin3 = 5.0 * (0.2 + 50e-6)
v.check("22-01.3a", 3.3 * 0.2 / pin3 * 100)
v.check("22-01.3b", pin3 - 0.66)
v.check("22-01.3c", 25 + 50 * (pin3 - 0.66))
v.check("22-01.3d", 3.3 + 0.27)

ib4 = 1.2 * 2e-3 / (0.85 * 3.8)
v.check("22-01.4a", 2.0)
v.check("22-01.4b", ib4 * 1e3)
v.check("22-01.4c", 2e-3 / ib4)
v.check("22-01.4d", 1.2 * 2e-3 / (3.8 * 2e-3) * 100)

for key, iq in (("a", 25e-9), ("b", 5e-6)):
    v.check(f"22-01.5{key}", optimize.brentq(lambda i, iq=iq: i / (i + iq) - 0.99, 1e-12, 1.0, xtol=1e-15) * 1e6)
v.check("22-01.5c", 3e-6 / (3e-6 + 25e-9) * 100)
v.check("22-01.5d", 3e-6 / (3e-6 + 5e-6) * 100)

for key, n in (("a", 1), ("b", 3), ("c", 10)):
    e = sum(rc_charge_loss(100e-9, 1.0, 0, 3.3 * k / n, 3.3 * (k - 1) / n) for k in range(1, n + 1))
    v.check(f"22-01.6{key}", e * 1e9)
# gate drive: charge through 2 ohm, discharge through 5 ohm, energy per cycle from the ODEs
eg = rc_charge_loss(2e-9, 2.0, 0, 5.0, 0.0) + rc_charge_loss(2e-9, 5.0, 0, 0.0, 5.0)
v.check("22-01.6d", eg * 1e6 * 1e3)

# switched-capacitor resistor: simulate a capacitor toggling between 1.85 V and 1.75 V sources
c7, f7 = 1e-6, 1e6
dv7 = 0.1 / (f7 * c7)
q7 = c7 * dv7
v.check("22-01.7a", dv7 / (q7 * f7))
v.check("22-01.7b", dv7)
e7 = rc_charge_loss(c7, 0.01, 0, 1.85, 1.75) + rc_charge_loss(c7, 0.01, 0, 1.75, 1.85)
v.check("22-01.7c", e7 * f7 * 1e3)
v.check("22-01.7d", 0.1 / (f7 * 0.018) * 1e6)

v.check("22-01.8a", 0.4 * 5)
v.check("22-01.8b", fft_harmonic(5.0, 0.4, 1))
v.check("22-01.8c", fft_harmonic(5.0, 0.4, 2))
v.check("22-01.8d", 2 * fft_harmonic(5.0, 0.4, 1) / abs(1 - 20 ** 2) * 1e3)
v.check("22-01.8e", fft_harmonic(5.0, 0.4, 2) / abs(1 - 40 ** 2) * 1e3)

for key_l, key_e, (p0, a, r) in (("a", "b", (0.08, 0.02, 0.01)), ("c", "d", (0.16, 0.04, 0.01))):
    lo = p0 + a * 3 + r * 9
    v.check(f"22-01.9{key_l}", lo)
    v.check(f"22-01.9{key_e}", 5.4 / (5.4 + lo) * 100)
v.check("22-01.9e", (0.16 + 0.12 + 0.09) / (0.08 + 0.06 + 0.09))
v.check("22-01.9f", 5.4 / (5.4 + 0.16 + 0.12 + 0.007 * 9) * 100)

# fit by least squares over the three points (exact here), then find the peak numerically
Ix = np.array([1.0, 5.0, 20.0])
Lx = np.array([1.227, 5.375, 21.5]) - Ix
coef = np.polyfit(Ix, Lx, 2)       # R, a, P0
r10, a10, p10 = coef
v.check("22-01.10a", r10 * 1e3)
v.check("22-01.10b", a10 * 1e3)
v.check("22-01.10c", p10 * 1e3)
ip10 = peak_current(p10, a10, r10)
v.check("22-01.10d", ip10)
v.check("22-01.10e", ip10 / (ip10 + np.polyval(coef, ip10)) * 100)
v.check("22-01.10f", 1 / 1.227 * 100)
v.check("22-01.10g", 5 / 5.375 * 100)
v.assert_true("5 A and 20 A efficiencies are equal (5 x 20 = I*^2)", abs(5 / 5.375 - 20 / 21.5) < 1e-12)

for key, n in (("a", 1), ("b", 2), ("c", 3)):
    v.check(f"22-01.11{key}", shed_point(n, 0.25, 0.001))
for key, n, i in (("d", 2, 30.0), ("e", 4, 30.0), ("f", 4, 80.0)):
    lo = n * 0.25 + 0.001 * i * i / n
    v.check(f"22-01.11{key}", 0.8 * i / (0.8 * i + lo) * 100)

vol12 = 50 * 40 * 25 / IN3_MM3
area12 = 2 * (50 * 40 + 50 * 25 + 40 * 25) * 1e-6
v.check("22-01.12a", 65 / vol12)
v.check("22-01.12b", 10 * area12 * 40)
v.check("22-01.12c", optimize.brentq(lambda e: loss(65, e) - 10 * area12 * 40, 0.5, 0.9999) * 100)
v.check("22-01.12d", loss(65, 0.93))
v.check("22-01.12e", loss(65, 0.93) / (10 * area12))

pb13 = 3000 / 0.97
v.check("22-01.13a", pb13)
c13a = holdup_c(pb13, 0.010, 390, 300)
c13b = holdup_c(pb13, 0.010, 390, 330)
v.check("22-01.13b", c13a * 1e3)
v.check("22-01.13c", c13b * 1e3)
v.check("22-01.13d", c13b / c13a)
v.check("22-01.13e", holdup_c(pb13, 0.020, 390, 300) * 1e3)

C14 = [0.94, 0.96, 0.88]
pin14 = chain_input(1000, C14)
v.check("22-01.14a", 1000 / pin14 * 100)
v.check("22-01.14b", pin14)
v.check("22-01.14c", pin14 - 1000)
s_vrm = pin14 - chain_input(1000, [0.94, 0.96, 0.90])
s_psu = pin14 - chain_input(1000, [0.96, 0.96, 0.88])
v.check("22-01.14d", s_vrm)
v.check("22-01.14e", s_psu)
v.check("22-01.14f", s_vrm / 2)
v.check("22-01.14g", s_psu / 2)

l15 = loss(3000, 0.99)
v.check("22-01.15a", l15)
v.check("22-01.15b", 3000 / 150)
v.check("22-01.15c", l15 / 20)
e15 = chain_forward(1, [0.99, 0.98])[1]
v.check("22-01.15d", e15 * 100)
v.check("22-01.15e", loss(3000, e15))
v.check("22-01.15f", loss(3000, e15) / 20)
v.check("22-01.15g", loss(3000, e15) / l15)
v.check("22-01.15h", optimize.brentq(lambda e: loss(150, e) - 3.0, 0.5, 0.99999) * 100)

# ---------------------------------------------------------------- lab
print("Lab")
sys.path.insert(0, str(LAB))
import power as pw  # noqa: E402

t, il, vo = pw.buck_pss(VIN, D, FS, LL, CC, RL)
v.assert_true("lab PSS ripple equals brute-force ripple", abs((vo.max() - vo.min()) - vpp) < 1e-5)
v.check("Lab 22-01.a", (il.max() - il.min()))
v.check("Lab 22-01.b", (VIN - 3.3) * D / FS / LL)
v.check("Lab 22-01.c", ip)

sys.exit(v.finish())
