#!/usr/bin/env python3
"""Verify chapter 16-11 (DSP hardware architectures): examples, text, problems and lab answers.

Routes:
- widths, budgets, critical paths and iteration bounds from their definitions;
- look-ahead recursions simulated here and compared with scipy.signal.lfilter of the original recursion;
- CSD digit counts by an independent search over signed-digit representations;
- CORDIC: gains by direct products, floating-point iterations re-implemented here and compared with math.cos/sin,
  the fixed-point model re-implemented here in integer arithmetic and compared with the lab's model and with the
  committed Verilog vectors;
- energy figures from the 45 nm values (R-208) and the published rates (R-233, R-252).
"""
from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

import numpy as np
from scipy import signal

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "16-11-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import hwarch as hw  # noqa: E402
import make_vectors as mv  # noqa: E402

CH = ROOT / "chapters" / "16-11-dsp-hardware-architectures.md"
v = Verifier.from_files("16-11", CH, ROOT / "solutions" / "16-11-solutions.md", LAB / "README.md")

# ---------------------------------------------------------------------------------------- widths and budgets
v.check("Ex 16-11.1a", 16 + 16)
v.check("Ex 16-11.1b", 16 + 16 + math.ceil(math.log2(256)))
v.check("16-11.1a", 12 + 18)
v.check("16-11.1b", 12 + 18 + math.ceil(math.log2(128)))
v.check("Ex 16-11.2a", 32 * 50e6 / 1e9)
v.check("Ex 16-11.2b", math.ceil(32 * 50e6 / 400e6))
v.check("Ex 16-11.2c", math.ceil(64 * 50e6 / 400e6))
v.check("Ex 16-11.2d", 64 // 2)
v.check("16-11.2a", math.ceil(64 * 100e6 / 500e6))
v.check("16-11.2b", math.ceil(128 * 100e6 / 500e6))
v.check("Txt 16-11.b", 400 / 16)
v.check("Txt 16-11.c", 10e9 / 625e6)
v.check("16-11.6a", 400 / 16)
v.check("16-11.6b", 4 * 400 / 16)

# ---------------------------------------------------------------------------------------- iteration bound, look-ahead
Tm, Ta = 2.0, 0.5
for M, kb, kr in ((1, "Ex 16-11.3a", "Ex 16-11.3b"), (2, "Ex 16-11.3c", "Ex 16-11.3d"), (4, "Ex 16-11.3e", "Ex 16-11.3f")):
    T = (Tm + Ta) / M
    v.check(kb, T)
    v.check(kr, 1000 / T if M < 4 else 1 / T)
v.check("16-11.5a", (Tm + Ta) / 4)
v.check("16-11.5b", 1 / ((Tm + Ta) / 4))
v.check("16-11.4a", max((Tm + 2 * Ta) / 1, (Tm + 2 * Ta) / 2))
v.check("16-11.4b", 1000 / (Tm + 2 * Ta))
rng = np.random.default_rng(16)
x = rng.standard_normal(1000)
ref = signal.lfilter([1], [1, -0.9], x)
y4 = signal.lfilter([1, 0.9, 0.81, 0.729], [1, 0, 0, 0, -0.9**4], x)
v.assert_true("look-ahead by 4 equals the original recursion", np.allclose(ref, y4))
v.assert_true("lab look-ahead by 2 equals the original recursion", np.allclose(ref, hw.iir1_lookahead2(0.9, x)))
v.check("16-11.11a", max(Tm, Ta))
v.check("16-11.11b", 1000 / max(Tm, Ta))
v.check("16-11.11c", 1 + int(math.log2(64)))

# ---------------------------------------------------------------------------------------- CSD


def min_signed_digits(value, frac):
    """Fewest nonzero signed digits representing round(value * 2^frac), by search over digit strings."""
    target = int(round(value * 2**frac))
    nbits = frac + 2
    best = None
    for digits in itertools.product((-1, 0, 1), repeat=nbits):
        if sum(d * 2**k for k, d in enumerate(digits)) == target:
            nz = sum(1 for d in digits if d)
            best = nz if best is None else min(best, nz)
    return best


for val, key in ((0.875, "16-11.3a"), (0.9375, "16-11.3b")):
    nz = min_signed_digits(val, 4)
    v.check(key, nz - 1)
    v.assert_true(f"lab CSD agrees for {val}", hw.csd_adders(val, 4) == nz - 1)

# ---------------------------------------------------------------------------------------- energy
E = {"mul8": 0.2, "add8": 0.03, "mul32": 3.1, "add32": 0.1, "fmul32": 3.7, "fadd32": 0.9, "instr": 70.0}   # pJ, R-208
v.check("Txt 16-11.d", E["mul32"] / E["mul8"])
v.check("16-11.9a", E["mul8"] + E["add8"])
v.check("16-11.9b", E["mul32"] + E["add32"])
v.check("16-11.9c", E["fmul32"] + E["fadd32"])
v.check("16-11.9d", 1300 / (E["mul32"] + E["add32"]))
v.check("16-11.9e", 2600 / (E["mul32"] + E["add32"]))
v.check("Ex 16-11.4a", 64 * E["instr"] / 1000)
v.check("Ex 16-11.4b", 64 * E["instr"] * 1e-12 * 48000 * 1e6)
v.check("Ex 16-11.4c", 64 * (E["mul32"] + E["add32"]))
v.check("Ex 16-11.4d", 64 * (E["mul32"] + E["add32"]) * 1e-12 * 48000 * 1e6)
v.check("Ex 16-11.4e", E["instr"] / (E["mul32"] + E["add32"]))
v.check("16-11.10a", 64 * 48000 / 1e6)
v.check("16-11.10b", 100 * 64 * 48000 / (4 * 100e6))      # R-233: four 16-bit MACs per cycle (M55)
v.check("16-11.10c", 100 * 64 * 48000 / (2 * 100e6))      # R-233: two 16-bit MACs per cycle (M52 single-beat)
v.check("Txt 16-11.e", 128 * 2 * 1.0)                     # R-252: 128 16x16 MACs/cycle at 1.0 GHz
v.check("Txt 16-11.f", 4096 * 2 * 1.0 / 1000)             # R-252: 4096 8-bit MACs/cycle at 1.0 GHz

# ---------------------------------------------------------------------------------------- CORDIC (floating point)


def gain(n):
    p = 1.0
    for i in range(n):
        p *= math.sqrt(1 + 4.0**-i)
    return p


def rot(theta, n):
    xx, yy, zz = 1 / gain(n), 0.0, theta
    for i in range(n):
        d = 1.0 if zz >= 0 else -1.0
        xx, yy, zz = xx - d * yy / 2**i, yy + d * xx / 2**i, zz - d * math.atan(2.0**-i)
    return xx, yy


v.check("Ex 16-11.5a", gain(12))
v.check("16-11.7a", gain(8))
v.check("16-11.7b", gain(16))
v.check("16-11.7c", next(n for n in range(2, 40) if math.atan(2.0 ** -(n - 1)) <= 2.0**-11 + 1e-15))
v.check("Txt 16-11.a", math.degrees(sum(math.atan(2.0**-i) for i in range(60))))
c12, s12 = rot(math.pi / 6, 12)
v.check("Ex 16-11.5b", c12)
v.check("Ex 16-11.5c", c12 - math.cos(math.pi / 6))
v.check("Ex 16-11.5d", s12)
v.check("Ex 16-11.5e", s12 - 0.5)
th = np.linspace(-math.pi / 2, math.pi / 2, 2001)


def worst(n):
    return max(max(abs(rot(t, n)[0] - math.cos(t)), abs(rot(t, n)[1] - math.sin(t))) for t in th)


need = next(n for n in range(8, 25) if worst(n) < 1e-4)
v.check("Lab 16-11.a", need)
v.check("Txt 16-11.g", need)
xv, yv, zv = 3.0, 4.0, 0.0
for i in range(16):
    d = -1.0 if yv >= 0 else 1.0
    xv, yv, zv = xv - d * yv / 2**i, yv + d * xv / 2**i, zv - d * math.atan(2.0**-i)
v.check("16-11.8a", xv / gain(16))
v.check("16-11.8b", math.degrees(zv))

# ---------------------------------------------------------------------------------------- CORDIC (fixed point)
v.check("Ex 16-11.5f", round(30 / 180 * 2**15))
x0 = round(2**14 / gain(14))
v.check("Ex 16-11.5g", x0)
atans = [round(math.atan(2.0**-i) / math.pi * 2**15) for i in range(14)]


def fixed(theta_code, n=14, gx=0, ga=0, rnd=False):
    """Independent fixed-point CORDIC with a quadrant stage; gx guard bits on x, y; ga extra angle bits."""
    th, flip = int(theta_code), False
    if th > 2**14:
        th, flip = th - 2**15, True
    elif th < -(2**14):
        th, flip = th + 2**15, True
    at = [round(math.atan(2.0**-i) / math.pi * 2 ** (15 + ga)) for i in range(n)]
    xx, yy, zz = round(2 ** (14 + gx) / gain(n)), 0, th << ga
    sh = (lambda v_, i: (v_ + (1 << (i - 1))) >> i if (rnd and i > 0) else v_ >> i)
    for i in range(n):
        if zz >= 0:
            xx, yy, zz = xx - sh(yy, i), yy + sh(xx, i), zz - at[i]
        else:
            xx, yy, zz = xx + sh(yy, i), yy - sh(xx, i), zz + at[i]
    if gx:
        xx, yy = (xx + (1 << (gx - 1))) >> gx, (yy + (1 << (gx - 1))) >> gx
    return (-xx, -yy) if flip else (xx, yy)


def worst_fixed(codes, **kw):
    w = 0.0
    for t in codes:
        xx, yy = fixed(t, **kw)
        a = t / 2**15 * math.pi
        w = max(w, abs(xx - math.cos(a) * 2**14), abs(yy - math.sin(a) * 2**14))
    return w


fx, fy = fixed(round(30 / 180 * 2**15))
v.check("Ex 16-11.5h", fx)
v.check("Ex 16-11.5i", fy)
v.assert_true("lab fixed-point model agrees on every test angle", all(fixed(t) == hw.cordic_fixed(t, 14)[:2] for t in mv.angles))
errs = []
for t in mv.angles:
    xx, yy = fixed(t)
    a = t / 2**15 * math.pi
    errs += [abs(xx - math.cos(a) * 2**14), abs(yy - math.sin(a) * 2**14)]
ALL = range(-(2**15), 2**15)
w_all = worst_fixed(ALL)
v.check("Ex 16-11.5j", max(errs))
v.assert_true("the test angles contain the exhaustive worst case", abs(max(errs) - w_all) < 1e-9)
v.check("16-11.12a", w_all)
v.check("16-11.12b", worst_fixed(ALL, rnd=True))
v.check("16-11.12c", worst_fixed(ALL, gx=3))
v.check("16-11.12d", worst_fixed(ALL, gx=3, ga=3))
v.check("16-11.12e", worst_fixed(ALL, gx=3, ga=3, n=16))
v.check("Ex 16-11.5l", math.pi / 2**15 * 2**14)


def angle_path_only(t):
    zz, ang = int(t), 0.0
    for i in range(14):
        d = 1 if zz >= 0 else -1
        zz -= d * atans[i]
        ang += d * math.atan(2.0**-i)
    a = t / 2**15 * math.pi
    return max(abs(math.cos(ang) - math.cos(a)), abs(math.sin(ang) - math.sin(a))) * 2**14


v.check("Ex 16-11.5k", max(angle_path_only(t) for t in range(-(2**14), 2**14 + 1)))
v.assert_true("quadrant stage: 120, 150, 180 degrees are right", all(
    abs(fixed(c)[0] / 2**14 - math.cos(c / 2**15 * math.pi)) < 1e-3 and abs(fixed(c)[1] / 2**14 - math.sin(c / 2**15 * math.pi)) < 1e-3
    for c in (21845, 27307, -32768, 32767)))
v.assert_true("vectors.hex is the current model output", (LAB / "vectors.hex").read_text().split() == mv.build())
v.assert_true("test angles include both ends of the convergence range, zero, both quadrant boundaries and -pi", {-16384, 16384, 0, 16385, -16385, -32768} <= set(mv.angles))

sys.exit(v.finish())
