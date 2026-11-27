#!/usr/bin/env python3
"""Verify the C1 option B design report: recompute the hand design and check the simulated summaries.

- Hand values (C1B.*) are recomputed from first principles. The compensator values are parsed from buck_avg.sub
  and buck_sw.sub, which must agree, so a component change that is not carried into the report fails here.
- The analytic loop model (averaged plant with DCR, switch resistance, ESR and load; exact Type III impedances;
  a single-pole error amplifier) is evaluated over the same 30 corners the netlists simulate.
- Simulated values quoted in the report (SB.*) are read from results.md, whose answer key CI checks against ngspice
  (tools/run_spice.py); worst cases and margins are recomputed, and every requirement is asserted at every corner.
- Second routes: the compensator's pole and zero frequencies from the exact impedance (by root-finding on its
  numerator and denominator) against the closed-form expressions; the ripple bound against a time-domain
  reconstruction of the triangular inductor current.
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

v = Verifier.from_files("C1B", HERE / "design-report.md")
VO, FSW, VRAMP = 1.2, 2e6, 1.0
L0, C0, ESR, DCR, RHS, RLS, VF, TD = 1e-6, 44e-6, 1.5e-3, 20e-3, 0.050, 0.030, 0.7, 10e-9
SI = {"k": 1e3, "Meg": 1e6, "u": 1e-6, "n": 1e-9, "p": 1e-12, "m": 1e-3}


def parse_comp(path):
    text = path.read_text(encoding="utf-8")
    out = {}
    for name in ("R1", "R2", "R3", "C1", "C2", "C3"):
        m = re.search(rf"^{name} \S+ \S+ ([0-9.]+)(Meg|[kunpm]?)\s*$", text, re.M)
        out[name] = float(m.group(1)) * SI.get(m.group(2), 1.0)
    return out


comp = parse_comp(HERE / "buck_avg.sub")
v.assert_true("buck_avg.sub and buck_sw.sub use the same compensator", comp == parse_comp(HERE / "buck_sw.sub"),
              str(comp))
R1, R2, R3, C1, C2, C3 = (comp[k] for k in ("R1", "R2", "R3", "C1", "C2", "C3"))

# ----------------------------------------------------------------- power stage
for code, vin in (("30", 3.0), ("36", 3.6), ("42", 4.2)):
    d = VO / vin
    v.check(f"C1B.d{code}", d)
    v.check(f"C1B.di{code}", VO * (1 - d) / (L0 * FSW))
v.check("C1B.lcalc", VO * (1 - VO / 4.2) / (0.4 * 1.0 * FSW) * 1e6)
di_lm = VO * (1 - VO / 4.2) / (0.8 * L0 * FSW)
v.check("C1B.dilm", di_lm)
v.check("C1B.ival", 1 - di_lm / 2)
v.check("C1B.ipk", 1 + di_lm / 2)
FC_TARGET = 85e3
v.check("C1B.cmin", 0.5 / (2 * math.pi * FC_TARGET * 0.025) * 1e6)
v.check("C1B.dev", 0.5 / (2 * math.pi * FC_TARGET * C0) * 1e3)
ripc = di_lm / (8 * FSW * 0.8 * C0)
ripe = di_lm * ESR
v.check("C1B.ripc", ripc * 1e3)
v.check("C1B.ripe", ripe * 1e3)
v.check("C1B.ripb", (ripc + ripe) * 1e3)
# time-domain check: capacitor charge from a triangular ripple current plus the ESR drop never exceeds the bound
t = np.linspace(0, 1 / FSW, 20001)
d42 = VO / 4.2
tri = np.where(t < d42 / FSW, -di_lm / 2 + di_lm * t / (d42 / FSW),
               di_lm / 2 - di_lm * (t - d42 / FSW) / ((1 - d42) / FSW))
vc = np.cumsum(tri) * (t[1] - t[0]) / (0.8 * C0)
vout = vc - vc.mean() + ESR * tri
v.assert_true("ripple: time-domain peak-to-peak is below the bound and above each term alone",
              max(ripc, ripe) <= np.ptp(vout) <= ripc + ripe, f"{np.ptp(vout) * 1e3:.3f} mV")
f0 = 1 / (2 * math.pi * math.sqrt(L0 * C0))
v.check("C1B.f0", f0 / 1e3)
v.check("C1B.fesr", 1 / (2 * math.pi * ESR * C0) / 1e6)
v.check("C1B.fz", 0.7 * f0 / 1e3)

# ----------------------------------------------------------------- compensator
f = np.logspace(2, 7, 60001)
s = 2j * np.pi * f


def gc_ideal(r2, c1, c2, r3, c3, sv=s):
    zi = 1 / (1 / R1 + 1 / (r3 + 1 / (sv * c3)))
    zf = 1 / (1 / (r2 + 1 / (sv * c1)) + sv * c2)
    return zf / zi


def plant(vin, lf, cf, il, rf, sv=s):
    d = VO / vin
    rs = DCR + (d * RHS + (1 - d) * RLS) * rf
    zc = ESR + 1 / (sv * C0 * cf)
    zp = 1 / (1 / zc + 1 / (VO / il))
    return (vin / VRAMP) * zp / (zp + sv * L0 * lf + rs)


def margins(vin, lf, cf, il, rf, parts, ea=True):
    g = gc_ideal(*parts)
    if ea:
        a = 1e4 / (1 + s / (2 * np.pi * 1e3))
        g = g / (1 + (1 + g) / a)
    tl = plant(vin, lf, cf, il, rf) * g
    mag, ph = np.abs(tl), np.unwrap(np.angle(tl)) * 180 / np.pi
    k = np.where(np.diff(np.sign(mag - 1)))[0][-1]
    j = [q for q in np.where(np.diff(np.sign(ph + 180)) != 0)[0] if f[q] > f[k]]
    return f[k], 180 + ph[k], -20 * np.log10(mag[j[0]]), ph[:k].min()


# exact placement for an 85 kHz crossover at 3.6 V, 0.1 A, ideal amplifier
wz, wp = 2 * math.pi * 0.7 * f0, 2 * math.pi * 1e6


def parts_for(wi):
    csum = 1 / (R1 * wi)
    c1 = csum * (wp - wz) / wp
    c2 = csum - c1
    r3 = R1 / (wp / wz - 1)
    return 1 / (wz * c1), c1, c2, r3, 1 / (wp * r3)


i85 = np.argmin(np.abs(f - FC_TARGET))
wi = optimize.brentq(lambda w: abs((plant(3.6, 1, 1, 0.1, 1) * gc_ideal(*parts_for(w)))[i85]) - 1, 1e2, 1e8)
r2x, c1x, c2x, r3x, c3x = parts_for(wi)
v.check("C1B.r2x", r2x)
v.check("C1B.c1x", c1x * 1e12)
v.check("C1B.c2x", c2x * 1e12)
v.check("C1B.r3x", r3x)
v.check("C1B.c3x", c3x * 1e12)
for name, exact, used, tol in (("R2", r2x, R2, 0.03), ("C1", c1x, C1, 0.03), ("C2", c2x, C2, 0.06),
                               ("R3", r3x, R3, 0.03), ("C3", c3x, C3, 0.03)):
    v.assert_true(f"standard value for {name} within {tol:.0%} of the exact one", abs(used / exact - 1) < tol,
                  f"{used:g} vs {exact:g}")

fz1, fz2 = 1 / (2 * math.pi * R2 * C1), 1 / (2 * math.pi * (R1 + R3) * C3)
fp1, fp2 = 1 / (2 * math.pi * R3 * C3), (C1 + C2) / (2 * math.pi * R2 * C1 * C2)
v.check("C1B.fz1", fz1 / 1e3)
v.check("C1B.fz2", fz2 / 1e3)
v.check("C1B.fp1", fp1 / 1e6)
v.check("C1B.fp2", fp2 / 1e6)
v.check("C1B.fi", 1 / (2 * math.pi * R1 * (C1 + C2)) / 1e3)
# second route: roots of the exact impedance ratio's numerator and denominator polynomials in s
num = np.polymul([R2 * C1, 1], [(R1 + R3) * C3, 1])            # zeros of Zf/Zi
den = np.polymul([R1 * (C1 + C2), 0], np.polymul([R3 * C3, 1], [R2 * C1 * C2 / (C1 + C2), 1]))
zeros = sorted(abs(np.roots(num)) / (2 * math.pi))
poles = sorted(abs(r) / (2 * math.pi) for r in np.roots(den) if abs(r) > 0)
ratio = gc_ideal(R2, C1, C2, R3, C3, sv=2j * math.pi * 3e5) / (
    np.polyval(num, 2j * math.pi * 3e5) / np.polyval(den, 2j * math.pi * 3e5))
v.assert_true("compensator: factored form equals the exact impedance ratio", abs(ratio - 1) < 1e-9, f"{ratio}")
v.assert_true("compensator: polynomial roots equal the closed-form zeros and poles",
              np.allclose(zeros, sorted([fz1, fz2])) and np.allclose(poles, sorted([fp1, fp2])))
hfg = R2 * (R1 + R3) / (R1 * R3)
v.check("C1B.hfg", hfg)
v.check("C1B.hfgdb", 20 * math.log10(hfg))
v.check("C1B.ea1m", 20 * math.log10(abs(1e4 / (1 + 1j * 1e6 / 1e3))), tol=0.5)

corners = [(vin, lf, cf, il, rf) for vin in (3.0, 3.6, 4.2)
           for lf, cf in ((1, 1), (0.8, 0.8), (1.2, 1), (0.8, 1), (1.2, 0.8)) for il, rf in ((0.1, 1.0), (1.0, 1.4))]
final = (R2, C1, C2, R3, C3)
first = (7.68e3, 1.2e-9, 22e-12, 169.0, 910e-12)
res = [margins(*c, final) for c in corners]
v.check("C1B.fclo", min(r[0] for r in res) / 1e3)
v.check("C1B.fchi", max(r[0] for r in res) / 1e3)
v.check("C1B.pmmin", min(r[1] for r in res))
v.check("C1B.gmmin", min(r[2] for r in res))
v.check("C1B.gmid", min(margins(*c, final, ea=False)[2] for c in corners))
v.check("C1B.dip", min(r[3] for r in res), tol=0.5)
nom = margins(3.6, 1, 1, 0.1, 1.0, final)
v.check("C1B.fcn", nom[0] / 1e3)
v.check("C1B.pmn", nom[1])
v.check("C1B.gmn", nom[2])
v.check("C1B.gm1st", min(margins(*c, first)[2] for c in corners))
# all 72 combinations the brief allows: the 30 simulated corners bound them
full = [(vin, lf, cf, il, rf) for vin in (3.0, 3.6, 4.2) for lf in (0.8, 1.0, 1.2) for cf in (0.8, 1.0)
        for il in (0.1, 1.0) for rf in (1.0, 1.4)]
res72 = [margins(*c, final) for c in full]
v.assert_true("72 combinations in the brief's corner set", len(full) == 72)
v.check("C1B.gm72", min(r[2] for r in res72))
v.check("C1B.pm72", min(r[1] for r in res72))
v.assert_true("no omitted combination is worse than the 30 analysed corners",
              min(r[2] for r in res72) >= min(r[2] for r in res) - 1e-9 and min(r[1] for r in res72) >= min(r[1] for r in res) - 1e-9)


def phase_cross(vin, lf, cf, il, rf, parts):
    g = gc_ideal(*parts)
    a = 1e4 / (1 + s / (2 * np.pi * 1e3))
    tl = plant(vin, lf, cf, il, rf) * g / (1 + (1 + g) / a)
    mag, ph = np.abs(tl), np.unwrap(np.angle(tl)) * 180 / np.pi
    k = np.where(np.diff(np.sign(mag - 1)))[0][-1]
    j = [q for q in np.where(np.diff(np.sign(ph + 180)) != 0)[0] if f[q] > f[k]]
    return f[j[0]]


fpc = [phase_cross(*c, final) for c in corners]
v.check("C1B.fpclo", min(fpc) / 1e6)
v.check("C1B.fpchi", max(fpc) / 1e6)
v.check("C1B.eapc", 20 * math.log10(1e4 / math.hypot(1, min(fpc) / 1e3)))
v.assert_true("at the phase crossover the amplifier's open-loop gain is below the network's high-frequency gain",
              20 * math.log10(1e4 / math.hypot(1, min(fpc) / 1e3)) < 20 * math.log10(hfg))
v.check("C1B.fix", 1 / (2 * math.pi * R1 * (c1x + c2x)) / 1e3)
v.check("C1B.tauc", 1 / (2 * math.pi * FC_TARGET) * 1e6)
v.check("C1B.tauz", 1 / (2 * math.pi * 0.7 * f0) * 1e6)
v.check("C1B.qfrac", 1 / (2 * math.pi))
dd = [(1 + 2 * VF / vin) * TD * FSW * 100 for vin in (3.0, 3.6, 4.2)]
v.check("C1B.ddlo", min(dd))
v.check("C1B.ddhi", max(dd))
v.check("C1B.gm1sti", min(margins(*c, first, ea=False)[2] for c in corners))


# ----------------------------------------------------------------- efficiency budget
def budget(iload, vin=3.6):
    d = VO / vin
    di = VO * (1 - d) / (L0 * FSW)
    pc = (d * RHS + (1 - d) * RLS + DCR) * (iload ** 2 + di ** 2 / 12)
    pd = VF * TD * FSW * (abs(iload + di / 2) + abs(iload - di / 2))
    pg = (2 * 2e-9 * FSW + 1e-3) * vin
    pesr = di ** 2 / 12 * ESR
    return pc, pd, pg, 100 * VO * iload / (VO * iload + pc + pd + pg + pesr)


for code, iload in (("01", 0.1), ("05", 0.5), ("10", 1.0)):
    pc, pd, pg, eta = budget(iload)
    v.check(f"C1B.pc{code}", pc * 1e3)
    v.check(f"C1B.pd{code}", pd * 1e3)
    v.check(f"C1B.eta{code}", eta)
v.check("C1B.pg", budget(0.5)[2] * 1e3)
v.check("C1B.pesr", (VO * (1 - VO / 3.6) / (L0 * FSW)) ** 2 / 12 * ESR * 1e3)

# ----------------------------------------------------------------- simulated values, from results.md
r = {k: pub.parts[0].value for k, (pub, _, _) in load_answer_key(HERE / "results.md").items()}
loops = sorted({k.rsplit(".", 1)[0] for k in r if k.startswith("B.L")})
v.assert_true("results.md has 30 loop corners", len(loops) == 30, str(len(loops)))
vos = [r[f"{p}.vo"] for p in loops] + [r[k] for k in r if k.startswith("B.E.") and k.endswith(".vo")] + [r["B.R.vo"]]
vomin = min(vos)
v.check("SB.vomin", vomin)
v.check("SB.vomar", 1e3 * min(vomin - 1.188, 1.212 - max(vos)))
fcs, pms, gms = ([r[f"{p}.{q}"] for p in loops] for q in ("fc", "pm", "gm"))
v.check("SB.fclo", min(fcs))
v.check("SB.fchi", max(fcs))
v.check("SB.fcmar", min(min(fcs) - 50, 200 - max(fcs)))
v.check("SB.pmmin", min(pms))
v.check("SB.pmmar", min(pms) - 45)
v.check("SB.gmmin", min(gms))
v.check("SB.gmmar", min(gms) - 10)
worst_pm = min(loops, key=lambda p: r[f"{p}.pm"])
worst_gm = min(loops, key=lambda p: r[f"{p}.gm"])
v.assert_true("worst phase margin at 3.0 V, L +20%, light load; worst gain margin at 4.2 V, L and C -20%, light load",
              (worst_pm, worst_gm) == ("B.L30.lp.lt", "B.L42.lmcm.lt"), f"{worst_pm}, {worst_gm}")
devs = {k: r[k] for k in r if k.endswith(".dev")}
recs = {k: r[k] for k in r if k.endswith(".rec")}
v.check("SB.devmax", max(devs.values()))
v.assert_true("worst deviation is the 3.0 V, L +20%, C -20% switching step", max(devs, key=devs.get) == "B.W.30.lpcm.dev")
v.check("SB.devnom", max(r[k] for k in ("B.W.30.dev", "B.W.36.dev", "B.W.42.dev")))
v.check("SB.devmar", 36 - max(devs.values()))
v.check("SB.recmax", max(recs.values()))
v.check("SB.recmar", 30 - max(recs.values()))
v.check("SB.rip", r["B.R.rip"])
v.check("SB.ripmar", 10 - r["B.R.rip"])
v.check("SB.eta05", r["B.E.500mA.eta"])
v.check("SB.etamar", r["B.E.500mA.eta"] - 85)
v.check("SB.eta01", r["B.E.100mA.eta"])
v.check("SB.eta10", r["B.E.1000mA.eta"])
v.check("SB.ipk", r["B.R.ipk"])
v.check("SB.ipkmar", 1.5 - r["B.R.ipk"])
v.check("SB.dev36a", r["B.S.36.nom.dev"])
v.check("SB.dev36s", r["B.W.36.dev"])
v.check("SB.devratio", 100 * (r["B.W.36.dev"] / r["B.S.36.nom.dev"] - 1))
v.check("SB.devhand", 100 * (1 - 0.5 / (2 * math.pi * FC_TARGET * C0) * 1e3 / r["B.S.36.nom.dev"]))
v.check("SB.devx", r["B.W.30.lpcm.dev"])
v.check("SB.devxmar", 36 - r["B.W.30.lpcm.dev"])

# every requirement at every simulated corner
v.assert_true("regulation within 1% everywhere", all(1.188 <= x <= 1.212 for x in vos))
v.assert_true("crossover within 50-200 kHz, PM >= 45 deg, GM >= 10 dB at all 30 corners",
              all(50 <= x <= 200 for x in fcs) and min(pms) >= 45 and min(gms) >= 10)
v.assert_true("load step: deviation <= 36 mV and recovery <= 30 us in every simulation",
              max(devs.values()) <= 36 and max(recs.values()) <= 30)
v.assert_true("ripple <= 10 mV, efficiency at 0.5 A >= 85%, peak current <= 1.5 A",
              r["B.R.rip"] <= 10 and r["B.E.500mA.eta"] >= 85 and r["B.R.ipk"] <= 1.5)

sys.exit(v.finish())
