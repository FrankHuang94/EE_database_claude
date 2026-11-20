#!/usr/bin/env python3
"""Verify chapter 15-09 (lead and lag compensation): examples, problems and lab answers.

Routes:
- lead geometry two ways: the closed form arcsin((a-1)/(a+1)) and a numerical maximization of the phase;
- designs from labs/15-09-lab/compensate.py, then margins by root finding (labs/15-07-lab/freqdomain.py) and step
  responses by exact simulation (labs/15-03-lab/specs.py);
- root-locus designs checked by confirming the desired point is a closed-loop root;
- the passive lead network's phase computed from its circuit equation; ngspice confirms it (lead_network.cir).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
for lab in ("15-09-lab", "15-07-lab", "15-03-lab"):
    sys.path.insert(0, str(ROOT / "labs" / lab))
from eeverify import Verifier  # noqa: E402
import compensate as cp  # noqa: E402
from freqdomain import _unwrapped_phase, freq_resp, margins  # noqa: E402
from specs import step_specs  # noqa: E402

CH = ROOT / "chapters" / "15-09-lead-lag-compensation.md"
v = Verifier.from_files("15-09", CH, ROOT / "solutions" / "15-09-solutions.md", ROOT / "labs" / "15-09-lab" / "README.md")


def max_phase_numeric(alpha):
    f = lambda lw: -math.degrees(math.atan(alpha * 10**lw) - math.atan(10**lw))  # noqa: E731
    r = minimize_scalar(f, bounds=(-4, 4), method="bounded", options={"xatol": 1e-12})
    return -r.fun, 10**r.x


def step_of(n, d, t_end):
    return step_specs(n, np.polyadd(d, n), t_end)


# ---------------------------------------------------------------------------------------- text
for a, key in ((2, "a"), (4, "b"), (16, "c")):
    v.check(f"Txt 15-09.{key}", max_phase_numeric(a)[0])
v.check("Txt 15-09.d", cp.lead_alpha(60))

# ---------------------------------------------------------------------------------------- Example 1
ph, xm = max_phase_numeric(10)
v.check("Ex 15-09.1a", ph)
v.assert_true("Ex 1: closed form equals the numerical maximum", abs(ph - cp.lead_phase(10)) < 1e-9)
v.assert_true("Ex 1: the peak is at wT = 1/sqrt(alpha)", abs(xm - 1 / math.sqrt(10)) < 1e-6)
C1 = lambda w: (1 + 1j * w * 10) / (1 + 1j * w)  # noqa: E731
v.check("Ex 15-09.1b", 20 * math.log10(abs(C1(1 / math.sqrt(10)))))
v.check("Ex 15-09.1c", 20 * math.log10(abs(C1(1e9))))

# ---------------------------------------------------------------------------------------- Example 2
G = ([10.0], [1.0, 1.0, 0.0])
m0 = margins(*G)
v.check("Ex 15-09.2a", m0["wc"])
v.check("Ex 15-09.2b", m0["pm"])
s0 = step_of(*G, 20)
v.check("Ex 15-09.2c", 100 * s0["overshoot"])
v.check("Ex 15-09.2d", s0["settle"])
d = cp.design_lead(*G, 45)
v.check("Ex 15-09.2e", d["phi"])
v.check("Ex 15-09.2f", d["alpha"])
v.check("Ex 15-09.2g", d["wm"])
v.check("Ex 15-09.2h", d["zero"])
v.check("Ex 15-09.2i", d["pole"])
n2, d2 = cp.with_comp(*G, d["cnum"], d["cden"])
m2 = margins(n2, d2)
v.check("Ex 15-09.2j", m2["pm"])
v.assert_true("Ex 2: the new crossover is at w_m", abs(m2["wc"] / d["wm"] - 1) < 1e-9)
s2 = step_of(n2, d2, 20)
v.check("Ex 15-09.2k", 100 * s2["overshoot"])
v.check("Ex 15-09.2l", s2["settle"])

# ---------------------------------------------------------------------------------------- Example 3
l = cp.design_lag(*G, 50)
v.check("Ex 15-09.3a", l["wc"])
v.check("Ex 15-09.3b", l["beta"])
v.check("Ex 15-09.3c", l["zero"])
v.check("Ex 15-09.3d", l["pole"])
v.assert_true("Ex 3: wc = tan 35 deg", abs(l["wc"] - math.tan(math.radians(35))) < 1e-9)
n3, d3 = cp.with_comp(*G, l["cnum"], l["cden"])
v.check("Ex 15-09.3e", margins(n3, d3)["pm"])
s3 = step_of(n3, d3, 80)
v.check("Ex 15-09.3f", 100 * s3["overshoot"])
v.check("Ex 15-09.3g", s3["settle"])

# ---------------------------------------------------------------------------------------- Example 4
sd = complex(-2, 2 * math.sqrt(3))
need = -180 + math.degrees(np.angle(sd)) + math.degrees(np.angle(sd + 1))
v.check("Ex 15-09.4a", need)
angp = math.degrees(np.angle(sd + 2)) - need
pc = sd.real - sd.imag / math.tan(math.radians(angp))
v.check("Ex 15-09.4b", pc)
K4 = abs(sd) * abs(sd + 1) * abs(sd - pc) / abs(sd + 2)
v.check("Ex 15-09.4c", K4)
num4 = np.polymul([K4], [1, 2])
den4 = np.polymul([1, 1, 0], [1, -pc])
cl4 = np.polyadd(den4, num4)
v.assert_true("Ex 4: s_d is a closed-loop root", abs(np.polyval(cl4, sd)) < 1e-9)
r4 = np.roots(cl4)
v.check("Ex 15-09.4d", float(r4[np.argmin(abs(r4.imag))].real))
v.check("Ex 15-09.4e", 100 * step_specs(num4, cl4, 10)["overshoot"])
v.check("Ex 15-09.4f", K4 * 2 / (-pc))
# Attribution: the dominant pair with the closed-loop zero at -2 alone (DC gain 1), then with the third pole.
wn4 = abs(sd)
v.check("Ex 15-09.4g", 100 * step_specs([wn4**2 / 2, wn4**2], [1, 4, wn4**2], 20)["overshoot"])
v.assert_true("Ex 4: the third pole reduces the overshoot below the pair-with-zero value",
              step_specs(num4, cl4, 10)["overshoot"] < step_specs([wn4**2 / 2, wn4**2], [1, 4, wn4**2], 20)["overshoot"])

# ---------------------------------------------------------------------------------------- Example 5
zl = d["wm"] / 10
pl = zl / 5
v.check("Ex 15-09.5a", zl)
v.check("Ex 15-09.5b", pl)
n5, d5 = cp.with_comp(np.polymul(d["cnum"], [10.0 * 5]), np.polymul(d["cden"], G[1]), [1 / zl, 1], [1 / pl, 1])
s_ = 1e-9
v.check("Ex 15-09.5c", abs(s_ * np.polyval(n5, s_) / np.polyval(d5, s_)))
m5 = margins(n5, d5)
v.check("Ex 15-09.5d", m5["pm"])
s5 = step_of(n5, d5, 40)
v.check("Ex 15-09.5e", 100 * s5["overshoot"])
v.check("Ex 15-09.5f", s5["settle"])

# ---------------------------------------------------------------------------------------- Example 6
Vin, Lb, Cb, Rb = 5.0, 1e-6, 100e-6, 1.0
w0 = 1 / math.sqrt(Lb * Cb)
v.check("Ex 15-09.6a", w0 / (2 * math.pi) / 1e3)
v.check("Ex 15-09.6b", Rb * math.sqrt(Cb / Lb))
wp6, wc6 = 2 * math.pi * 300e3, 2 * math.pi * 60e3


def type3(wz, wI, C=Cb):
    n = np.polymul(wI * np.polymul([1 / wz, 1], [1 / wz, 1]), [Vin])
    dd = np.polymul(np.polymul([1, 0], np.polymul([1 / wp6, 1], [1 / wp6, 1])), [Lb * C, Lb / Rb, 1])
    return n, dd


res6 = {}
for kz, keys in ((1.0, "cde"), (0.5, "hfg")):
    wI = brentq(lambda x: abs(freq_resp(*type3(kz * w0, x), wc6)) - 1, 1, 1e9, xtol=1e-9)
    m = margins(*type3(kz * w0, wI), w_lo=1e2, w_hi=1e8)
    v.check(f"Ex 15-09.6{keys[0]}", wI)
    v.check(f"Ex 15-09.6{keys[1]}", m["pm"])
    v.check(f"Ex 15-09.6{keys[2]}", m["gm_db"])
    res6[kz] = wI
# Op-amp realization of the f0/2 design (section 3.6): R1 chosen, the rest from the corner frequencies.
wz6, R1o = 0.5 * w0, 10e3
v.check("Ex 15-09.6p", wz6 / (2 * math.pi) / 1e3)
C12 = 1 / (R1o * res6[0.5])
ratio6 = wp6 / wz6
C2o = C12 / ratio6
C1o = C12 - C2o
R2o = 1 / (wz6 * C1o)
R3o = R1o / (ratio6 - 1)
C3o = 1 / (wp6 * R3o)
for key, val in (("i", C12 * 1e9), ("j", C2o * 1e12), ("k", C1o * 1e9), ("l", R2o / 1e3), ("m", ratio6),
                 ("n", R3o), ("o", C3o * 1e9)):
    v.check(f"Ex 15-09.6{key}", val)
wq = np.logspace(2, 7, 2001)
sq = 1j * wq
Zf = 1 / (1 / (R2o + 1 / (sq * C1o)) + sq * C2o)
Zin = 1 / (1 / R1o + 1 / (R3o + 1 / (sq * C3o)))
Hc = -Zf / Zin
Ht = res6[0.5] * (1 + sq / wz6) ** 2 / (sq * (1 + sq / wp6) ** 2)
v.assert_true("Ex 6: the op-amp network equals minus the Type III transfer function at every frequency",
              np.max(np.abs(Hc + Ht) / np.abs(Ht)) < 1e-9)
w = np.logspace(2, 8, 400001)
Lw = np.abs(freq_resp(*type3(0.5 * w0, res6[0.5]), w))
crossings = int(np.sum((Lw[:-1] - 1) * (Lw[1:] - 1) < 0))

# ---------------------------------------------------------------------------------------- Problem 1
for phi, key in ((30, "a"), (45, "b"), (60, "c")):
    a = cp.lead_alpha(phi)
    v.check(f"15-09.1{key}", a)
    v.assert_true(f"P1: alpha gives {phi} deg", abs(max_phase_numeric(a)[0] - phi) < 1e-6)

# ---------------------------------------------------------------------------------------- Problem 2
for f, key in ((10, "a"), (5, "b")):
    z, p = 1 / f, 1 / (f * 10)
    v.check(f"15-09.2{key}", math.degrees(np.angle((1 + 1j / z) / (1 + 1j / p))))

# ---------------------------------------------------------------------------------------- Problem 3
R1, C1v = cp.lead_rc(4, 1000.0, 10e3)
v.check("15-09.3a", R1 / 1e3)
v.check("15-09.3b", C1v * 1e9)
H = lambda w: (10e3 / (R1 + 10e3)) * (1 + 1j * w * R1 * C1v) / (1 + 1j * w * (R1 * 10e3 / (R1 + 10e3)) * C1v)  # noqa: E731
wpk = 10 ** minimize_scalar(lambda lw: -np.angle(H(10**lw)), bounds=(1, 5), method="bounded", options={"xatol": 1e-12}).x
v.assert_true("P3: the network's phase peaks at 1000 rad/s", abs(wpk - 1000) < 1e-3)

# ---------------------------------------------------------------------------------------- Problem 4
# Kv = lim s*K*P(s) = K/2 must equal 20; solve for K from the plant's limit rather than restating it.
Kp4 = 20.0 / (1.0 / np.polyval([1.0, 2.0], 0.0))
v.check("15-09.4a", Kp4)
G4 = ([Kp4], [1.0, 2.0, 0.0])
m = margins(*G4)
v.check("15-09.4b", m["wc"])
v.check("15-09.4c", m["pm"])
d4 = cp.design_lead(*G4, 50)
v.check("15-09.4d", d4["alpha"])
v.check("15-09.4e", d4["wm"])
v.check("15-09.4f", d4["zero"])
v.check("15-09.4g", d4["pole"])
n, dd = cp.with_comp(*G4, d4["cnum"], d4["cden"])
v.check("15-09.4h", margins(n, dd)["pm"])
s = step_of(n, dd, 10)
v.check("15-09.4i", 100 * s["overshoot"])
v.check("15-09.4j", s["settle"])

# ---------------------------------------------------------------------------------------- Problem 5
l5 = cp.design_lag(*G4, 50)
v.check("15-09.5a", l5["wc"])
v.check("15-09.5b", l5["beta"])
v.check("15-09.5c", l5["zero"])
v.check("15-09.5d", l5["pole"])
n, dd = cp.with_comp(*G4, l5["cnum"], l5["cden"])
v.check("15-09.5e", margins(n, dd)["pm"])
s = step_of(n, dd, 60)
v.check("15-09.5f", 100 * s["overshoot"])
v.check("15-09.5g", s["settle"])

# ---------------------------------------------------------------------------------------- Problem 6
sd6 = complex(-3, 4)
need6 = -180 + math.degrees(np.angle(sd6)) + math.degrees(np.angle(sd6 + 2))
v.check("15-09.6a", need6)
pc6 = -3 - 4 / math.tan(math.radians(90 - need6))
v.check("15-09.6b", pc6)
K6 = abs(sd6) * abs(sd6 + 2) * abs(sd6 - pc6) / abs(sd6 + 3)
v.check("15-09.6c", K6)
cl6 = np.polyadd(np.polymul([1, 2, 0], [1, -pc6]), np.polymul([K6], [1, 3]))
v.assert_true("P6: -3+j4 is a closed-loop root", abs(np.polyval(cl6, sd6)) < 1e-9)
r6 = np.roots(cl6)
v.check("15-09.6d", float(r6[np.argmin(abs(r6.imag))].real))
v.check("15-09.6e", K6 * 3 / (-pc6) / 2)

# ---------------------------------------------------------------------------------------- Problem 7
m7 = margins([8.0], [1.0, 4.0, 0.0])
z7 = m7["wc"] / 10
v.check("15-09.7a", z7)
v.check("15-09.7b", z7 / 10)
n, dd = cp.with_comp([80.0], [1.0, 4.0, 0.0], [1 / z7, 1], [10 / z7, 1])
v.check("15-09.7c", abs(1e-9 * np.polyval(n, 1e-9) / np.polyval(dd, 1e-9)))
v.check("15-09.7d", margins(n, dd)["pm"])

# ---------------------------------------------------------------------------------------- Problem 8
G8 = ([50.0], np.polymul([1, 0], np.polymul([1, 1], [1, 5])))
v.check("15-09.8a", margins(*G8)["gm"])


def two_stage(alpha):
    wm = brentq(lambda x: abs(freq_resp(*G8, x)) - 1 / alpha, 1e-2, 1e3, xtol=1e-14)
    T = 1 / (wm * math.sqrt(alpha))
    c = np.polymul([alpha * T, 1], [alpha * T, 1])
    cd = np.polymul([T, 1], [T, 1])
    n, dd = cp.with_comp(*G8, c, cd)
    return margins(n, dd, w_lo=1e-3, w_hi=1e4), wm, T


a8 = brentq(lambda a: two_stage(a)[0]["pm"] - 45, 2, 200, xtol=1e-12)
m8, wm8, T8 = two_stage(a8)
v.check("15-09.8b", a8)
v.check("15-09.8c", cp.lead_phase(a8))
v.check("15-09.8d", wm8)
v.check("15-09.8e", 1 / (a8 * T8))
v.check("15-09.8f", 1 / T8)
v.check("15-09.8g", m8["gm"])
v.assert_true("P8: a single stage would need alpha > 300", cp.lead_alpha(2 * cp.lead_phase(a8)) > 300)

# ---------------------------------------------------------------------------------------- Problem 9
C9 = 70e-6
v.check("15-09.9a", 1 / (2 * math.pi * math.sqrt(Lb * C9)) / 1e3)
v.check("15-09.9b", Rb * math.sqrt(C9 / Lb))
m9 = margins(*type3(0.5 * w0, res6[0.5], C=C9), w_lo=1e2, w_hi=1e8)
v.check("15-09.9c", m9["wc"] / (2 * math.pi) / 1e3)
v.check("15-09.9d", m9["pm"])
v.check("15-09.9e", m9["gm_db"])

# ---------------------------------------------------------------------------------------- Problem 10
v.check("15-09.10a", 20 * math.log10(d["alpha"]))

# ---------------------------------------------------------------------------------------- Lab
Hn = lambda w: (1e3 / 10e3) * (1 + 1j * w * 9e3 * 10e-9) / (1 + 1j * w * 900 * 10e-9)  # noqa: E731
r = minimize_scalar(lambda lw: -np.angle(Hn(10**lw)), bounds=(3, 6), method="bounded", options={"xatol": 1e-12})
v.check("Lab 15-09.a", math.degrees(-r.fun))
v.check("Lab 15-09.b", 10**r.x / (2 * math.pi) / 1e3)
v.check("Lab 15-09.c", crossings)

# Part 3: move the lead zero; the pole follows from the angle condition at s_d = -2 + j2*sqrt(3) on 1/[s(s+1)].
sd3 = complex(-2, 2 * math.sqrt(3))
need3 = -180 + math.degrees(np.angle(sd3)) + math.degrees(np.angle(sd3 + 1))
for zc, kp, kk, kt, ka in ((-1.5, "d", "f", "h", "j"), (-3.0, "e", "g", "i", "k")):
    zang = math.degrees(np.angle(sd3 - zc))
    pc = sd3.real - sd3.imag / math.tan(math.radians(zang - need3))
    K3 = abs(sd3) * abs(sd3 + 1) * abs(sd3 - pc) / abs(sd3 - zc)
    cl3 = np.polyadd(np.polymul([1, 1, 0], [1, -pc]), np.polymul([K3], [1, -zc]))
    v.assert_true(f"Lab Part 3: s_d is a closed-loop root for zero {zc}", abs(np.polyval(cl3, sd3)) < 1e-9)
    r3 = np.roots(cl3)
    v.check(f"Lab 15-09.{ka}", zang)
    v.check(f"Lab 15-09.{kp}", pc)
    v.check(f"Lab 15-09.{kk}", K3 * zc / pc)
    v.check(f"Lab 15-09.{kt}", float(r3[np.argmin(abs(r3.imag))].real))

# Part 4: Type III sweep with crossover held at 60 kHz.
w4 = np.logspace(2, 8, 600001)


def type3_at(kz):
    wI = brentq(lambda x: abs(freq_resp(*type3(kz * w0, x), wc6)) - 1, 1, 1e9, xtol=1e-9)
    n, dd = type3(kz * w0, wI)
    H = freq_resp(n, dd, w4)
    mag, ph = np.abs(H), np.degrees(np.unwrap(np.angle(H)))
    one = int(np.sum((mag[:-1] - 1) * (mag[1:] - 1) < 0)) == 1
    lf = 20 * math.log10(abs(freq_resp(n, dd, 2 * math.pi * 1e3)))
    return margins(n, dd, w_lo=1e2, w_hi=1e8), one, ph[mag > 1].min(), lf


sweep = {kz: type3_at(kz) for kz in (0.3, 0.5, 1.0, 1.5)}
v.assert_true("Lab Part 4: one 0 dB crossing for zeros at 0.3, 0.5, 1 and 1.5 f0", all(r[1] for r in sweep.values()))
v.assert_true("Lab Part 4: the sweep reproduces Example 15-09.6 at f0 and f0/2",
              abs(sweep[1.0][0]["pm"] - margins(*type3(w0, res6[1.0]), w_lo=1e2, w_hi=1e8)["pm"]) < 1e-6
              and abs(sweep[0.5][0]["pm"] - margins(*type3(0.5 * w0, res6[0.5]), w_lo=1e2, w_hi=1e8)["pm"]) < 1e-6)
v.assert_true("Lab Part 4: phase stays above -180 deg while |L| > 1 for zeros at 0.3, 0.5 and 1 f0",
              all(sweep[k][2] > -180 for k in (0.3, 0.5, 1.0)))
v.assert_true("Lab Part 4: the phase dips below -180 deg while |L| > 1 for zeros at 1.5 f0", sweep[1.5][2] < -180)
v.assert_true("Lab Part 4: PM falls monotonically as the zeros rise",
              sweep[0.3][0]["pm"] > sweep[0.5][0]["pm"] > sweep[1.0][0]["pm"] > sweep[1.5][0]["pm"])
v.check("Lab 15-09.l", sweep[1.5][0]["pm"])
v.check("Lab 15-09.m", sweep[0.3][0]["pm"])
v.check("Lab 15-09.n", sweep[1.0][3])
v.check("Lab 15-09.o", sweep[0.3][3])
v.check("Lab 15-09.q", sweep[1.0][3] - sweep[0.3][3])
# Conditional stability at 1.5 f0: the two -180 deg crossings below wc, then closed-loop roots against gain reduction.
wI15 = brentq(lambda x: abs(freq_resp(*type3(1.5 * w0, x), wc6)) - 1, 1, 1e9, xtol=1e-9)
n15, d15 = type3(1.5 * w0, wI15)
wf = np.logspace(4, 6, 200001)
phf = _unwrapped_phase(n15, d15, wf, 0.0)
jj = np.flatnonzero((phf[:-1] + math.pi) * (phf[1:] + math.pi) < 0)
v.assert_true("Lab Part 4: at least two -180 deg crossings between 10^4 and 10^6 rad/s", len(jj) >= 2)
w180s = [brentq(lambda x: float(_unwrapped_phase(n15, d15, np.array([x]), 0.0)[0]) + math.pi, wf[i], wf[i + 1], xtol=1e-9)
          for i in jj[:2]]
v.assert_true("Lab Part 4: both crossings lie below the 60 kHz crossover", all(x < wc6 for x in w180s))
v.check("Lab 15-09.t", w180s[0] / (2 * math.pi) / 1e3)
v.check("Lab 15-09.u", w180s[1] / (2 * math.pi) / 1e3)
gdb = [20 * math.log10(abs(freq_resp(n15, d15, x))) for x in w180s]


def max_re(db):
    return float(np.roots(np.polyadd(d15, 10 ** (-db / 20) * n15)).real.max())


v.assert_true("Lab Part 4: the loop as designed is stable", max_re(0.0) < 0)
lo_db = brentq(max_re, 10, 20, xtol=1e-10)
hi_db = brentq(max_re, 25, 35, xtol=1e-10)
v.assert_true("Lab Part 4: unstable inside the interval, stable outside it",
              max_re(0.5 * (lo_db + hi_db)) > 0 and max_re(lo_db - 1) < 0 and max_re(hi_db + 1) < 0)
v.assert_true("Lab Part 4: the interval ends are the loop gains at the -180 deg crossings",
              abs(lo_db - gdb[1]) < 1e-6 and abs(hi_db - gdb[0]) < 1e-6)
v.check("Lab 15-09.r", lo_db)
v.check("Lab 15-09.s", hi_db)
kstar = brentq(lambda k: type3_at(k)[2] + 180, 1.3, 1.45, xtol=1e-6)
v.check("Lab 15-09.p", kstar)

sys.exit(v.finish())
