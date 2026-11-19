#!/usr/bin/env python3
"""Verify every number published in chapter 06-10, its solutions and its lab handout.

Independent routes. The text applies the ideal rules (virtual short, no input current) and closed
forms such as -R2/R1, 1 + R2/R1, (1 + G)/(4t) and 1 + 2R/R_G. This script instead solves every
circuit with a sparse-tableau solver in which each op-amp is a VCVS of very large (or the stated
finite) gain, finds worst-case common-mode gains by searching all tolerance corners, builds error
budgets from explicit offset and bias-current sources (individually, with every sign combination,
and with the physical signs), handles saturation piecewise and with a smooth tanh model, and obtains
the Monte Carlo CMRR statistics from the exact Irwin-Hall distribution of a sum of uniform errors.
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

C_DIR = HERE.parent
v = Verifier.from_files("06-10", C_DIR / "chapters" / "06-10-ideal-op-amp.md",
                        C_DIR / "solutions" / "06-10-solutions.md", C_DIR / "labs" / "06-10-lab" / "README.md")

BIG = 1e10  # "ideal" open-loop gain: relative error about 1e-9, far below any published digit


def tableau(elements):
    """Sparse tableau with dependent sources. Each element is (name, kind, a, b, value) where
    branch current flows a -> b through the element and branch voltage is v_a - v_b:
      R: v = value * i;  I: i = value;  V: v = value;
      G: i = g * (v_c - v_d) with value = (c, d, g);   E: v = mu * (v_c - v_d) with value = (c, d, mu);
      F: i = beta * i_ctrl with value = (ctrl, beta);  H: v = r * i_ctrl with value = (ctrl, r)."""
    nodes = sorted({n for _, _, a, b, _ in elements for n in (a, b) if n != "0"})
    nn, nb = len(nodes), len(elements)
    idx = {n: k for k, n in enumerate(nodes)}
    bidx = {el[0]: k for k, el in enumerate(elements)}
    A = np.zeros((nn, nb))
    for k, (_, _, a, b, _) in enumerate(elements):
        if a != "0":
            A[idx[a], k] += 1.0
        if b != "0":
            A[idx[b], k] -= 1.0
    size = nn + 2 * nb
    M, z = np.zeros((size, size)), np.zeros(size)
    M[:nn, nn:nn + nb] = A
    M[nn:nn + nb, :nn] = -A.T
    M[nn:nn + nb, nn + nb:] = np.eye(nb)

    def node_col(n):
        return None if n == "0" else idx[n]

    for k, (_, kind, _, _, val) in enumerate(elements):
        r = nn + nb + k
        ci, cv = nn + k, nn + nb + k
        if kind == "R":
            M[r, cv], M[r, ci] = 1.0, -val
        elif kind == "I":
            M[r, ci], z[r] = 1.0, val
        elif kind == "V":
            M[r, cv], z[r] = 1.0, val
        elif kind in "GE":
            c, d, gain = val
            M[r, ci if kind == "G" else cv] = 1.0
            for node, sgn in ((c, -1.0), (d, 1.0)):
                if node_col(node) is not None:
                    M[r, node_col(node)] += sgn * gain
        elif kind in "FH":
            ctrl, gain = val
            M[r, ci if kind == "F" else cv] = 1.0
            M[r, nn + bidx[ctrl]] -= gain
        else:
            raise ValueError(kind)
    x = np.linalg.solve(M, z)
    e = {"0": 0.0, **{n: x[idx[n]] for n in nodes}}
    cur = {el[0]: x[nn + k] for k, el in enumerate(elements)}
    vol = {el[0]: x[nn + nb + k] for k, el in enumerate(elements)}
    return e, cur, vol



def opamp(name, plus, minus, out, A=BIG):
    """Op-amp as a VCVS from out to ground: v_out = A (v_plus - v_minus)."""
    return (name, "E", out, "0", (plus, minus, A))


def db(x):
    return 20 * math.log10(x)


# Units throughout: kΩ, V, mA (so 1 µA = 1e-3 mA, 1 nA = 1e-6 mA, 1 pA = 1e-9 mA).

# ================================================================ theory
v.check("T 06-10.a", db(1e8))
v.check("T 06-10.b", 10 ** (160 / 20))
v.check("T 06-10.c", db(101 / (4 * 0.01)))
v.check("T 06-10.d", db(101 / (4 * 0.0001)))


# ================================================================ examples
def inverting(vin, R1, R2, A=BIG):
    return [("Vi", "V", "i", "0", vin), ("R1", "R", "i", "n", R1), ("R2", "R", "n", "o", R2),
            opamp("U", "0", "n", "o", A)]


e1, c1, _ = tableau(inverting(0.5, 10.0, 47.0))
v.check("Ex 06-10.1a", e1["o"] / 0.5)
v.check("Ex 06-10.1b", e1["o"])
v.check("Ex 06-10.1c", 1e3 * c1["R1"])            # mA -> µA
v.check("Ex 06-10.1d", 0.5 / c1["R1"])             # kΩ
v.assert_true("Ex 1: same current in R2", abs(c1["R2"] - c1["R1"]) < 1e-9)


def dac(code):
    bits = [5.0 * int(ch) for ch in code]          # b2 b1 b0
    els = [("Rf", "R", "n", "o", 10.0), opamp("U", "0", "n", "o")]
    for k, (vb, R) in enumerate(zip(bits, (10.0, 20.0, 40.0))):
        els += [(f"V{k}", "V", f"b{k}", "0", vb), (f"R{k}", "R", f"b{k}", "n", R)]
    return tableau(els)[0]["o"]


v.check("Ex 06-10.2a", dac("101"))
v.check("Ex 06-10.2b", dac("111"))
v.check("Ex 06-10.2c", dac("001"))
# a load on the output changes nothing (zero output resistance)
v.assert_true("Ex 2: load-independent", abs(tableau([("Rf", "R", "n", "o", 10.0), opamp("U", "0", "n", "o"),
              ("V0", "V", "b", "0", 5.0), ("R0", "R", "b", "n", 10.0), ("RL", "R", "o", "0", 0.1)])[0]["o"] + 5) < 1e-6)


def diffamp(v1, v2, R1, R2, R3, R4, A=BIG):
    els = [("V1", "V", "a", "0", v1), ("V2", "V", "b", "0", v2), ("R1", "R", "a", "n", R1),
           ("R2", "R", "n", "o", R2), ("R3", "R", "b", "p", R3), ("R4", "R", "p", "0", R4), opamp("U", "p", "n", "o", A)]
    return tableau(els)[0]["o"]


def worst_cm(R1, R2, R3, R4, t, vcm):
    """Largest |output| for a pure common-mode input over all 16 tolerance corners."""
    return max(abs(diffamp(vcm, vcm, R1 * (1 + s1 * t), R2 * (1 + s2 * t), R3 * (1 + s3 * t), R4 * (1 + s4 * t)))
               for s1, s2, s3, s4 in itertools.product((-1, 1), repeat=4))


vd3 = 1.249e-3
out3 = diffamp(1.25 - vd3 / 2, 1.25 + vd3 / 2, 1.0, 100.0, 1.0, 100.0)
cm3 = worst_cm(1.0, 100.0, 1.0, 100.0, 0.01, 1.25)
acm3 = cm3 / 1.25
v.check("Ex 06-10.3a", 1e3 * out3)
v.check("Ex 06-10.3b", 1e3 * cm3)
v.check("Ex 06-10.3c", acm3)
v.check("Ex 06-10.3d", 100 / acm3)
v.check("Ex 06-10.3e", db(100 / acm3))
v.check("Ex 06-10.3f", 101 / (4 * 0.01))
v.check("Ex 06-10.3g", 100 * cm3 / out3)
# the two candidate corners named in the text: (R2/R1 high, R4/R3 low) and its opposite
hi = abs(diffamp(1.25, 1.25, 1.0 * 0.99, 100.0 * 1.01, 1.0 * 1.01, 100.0 * 0.99))
lo = abs(diffamp(1.25, 1.25, 1.0 * 1.01, 100.0 * 0.99, 1.0 * 0.99, 100.0 * 1.01))
v.assert_true("Ex 3: the worst corner is R2/R1 high, R4/R3 low", abs(hi - cm3) < 1e-12 and lo < hi)
v.check("Ex 06-10.3h", 1e3 * lo)


def noninv_errors(vs=0.0, vos=0.0, ibm=0.0, ibp=0.0, Rs=10.0, R1=1.0, R2=100.0):
    """Non-inverting amplifier with source resistance Rs. vos sits in series with the + input
    (the op-amp senses v_p + vos); ibm, ibp are currents flowing OUT of the - and + pins (mA)."""
    els = [("Vs", "V", "s", "0", vs), ("Rs", "R", "s", "p", Rs), ("Vos", "V", "q", "p", vos),
           ("R1", "R", "n", "0", R1), ("R2", "R", "n", "o", R2),
           ("Ibm", "I", "0", "n", ibm), ("Ibp", "I", "0", "p", ibp), opamp("U", "q", "n", "o")]
    return tableau(els)[0]["o"]


v.check("Ex 06-10.4a", noninv_errors(vs=0.01))
budget = {}
for part, (vos, ib) in {"LM358": (7e-3, 250e-6), "OPA187": (10e-6, 350e-9)}.items():
    t_vos = noninv_errors(vos=vos)
    t_ibm = noninv_errors(ibm=ib)
    t_ibp = noninv_errors(ibp=ib)
    worst = max(abs(noninv_errors(vos=a * vos, ibm=b * ib, ibp=c * ib))
                for a, b, c in itertools.product((-1, 1), repeat=3))
    budget[part] = (t_vos, t_ibm, t_ibp, worst)
    v.assert_true(f"Ex 4 {part}: corner search = sum of magnitudes",
                  abs(worst - (abs(t_vos) + abs(t_ibm) + abs(t_ibp))) < 1e-9)
lm, opa = budget["LM358"], budget["OPA187"]
v.check("Ex 06-10.4b", 1e3 * lm[0])
v.check("Ex 06-10.4c", -1e3 * lm[1])          # current out of the - pin lowers the output
v.check("Ex 06-10.4d", 1e3 * lm[2])
v.check("Ex 06-10.4e", 1e3 * lm[3])
v.check("Ex 06-10.4f", 1e3 * opa[0])
v.check("Ex 06-10.4g", -1e3 * opa[1])
v.check("Ex 06-10.4h", 1e3 * opa[2])
v.check("Ex 06-10.4i", 1e3 * opa[3])
v.check("Ex 06-10.4j", 7e-3 / 10e-6)
v.check("Ex 06-10.4k", 3e-3 / 1e-6)
v.check("Ex 06-10.4l", 100 * lm[3] / 1.01)
v.check("Ex 06-10.4m", 100 * opa[3] / 1.01)
signed = noninv_errors(vos=7e-3, ibm=250e-6, ibp=250e-6)  # both currents out of the pins, positive offset
v.check("Ex 06-10.4n", 1e3 * signed)
v.check("Lab 06-10.i", 1e3 * max(abs(signed), abs(noninv_errors(vos=-7e-3, ibm=250e-6, ibp=250e-6))))


def inamp(vm, vp, R=25.0, RG=0.5, rd=(10.0, 10.0, 10.0, 10.0)):
    """Three-op-amp in-amp: A1 buffers v_-, A2 buffers v_+; difference stage R1 (A1 side), R2 feedback,
    R3 (A2 side), R4 to ground. Returns (out, oa, ob)."""
    r1, r2, r3, r4 = rd
    els = [("Vm", "V", "im", "0", vm), ("Vp", "V", "ip", "0", vp),
           opamp("A1", "im", "j1", "oa"), opamp("A2", "ip", "j2", "ob"),
           ("Ra", "R", "oa", "j1", R), ("RG", "R", "j1", "j2", RG), ("Rb", "R", "j2", "ob", R),
           ("R1", "R", "oa", "n", r1), ("R2", "R", "n", "o", r2), ("R3", "R", "ob", "p", r3), ("R4", "R", "p", "0", r4),
           opamp("A3", "p", "n", "o")]
    e = tableau(els)[0]
    return e["o"], e["oa"], e["ob"]


out5, oa5, ob5 = inamp(1.25 - vd3 / 2, 1.25 + vd3 / 2)
cm5 = max(abs(inamp(1.25, 1.25, rd=tuple(10.0 * (1 + s * 0.01) for s in signs))[0])
          for signs in itertools.product((-1, 1), repeat=4))
acm5 = cm5 / 1.25
v.check("Ex 06-10.5a", (ob5 - oa5) / vd3)
v.check("Ex 06-10.5b", 1e3 * out5)
v.check("Ex 06-10.5c", acm5)
v.check("Ex 06-10.5d", 1e3 * cm5)
# The exact value is 101/0.0202020... = 4999.5, a rounding tie at the units digit; published as 5000.
v.check("Ex 06-10.5e", 101 / acm5, tol=0.51)
v.check("Ex 06-10.5f", db(101 / acm5))
v.check("Ex 06-10.5g", 100 * cm5 / out5)
v.assert_true("Ex 5: first stage passes common mode with gain 1",
              abs(inamp(1.25, 1.25)[1] - 1.25) < 1e-8 and abs(inamp(1.25, 1.25)[2] - 1.25) < 1e-8)

# ================================================================ solutions
e, c, _ = tableau(inverting(0.1, 4.7, 100.0))
v.check("06-10.1a", e["o"] / 0.1)
v.check("06-10.1b", e["o"])
v.check("06-10.1c", 0.1 / c["R1"])

R2_p2 = brentq(lambda r2: tableau([("Vi", "V", "p", "0", 1.0), ("R1", "R", "n", "0", 1.0), ("R2", "R", "n", "o", r2),
                                   opamp("U", "p", "n", "o")])[0]["o"] - 25.0, 1.0, 100.0, xtol=1e-12)
v.check("06-10.2a", R2_p2)
v.check("06-10.2b", tableau([("Vi", "V", "p", "0", 0.2), ("R1", "R", "n", "0", 1.0), ("R2", "R", "n", "o", R2_p2),
                             opamp("U", "p", "n", "o")])[0]["o"])

els3 = [("Rf", "R", "n", "o", 20.0), opamp("U", "0", "n", "o")]
for k, (vk, R) in enumerate(((1.0, 10.0), (-0.5, 20.0), (2.0, 40.0))):
    els3 += [(f"V{k}", "V", f"x{k}", "0", vk), (f"R{k}", "R", f"x{k}", "n", R)]
v.check("06-10.3a", tableau(els3)[0]["o"])

v.check("06-10.4a", diffamp(2.00, 2.05, 10.0, 100.0, 10.0, 100.0))
o4b = diffamp(2.00, 2.05, 10.0, 100.0, 10.0, 101.0)
o4d = diffamp(2.00, 2.00, 10.0, 100.0, 10.0, 101.0)
v.check("06-10.4b", o4b)
v.check("06-10.4c", 1e3 * (o4b - 0.5))
v.check("06-10.4d", 1e3 * o4d)
v.check("06-10.4e", o4d / 2.0)
v.check("06-10.4f", 10 / (o4d / 2.0))
v.check("06-10.4g", db(10 / (o4d / 2.0)))
v.check("06-10.4h", (1 + 10) / 0.01)


def tia(iin, ib=0.0, Rf=500.0):
    """Transimpedance amplifier: iin flows into the virtual ground; ib flows out of the - pin."""
    els = [("Ii", "I", "0", "n", iin), ("Ib", "I", "0", "n", ib), ("Rf", "R", "n", "o", Rf), opamp("U", "0", "n", "o")]
    return tableau(els)[0]["o"]


v.check("06-10.5a", tia(5e-3))
v.check("06-10.5b", abs(1e3 * tia(0.0, ib=250e-6)))        # 250 nA = 250e-6 mA; V -> mV
v.check("06-10.5c", abs(1e6 * tia(0.0, ib=350e-9)))        # 350 pA = 350e-9 mA; V -> µV

v.check("06-10.6a", tableau([("Vs", "V", "s", "0", 1.0), ("Rs", "R", "s", "a", 100.0), ("Rin", "R", "a", "0", 10.0)])[0]["a"])
fol = [("Vs", "V", "s", "0", 1.0), ("Rs", "R", "s", "p", 100.0), opamp("U", "p", "o", "o"), ("Rin", "R", "o", "0", 10.0)]
v.check("06-10.6b", tableau(fol)[0]["o"])
fol[2] = opamp("U", "p", "o", "o", 1e5)
v.check("06-10.6c", tableau(fol)[0]["o"])

v.check("06-10.7a", tableau(inverting(1.0, 1.0, 10.0))[0]["o"])
os7 = [("R1", "R", "n", "0", 1.0), ("R2", "R", "n", "o", 10.0), ("Vos", "V", "q", "0", 2e-3), opamp("U", "q", "n", "o")]
v.check("06-10.7b", 1e3 * tableau(os7)[0]["o"])


def bias8(R3, ibm, ibp, R1=10.0, R2=100.0):
    """Inverting amplifier with its input grounded; bias currents ibm, ibp flow INTO the pins (mA)."""
    els = [("R1", "R", "n", "0", R1), ("R2", "R", "n", "o", R2), ("R3", "R", "p", "0", R3),
           ("Ibm", "I", "n", "0", ibm), ("Ibp", "I", "p", "0", ibp), opamp("U", "p", "n", "o")]
    return tableau(els)[0]["o"]


v.check("06-10.8a", 1e3 * bias8(1e-12, 100e-6, 100e-6))
R3_8 = 1 / (1 / 10.0 + 1 / 100.0)
v.check("06-10.8b", R3_8)
v.check("06-10.8c", 1e3 * max(abs(bias8(R3_8, 100e-6, 100e-6 + s * 10e-6)) for s in (-1, 1)))


def sat_inverting(vin, R1=10.0, R2=47.0, vmax=12.0):
    """Piecewise-ideal: linear solution if it fits inside the rails, otherwise clamp and solve the divider."""
    vo = -R2 / R1 * vin
    if abs(vo) <= vmax:
        return vo, 0.0
    vo = math.copysign(vmax, vo)
    vm = tableau([("Vi", "V", "i", "0", vin), ("R1", "R", "i", "n", R1), ("R2", "R", "n", "o", R2),
                  ("Vo", "V", "o", "0", vo)])[0]["n"]
    return vo, vm


lim = brentq(lambda x: abs(tableau(inverting(x, 10.0, 47.0))[0]["o"]) - 12.0, 0.1, 10.0, xtol=1e-12)
v.check("06-10.9a", lim)
vo9, vm9 = sat_inverting(3.0)
v.check("06-10.9b", vo9)
v.check("06-10.9c", vm9)
v.check("06-10.10a", brentq(lambda rg: (inamp(0.0, 1e-3, R=24.7, RG=rg)[2] - inamp(0.0, 1e-3, R=24.7, RG=rg)[1]) / 1e-3 - 1000,
                            1e-3, 1.0, xtol=1e-14) * 1e3)                       # kΩ -> Ω
v.check("06-10.10b", brentq(lambda rg: (inamp(0.0, 1e-3, R=24.7, RG=rg)[2] - inamp(0.0, 1e-3, R=24.7, RG=rg)[1]) / 1e-3 - 100,
                            1e-2, 10.0, xtol=1e-14) * 1e3)
cmrr10 = (1 + 1) / (4 * 0.0002)
v.check("06-10.10c", cmrr10)
cm10 = max(abs(inamp(1.0, 1.0, rd=tuple(10.0 * (1 + s * 0.0002) for s in signs))[0])
           for signs in itertools.product((-1, 1), repeat=4))
v.assert_true("10: corner search agrees with (1 + G)/(4t) to 0.1%", abs(1 / cm10 / cmrr10 - 1) < 1e-3)
v.check("06-10.10d", cmrr10 * 100)
v.check("06-10.10e", db(cmrr10 * 100))

g11 = tableau(inverting(1.0, 1.0, 100.0, A=1e4))[0]["o"]
v.check("06-10.11a", g11)
v.check("06-10.11b", 100 * (1 - g11 / -100))
v.assert_true("11: closed form", abs(g11 + 100 / (1 + 101 / 1e4)) < 1e-9)

v.check("06-10.12a", 1e-3 * 50e-3 * 1e6)
v.check("06-10.12b", 100 * 10e-6 / 50e-6)
v.check("06-10.12c", 7e-3 / 50e-6)

# ---- Problem 06-10.13: comparator, solved as a nonlinear circuit (tanh-limited op-amp, no feedback)
thr = tableau([("V", "V", "s", "0", 5.0), ("Rt", "R", "s", "m", 30.0), ("Rb", "R", "m", "0", 20.0)])[0]["m"]
v.check("06-10.13a", thr)
comp = lambda vin: 12.0 * math.tanh(1e5 * (vin - thr) / 12.0)       # noqa: E731
v.check("06-10.13b", comp(1.8))
v.check("06-10.13c", comp(2.3))
v.check("06-10.13d", 2.3 - thr)
v.check("06-10.13e", 1e6 * brentq(lambda d: 1e5 * d - 12.0, 0.0, 1.0))

# ================================================================ lab
ga = tableau(inverting(1.0, 10.0, 47.0, A=1e3))[0]["o"]
v.check("Lab 06-10.a", ga)
v.check("Lab 06-10.b", 100 * (1 - ga / -4.7))
v.check("Lab 06-10.c", 1e6 * (1 - tableau(inverting(1.0, 10.0, 47.0, A=1e5))[0]["o"] / -4.7))


def noninv_gain(R1, R2, A):
    return tableau([("Vi", "V", "p", "0", 1.0), ("R1", "R", "n", "0", R1), ("R2", "R", "n", "o", R2),
                    opamp("U", "p", "n", "o", A)])[0]["o"]


v.check("Lab 06-10.d", noninv_gain(1.0, 100.0, 1e3))
v.check("Lab 06-10.e", lim)


def tanh_vm(vin, A=1e6, R1=10.0, R2=47.0, vs=12.0):
    f = lambda vm: (vin - vm) / R1 + (vs * math.tanh(-A * vm / vs) - vm) / R2
    return brentq(f, -5, 5, xtol=1e-15)


v.check("Lab 06-10.f", tanh_vm(3.0))
v.assert_true("Lab: v- tiny in the linear region", abs(tanh_vm(2.0)) < 1e-4)  # 12.6 µV with the tanh model


def irwin_hall_cdf(y, n=4):
    """CDF of the sum of n independent U(0, 1) variables."""
    return sum((-1) ** k * math.comb(n, k) * (y - k) ** n for k in range(int(math.floor(y)) + 1)) / math.factorial(n)


def abs_sum_quantile(q, t=0.01):
    """Quantile of |e1 - e2 - e3 + e4| for e_i iid U(-t, t): S = t (2Y - 4) with Y Irwin-Hall(4)."""
    m = brentq(lambda m: irwin_hall_cdf(2 + m) - irwin_hall_cdf(2 - m) - q, 0, 2, xtol=1e-14)
    return 2 * t * m


# To first order A_cm = G (delta_b - delta_a)/(1 + G) with delta_a = e2 - e1, delta_b = e4 - e3, so CMRR = (1 + G)/|S|.
v.check("Lab 06-10.g", db(101 / abs_sum_quantile(0.5)))
v.check("Lab 06-10.h", db(101 / abs_sum_quantile(0.99)))
A_req = brentq(lambda A: (1 - noninv_gain(1.0, 999.0, A) / 1000) - 1e-3, 1e4, 1e8, xtol=1)
v.check("Lab 06-10.j", A_req)
cm_k = worst_cm(1.0, 100.0, 1.0, 100.0, 0.001, 1.0)
v.check("Lab 06-10.k", db(100 / cm_k))
v.check("Lab 06-10.l", 1e3 * noninv_errors(ibp=250e-6, Rs=1 / (1 / 1.0 + 1 / 100.0)))

v.finish()
