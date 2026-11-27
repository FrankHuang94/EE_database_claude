#!/usr/bin/env python3
"""Verify the C2 design report: recompute the arithmetic and cost estimates, check the test vectors, prove that the
testbench catches injected bugs, and check the synthesis summaries against results.md.

- Filter facts (H.*) from the coefficients: sums, the magnitude response by direct evaluation and by an FFT, the
  accumulator bound by brute force over worst-case inputs.
- Test facts (T.*) by regenerating the vectors with golden.py and comparing them with the committed files; the
  mutation test copies fir_transposed.v, injects one bug at a time and runs the testbench under Icarus (skipped with
  a clear message only if iverilog is absent; CI's verification job installs it).
- Cost facts (A.*) by canonical-signed-digit recoding, checked against a brute-force minimal signed-digit search.
- Synthesis facts (S.*) from results.md, which synth.py regenerates and CI compares; the targets are asserted.
"""
from __future__ import annotations

import importlib.util
import math
import re
import shutil
import subprocess
import sys
import tempfile
from itertools import product
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import Verifier, load_answer_key  # noqa: E402

v = Verifier.from_files("C2", HERE / "design-report.md")
spec = importlib.util.spec_from_file_location("golden", HERE / "golden.py")
golden = importlib.util.module_from_spec(spec)
spec.loader.exec_module(golden)
H = golden.H

# ----------------------------------------------------------------- filter and arithmetic
v.check("H.sum", sum(H))
v.assert_true("coefficients are symmetric", H == H[::-1])


def mag_db(w):
    return 20 * math.log10(abs(sum(h * np.exp(-1j * w * k) for k, h in enumerate(H))) / 2 ** 15)


v.check("H.db8", mag_db(math.pi / 4))
v.check("H.db4", mag_db(math.pi / 2))
v.check("H.db38", mag_db(3 * math.pi / 4))
spectrum = np.abs(np.fft.fft(np.array(H, dtype=float), 8)) / 2 ** 15
v.assert_true("FFT bins agree with direct evaluation at fs/8 and fs/4",
              abs(20 * math.log10(spectrum[1]) - mag_db(math.pi / 4)) < 1e-9
              and abs(20 * math.log10(spectrum[2]) - mag_db(math.pi / 2)) < 1e-9)
v.assert_true("exact zero at fs/2", sum(h * (-1) ** k for k, h in enumerate(H)) == 0)
v.check("H.gd", (len(H) - 1) / 2)
sumabs = sum(abs(h) for h in H)
v.check("H.sumabs", sumabs)
v.check("H.gmax", sumabs / 2 ** 15)
accmax = sumabs * 2 ** 15 + 2 ** 14
v.check("H.accmax", accmax)
# brute force: the extreme accumulator values over all sign-aligned inputs equal the bound
extremes = [sum(h * x for h, x in zip(H, xs)) + 2 ** 14 for xs in product((-32768, 32767), repeat=8)]
v.assert_true("brute-force extreme of the accumulator is within the bound", max(abs(e) for e in extremes) <= accmax)
v.check("H.accbits", max(abs(e) for e in extremes).bit_length() + 1)          # sign bit included
v.assert_true("a 32-bit signed accumulator suffices; 31 bits do not",
              accmax < 2 ** 31 and max(abs(e) for e in extremes) >= 2 ** 30)

# ----------------------------------------------------------------- test vectors and testbench
samples, cycles = golden.stimulus()
expected = golden.fir(samples)
v.check("T.samples", len(samples))
v.check("T.cycles", len(cycles))
v.check("T.gaps", len(cycles) - len(samples))
v.check("T.sathi", expected.count(32767))
v.check("T.satlo", expected.count(-32768))
stim_now = "".join(f"{a:01x}{d & 0xffff:04x}\n" for a, d in cycles)
exp_now = "".join(f"{y & 0xffff:04x}\n" for y in expected)
v.assert_true("committed stim.hex and expected.hex match a fresh golden.py run",
              (HERE / "stim.hex").read_text() == stim_now and (HERE / "expected.hex").read_text() == exp_now)
tb = (HERE / "fir_tb.v").read_text()
v.assert_true("testbench sizes match the vectors",
              f"NCYC = {len(cycles)}, NOUT = {len(samples)}" in tb)
# impulse response equals the coefficients scaled by 32767/32768 and rounded
v.assert_true("impulse response reads out the coefficients", expected[:8] == [(h * 32767 + 2 ** 14) >> 15 for h in H])

