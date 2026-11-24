#!/usr/bin/env python3
"""Verify every number in chapter 20-05 (comparators and sample-and-hold circuits), its problems and its lab.

Independent routes:
- kT/C by numerically integrating 4kTR/(1 + (2 pi f R C)^2) for several R (scipy quad), not from the closed form;
- switch widths by root-finding R_on(W) on a separately written threshold/overdrive model;
- the distortion estimate's alpha and beta from analytic derivatives of R_on(v) (the lab uses finite differences);
- tracking distortion re-simulated in phase time (theta = omega t) with Radau and harmonics taken by numerical
  quadrature of the Fourier integrals over the last period (the lab uses DOP853 and an FFT);
- the jitter law checked by a seeded Monte Carlo of jittered sampling, and the StrongARM integration-noise law by a
  seeded Monte Carlo of integrated white noise;
- the metastability probability by explicit summation over decisions, compared with the closed form;
- the current-limited latch as the full two-node system with Radau (the lab uses the symmetric one-node reduction);
- ngspice confirms kT/C, the switch distortion and the latch (run_spice); the lab module (sh.py) is asserted to agree.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "20-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import sh as lab  # noqa: E402

v = Verifier.from_files("20-05", ROOT / "chapters" / "20-05-comparators-and-sample-and-hold.md",
                        ROOT / "solutions" / "20-05-solutions.md", LAB / "README.md")

KT = 1.380649e-23 * 300.0
MUN, MUP, COX, VT0, GB, PHI, L, VDD = 350e-4, 100e-4, 8.6e-3, 0.45, 0.4, 0.8, 0.13e-6, 1.2
N, VFS = 12, 1.6
LSB = VFS / 2 ** N
A_FS = VFS / 2
SIG = A_FS ** 2 / 2


def ktc_numeric(r, c):
    fc = 1 / (2 * math.pi * r * c)
    val, _ = quad(lambda x: 4 * KT * r / (1 + x * x) * fc, 0, np.inf, limit=200)
    return val


def vth_n(vsb):
    return VT0 + GB * (math.sqrt(PHI + vsb) - math.sqrt(PHI))


def vth_p(v_node):
    return VT0 + GB * (math.sqrt(PHI + (VDD - v_node)) - math.sqrt(PHI))


def g_switch(w, vov, mu=MUN):
    return mu * COX * (w / L) * vov if vov > 0 else 0.0


def db(x):
    return 20 * math.log10(x)


# ------------------------------------------------------------------ Example 20-05.1
print("Example 20-05.1")
C = 24 * KT / LSB ** 2
v.check("Ex 20-05.1a", LSB * 1e6)
v.check("Ex 20-05.1b", LSB / math.sqrt(12) * 1e6)
v.check("Ex 20-05.1c", C * 1e12)
v.check("Ex 20-05.1d", math.sqrt(ktc_numeric(852.0, C)) * 1e6)
v.check("Ex 20-05.1e", math.sqrt(2 * ktc_numeric(100.0, C)) * 1e6)
for r in (10.0, 1e3, 1e5):
    v.assert_true(f"kT/C independent of R = {r:g}", abs(ktc_numeric(r, C) / (KT / C) - 1) < 1e-8)
snr = lambda c, extra=0.0: 10 * math.log10(SIG / (LSB ** 2 / 12 + 2 * KT / c + extra))  # noqa: E731
v.check("Ex 20-05.1f", 10 * math.log10(SIG / (LSB ** 2 / 12)))
v.check("Ex 20-05.1g", snr(C))
v.check("Ex 20-05.1h", (snr(C) - 1.76) / 6.02)
v.check("Ex 20-05.1i", snr(2 * C))
v.check("Ex 20-05.1j", snr(4 * C))
v.check("Txt 20-05.a", math.sqrt(ktc_numeric(1e3, 1e-12)) * 1e6)
v.check("Txt 20-05.d", 24 * KT / (VFS / 2 ** 14) ** 2 * 1e12)

# ------------------------------------------------------------------ Example 20-05.2
print("Example 20-05.2")
TAU = 5e-9 / ((N + 1) * math.log(2))
RMAX = TAU / C
v.check("Ex 20-05.2a", TAU * 1e9)
v.check("Ex 20-05.2b", RMAX)
v.check("Txt 20-05.b", (N + 1) * math.log(2))
for key, vin in (("2c", 0.2), ("2d", 0.6), ("2e", 1.0)):
    v.check(f"Ex 20-05.{key}", vth_n(vin))
v.check("Ex 20-05.2f", VDD - vth_n(1.0))
W = brentq(lambda w: 1 / g_switch(w, VDD - vth_n(1.0)) - RMAX, 1e-8, 1e-4, xtol=1e-18)
v.check("Ex 20-05.2g", W / L)
v.check("Ex 20-05.2h", W * 1e6)
r_boot = lambda vin: 1 / g_switch(W, VDD - vth_n(vin))  # noqa: E731
r_plain = lambda vin: 1 / g_switch(W, VDD - vin - vth_n(vin))  # noqa: E731
v.check("Ex 20-05.2i", r_boot(0.2))
v.check("Ex 20-05.2j", r_boot(0.6))
v.check("Ex 20-05.2k", r_plain(0.2))
v.check("Ex 20-05.2l", r_plain(0.6) / 1e3)
v.check("Ex 20-05.2m", VDD - 1.0 - vth_n(1.0))
v.check("Ex 20-05.2n", brentq(lambda x: r_plain(x) - RMAX, 0.0, 0.5, xtol=1e-14))
v.check("Ex 20-05.2o", 1 / (2 * math.pi * TAU) / 1e6)
v_cut = brentq(lambda x: VDD - x - vth_n(x), 0.0, 1.2, xtol=1e-14)
v.check("Txt 20-05.c", v_cut)

# ------------------------------------------------------------------ Example 20-05.3
print("Example 20-05.3")
WLC = W * L * COX
v.check("Ex 20-05.3a", WLC * 1e15)
inj = {}
for (kq, kv, kl), vin in ((("3b", "3e", "3h"), 0.2), (("3c", "3f", "3i"), 0.6), (("3d", "3g", "3j"), 1.0)):
    q = WLC * (VDD - vth_n(vin))
    inj[vin] = q / (2 * C)
    v.check(f"Ex 20-05.{kq}", q * 1e15)
    v.check(f"Ex 20-05.{kv}", inj[vin] * 1e3)
    v.check(f"Ex 20-05.{kl}", inj[vin] / LSB)
COV = 0.3e-15 / 1e-6 * W
v.check("Ex 20-05.3k", COV * 1e15)
v.check("Ex 20-05.3l", (0.2 + VDD) * COV / (COV + C) * 1e3)
v.check("Ex 20-05.3m", (1.0 + VDD) * COV / (COV + C) * 1e3)
v.check("Ex 20-05.3n", (inj[0.2] - inj[1.0]) * 1e3)
v.check("Ex 20-05.3o", (inj[0.2] - inj[1.0]) / LSB)

# ------------------------------------------------------------------ Example 20-05.4
print("Example 20-05.4")
K = MUN * COX * W / L


def ron_v(x):
    return 1 / (K * (VDD - vth_n(x)))


g0 = VDD - vth_n(0.6)
d1 = GB / (2 * math.sqrt(PHI + 0.6))
d2 = -GB / (4 * (PHI + 0.6) ** 1.5)
ALPHA = d1 / g0
BETA = d2 / (2 * g0) + d1 ** 2 / g0 ** 2
R0 = ron_v(0.6)
v.check("Ex 20-05.4a", R0)
v.check("Ex 20-05.4b", ALPHA)
v.check("Ex 20-05.4c", BETA)
h = 1e-4
v.assert_true("analytic alpha matches a central difference",
              abs((ron_v(0.6 + h) - ron_v(0.6 - h)) / (2 * h * R0) / ALPHA - 1) < 1e-6)
for kw, ke2, ke3, f in (("4d", "4f", "4h", 10e6), ("4e", "4g", "4i", 49e6)):
    wrc = 2 * math.pi * f * R0 * C
    v.check(f"Ex 20-05.{kw}", wrc)
    v.check(f"Ex 20-05.{ke2}", db(wrc * ALPHA * 0.4 / 2))
    v.check(f"Ex 20-05.{ke3}", db(wrc * BETA * 0.4 ** 2 / 4))


def track_harmonics(f, amp, body, w=W, periods=10):
    """Simulate in phase time theta = omega t; harmonics by quadrature over the last period."""
    k = MUN * COX * w / L
    om = 2 * math.pi * f

    def dv(theta, y):
        vi = 0.6 + amp * math.sin(theta)
        vo = y[0]
        vm = 0.5 * (vi + vo)
        vt = vth_n(max(vm, -0.4)) if body else VT0
        i = k * max(vi + VDD - vt - vm, 0.0) * (vi - vo)
        return [i / C / om]
    sol = solve_ivp(dv, (0, 2 * math.pi * periods), [0.6], method="Radau", rtol=1e-12, atol=1e-15,
                    dense_output=True)
    t0 = 2 * math.pi * (periods - 1)
    hk = []
    for m in (1, 2, 3):
        a = quad(lambda th: (sol.sol(t0 + th)[0] - 0.6) * math.cos(m * th), 0, 2 * math.pi, limit=400, epsabs=1e-12)[0]
        b = quad(lambda th: (sol.sol(t0 + th)[0] - 0.6) * math.sin(m * th), 0, 2 * math.pi, limit=400, epsabs=1e-12)[0]
        hk.append(math.hypot(a, b) / math.pi)
    return db(hk[1] / hk[0]), db(hk[2] / hk[0])


H = {}
for body in (True, False):
    for f in (10e6, 49e6):
        H[(body, f)] = track_harmonics(f, 0.4, body)
v.check("Ex 20-05.4j", H[(True, 10e6)][0])
v.check("Ex 20-05.4k", H[(True, 10e6)][1])
v.check("Ex 20-05.4l", H[(True, 49e6)][0])
v.check("Ex 20-05.4m", H[(True, 49e6)][1])
v.check("Ex 20-05.4n", H[(False, 10e6)][0])
v.check("Ex 20-05.4o", H[(False, 10e6)][1])
v.check("Ex 20-05.4p", H[(False, 49e6)][0])
v.check("Ex 20-05.4q", H[(False, 49e6)][1])
v.check("Ex 20-05.4r", H[(True, 10e6)][1] - db(2 * math.pi * 10e6 * R0 * C * BETA * 0.4 ** 2 / 4))
v.check("Ex 20-05.4s", H[(True, 49e6)][1] - db(2 * math.pi * 49e6 * R0 * C * BETA * 0.4 ** 2 / 4))
v.check("Ex 20-05.4t", H[(True, 49e6)][1] - H[(False, 49e6)][1])

# ------------------------------------------------------------------ Example 20-05.5
print("Example 20-05.5")
jit = lambda f, s: -db(2 * math.pi * f * s)  # noqa: E731
v.check("Ex 20-05.5a", jit(49e6, 1e-12))
jn = SIG * (2 * math.pi * 49e6 * 1e-12) ** 2
v.check("Ex 20-05.5b", snr(C, jn))
v.check("Ex 20-05.5c", 10 ** (-80 / 20) / (2 * math.pi * 50e6) * 1e12)
v.check("Ex 20-05.5d", jit(1e9, 100e-15))
v.check("Ex 20-05.5e", snr(C) - snr(C, jn))
v.check("Ex 20-05.5f", (jit(1e9, 100e-15) - 1.76) / 6.02)
rng = np.random.default_rng(2005)
tt = rng.uniform(0, 1 / 49e6, 400000)
err = A_FS * (np.sin(2 * math.pi * 49e6 * (tt + rng.normal(0, 1e-12, tt.size))) - np.sin(2 * math.pi * 49e6 * tt))
v.assert_true("Monte Carlo jitter SNR matches the formula", abs(10 * math.log10(SIG / np.mean(err ** 2)) -
                                                                  jit(49e6, 1e-12)) < 0.05)

# ------------------------------------------------------------------ Example 20-05.6
print("Example 20-05.6")
GAM = 2 / 3
AINT = 15 * 0.45
v.check("Ex 20-05.6a", AINT)
sig20 = math.sqrt(4 * GAM * KT / (AINT * 20e-15))
v.check("Ex 20-05.6b", sig20 * 1e3)
v.check("Ex 20-05.6c", sig20 / LSB)
v.check("Ex 20-05.6d", LSB / 4 * 1e6)
CC = 4 * GAM * KT / (AINT * (LSB / 4) ** 2)
v.check("Ex 20-05.6e", CC * 1e15)
E = 2 * CC * VDD ** 2
v.check("Ex 20-05.6f", E * 1e12)
v.check("Ex 20-05.6g", 12 * E * 1e12)
v.check("Ex 20-05.6h", 12 * E * 100e6 * 1e3)
os_ = 3.5e-9 / math.sqrt(4e-6 * 0.13e-6)
v.check("Ex 20-05.6i", os_ * 1e3)
v.check("Ex 20-05.6j", os_ / LSB)
kick = 1.2 * 1.2e-15 / (1.2e-15 + C)
v.check("Ex 20-05.6k", kick * 1e3)
v.check("Ex 20-05.6l", kick / LSB)
# Monte Carlo of the integration noise: white current noise of one-sided density 4kT gamma g_m on each node
gm_mc, cn = 1e-3, 20e-15
tint = AINT * cn / gm_mc
nsteps, ntrial = 400, 20000
dt = tint / nsteps
s_i = 4 * KT * GAM * gm_mc
qn = rng.normal(0, math.sqrt(s_i / 2 / dt), (ntrial, 2, nsteps)).sum(axis=2) * dt
vdiff = (qn[:, 0] - qn[:, 1]) / cn
v.assert_true("Monte Carlo StrongARM integration noise matches 4 gamma kT/(A C)",
              abs(np.std(vdiff) / AINT / math.sqrt(4 * GAM * KT / (AINT * cn)) - 1) < 0.02)

# ------------------------------------------------------------------ Example 20-05.7
print("Example 20-05.7")
TAUL = 60e-15 / 3e-3
v.check("Ex 20-05.7a", TAUL * 1e12)
v0 = AINT * LSB / 2
v.check("Ex 20-05.7b", v0 * 1e3)
v.check("Ex 20-05.7c", TAUL * math.log(0.6 / v0) * 1e12)


def p_sar(t, tau=TAUL, a0=AINT, n=N, vfs=VFS):
    vmin = 0.6 / a0 * math.exp(-t / tau)
    return sum(2 * vmin / (vfs / 2 ** (k - 1)) for k in range(1, n + 1)), vmin


p300, vmin300 = p_sar(300e-12)
v.check("Ex 20-05.7d", vmin300 * 1e9)
v.check("Ex 20-05.7e", p300)
v.check("Ex 20-05.7f", p300 * 100e6)
v.assert_true("SAR sum matches the closed form", abs(p300 / (2 * vmin300 * (2 ** N - 1) / VFS) - 1) < 1e-12)
t9 = brentq(lambda t: math.log(p_sar(t)[0]) - math.log(1e-9), 100e-12, 2e-9, xtol=1e-18)
v.check("Ex 20-05.7g", t9 * 1e12)
v.check("Ex 20-05.7h", 1 / (1e-9 * 100e6))
v.check("Ex 20-05.7i", (t9 - 300e-12) / TAUL)
v.check("Ex 20-05.7j", 12 * t9 * 1e9)

# ------------------------------------------------------------------ lab


def latch_time(v0d, gm=3e-3, cap=60e-15, imax=0.3e-3, target=0.6):
    def rhs(t, y):
        x, yy = y
        return [imax * math.tanh(-gm * yy / imax) / cap, imax * math.tanh(-gm * x / imax) / cap]

    def ev(t, y):
        return (y[0] - y[1]) - target
    ev.terminal = True
    sol = solve_ivp(rhs, (0, 1e-9), [v0d / 2, -v0d / 2], method="Radau", events=ev, rtol=1e-11, atol=1e-16,
                    max_step=0.5e-12)
    return float(sol.t_events[0][0])


print("Lab 20-05")
tl = [latch_time(AINT * x) for x in (LSB / 2, 1e-3, 10e-3)]
v.check("Lab 20-05.a", tl[0] * 1e12)
v.check("Lab 20-05.b", tl[1] * 1e12)
v.check("Lab 20-05.c", tl[2] * 1e12)
est = [TAUL * math.log(0.6 / (AINT * x)) for x in (LSB / 2, 1e-3, 10e-3)]
v.check("Lab 20-05.d", est[1] * 1e12)
v.check("Lab 20-05.e", est[2] * 1e12)
v.check("Lab 20-05.f", np.mean(np.array(tl) - np.array(est)) * 1e12)
v.check("Lab 20-05.g", 0.3e-3 / 3e-3)
v.check("Lab 20-05.h", math.sqrt((LSB ** 2 / 12 + 2 * KT / C) / SIG) / (2 * math.pi * 1e-12) / 1e6)

# ------------------------------------------------------------------ problems
print("Problems")
for key, cap in (("1a", 100e-15), ("1b", 1e-12), ("1c", 10e-12)):
    v.check(f"20-05.{key}", math.sqrt(ktc_numeric(1e3, cap)) * 1e6)
lsb10 = 1.0 / 1024
c10 = 24 * KT / lsb10 ** 2
v.check("20-05.1d", lsb10 * 1e3)
v.check("20-05.1e", c10 * 1e15)
v.check("20-05.1f", 10 * math.log10(0.125 / (lsb10 ** 2 / 12)))
v.check("20-05.1g", 10 * math.log10(0.125 / (lsb10 ** 2 / 12 + 2 * KT / c10)))
for key, n in (("2a", 10), ("2b", 12), ("2c", 14), ("2d", 16)):
    v.check(f"20-05.{key}", 24 * KT / (VFS / 2 ** n) ** 2 * 1e12)
v.check("20-05.2e", (24 * KT / (VFS / 2 ** 13) ** 2) / (24 * KT / (VFS / 2 ** 12) ** 2))
tau3 = 2.5e-9 / (11 * math.log(2))
r3 = tau3 / c10
v.check("20-05.3a", tau3 * 1e9)
v.check("20-05.3b", r3 / 1e3)
v.check("20-05.3c", vth_n(0.85))
v.check("20-05.3d", VDD - vth_n(0.85))
w3 = brentq(lambda w: 1 / g_switch(w, VDD - vth_n(0.85)) - r3, 1e-9, 1e-4, xtol=1e-18)
v.check("20-05.3e", w3 / L)
v.check("20-05.3f", w3 * 1e6)
v.check("20-05.3g", 11 * math.log(2))
vgs4 = VDD * 0.3 / 0.33
v.check("20-05.4a", vgs4)
v.check("20-05.4b", 1 / g_switch(W, vgs4 - vth_n(1.0)))
v.check("20-05.4c", (VDD - vth_n(1.0)) / (vgs4 - vth_n(1.0)))
v.check("20-05.4d", vgs4 - vth_n(1.0))
v.check("20-05.5a", v_cut)
v.check("20-05.5b", brentq(lambda x: x - vth_p(x), 0.0, 1.2, xtol=1e-14))


def r_tg(x):
    return 1 / (g_switch(W, VDD - x - vth_n(x)) + g_switch(3 * W, x - vth_p(x), MUP))


v.check("20-05.5c", r_tg(0.2))
v.check("20-05.5d", r_tg(0.6) / 1e3)
v.check("20-05.5e", r_tg(1.0))
lc = L ** 2 / (2 * MUN)
v.check("20-05.6a", lc)
v.check("20-05.6b", lc / TAU * 1e3)
v.check("20-05.6c", (65e-9) ** 2 / (2 * MUN) / TAU * 1e3)
v.assert_true("Delta V_inj tau = L^2/(2 mu) at 1.0 V", abs(inj[1.0] * TAU / lc - 1) < 1e-9)
wrc25 = 2 * math.pi * 25e6 * R0 * C
v.check("20-05.7a", wrc25)
v.check("20-05.7b", db(wrc25 * ALPHA * 0.2 / 2))
v.check("20-05.7c", db(2 * math.pi * 49e6 * (R0 / 2) * C * ALPHA * 0.4 / 2))
for (ks, ke), f in ((("8a", "8b"), 10e6), (("8c", "8d"), 100e6), (("8e", "8f"), 1e9)):
    s = jit(f, 0.5e-12)
    v.check(f"20-05.{ks}", s)
    v.check(f"20-05.{ke}", (s - 1.76) / 6.02)
v.check("20-05.8g", 20 / 6.02)
terms = [LSB ** 2 / 12, 2 * KT / C, SIG * (2 * math.pi * 49e6 * 0.5e-12) ** 2, (LSB / 4) ** 2]
tot = sum(terms)
v.check("20-05.9a", math.sqrt(terms[2]) * 1e6)
v.check("20-05.9b", math.sqrt(tot) * 1e6)
v.check("20-05.9c", 10 * math.log10(SIG / tot))
v.check("20-05.9d", (10 * math.log10(SIG / tot) - 1.76) / 6.02)
v.check("20-05.9e", max(10 * math.log10(tot / (tot - t)) for t in terms))
a10 = 20 * 0.45
c10b = 4 * GAM * KT / (a10 * (50e-6) ** 2)
v.check("20-05.10a", a10)
v.check("20-05.10b", c10b * 1e15)
v.check("20-05.10c", 2 * c10b * VDD ** 2 * 1e12)
v.check("20-05.10d", 2 * c10b * VDD ** 2 * (50e-6) ** 2)
v.assert_true("E sigma^2 identity", abs(2 * c10b * VDD ** 2 * (50e-6) ** 2 / (8 * GAM * KT * VDD ** 2 / a10) - 1)
              < 1e-12)
c15 = 4 * GAM * KT / (AINT * (50e-6) ** 2)
v.check("20-05.10e", c15 * 1e15)
v.check("20-05.10f", c15 / c10b)
l6 = 1.0 / 64
phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))  # noqa: E731
v.check("20-05.11a", l6 * 1e3)
v.check("20-05.11b", l6 / 4 * 1e3)
v.check("20-05.11c", (3.5e-9 / (l6 / 4)) ** 2 * 1e12)
p2 = phi(2) - phi(-2)
v.check("20-05.11d", p2)
v.check("20-05.11e", p2 ** 63)
v.check("20-05.11f", (3.5e-9 / (l6 / 8)) ** 2 * 1e12)
v.check("20-05.11g", (phi(4) - phi(-4)) ** 63)
tau12 = 40e-15 / 2e-3
v.check("20-05.12a", tau12 * 1e12)
v.check("20-05.12b", tau12 * math.log(0.6 / 5e-3) * 1e12)
v.check("20-05.12c", tau12 * math.log(0.6 / 50e-6) * 1e12)
vm12 = 0.6 / 5 * math.exp(-200e-12 / tau12)
v.check("20-05.12d", vm12 * 1e6)
v.check("20-05.12e", 2 * vm12 / l6)
v.check("20-05.12f", 2 * vm12 / l6 * 1e9)
t13 = 7.5e-9 / 12 - 300e-12
ratio13 = brentq(lambda x: p_sar(x * 1e-12, tau=1e-12)[0] - 1e-9, 1, 100)
v.check("20-05.13a", t13 * 1e12)
v.check("20-05.13b", ratio13)
v.check("20-05.13c", t13 / ratio13 * 1e12)
v.check("20-05.13d", 60e-15 / (t13 / ratio13) * 1e3)
v.check("20-05.13e", TAUL / (t13 / ratio13))
for (ka, kt_, ks), cgd in ((("14a", "14b", "14c"), 2e-15), (("14d", "14e", "14f"), 0.2e-15)):
    k14 = 1.2 * cgd / (cgd + 50e-15)
    t14 = 500 * (cgd + 50e-15)
    v.check(f"20-05.{ka}", k14 * 1e3)
    v.check(f"20-05.{kt_}", t14 * 1e12)
    v.check(f"20-05.{ks}", t14 * math.log(k14 / (0.1 * l6)) * 1e12)
h04 = track_harmonics(49e6, 0.4, True)
h02 = track_harmonics(49e6, 0.2, True)
v.check("20-05.15a", h04[0])
v.check("20-05.15b", h04[1])
v.check("20-05.15c", h02[0])
v.check("20-05.15d", h02[1])
v.check("20-05.15e", h04[0] - h02[0])
v.check("20-05.15f", h04[1] - h02[1])

# ------------------------------------------------------------------ practitioner-lens arithmetic
print("Text")
v.check("Txt 20-05.e", 2 * GAM * AINT)
v.check("Txt 20-05.f", jit(7.997e9, 60e-15))
v.check("Txt 20-05.g", jit(7.997e9, 50e-15))
v.check("Txt 20-05.h", E * (LSB / 4) ** 2 / 1e-21)
v.check("Txt 20-05.i", 0.69 * 23)
v.check("Txt 20-05.j", jit(3.5e9, 90e-15))
v.check("Txt 20-05.k", 44 / math.log(10))
v.check("Txt 20-05.l", (jit(7.997e9, 60e-15) - 1.76) / 6.02)
v.check("Txt 20-05.m", 1e18 / 10.4e9 / (365.25 * 86400))
v.check("Txt 20-05.n", 1e15 / 3e9 / 86400)
v.check("Txt 20-05.o", TAUL * math.log(10) * 1e12)
v.assert_true("precharge kT/C referred to the input is 2 gamma A_int below the input pair's term",
              abs((4 * GAM * KT / (AINT * CC)) / (2 * KT / (CC * AINT ** 2)) - 2 * GAM * AINT) < 1e-12)

# ------------------------------------------------------------------ agreement with the lab module
print("Lab module agreement")
v.assert_true("sh.py capacitor matches", abs(lab.ktc_cap(12, 1.6) / C - 1) < 1e-12)
v.assert_true("sh.py on-resistance matches", abs(lab.ron(W, 1.0 + VDD, 1.0) / RMAX - 1) < 1e-9)
tr = lab.track(W, C, 49e6, 0.4, mode="boot")
v.assert_true("sh.py tracking HD3 matches", abs(tr["hd3_db"] - H[(True, 49e6)][1]) < 0.01,
              f"{tr['hd3_db']} vs {H[(True, 49e6)][1]}")
v.assert_true("sh.py latch matches", abs(lab.regen(AINT * LSB / 2, 3e-3, 60e-15, 0.3e-3, 0.6) / tl[0] - 1) < 1e-5)
v.assert_true("sh.py SAR probability matches",
              abs(lab.sar_meta_probability(300e-12, AINT, TAUL, 12, 1.6) / p300 - 1) < 1e-12)

sys.exit(v.finish())
