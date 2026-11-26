#!/usr/bin/env python3
"""Verify the C1 option A design report: recompute the hand sizing and check the simulated summaries.

- Hand values (C1A.*) are recomputed from the process parameters in ../models/c1_process.lib, which this script
  parses rather than retyping, so a change to the deck that is not carried into the report fails here.
- Simulated values quoted in the report (S.*) are read from results.md, whose answer key CI checks against ngspice
  (tools/run_spice.py); the worst cases and margins are recomputed from all eleven corners, and every requirement
  of the specification is asserted at every corner.
- Second routes: the two-pole crossover by root-finding and by a frequency sweep; the body-effect iteration by
  fixed point and by brentq; KP's temperature scaling against the threshold-free square law.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, load_answer_key  # noqa: E402

v = Verifier.from_files("C1A", HERE / "design-report.md")


# ----------------------------------------------------------------- process parameters, parsed from the deck
def deck(section):
    text = (HERE.parent / "models" / "c1_process.lib").read_text(encoding="utf-8")
    body = text.split(f".lib {section}\n", 1)[1].split(f".endl {section}", 1)[0].replace("\n+", " ")
    models = {}
    for name, params in re.findall(r"\.model (\w+) \w+ \(([^)]*)\)", body):
        kv = {}
        for key, val in re.findall(r"(\w+)=([-+0-9.eE]+[a-z]?)", params):
            mult = {"u": 1e-6, "n": 1e-9, "m": 1e-3, "p": 1e-12}.get(val[-1], 1.0) if val[-1].isalpha() else 1.0
            kv[key.lower()] = float(val.rstrip("unmp")) * mult
        models[name] = kv
    return models


tt, ss = deck("tt"), deck("ss")
N, P = tt["nch"], tt["pch"]
KPn, KPp, VTn = N["kp"], P["kp"], N["vto"]
lamn, lamp, gam, PHI = N["lambda"], P["lambda"], N["gamma"], N["phi"]
COV = N["cgso"]                                     # F/m
EPS0 = 8.8541878128e-12
Cox = 3.9 * EPS0 / N["tox"]                         # F/m^2
v.assert_true("deck: PMOS overlap equals NMOS overlap", P["cgso"] == COV)
v.assert_true("deck: SS is KP -15% and |VTO| +50 mV",
              abs(ss["nch"]["kp"] / KPn - 0.85) < 1e-12 and abs(ss["nch"]["vto"] - VTn - 0.05) < 1e-12)

k_B, T = 1.380649e-23, 300.15
CL, Cc, L, VDD = 2e-12, 1.5e-12, 0.5e-6, 1.8

v.check("C1A.cox", Cox * 1e3)                       # F/m^2 -> fF/um^2
v.check("C1A.kpratio", KPn / KPp)

# ----------------------------------------------------------------- corner strategy
kp_ss_hot = (ss["nch"]["kp"] / KPn) * ((125 + 273.15) / (27 + 273.15)) ** -1.5
v.check("C1A.kpss", kp_ss_hot)
v.check("C1A.gmss", math.sqrt(kp_ss_hot))

# ----------------------------------------------------------------- hand sizing
gm1 = 400e-6
gbw = gm1 / (2 * math.pi * Cc)
v.check("C1A.gm1", gm1 * 1e6)
v.check("C1A.gbw", gbw / 1e6)
v.check("C1A.gbwss0", gbw / 1e6)
v.check("C1A.gbwss", gbw * math.sqrt(kp_ss_hot) / 1e6)
Vov1 = 0.1
ID1 = gm1 * Vov1 / 2
I5 = 2 * ID1
v.check("C1A.id1", ID1 * 1e6)
v.check("C1A.i5", I5 * 1e6)
v.check("C1A.sr", I5 / Cc / 1e6)
wl1 = 2 * ID1 / (KPn * Vov1 ** 2)
v.check("C1A.wl1", wl1)
v.check("C1A.w1", wl1 * L * 1e6)
v.assert_true("square law: (W/L)_1 reproduces g_m1", abs(math.sqrt(2 * KPn * wl1 * ID1) - gm1) < 1e-12)

v.check("C1A.gm6min", 2.2 * (CL / Cc) * gm1 * 1e6)
gm6, Vov6 = 1.6e-3, 0.2
I6 = gm6 * Vov6 / 2
wl6 = 2 * I6 / (KPp * Vov6 ** 2)
v.check("C1A.i6", I6 * 1e6)
v.check("C1A.wl6", wl6)
v.check("C1A.w6", wl6 * L * 1e6)
wl3 = wl6 * ID1 / I6
v.check("C1A.wl3", wl3)
v.check("C1A.w3", wl3 * L * 1e6)
v.assert_true("mirror: M3 at M6's current density gives equal overdrive",
              abs(math.sqrt(2 * ID1 / (KPp * wl3)) - Vov6) < 1e-12)
Vov5 = 0.15
wl5 = 2 * I5 / (KPn * Vov5 ** 2)
v.check("C1A.wl5", wl5)
v.check("C1A.w5", wl5 * L * 1e6)
v.check("C1A.w8", wl5 * (20e-6 / I5) * L * 1e6)
v.check("C1A.w7", wl5 * (I6 / I5) * L * 1e6)
v.check("C1A.zrhp", gm6 / (2 * math.pi * Cc) / 1e6)
v.check("C1A.rz", 1 / gm6)

# drawn widths in the netlist are the rounded hand values
sub = (HERE / "opamp.sub").read_text(encoding="utf-8")
drawn = {m: float(w) for m, w in re.findall(r"^(M\d) \S+ \S+ \S+ \S+ \w+ W=([0-9.]+)u", sub, re.M)}
for m, hand in (("M1", wl1 * 0.5), ("M3", wl3 * 0.5), ("M5", wl5 * 0.5), ("M6", wl6 * 0.5)):
    v.assert_true(f"netlist: {m} drawn within 1% of the hand width", abs(drawn[m] / hand - 1) < 0.01,
                  f"{drawn[m]} vs {hand:.3f}")
v.assert_true("netlist: W7/W5 = 4 and W5/W8 = 2 (exact mirror ratios)",
              abs(drawn["M7"] / drawn["M5"] - 4) < 1e-12 and abs(drawn["M5"] / drawn["M8"] - 2) < 1e-12)
v.assert_true("netlist: Cc = 1.5 pF and Rz = 625 ohm", "CC nz out 1.5p" in sub and "RZ n1 nz 625" in sub)

# ----------------------------------------------------------------- predictions
a1 = gm1 / ((lamn + lamp) * ID1)
a2 = gm6 / ((lamn + lamp) * I6)
v.check("C1A.a1", a1)
v.check("C1A.a2", a2)
v.check("C1A.a0", a1 * a2)
v.check("C1A.a0db", 20 * math.log10(a1 * a2))

W6, W4, W2, W7 = (drawn[m] * 1e-6 for m in ("M6", "M4" if "M4" in drawn else "M3", "M2" if "M2" in drawn else "M1",
                                             "M7"))
cgs6 = 2 / 3 * W6 * L * Cox + W6 * COV
c1 = cgs6 + W4 * COV + W2 * COV
c2 = CL + W6 * COV + W7 * COV
v.check("C1A.cgs6", cgs6 * 1e15)
v.check("C1A.c1", c1 * 1e15)
v.check("C1A.c2", c2 * 1e12)
p2 = gm6 * Cc / (c1 * c2 + Cc * (c1 + c2))
wu = gm1 / Cc
v.check("C1A.p2", p2 / (2 * math.pi) / 1e6)
v.check("C1A.p2r", p2 / wu)
v.check("C1A.pm1", 90 - math.degrees(math.atan(wu / p2)))
fp2, fg = p2 / (2 * math.pi), gbw
fu = optimize.brentq(lambda f: (fg / f) / math.sqrt(1 + (f / fp2) ** 2) - 1, 1e6, fg)
f_sweep = np.logspace(6, 9, 300_001)
mag = (fg / f_sweep) / np.sqrt(1 + (f_sweep / fp2) ** 2)
v.assert_true("two-pole crossover: sweep agrees with brentq within 0.01%",
              abs(f_sweep[np.argmin(np.abs(mag - 1))] / fu - 1) < 1e-4)
v.check("C1A.fu2", fu / 1e6)
v.check("C1A.pm2", 90 - math.degrees(math.atan(fu / fp2)))


def dvt(vsb):
    return gam * (math.sqrt(PHI + vsb) - math.sqrt(PHI))


v.check("C1A.dvt", dvt(Vov5) * 1e3)
v.check("C1A.vcmmin", VTn + dvt(Vov5) + Vov1 + Vov5)
tail = 0.3
for _ in range(200):
    tail = 0.9 - (VTn + dvt(tail) + Vov1)
tail_b = optimize.brentq(lambda t: t - (0.9 - (VTn + dvt(t) + Vov1)), 0.0, 0.9)
v.assert_true("body-effect iteration: fixed point equals brentq", abs(tail - tail_b) < 1e-12)
v.check("C1A.vtail", tail)
v.check("C1A.tailmar", (tail - Vov5) * 1e3)
vsg3 = abs(P["vto"]) + Vov6
vs_max = optimize.brentq(lambda vs: vs - ((VDD - vsg3 + VTn + dvt(vs)) - (VTn + dvt(vs) + Vov1)), 0.0, 1.8)
v.check("C1A.vcmmax", VDD - vsg3 + VTn + dvt(vs_max))
v.check("C1A.outhi", VDD - Vov6)
v.check("C1A.outlo", Vov5)
gm3 = 2 * ID1 / Vov6
v.check("C1A.vn", math.sqrt(16 * k_B * T / (3 * gm1) * (1 + gm3 / gm1)) * 1e9)
i_total = 20e-6 + I5 + I6
v.check("C1A.pwr", i_total * VDD * 1e6)
v.check("C1A.share6", 100 * I6 / i_total)

# ----------------------------------------------------------------- simulated values, from results.md
res = {k: pub.parts[0].value for k, (pub, _, _) in load_answer_key(HERE / "results.md").items()}
corners = sorted({k.split(".")[1] for k in res if k.count(".") == 2 and k.split(".")[1] != "TT-N"} | {"TT-N"})
v.assert_true("results.md covers eleven corners", len(corners) == 11, str(corners))
for name in ("a0", "ugf", "pm", "srr", "srf", "outlo", "outhi", "m5mar", "pwr"):
    v.check(f"S.tt.{name}", res[f"A.TT-N.{name}"])
v.check("S.tt.vn", res["A.TT-N.vn1m"])
v.check("S.tt.cmrr", res["A.TT-N.cmrr"])
v.check("S.tt.psrr", res["A.TT-N.psrr"])


def col(name):
    return {c: res[f"A.{c}.{name}"] for c in corners}


def worst(name, fn):
    d = col(name)
    c = fn(d, key=d.get)
    return c, d[c]


c_a0, w_a0 = worst("a0", min)
c_ugf, w_ugf = worst("ugf", min)
c_pm, w_pm = worst("pm", min)
srmin = {c: min(res[f"A.{c}.srr"], res[f"A.{c}.srf"]) for c in corners}
c_sr = min(srmin, key=srmin.get)
c_pwr, w_pwr = worst("pwr", max)
c_m5, w_m5 = worst("m5mar", min)
vdd_of = {c: {"C": 1.98, "N": 1.80, "H": 1.62}[c[-1]] for c in corners}
hi_margin = {c: res[f"A.{c}.outhi"] - (vdd_of[c] - 0.25) for c in corners}
c_hi = min(hi_margin, key=hi_margin.get)
lo_margin = {c: 0.25 - res[f"A.{c}.outlo"] for c in corners}
c_lo = min(lo_margin, key=lo_margin.get)
v.assert_true("worst corners as the report states: SS-H, SS-H, FS-N, SS-C, FF-C, SS-C, SS-H, SS-H",
              (c_a0, c_ugf, c_pm, c_sr, c_pwr, c_m5, c_hi, c_lo) == ("SS-H", "SS-H", "FS-N", "SS-C", "FF-C", "SS-C",
                                                                       "SS-H", "SS-H"),
              str((c_a0, c_ugf, c_pm, c_sr, c_pwr, c_m5, c_hi, c_lo)))
v.check("S.min.a0", w_a0)
v.check("S.min.ugf", w_ugf)
v.check("S.min.pm", w_pm)
v.check("S.min.sr", srmin[c_sr])
v.check("S.max.pwr", w_pwr)
v.check("S.min.m5mar", w_m5)
v.check("S.min.outhi", res[f"A.{c_hi}.outhi"])
v.check("S.max.outlo", res[f"A.{c_lo}.outlo"])
v.check("S.req.outhi", vdd_of[c_hi] - 0.25)
v.check("S.mar.a0", w_a0 - 65)
v.check("S.mar.ugf", 100 * (w_ugf / 25 - 1))
v.check("S.mar.pm", w_pm - 60)
v.check("S.mar.sr", srmin[c_sr] - 20)
v.check("S.mar.pwr", 100 * (1 - w_pwr / 500))
v.check("S.mar.m5", w_m5 - 50)
v.check("S.mar.outhi", 1e3 * hi_margin[c_hi])
v.check("S.mar.outlo", 1e3 * lo_margin[c_lo])
v.check("S.err.ssh", 100 * (1 - w_ugf / (gbw * math.sqrt(kp_ss_hot) / 1e6)))
v.check("S.gain.diff", res["A.TT-N.a0"] - 20 * math.log10(a1 * a2))

# every requirement at every corner
for c in corners:
    ok = (res[f"A.{c}.a0"] >= 65 and res[f"A.{c}.ugf"] >= 25 and res[f"A.{c}.pm"] >= 60 and srmin[c] >= 20
          and res[f"A.{c}.pwr"] <= 500 and res[f"A.{c}.m5mar"] >= 50 and hi_margin[c] >= 0 and lo_margin[c] >= 0)
    v.assert_true(f"specification met at {c}", ok)
v.assert_true("TT-only requirements: noise <= 15 nV/rtHz, CMRR and PSRR+ >= 60 dB",
              res["A.TT-N.vn1m"] <= 15 and res["A.TT-N.cmrr"] >= 60 and res["A.TT-N.psrr"] >= 60)

sys.exit(v.finish())