MUTATIONS = [
    ("drop the rounding constant", "s7 <= e0 + 36'sd16384;", "s7 <= e0;"),
    ("remove the saturation", "wire signed [15:0] y = (q > 21'sd32767) ? 16'sh7fff : (q < -21'sd32768) ? 16'sh8000 : q[15:0];",
     "wire signed [15:0] y = q[15:0];"),
    ("advance on idle cycles", "            if (in_valid) begin\n                s7", "            if (1'b1) begin\n                s7"),
]
caught = 0
if shutil.which("iverilog") and shutil.which("vvp"):
    src = (HERE / "fir_transposed.v").read_text()
    for name, old, new in MUTATIONS:
        v.assert_true(f"mutation '{name}' applies", src.count(old) == 1)
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            for f in ("fir_tb.v", "fir_direct.v", "fir_pipelined.v", "stim.hex", "expected.hex"):
                shutil.copy(HERE / f, work / f)
            (work / "fir_transposed.v").write_text(src.replace(old, new))
            subprocess.run(["iverilog", "-g2012", "-o", "sim", "fir_tb.v", "fir_direct.v", "fir_transposed.v",
                            "fir_pipelined.v"], cwd=work, check=True, capture_output=True)
            out = subprocess.run(["vvp", "sim"], cwd=work, capture_output=True, text=True, timeout=300).stdout
            hit = "TEST FAILED" in out and "fir_transposed" in out and "TEST PASSED" not in out
            v.assert_true(f"testbench catches: {name}", hit)
            caught += hit
    v.check("T.mut", caught)
    v.check("T.mutn", len(MUTATIONS))
else:
    sys.exit("verify_c2: iverilog is needed for the mutation test")

# ----------------------------------------------------------------- arithmetic cost by CSD


def csd(n):
    n, digits = abs(n), []
    while n:
        if n & 1:
            d = 2 - (n & 3)
            n -= d
            digits.append(d)
        else:
            digits.append(0)
        n >>= 1
    return digits


def min_signed_digits(n, width=16):
    """Brute force: the fewest nonzero digits in any {-1, 0, 1} representation (CSD is known to be minimal)."""
    best = None
    for k in range(1, 9):
        for pos in __import__("itertools").combinations(range(width + 1), k):
            for signs in product((1, -1), repeat=k):
                if sum(s << p for s, p in zip(signs, pos)) == n:
                    return k
    return best


adders = {}
for c in (169, 750, 3170, 14133):
    nz = sum(1 for d in csd(c) if d)
    v.assert_true(f"CSD digits of {c} reconstruct it and are minimal",
                  sum(d << i for i, d in enumerate(csd(c))) == c and nz == min_signed_digits(c))
    v.check(f"A.csd{c}", nz)
    v.check(f"A.add{c}", nz - 1)
    adders[c] = nz - 1
mul_shared = sum(adders.values())
v.check("A.mult", mul_shared)
v.check("A.muld", 2 * mul_shared)
v.check("A.totd", 2 * mul_shared + 8)
v.check("A.tott", mul_shared + 8)
v.check("A.ratio", (mul_shared + 8) / (2 * mul_shared + 8))

# ----------------------------------------------------------------- synthesis summaries
r = {k: pub.parts[0].value for k, (pub, _, _) in load_answer_key(HERE / "results.md").items()}
for tag, k in (("d", "direct"), ("t", "transposed"), ("p", "pipelined")):
    v.check(f"S.l{tag}", r[f"C2.{k}.logic"])
    v.check(f"S.r{tag}", r[f"C2.{k}.regs"])
    v.check(f"S.a{tag}", r[f"C2.{k}.area"])
    v.check(f"S.d{tag}", r[f"C2.{k}.depth"])
    v.check(f"S.f{tag}", r[f"C2.{k}.fmax"])
v.check("S.pp", r["C2.pipelined.period"])
v.check("S.ffd", r["C2.direct.ffs"])
v.check("S.ratio", r["C2.transposed.logic"] / r["C2.direct.logic"])
v.check("S.logicsave", 100 * (1 - r["C2.transposed.logic"] / r["C2.direct.logic"]))
v.check("S.regcost", r["C2.pipelined.regs"] - r["C2.transposed.regs"])
v.check("S.fmaxmar", 100 * (r["C2.pipelined.fmax"] / 800 - 1))
v.check("S.areamar", 6000 - r["C2.pipelined.area"])
v.check("S.lat", 3 / 0.8)
v.assert_true("only the pipelined version meets both targets",
              r["C2.pipelined.period"] <= 1250 and r["C2.pipelined.area"] <= 6000
              and r["C2.transposed.period"] > 1250 and r["C2.transposed.area"] <= 6000
              and r["C2.direct.period"] > 1250 and r["C2.direct.area"] > 6000)
v.assert_true("fmax column is 1/period", all(abs(r[f"C2.{k}.fmax"] - 1e6 / r[f"C2.{k}.period"]) <= 1.0
                                             for k in ("direct", "transposed", "pipelined")))
v.assert_true("pipelined latency 3 is within the 4-edge limit", "Latency: 3 clock edges" in
              (HERE / "fir_pipelined.v").read_text())

sys.exit(v.finish())
