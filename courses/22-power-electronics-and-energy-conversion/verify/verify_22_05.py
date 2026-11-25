#!/usr/bin/env python3
"""Verify every number in chapter 22-05 (magnetics design), its problems and its lab.

Independent routes (the lab module magnetics.py uses closed forms):
- inductance comes from the effective-permeability form µ0 µ_e N² A_e/ℓ_e and from field energy ∫B²/(2µ) dV;
- gaps come from root finding on L(g) or on the vendor's A_L fit, not from the inverted formula;
- RMS currents come from numerical integration of the waveforms;
- the iGSE constant comes from quadrature, and triangle-wave loss from averaging |dB/dt|^α over a sampled
  waveform; the transformer optimum from numerical minimization;
- eddy loss comes from integrating E²/ρ over the lamination (or rod) and the period;
- Dowell's factor comes from a finite-difference solution of the diffusion equation in each layer;
- skin depth from the real part of the diffusion propagation constant √(jωµ0/ρ);
- leakage inductance from integrating µ0 H²/2 over the stacked winding sections;
- the lab's saturation currents from root finding on the B–H curve.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize, sparse
from scipy.sparse.linalg import spsolve

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "22-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

v = Verifier.from_files("22-05", ROOT / "chapters" / "22-05-magnetics-design.md",
                        ROOT / "solutions" / "22-05-solutions.md", LAB / "README.md")

MU0 = 4e-7 * math.pi
RHO20, ALPHA = 1 / 58e6, 0.00393                         # IEC annealed copper: 1/58 Ω·mm²/m, 0.393 %/K
AE, LE, VE, AN, MLT, AL0, DPOLE = 97.1e-6, 78.6e-3, 7630e-9, 122e-6, 60.5e-3, 2600e-9, 11.1e-3
A87, B87 = 1.635, 2.253                                  # N87 sine-fit Steinmetz exponents (NETL)
ANCHOR_W = 4.00                                          # W per ETD34 N87 set, max, 200 mT, 100 kHz, 100 °C
RHO100 = RHO20 * (1 + ALPHA * 80)


# ---------------------------------------------------------------- independent helpers
def mu_eff(mur, le, g):
    return mur / (1 + mur * g / le)


def ind_mu_eff(n, mue, ae=AE, le=LE):
    return MU0 * mue * n * n * ae / le


MUE0 = AL0 * LE / (MU0 * AE)                              # ungapped set's effective permeability


def l_of_gap(n, g):
    return ind_mu_eff(n, mu_eff(MUE0, LE, g))


def field_energy(b, g, ae=AE, le=LE, mur=MUE0):
    """∫B²/(2µ) dV over the core path and the gap (uniform B)."""
    return b * b / (2 * MU0 * mur) * ae * le + b * b / (2 * MU0) * ae * g


def rms_numeric(f, t0, t1, n=200001):
    t = np.linspace(t0, t1, n)
    return math.sqrt(integrate.simpson(f(t) ** 2, x=t) / (t1 - t0))


def cos_power_integral(a):
    return integrate.quad(lambda th: abs(math.cos(th)) ** a, 0, 2 * math.pi, limit=400, points=[math.pi / 2, 3 * math.pi / 2])[0]


def ki_over_k(a=A87, b=B87):
    return 1 / ((2 * math.pi) ** (a - 1) * cos_power_integral(a) * 2 ** (b - a))


def igse_wave(wave, f, a=A87, b=B87, n=400000):
    """Mean of (k_i/k) |dB/dt|^α ΔB^(β−α) over one period of a sampled waveform (k = 1)."""
    t = (np.arange(n) + 0.5) / (n * f)
    bw = wave(t)
    db = np.diff(np.concatenate([bw, bw[:1]])) * n * f
    dB = bw.max() - bw.min()
    return ki_over_k(a, b) * np.mean(np.abs(db) ** a) * dB ** (b - a)


def tri(delta_b, d, f):
    def w(t):
        x = (t * f) % 1.0
        return np.where(x < d, x / d, (1 - x) / (1 - d)) * delta_b
    return w


def sine(bpk, f):
    return lambda t: bpk * np.sin(2 * np.pi * f * t)


def eddy_slab_numeric(f, bpk, thick, rho, nx=1201, nt=1201):
    x = np.linspace(-thick / 2, thick / 2, nx)
    t = np.linspace(0, 1 / f, nt)
    dbdt = 2 * np.pi * f * bpk * np.cos(2 * np.pi * f * t)
    px = integrate.simpson(x * x, x=x) / thick / rho
    return integrate.simpson(px * dbdt ** 2, x=t) * f


def eddy_rod_numeric(f, bpk, d, rho, nr=1201, nt=1201):
    r = np.linspace(0, d / 2, nr)
    t = np.linspace(0, 1 / f, nt)
    dbdt = 2 * np.pi * f * bpk * np.cos(2 * np.pi * f * t)
    pr = integrate.simpson((r / 2) ** 2 * 2 * np.pi * r, x=r) / (np.pi * (d / 2) ** 2) / rho
    return integrate.simpson(pr * dbdt ** 2, x=t) * f


def delta_numeric(f, rho):
    gamma = np.sqrt(1j * 2 * np.pi * f * MU0 / rho)
    return 1 / gamma.real


def layer_loss_fd(delta_ratio, h_in, h_out, n=3000):
    k2 = 2j * delta_ratio ** 2
    x = np.linspace(0, 1, n + 1)
    dx = x[1] - x[0]
    main = np.full(n - 1, -2.0 / dx ** 2 - k2, dtype=complex)
    off = np.full(n - 2, 1.0 / dx ** 2, dtype=complex)
    A = sparse.diags([off, main, off], [-1, 0, 1], format="csc")
    rhs = np.zeros(n - 1, dtype=complex)
    rhs[0] -= h_in / dx ** 2
    rhs[-1] -= h_out / dx ** 2
    H = np.concatenate([[h_in], spsolve(A, rhs), [h_out]])
    J = np.gradient(H, dx, edge_order=2)
    return integrate.simpson(np.abs(J) ** 2, x=x)


def dowell_fd(delta_ratio, layers, n=3000):
    return sum(layer_loss_fd(delta_ratio, m - 1, m, n) for m in range(1, layers + 1)) / layers


def leakage_numeric(mlt, bw, sections, npts=4001):
    """sections: (thickness, ampere-turns per ampere); returns 2W/I² with W = µ0/2 ∫H² dV."""
    energy, h0 = 0.0, 0.0
    for thick, at in sections:
        x = np.linspace(0, thick, npts)
        H = h0 + at / bw * x / thick
        energy += MU0 / 2 * integrate.simpson(H ** 2, x=x) * bw * mlt
        h0 = H[-1]
    return 2 * energy


def al_fit(s_mm):
    return 153 * s_mm ** -0.713                           # nH, TDK ETD34 N27/N87 fit, 0.1–2.5 mm


def gap_from_fit(al_nh):
    return optimize.brentq(lambda s: al_fit(s) - al_nh, 0.1, 2.5, xtol=1e-12)


def gap_from_model(l_target, n):
    return optimize.brentq(lambda g: l_of_gap(n, g) - l_target, 1e-7, 5e-3, xtol=1e-15)


# ---------------------------------------------------------------- Example 22-05.1
print("Example 22-05.1")
g1 = 0.5e-3
rc = LE / (MUE0 * MU0 * AE)
rg = g1 / (MU0 * AE)
v.check("Ex 22-05.1a", rc / 1e5)
v.check("Ex 22-05.1b", rg / 1e6)
al_ideal = l_of_gap(1, g1)
v.check("Ex 22-05.1c", al_ideal * 1e9)
v.check("Ex 22-05.1d", rg / (rc + rg) * 100)
ag = math.pi * (DPOLE + g1) ** 2 / 4 * AE / (math.pi * DPOLE ** 2 / 4)
v.check("Ex 22-05.1e", ag * 1e6)
al_fr = 1 / (rc + g1 / (MU0 * ag))
v.check("Ex 22-05.1f", al_fr * 1e9)
v.check("Ex 22-05.1g", (al_ideal / 251e-9 - 1) * 100)
v.check("Ex 22-05.1h", (al_fr / 251e-9 - 1) * 100)
v.check("Ex 22-05.1i", 251e-9 * 20 ** 2 * 1e6)
v.check("Ex 22-05.1j", 251e-9 / (MU0 * AE / LE))
v.check("Ex 22-05.1k", (ag / AE - 1) * 100)
v.assert_true("ungapped µ_e reproduces the data sheet's 1670 to within 0.3%", abs(MUE0 / 1670 - 1) < 3e-3)

# ---------------------------------------------------------------- Example 22-05.2
print("Example 22-05.2")
L2, N2 = 251e-9 * 400, 20
bpa = L2 / (N2 * AE)
v.check("Ex 22-05.2a", bpa)
v.check("Ex 22-05.2b", optimize.brentq(lambda i: L2 * i / (N2 * AE) - 0.39, 0, 100))
i300 = optimize.brentq(lambda i: L2 * i / (N2 * AE) - 0.3, 0, 100)
v.check("Ex 22-05.2c", i300)
w_gap = 0.5 * L2 * i300 ** 2
v.check("Ex 22-05.2d", w_gap * 1e3)
L0 = AL0 * 400
v.check("Ex 22-05.2e", L0 * 1e3)
i0 = 0.3 * N2 * AE / L0
v.check("Ex 22-05.2f", i0)
w0 = 0.5 * L0 * i0 ** 2
v.check("Ex 22-05.2g", w0 * 1e3)
v.check("Ex 22-05.2h", w_gap / w0)
v.assert_true("ungapped energy equals ∫B²/2µ over the core (residual gap folded into µ_e)",
              abs(field_energy(0.3, 0.0) - w0) < 1e-12 * max(1, w0) + 1e-15)

# ---------------------------------------------------------------- Example 22-05.3
print("Example 22-05.3")
LM, IPK, D3, NP, NS, F3 = 223e-6, 2.52, 0.561, 32, 5, 100e3
v.check("Ex 22-05.3a", LM / NP ** 2 * 1e9)
b3 = LM * IPK / (NP * AE)
v.check("Ex 22-05.3b", b3)
v.check("Ex 22-05.3c", gap_from_fit(LM / NP ** 2 * 1e9))
g3 = gap_from_model(LM, NP)
v.check("Ex 22-05.3d", g3 * 1e3)
w3 = field_energy(b3, g3)
v.check("Ex 22-05.3e", w3 * 1e3)
v.assert_true("field energy equals ½LI² for the modelled gap", abs(w3 - 0.5 * LM * IPK ** 2) < 1e-9)
T3 = 1 / F3
ip = rms_numeric(lambda t: np.where(t < D3 * T3, IPK * t / (D3 * T3), 0.0), 0, T3)
v.check("Ex 22-05.3f", ip)
isp = 6.4 * IPK
v.check("Ex 22-05.3g", isp)
isr = rms_numeric(lambda t: np.where(t >= D3 * T3, isp * (T3 - t) / ((1 - D3) * T3), 0.0), 0, T3)
v.check("Ex 22-05.3h", isr)
cu = (NP * ip + NS * isr) / 4.2e6
v.check("Ex 22-05.3i", cu * 1e6)
v.check("Ex 22-05.3j", cu / AN)

# ---------------------------------------------------------------- Example 22-05.4
print("Example 22-05.4")
pv_anchor = ANCHOR_W / VE
v.check("Ex 22-05.4a", pv_anchor / 1e3)
v.check("Ex 22-05.4h", cos_power_integral(A87))
v.check("Ex 22-05.4b", ki_over_k())
v.check("Ex 22-05.4c", D3 ** (1 - A87) + (1 - D3) ** (1 - A87))
sine_ref = igse_wave(sine(0.2, F3), F3)                   # iGSE on the anchor's own sine reproduces k f^α B^β
v.assert_true("iGSE on a sinusoid reproduces Steinmetz", abs(sine_ref / (F3 ** A87 * 0.2 ** B87) - 1) < 1e-6)
ratio4 = igse_wave(tri(b3, D3, F3), F3) / sine_ref
v.check("Ex 22-05.4d", ratio4)
v.check("Ex 22-05.4e", ratio4 * ANCHOR_W)
v.check("Ex 22-05.4f", igse_wave(sine(b3 / 2, F3), F3) / sine_ref * ANCHOR_W)
v.check("Ex 22-05.4g", ratio4 * ANCHOR_W / (65 / 0.92) * 100)

# ---------------------------------------------------------------- Example 22-05.5
print("Example 22-05.5")
pn = eddy_slab_numeric(100e3, 0.3, 18e-6, 1.15e-6)
v.check("Ex 22-05.5a", pn / 1e3)
v.check("Ex 22-05.5f", 80 * 7350 / 1e3)
v.check("Ex 22-05.5b", pn / (80 * 7350) * 100)
v.check("Ex 22-05.5g", (0.35e-3 / 18e-6) ** 2)
v.check("Ex 22-05.5c", eddy_slab_numeric(100e3, 0.3, 0.35e-3, 1.15e-6) / 1e6)
pf = eddy_slab_numeric(100e3, 0.2, DPOLE, 5.0)
v.check("Ex 22-05.5d", pf / 1e3)
v.check("Ex 22-05.5e", pf / 290e3 * 100)

# ---------------------------------------------------------------- Example 22-05.6
print("Example 22-05.6")
d6 = delta_numeric(100e3, RHO100)
v.check("Ex 22-05.6a", d6 * 1e3)


def foil(h, layers, n_turns=4, width=20e-3, irms=20.0):
    rdc = RHO100 * n_turns * MLT / (h * width)
    fr = dowell_fd(h / d6, layers)
    return rdc, h / d6, fr, irms ** 2 * rdc * fr


for keys, h, m in (("bcde", 0.1e-3, 4), ("fghi", 0.3e-3, 4)):
    rdc, dl, fr, p = foil(h, m)
    for k, val in zip(keys, (rdc * 1e3, dl, fr, p)):
        v.check(f"Ex 22-05.6{k}", val)
_, _, fr_int, p_int = foil(0.3e-3, 2)
v.check("Ex 22-05.6j", fr_int)
v.check("Ex 22-05.6k", p_int)
opt6 = optimize.minimize_scalar(lambda h: foil(h, 4)[3], bounds=(0.05e-3, 0.4e-3), method="bounded",
                                options={"xatol": 1e-9})
v.check("Ex 22-05.6l", opt6.x * 1e3)
v.check("Ex 22-05.6m", opt6.fun)
v.check("Ex 22-05.6n", foil(opt6.x, 4)[1])

# ---------------------------------------------------------------- Example 22-05.7
print("Example 22-05.7")
VIN7, V7, I7, F7 = 48.0, 12.0, 20.0, 250e3
D7 = V7 / VIN7
di7 = 0.3 * I7
L7 = optimize.brentq(lambda L: (VIN7 - V7) * D7 / (F7 * L) - di7, 1e-7, 1e-4, xtol=1e-18)   # on-time volt-seconds
v.check("Ex 22-05.7a", L7 * 1e6)
ipk7 = I7 + di7 / 2
v.check("Ex 22-05.7b", ipk7)
T7 = 1 / F7
irms7 = rms_numeric(lambda t: np.where(t < D7 * T7, I7 - di7 / 2 + di7 * t / (D7 * T7),
                                       I7 + di7 / 2 - di7 * (t - D7 * T7) / ((1 - D7) * T7)), 0, T7)
v.check("Ex 22-05.7c", irms7)
KU, J, BMAX = 0.4, 4.2e6, 0.3
n_needed = L7 * ipk7 / (BMAX * AE)
ap = (L7 * ipk7 / BMAX) * (irms7 / (KU * J))              # (N·A_e) × (window per N)
v.check("Ex 22-05.7d", ap * 1e12 / 1e3)
v.check("Ex 22-05.7e", AE * AN * 1e12 / 1e4)
v.check("Ex 22-05.7f", n_needed)
N7 = 5
v.check("Ex 22-05.7g", L7 * ipk7 / (N7 * AE))
v.check("Ex 22-05.7h", gap_from_model(L7, N7) * 1e3)
v.check("Ex 22-05.7i", gap_from_fit(L7 / N7 ** 2 * 1e9))
aw7 = KU * AN / N7
v.check("Ex 22-05.7j", aw7 * 1e6)
r7 = RHO100 * N7 * MLT / aw7
v.check("Ex 22-05.7k", r7 * 1e3)
v.check("Ex 22-05.7l", irms7 ** 2 * r7)
v.check("Ex 22-05.7m", AE ** 2 * AN / MLT / 1e-11)
# K_g required: the core whose copper loss would be exactly 0.5 W, by scaling the ETD34 result (P_cu ∝ 1/K_g)
pcu_etd = (L7 * ipk7 / (BMAX * AE)) ** 2 * RHO100 * MLT * irms7 ** 2 / (KU * AN)
v.check("Ex 22-05.7n", AE ** 2 * AN / MLT * pcu_etd / 0.5 / 1e-12)
db7 = L7 * di7 / (N7 * AE)
v.check("Ex 22-05.7o", db7)
v.check("Ex 22-05.7p", igse_wave(tri(db7, D7, F7), F7) / sine_ref * ANCHOR_W)
v.check("Ex 22-05.7q", (di7 / math.sqrt(12)) ** 2 * 10 * r7)
tt7 = np.linspace(0, 1, 200001)
v.check("Ex 22-05.7r", math.sqrt(np.mean((di7 * (tt7 - 0.5)) ** 2)))  # sampled triangle (sawtooth has the same RMS)

# ---------------------------------------------------------------- Example 22-05.8
print("Example 22-05.8")
a8, b8 = 1.2 / 0.2 ** B87, 0.3 * 0.2 ** 2
opt8 = optimize.minimize_scalar(lambda x: a8 * x ** B87 + b8 / x ** 2, bounds=(0.02, 0.5), method="bounded",
                                options={"xatol": 1e-12})
v.check("Ex 22-05.8a", opt8.x)
v.check("Ex 22-05.8b", a8 * opt8.x ** B87)
v.check("Ex 22-05.8c", b8 / opt8.x ** 2)
v.check("Ex 22-05.8d", opt8.fun)
v.assert_true("at the optimum P_core/P_cu = 2/β", abs(a8 * opt8.x ** B87 / (b8 / opt8.x ** 2) - 2 / B87) < 1e-6)
v.check("Ex 22-05.8e", 6 * 0.2 / opt8.x)
b9 = 0.2 * 6 / 9
v.check("Ex 22-05.8f", a8 * b9 ** B87 + 0.3 * (9 / 6) ** 2)
llk8 = leakage_numeric(MLT, 20.9e-3, [(0.6e-3, 9), (0.1e-3, 0), (0.6e-3, -9)])
lint8 = leakage_numeric(MLT, 20.9e-3, [(0.3e-3, 4.5), (0.1e-3, 0), (0.6e-3, -9), (0.1e-3, 0), (0.3e-3, 4.5)])
v.check("Ex 22-05.8g", llk8 * 1e6)
v.check("Ex 22-05.8h", lint8 * 1e6)
lm8 = AL0 * 81
v.check("Ex 22-05.8i", lm8 * 1e6)
v.check("Ex 22-05.8j", b9)
v.check("Ex 22-05.8k", a8 * b9 ** B87)
v.check("Ex 22-05.8l", b8 / b9 ** 2)

# ---------------------------------------------------------------- text numbers
print("Text")
v.check("Txt 22-05.a", field_energy(0.3, 1.0, ae=1.0, le=0.0) / 1e3)
w_fly = 0.5 * 223e-6 * 2.52 ** 2
vgap = optimize.brentq(lambda vg: 0.3 ** 2 / (2 * MU0) * vg - w_fly, 0, 1)
v.check("Txt 22-05.b", vgap * 1e9)
v.check("Txt 22-05.c", vgap / 100e-6 * 1e3)
v.check("Txt 22-05.d", sine_ref / igse_wave(sine(0.1, F3), F3))
v.check("Txt 22-05.e", RHO100 * 1e9)
v.check("Txt 22-05.f", (RHO100 / RHO20 - 1) * 100)
v.check("Txt 22-05.g", delta_numeric(100e3, RHO20) * 1e3)
v.check("Txt 22-05.h", delta_numeric(100e3, RHO100) * 1e3)
v.check("Txt 22-05.i", dowell_fd(1.0, 5))
v.check("Txt 22-05.j", dowell_fd(1.0, 1))
s01 = igse_wave(sine(0.1, F3), F3)
v.check("Txt 22-05.k", igse_wave(tri(0.2, 0.5, F3), F3) / s01)
v.check("Txt 22-05.l", igse_wave(tri(0.2, 0.1, F3), F3) / s01)
v.check("Txt 22-05.m", igse_wave(tri(0.2, 0.1, F3), F3) / igse_wave(tri(0.2, 0.5, F3), F3))
v.check("Txt 22-05.n", optimize.brentq(lambda s: s ** 5 - 2, 1, 2))
v.check("Txt 22-05.o", 2 / B87)
v.check("Txt 22-05.p", (100e3 / 50) ** 2 / 1e6)
v.check("Txt 22-05.q", 5.0 / 1.15e-6 / 1e6)
OE = 1e3 / (4 * math.pi)                                  # A/m per oersted
v.check("Txt 22-05.r", 45 * OE / 1e3)
v.check("Txt 22-05.s", 95 * OE / 1e3)
v.check("Txt 22-05.t", 3.700 / 7640e-9 / 1e3)
v.check("Txt 22-05.u", 3.700 / 7640e-9 / 290e3)
v.check("Txt 22-05.v", 1 / (0.01 + 2.142e-6 * 50 ** 1.855))
v.check("Txt 22-05.w", 1 / (0.01 + 2.142e-6 * 100 ** 1.855))
v.check("Txt 22-05.x", lint8 / lm8 * 100)

# ---------------------------------------------------------------- problems
print("Problems")
v.check("22-05.1a", math.sqrt(50e-6 / 482e-9))
v.check("22-05.1b", 482e-9 * 121 * 1e6)
v.check("22-05.1c", l_of_gap(1, 0.2e-3) * 1e9)
v.check("22-05.2a", (field_energy(0.1, 0.1e-3) - field_energy(0.1, 0.0)) / field_energy(0.1, 0.1e-3) * 100)
v.check("22-05.2b", (field_energy(0.1, 1e-3) - field_energy(0.1, 0.0)) / field_energy(0.1, 1e-3) * 100)
b3p = 22e-6 * 8 / (15 * 52e-6)
v.check("22-05.3a", b3p)
v.check("22-05.3b", optimize.brentq(lambda i: 22e-6 * i / (15 * 52e-6) - 0.39, 0, 100))
v.check("22-05.4a", 100e-6 * 6 / (0.25 * AE))
v.check("22-05.4b", 100e-6 * 6 / (25 * AE))
v.check("22-05.4c", gap_from_model(100e-6, 25) * 1e3)
v.check("22-05.4d", 100e-6 / 625 * 1e9)
v.check("22-05.4e", gap_from_fit(160))
v.check("22-05.5a", igse_wave(sine(0.1, 2 * F3), 2 * F3) / s01)
v.check("22-05.5b", igse_wave(sine(0.2, F3), F3) / s01)
v.check("22-05.5c", igse_wave(sine(0.05, 2 * F3), 2 * F3) / s01)
br = lambda d: igse_wave(tri(0.2, d, F3), F3) / (ki_over_k() * 0.2 ** B87 * F3 ** A87)
v.check("22-05.6a", br(1 / 12))
v.check("22-05.6b", br(0.75))
v.check("22-05.6c", br(1 / 12) / br(0.5))
v.check("22-05.6d", br(0.75) / br(0.5))
p7 = eddy_slab_numeric(50, 1.5, 0.35e-3, 0.5e-6)
v.check("22-05.7a", p7 / 1e3)
v.check("22-05.7b", p7 / 7650)
v.check("22-05.7c", eddy_slab_numeric(20e3, 0.1, 0.35e-3, 0.5e-6) / 1e6)
d8 = delta_numeric(200e3, RHO100)
v.check("22-05.8a", d8 * 1e3)
v.check("22-05.8b", 2 * d8 * 1e3)
dl9 = 0.2e-3 / d6
v.check("22-05.9a", dl9)
v.check("22-05.9b", dowell_fd(dl9, 3))
v.check("22-05.9c", 1 + (5 * 9 - 1) * dl9 ** 4 / 45)
v.check("22-05.10a", 10 * RHO100 / RHO20)
v.check("22-05.10b", 25 * 10e-3 * RHO100 / RHO20)
prod = eddy_rod_numeric(100e3, 0.2, DPOLE, 5.0)
v.check("22-05.11b", prod / eddy_slab_numeric(100e3, 0.2, DPOLE, 5.0))
v.check("22-05.11c", prod / 1e3)
L12 = optimize.brentq(lambda L: (12 - 5) * (5 / 12) / (500e3 * L) - 4, 1e-8, 1e-4, xtol=1e-18)
v.check("22-05.12a", L12 * 1e6)
irms12 = rms_numeric(lambda t: np.where(t < 5 / 12 * 2e-6, 8 + 4 * t / (5 / 12 * 2e-6),
                                        12 - 4 * (t - 5 / 12 * 2e-6) / (7 / 12 * 2e-6)), 0, 2e-6)
v.check("22-05.12b", irms12)
v.check("22-05.12c", (L12 * 12 / 0.25) * (irms12 / (0.4 * 5e6)) * 1e12)
kg12 = RHO100 * L12 ** 2 * 12 ** 2 * irms12 ** 2 / (0.25 ** 2 * 0.2 * 0.4)
v.check("22-05.12d", kg12 / 1e-13)
v.check("22-05.12e", 1.90e-11 / kg12)
a13, b13 = 0.8 / 0.1 ** 2.5, 1.6 * 0.1 ** 2
opt13 = optimize.minimize_scalar(lambda x: a13 * x ** 2.5 + b13 / x ** 2, bounds=(0.02, 0.5), method="bounded",
                                 options={"xatol": 1e-12})
v.check("22-05.13a", opt13.x)
v.check("22-05.13b", a13 * opt13.x ** 2.5)
v.check("22-05.13c", b13 / opt13.x ** 2)
v.check("22-05.13d", opt13.fun)
v.check("22-05.13e", (a13 * opt13.x ** 2.5) / (b13 / opt13.x ** 2))
v.check("22-05.13f", 0.1 / opt13.x)
l14 = leakage_numeric(MLT, 20.9e-3, [(1.2e-3, 32), (0.4e-3, 0), (0.8e-3, -32)])
l14i = leakage_numeric(MLT, 20.9e-3, [(0.6e-3, 16), (0.4e-3, 0), (0.8e-3, -32), (0.4e-3, 0), (0.6e-3, 16)])
for keys, L in (("abcd", l14), ("efgh", l14i)):
    e = 0.5 * L * 2.52 ** 2
    for k, val in zip(keys, (L * 1e6, L / 223e-6 * 100, e * 1e6, e * 200 / (200 - 128) * 100e3)):
        v.check(f"22-05.14{k}", val)

# ---------------------------------------------------------------- lab
print("Lab")
NL, BS = 32, 0.39
GL = gap_from_model(223e-6, NL)


def sat_current(t):
    b = 100 * t / (NL * AE)
    h = optimize.brentq(lambda x: BS * math.tanh(MUE0 * MU0 * x / BS) + MU0 * x - b, 0, 1e8, xtol=1e-12)
    return (h * LE + b * GL / MU0) / NL


v.check("Lab 22-05.a", sat_current(5.61e-6))
v.check("Lab 22-05.b", sat_current(11.5e-6))
v.check("Lab 22-05.c", sat_current(12.5e-6))
v.check("Lab 22-05.d", optimize.brentq(lambda t: 100 * t / (NL * AE) - BS, 0, 1e-4) * 1e6)
v.check("Lab 22-05.e", 100 * 12.5e-6 / 223e-6)
v.assert_true("netlist gap parameter matches the modelled gap", abs(GL - 0.51337404e-3) < 1e-10)

sys.path.insert(0, str(LAB))
import magnetics as mg  # noqa: E402

v.assert_true("lab gapped_inductance matches the µ_e route",
              abs(mg.gapped_inductance(20, AE, LE, MUE0, 0.5e-3) - l_of_gap(20, 0.5e-3)) < 1e-15)
v.assert_true("lab dowell_fr matches the finite-difference solution",
              all(abs(mg.dowell_fr(d, m) / dowell_fd(d, m) - 1) < 1e-5 for d in (0.3, 1.0, 2.0) for m in (1, 3)))
v.assert_true("lab igse_triangle matches the sampled-waveform iGSE",
              abs(mg.igse_triangle(1.0, A87, B87, F3, 0.2, 0.3) / igse_wave(tri(0.2, 0.3, F3), F3) - 1) < 1e-4)
v.assert_true("lab eddy formula matches the integral", abs(mg.eddy_loss_lamination(1e5, 0.3, 18e-6, 1.15e-6) / pn - 1) < 1e-6)
v.assert_true("lab leakage formulas match the field integrals",
              abs(mg.leakage_inductance(9, MLT, 20.9e-3, 0.6e-3, 0.6e-3, 0.1e-3) / llk8 - 1) < 1e-9
              and abs(mg.leakage_interleaved(9, MLT, 20.9e-3, 0.6e-3, 0.6e-3, 0.1e-3) / lint8 - 1) < 1e-9)
v.assert_true("lab optimum_flux_swing matches numerical minimization",
              abs(mg.optimum_flux_swing(a8, B87, b8) / opt8.x - 1) < 1e-8)
v.assert_true("lab kg_required matches the scaling route",
              abs(mg.kg_required(RHO100, L7, ipk7, irms7, BMAX, 0.5, KU) / (AE ** 2 * AN / MLT * pcu_etd / 0.5) - 1) < 1e-9)

# ---------------------------------------------------------------- Problem 22-05.15 (powder core)
OE = 1000 / (4 * math.pi)        # A/m per oersted
le15, n15, l0_15 = 98.4e-3, 20, 10.0e-6
perm15 = {45: 0.80, 95: 0.50}    # fraction of initial permeability at each bias (chapter data)
i45 = optimize.brentq(lambda i: n15 * i / le15 - 45 * OE, 0, 100)
i95 = optimize.brentq(lambda i: n15 * i / le15 - 95 * OE, 0, 100)
v.check("22-05.15a", i45)
v.check("22-05.15b", i95)
v.check("22-05.15c", 1e6 * l0_15 * perm15[45])
v.check("22-05.15d", 1e6 * l0_15 * perm15[95])
v.check("22-05.15e", 2.0 * l0_15 / (l0_15 * perm15[45]))

v.finish()
