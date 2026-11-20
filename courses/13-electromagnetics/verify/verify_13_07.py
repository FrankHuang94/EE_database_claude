#!/usr/bin/env python3
"""Verify every number in chapter 13-07 (transmission lines in the time domain), its solutions and lab.

Independent routes (not the bounce-diagram sums used in the text):
- line parameters from the field formulas of 13-02 and 13-03;
- every waveform from a finite-difference (FDTD) solution of the telegrapher's equations, at the magic time step
  (exact for a lossless line), with the source, load and lumped capacitors or inductors as node equations;
- TDR areas by integrating the simulated reflection;
- rise times and critical lengths by root finding on the simulated or analytic responses.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
files = [COURSE / "chapters" / "13-07-transmission-lines-time-domain.md",
         COURSE / "solutions" / "13-07-solutions.md"]
lab = COURSE / "labs" / "13-07-lab" / "README.md"
if lab.exists():
    files.append(lab)
v = Verifier.from_files("13-07", *files)
mu0 = 1.25663706212e-6
e0 = 8.8541878128e-12
c0 = 1 / math.sqrt(mu0 * e0)


# ---------------------------------------------------------------- telegrapher FDTD
def simulate(Z0s, TDs, Vs, Rs, RL, t_end, cells_per_ns=400, shunt_C=None, series_L=None, rise=0.0, probes=()):
    """Cascade of lossless lines (impedances Z0s, delays TDs) from a step source (Vs, Rs, linear rise) to RL
    (None = open). shunt_C = (line_index_boundary, C) puts a capacitor at the junction after line k;
    series_L = (boundary, L) puts an inductor in series there. Probes are node names: 'in', 'out', or ('j', k).
    Returns time and probe voltages. Uses dt = dz/v in every section (magic time step)."""
    dt = 1e-9 / cells_per_ns
    nodes_v = []   # list of arrays per section
    nodes_i = []
    for Z0, TD in zip(Z0s, TDs):
        n = int(round(TD / dt))
        nodes_v.append(np.zeros(n + 1))
        nodes_i.append(np.zeros(n))
    # per-cell L and C so that each cell has delay dt: L dz = Z0 dt, C dz = dt / Z0
    steps = int(round(t_end / dt))
    t = np.arange(steps + 1) * dt
    out = {p: np.zeros(steps + 1) for p in probes}
    iL = 0.0  # series inductor current
    for nstep in range(1, steps + 1):
        tn = nstep * dt
        vs = Vs * (min(1.0, tn / rise) if rise > 0 else 1.0)
        # current updates (interior half-cells)
        for k, Z0 in enumerate(Z0s):
            vk, ik = nodes_v[k], nodes_i[k]
            ik -= (dt / (Z0 * dt)) * (vk[1:] - vk[:-1])   # dt/(L dz) = 1/Z0
        # voltage updates: interior nodes
        for k, Z0 in enumerate(Z0s):
            vk, ik = nodes_v[k], nodes_i[k]
            vk[1:-1] -= Z0 * (ik[1:] - ik[:-1])            # dt/(C dz) = Z0
        # source node (half cell, capacitance dt/(2 Z0)): trapezoid-free implicit update
        Z0 = Z0s[0]
        Ch = dt / (2 * Z0)
        v0 = nodes_v[0][0]
        nodes_v[0][0] = (Ch / dt * v0 + vs / Rs - nodes_i[0][0]) / (Ch / dt + 1 / Rs)
        # junctions between sections
        for k in range(len(Z0s) - 1):
            Za, Zb = Z0s[k], Z0s[k + 1]
            Cj = dt / (2 * Za) + dt / (2 * Zb)
            if shunt_C and shunt_C[0] == k:
                Cj += shunt_C[1]
            if series_L and series_L[0] == k:
                # node a (end of k) and node b (start of k+1) joined by an inductor
                # implicit (backward Euler) solve of the two half-cell nodes and the inductor current
                va, vb = nodes_v[k][-1], nodes_v[k + 1][0]
                Ca, Cb, Ls = dt / (2 * Za), dt / (2 * Zb), series_L[1]
                M = np.array([[Ca / dt, 0.0, 1.0], [0.0, Cb / dt, -1.0], [-1.0, 1.0, Ls / dt]])
                rhs = np.array([Ca / dt * va + nodes_i[k][-1], Cb / dt * vb - nodes_i[k + 1][0], Ls / dt * iL])
                va, vb, iL = np.linalg.solve(M, rhs)
                nodes_v[k][-1], nodes_v[k + 1][0] = va, vb
            else:
                vj = nodes_v[k][-1] + dt / Cj * (nodes_i[k][-1] - nodes_i[k + 1][0])
                nodes_v[k][-1] = vj
                nodes_v[k + 1][0] = vj
        # load node
        Zl = Z0s[-1]
        Cl = dt / (2 * Zl)
        if shunt_C and shunt_C[0] == len(Z0s) - 1:
            Cl += shunt_C[1]
        vl = nodes_v[-1][-1]
        if RL is None:
            nodes_v[-1][-1] = vl + dt / Cl * nodes_i[-1][-1]
        else:
            nodes_v[-1][-1] = (Cl / dt * vl + nodes_i[-1][-1]) / (Cl / dt + 1 / RL)
        for p in probes:
            if p == "in":
                out[p][nstep] = nodes_v[0][0]
            elif p == "out":
                out[p][nstep] = nodes_v[-1][-1]
            else:
                out[p][nstep] = nodes_v[p[1]][-1]
    return t, out


def at(t, wave, time):
    return float(np.interp(time, t, wave))


# ---------------------------------------------------------------- theory
v.check("T 13-07.a", 3.3**2 / 50)
d_per_mm = math.sqrt(4) / c0 * 1e-3
v.check("T 13-07.b", (100e-12 / 6) / d_per_mm)

# ---------------------------------------------------------------- Example 1
a, b = 0.5e-3, 1.75e-3
Lp = mu0 / (2 * math.pi) * math.log(b / a)
Cp = 2 * math.pi * 2.25 * e0 / math.log(b / a)
v.check("Ex 13-07.1a", math.sqrt(Lp / Cp))
v.check("Ex 13-07.1b", 1 / math.sqrt(Lp * Cp))
v.check("Ex 13-07.1c", math.sqrt(Lp * Cp) * 1e9)
v.check("Ex 13-07.1d", d_per_mm * 1e12)

# ---------------------------------------------------------------- Example 2
t, o = simulate([50], [1e-9], 1.0, 50, 100, 4e-9, probes=("in", "out"))
v.check("Ex 13-07.2a", at(t, o["in"], 0.5e-9))
v.check("Ex 13-07.2b", at(t, o["out"], 1.5e-9) / at(t, o["in"], 0.5e-9) - 1)
v.check("Ex 13-07.2c", at(t, o["out"], 3.5e-9))

# ---------------------------------------------------------------- Example 3
t, o = simulate([50], [1e-9], 1.0, 10, None, 80e-9, probes=("in", "out"))
vp3 = at(t, o["in"], 0.5e-9)
v.check("Ex 13-07.3a", vp3)
# source reflection from the change at the input when the first echo returns: v_in(2.5) - v_in(1.5) = Gs*2vp... use
v_in_after = at(t, o["in"], 2.5e-9)
Gs3 = (v_in_after - vp3) / vp3 - 1  # echo vp (Gamma_L = 1) arrives and adds vp(1 + Gs)
v.check("Ex 13-07.3b", Gs3)
for time, key in ((1.5e-9, "c"), (3.5e-9, "d"), (5.5e-9, "e"), (7.5e-9, "f")):
    v.check(f"Ex 13-07.3{key}", at(t, o["out"], time))
final3 = at(t, o["out"], 79.5e-9)
v.check("Ex 13-07.3g", (at(t, o["out"], 1.5e-9) / final3 - 1) * 100)
# ringing frequency from the period of the receiver waveform (zero crossings of v - final)
w = o["out"] - final3
sgn = np.sign(w[t > 0.5e-9])
cross = np.where(np.diff(sgn) != 0)[0]
period = 2 * np.mean(np.diff(cross[:4])) * (t[1] - t[0])  # early crossings, before rounding noise
v.check("Ex 13-07.3h", 1 / period / 1e6)

# ---------------------------------------------------------------- Example 4
Rser = brentq(lambda r: (10 + r - 50), 0, 100)
t, o = simulate([50], [1e-9], 1.0, 10 + Rser, None, 6e-9, probes=("in", "out"))
v.check("Ex 13-07.4a", Rser)
v.check("Ex 13-07.4b", at(t, o["in"], 0.5e-9))
v.check("Ex 13-07.4c", at(t, o["out"], 4.5e-9))
v.check("Ex 13-07.4d", at(t, o["in"], 1.5e-9))

# ---------------------------------------------------------------- Example 5 (via) and Sim d
t, o = simulate([50, 50], [1e-9, 1e-9], 2.0, 50, 50, 5e-9, shunt_C=(0, 2e-12), rise=20e-12, probes=("in",),
                cells_per_ns=5000)
refl = o["in"] - 1.0
mask = (t > 1.5e-9) & (t < 4.5e-9)
area5 = np.sum(refl[mask]) * (t[1] - t[0])
v.check("Ex 13-07.5a", 25 * 2e-12 * 1e12)
t_ideal, o_ideal = simulate([50, 50], [1e-9, 1e-9], 2.0, 50, 50, 3e-9, shunt_C=(0, 2e-12), probes=("in",),
                            cells_per_ns=2000)
v.check("Ex 13-07.5b", round(min(o_ideal["in"][(t_ideal > 1.9e-9)] - 1.0), 2))
v.check("Ex 13-07.5c", area5 * 1e12)
v.check("Ex 13-07.5d", -2 * area5 / 50 * 1e12)
v.check("Sim 13-07.d", area5 * 1e12)

# ---------------------------------------------------------------- Example 6 (step section on an er = 4 stripline)
vel = c0 / 2
t, o = simulate([50, 45, 50], [0.6e-9, 0.3e-9, 1e-9], 2.0, 50, 50, 3e-9, probes=("in",), cells_per_ns=1000)
rho = o["in"] - 1.0
late = t > 0.1e-9
start = t[late][np.argmax(rho[late] < -0.02)]
v.check("Ex 13-07.6a", 50 * (1 + at(t, rho, 1.5e-9)) / (1 - at(t, rho, 1.5e-9)))
v.assert_true("FDTD reflection begins at the 1.2 ns round trip", abs(start - 1.2e-9) < 3e-12, str(start))
v.check("Ex 13-07.6b", vel * 1.2e-9 / 2 * 100)
v.check("Ex 13-07.6c", vel * 0.6e-9 / 2 * 100)

# ---------------------------------------------------------------- practitioner and simulation
v.check("Prac 13-07.a", math.sqrt(4.6) / c0 * 1e-3 * 1e12)
t, o = simulate([50], [1e-9], 1.0, 10, None, 6e-9, probes=("out",))
v.check("Sim 13-07.a", at(t, o["out"], 1.5e-9))
v.check("Sim 13-07.b", at(t, o["out"], 3.5e-9))
v.check("Sim 13-07.c", at(t, o["out"], 5.5e-9))

# ---------------------------------------------------------------- Problems
L1, C1 = 333.6e-9, 133.4e-12
v.check("13-07.1a", math.sqrt(L1 / C1))
v.check("13-07.1b", 1 / math.sqrt(L1 * C1))
v.check("13-07.1c", math.sqrt(L1 * C1) * 1e-3 * 1e12)
v.check("13-07.1d", c0**2 * L1 * C1)
for RL, key in ((1e-9, "a"), (None, "b"), (25, "c"), (75, "d"), (100, "e")):
    t, o = simulate([50], [1e-9], 2.0, 50, RL, 2e-9, probes=("out",))
    v.check(f"13-07.2{key}", at(t, o["out"], 1.5e-9) - 1.0)  # v_L = v+(1 + Gamma) with v+ = 1
t, o = simulate([50], [1e-9], 3.3, 25, 50, 2e-9, probes=("in",))
v.check("13-07.3a", at(t, o["in"], 0.5e-9))
t, o = simulate([50], [1e-9], 1.0, 100, 25, 20e-9, probes=("in", "out"))
v.check("13-07.4a", at(t, o["in"], 0.5e-9))
gl4 = at(t, o["out"], 1.5e-9) / at(t, o["in"], 0.5e-9) - 1
v.check("13-07.4c", gl4)
# source reflection from the second arrival: v_out(3.5) - v_out(1.5) = vp(1+GL) GL GS
v.check("13-07.4b", (at(t, o["out"], 3.5e-9) - at(t, o["out"], 1.5e-9)) / (at(t, o["out"], 1.5e-9) * gl4))
for time, key in ((1.5e-9, "d"), (3.5e-9, "e"), (5.5e-9, "f"), (19.5e-9, "g")):
    v.check(f"13-07.4{key}", at(t, o["out"], time))
t, o = simulate([50], [0.8e-9], 1.8, 15 + 35, None, 5e-9, probes=("in", "out"))
v.check("13-07.5a", brentq(lambda r: 15 + r - 50, 0, 100))
v.check("13-07.5b", at(t, o["in"], 0.4e-9))
v.check("13-07.5c", at(t, o["out"], 2.0e-9))
v.check("13-07.5d", at(t, o["in"], 1.2e-9))
plateau = t[(o["in"] > 0.85) & (o["in"] < 0.95)]
v.check("13-07.5e", (plateau.max() - plateau.min()) * 1e9)
v.check("13-07.6a", 3.3**2 / 50)
v.check("13-07.6b", 3.3**2 / 100)
v.check("13-07.6c", 3.3 * (3.3 / 200))
t, o = simulate([50], [1e-9], 1.0, 50, None, 6e-9, shunt_C=(0, 5e-12), probes=("out",), cells_per_ns=1000)
vout = o["out"]
t10 = brentq(lambda tt: at(t, vout, tt) - 0.1, 1.0e-9, 4e-9)
t90 = brentq(lambda tt: at(t, vout, tt) - 0.9, 1.0e-9, 5.5e-9)
v.check("13-07.7a", (t90 - t10) / math.log(9) * 1e12)
v.check("13-07.7b", at(t, vout, 5.99e-9) / (1 - math.exp(-4.99e-9 / 250e-12)))
v.check("13-07.7c", (t90 - t10) * 1e12)
v.check("13-07.8a", 0.66 * c0 * 4.2e-9 / 2)
v.check("13-07.9a", (100e-12 / 6) / d_per_mm)
v.check("13-07.9b", (1e-9 / 6) / d_per_mm / 10)
# 10: simulate a series inductor and a shunt capacitor and integrate the reflections
t, o = simulate([50, 50], [1e-9, 1e-9], 2.0, 50, 50, 5e-9, series_L=(0, 1e-9), rise=20e-12, probes=("in",),
                cells_per_ns=5000)
areaL = np.sum((o["in"] - 1.0)[(t > 1.5e-9) & (t < 4.5e-9)]) * (t[1] - t[0])
v.check("13-07.10a", 2 * 50 * areaL * 1e9)
t, o = simulate([50, 50], [1e-9, 1e-9], 2.0, 50, 50, 5e-9, shunt_C=(0, 1e-12), rise=20e-12, probes=("in",),
                cells_per_ns=5000)
areaC = np.sum((o["in"] - 1.0)[(t > 1.5e-9) & (t < 4.5e-9)]) * (t[1] - t[0])
v.check("13-07.10b", -2 * areaC / 50 * 1e12)
vel11 = 0.66 * c0
v.check("13-07.11a", 1 / (vel11**2 * 101e-12) * 1e9)
v.check("13-07.11b", math.sqrt((1 / (vel11**2 * 101e-12)) / 101e-12))
t, o = simulate([75], [1e-9], 1.0, 25, 150, 20e-9, probes=("in", "out"))
vp12 = at(t, o["in"], 0.5e-9)
v.check("13-07.12a", vp12)
gl12 = at(t, o["out"], 1.5e-9) / vp12 - 1
v.check("13-07.12b", gl12)
v.check("13-07.12c", (at(t, o["out"], 3.5e-9) - at(t, o["out"], 1.5e-9)) / (at(t, o["out"], 1.5e-9) * gl12))
for time, key in ((1.5e-9, "d"), (3.5e-9, "e"), (5.5e-9, "f"), (7.5e-9, "g"), (19.5e-9, "h")):
    v.check(f"13-07.12{key}", at(t, o["out"], time))
t, o = simulate([50], [1e-9], 1.0, 1e-3, None, 40e-9, probes=("out",))
w = o["out"] - 1.0
sgn = np.sign(w[int(0.5e-9 / (t[1] - t[0])):])
cross = np.where(np.diff(sgn) != 0)[0]
v.check("13-07.13a", 1 / (2 * np.mean(np.diff(cross[:4])) * (t[1] - t[0])) / 1e6)
t, o = simulate([50, 75], [1e-9, 1e-9], 1.0, 50, 75, 4e-9, probes=("in", ("j", 0), "out"))
v.check("13-07.14a", at(t, o[("j", 0)], 1.5e-9) / 0.5)
v.check("13-07.14b", at(t, o["out"], 2.5e-9))
v.check("13-07.14c", at(t, o["in"], 2.5e-9) - 0.5)

# ---------------------------------------------------------------- Lab
if lab.exists():
    # overshoot at the open end of a line driven through 10 ohm with a 100 ps linear edge, for delay = tr/6 and tr
    for ratio, key in ((1 / 10, "a"), (1 / 6, "b"), (1.0, "c")):
        TD = 100e-12 * ratio
        t, o = simulate([50], [TD], 1.0, 10, None, 20 * max(TD, 100e-12) + 2e-9, rise=100e-12, probes=("out",),
                        cells_per_ns=20000)
        v.check(f"Lab 13-07.{key}", (o["out"].max() - 1.0) * 100)

sys.exit(v.finish())
