#!/usr/bin/env python3
"""Verify every number in chapter 14-06, its problem set and its lab.

Independent routes:
- every ```asm listing in the chapter and problems is assembled with LLVM and run on the lab's five-stage
  pipelined Verilog core (Icarus), whose cycles, stalls and flushes are compared with the cycle model
  N + 4 + S + 2T computed from the Python simulator's trace, and whose register-write trace must equal the
  simulator's (_pipe.py);
- loop costs per element are measured as the difference between runs with 10 and 11 elements;
- stage delays and speedups are recomputed from 14-05's delay table; the optimal depth is found by numerical
  minimization as well as by the closed form; branch resolution in ID is evaluated with a separate cost model
  applied to the dynamic trace.
"""
from __future__ import annotations

import math
import sys
import tempfile
from pathlib import Path

from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(HERE))
from eeverify import Verifier, markdown_code_blocks  # noqa: E402
import _pipe  # noqa: E402
from _rv32 import Sim, build  # noqa: E402

ROOT = HERE.parent
LAB = ROOT / "labs" / "14-06-lab"
CH = ROOT / "chapters" / "14-06-pipelining-and-hazards.md"
PR = ROOT / "problems" / "14-06-problems.md"
v = Verifier.from_files("14-06", CH, ROOT / "solutions" / "14-06-solutions.md", LAB / "README.md")
IV = _pipe.have_iverilog()
if not IV:
    print("  note: iverilog not found; Verilog runs are skipped and model counts are used")

HDR = "    .text\n    .globl _start\n"


def asm(path: Path) -> list[str]:
    return [code for lang, code, _, _ in markdown_code_blocks(path) if lang == "asm"]


def checked(code: str, array=None, label="") -> dict:
    r = _pipe.run(code, array)
    if IV:
        v.assert_true(f"{label}: Verilog passes, trace matches, counts equal the model",
                      r["verilog_passed"] and r["trace_match"] and r["cycles"] == r["model_cycles"]
                      and r["v_stalls"] == r["stalls"] and r["v_flushes"] == r["taken"])
    r["c"] = r["cycles"] if IV else r["model_cycles"]
    return r


# --------------------------------------------------------------------------- stage delays (14-05's delays)
cq, su, mem_t, rf, mux, alu = 40, 20, 200, 100, 25, 120
stages = dict(IF=cq + mem_t + mux + su, ID=cq + rf + mux + su, EX=cq + mux + mux + alu + su, MEM=cq + mem_t + mux + su)
T = max(stages.values())
T_single = 730
v.check("Ex 14-06.2a", stages["IF"])
v.check("Ex 14-06.2b", stages["ID"])
v.check("Ex 14-06.2c", stages["EX"])
v.check("Ex 14-06.2d", stages["MEM"])
v.check("Ex 14-06.2e", T)
v.check("Ex 14-06.2f", 1e3 / T)
v.check("Ex 14-06.2g", 5 * T)
v.assert_true("14-05's single-cycle period is 730 ps", (HERE.parent / "chapters" / "14-05-single-cycle-datapath.md").read_text().count("| Ex 14-05.3f | clock period | 730 | ps |") == 1)

v.check("Ex 14-06.1a", 100 + 4)
v.check("Ex 14-06.1b", 104 * T / 1e3)
v.check("Ex 14-06.1c", 100 * T_single / (104 * T))
v.check("Ex 14-06.1d", T_single / T)

# --------------------------------------------------------------------------- examples 3-5 on the Verilog core
cb = asm(CH)
ex3, ex4a, ex4b, ex5c = cb[0], cb[1], cb[2], cb[3]
r = checked(HDR + ex3, label="Example 3")
v.assert_true("Example 3 computes x5 = 7, x8 = 6, x10 = 7 | 6", r["sim"].x[5] == 7 and r["sim"].x[8] == 6 and r["sim"].x[10] == 7)
v.check("Ex 14-06.3a", r["stalls"])
v.check("Ex 14-06.3b", r["c"])
ra = checked(HDR + ex4a.replace("# (a)", ""), [42], "Example 4a")
rb = checked(HDR + ex4b.replace("# (b) the same work, reordered", ""), [42], "Example 4b")
v.assert_true("both versions give x6 = 47", ra["sim"].x[6] == rb["sim"].x[6] == 47)
v.check("Ex 14-06.4a", ra["stalls"])
v.check("Ex 14-06.4b", ra["c"])
v.check("Ex 14-06.4c", rb["stalls"])
v.check("Ex 14-06.4d", rb["c"])

L14 = ROOT / "labs" / "14-02-lab"
TOP = (L14 / "sum_rv32.s").read_text()
ROT = (L14 / "sum_rv32_rot.s").read_text()
HEAD = HDR + "_start:\n    li sp, 0x4000\n    li a0, 0x2000\n    li a1, {n}\n    call sum\n    ebreak\n"
ARR = list(range(1, 13))
per = {}
for key, body in (("top", TOP), ("rot", ROT), ("sched", ex5c)):
    c = {n: checked(HEAD.format(n=n) + body, ARR, f"Example 5 {key} n={n}") for n in (10, 11)}
    v.assert_true(f"Example 5 {key}: sums correct", c[10]["sim"].x[10] == sum(ARR[:10]) and c[11]["sim"].x[10] == sum(ARR[:11]))
    per[key] = c[11]["c"] - c[10]["c"]
v.check("Ex 14-06.5a", per["top"])
v.check("Ex 14-06.5b", per["rot"])
v.check("Ex 14-06.5c", per["sched"])

# --------------------------------------------------------------------------- example 6 and the lab: the full program
sys.path.insert(0, str(LAB))
import make_program  # noqa: E402

with tempfile.TemporaryDirectory() as td:
    gen = make_program.generate(Path(td))
    same = all((Path(td) / f).read_text() == (LAB / f).read_text() for f in ("program.hex", "data.hex", "expected.vh"))
v.assert_true("committed program.hex, data.hex and expected.vh are up to date", same)
rp = checked((LAB / "program.s").read_text(), make_program.ARRAY, "lab program")
v.assert_true("lab program stores 115 and 55", gen["sum"] == 115 and gen["fib"] == 55)
N, S, Tk = rp["instr"], rp["stalls"], rp["taken"]
v.assert_true("N = 1924, S = 10, T = 456 as the chapter states", (N, S, Tk) == (1924, 10, 456))
cyc = rp["c"]
v.check("Ex 14-06.6a", cyc)
v.check("Ex 14-06.6b", cyc / N)
v.check("Ex 14-06.6c", cyc * T / 1e3)
single_ns = 1923 * T_single / 1e3
v.check("Ex 14-06.6d", single_ns / (cyc * T / 1e3))
v.check("Ex 14-06.6e", N + 4 + S)
v.check("Ex 14-06.6f", single_ns / ((N + 4 + S) * T / 1e3))
v.assert_true("taken jumps are 24% of instructions", round(100 * Tk / N) == 24)
v.check("Lab 14-06.a", cyc)
v.check("Lab 14-06.b", S)
v.check("Lab 14-06.c", Tk)
v.check("Lab 14-06.d", cyc * T / 1e6)

# Figure 1's sequence, on the Verilog core: 7 instructions (two li set up x10 and x7), 1 stall, 1 taken branch
FIG = HDR + """_start:
    li   x10, 0x2000
    li   x7, 5
    lw   x5, 0(x10)
    add  x6, x5, x7
    beq  x6, x6, L
    sub  x9, x6, x5
    or   x9, x6, x5
L:  xor  x8, x6, x5
    ebreak
"""
rf = checked(FIG, [42], "Figure 1 sequence")
v.assert_true("Figure 1: 1 stall, 1 flush, 7 + 4 + 1 + 2 = 14 cycles (12 without the two li)", rf["stalls"] == 1 and rf["taken"] == 1 and rf["c"] == 14
              and rf["sim"].x[8] == (47 ^ 42) and rf["sim"].x[9] == 0)

# --------------------------------------------------------------------------- problems
v.check("14-06.1a", 1000 + 4)
v.check("14-06.1b", 1000 + 9)
pb = asm(PR)
p2, p5, p6a, p6b = pb[0], pb[1], pb[2], pb[3]
r = checked(HDR + p2, [42, 0], "Problem 2")
v.assert_true("Problem 2 stores 42 (x7 = 84 - 42) at 0x2004", int.from_bytes(bytes(r["sim"].mem[0x2004 + k] for k in range(4)), "little") == 42)
v.check("14-06.2a", r["stalls"])
v.check("14-06.2b", r["c"])
v.check("14-06.3a", 300 + 30)
v.check("14-06.3b", (1000 + 30) / (300 + 30))
v.check("14-06.4a", 250 + 30)
v.check("14-06.4b", (1000 + 30) / (250 + 30))
r = checked(HDR + p5, label="Problem 5")
v.check("14-06.5a", r["sim"].x[6])
v.check("14-06.5b", 3 + 3)
ra = checked(HDR + p6a.replace("# (a)", ""), [42, 7], "Problem 6a")
rb = checked(HDR + p6b.replace("# (b)", ""), [42, 7], "Problem 6b")
v.assert_true("both versions give x8 = 91", ra["sim"].x[8] == rb["sim"].x[8] == 91)
v.check("14-06.6a", ra["stalls"])
v.check("14-06.6b", ra["c"])
v.check("14-06.6c", rb["stalls"])
v.check("14-06.6d", rb["c"])
tk = 0.20 * 0.60 + 0.05
v.check("14-06.7a", 1 + 2 * tk)
v.check("14-06.7b", 1 + tk)
v.check("14-06.8a", 1 + 0.35)
v.check("14-06.9a", 20 - 1)
v.check("14-06.9b", 1 + 0.01 * 19)

src15 = (LAB / "program.s").read_text().replace("    li   a0, 10\n    call fib", "    li   a0, 15\n    call fib")
g15 = make_program.generate(Path(tempfile.mkdtemp()), source=src15)
v.assert_true("fib(15) run: N = 20782, S = 10", g15["instr"] == 20782 and g15["stalls"] == 10 and g15["fib"] == 610)
v.check("14-06.10a", g15["cycles"])
v.check("14-06.10b", g15["cycles"] / g15["instr"])
if IV:
    r15 = checked(src15, make_program.ARRAY, "fib(15) program")
    v.assert_true("Verilog fib(15) cycles equal the model", r15["cycles"] == g15["cycles"])

tl, tr_, cc = 1000.0, 50.0, 0.1
t = lambda k: (tl / k + tr_) * (1 + cc * k)  # noqa: E731
kstar = math.sqrt(tl / (cc * tr_))
num = minimize_scalar(t, bounds=(1, 100), method="bounded", options=dict(xatol=1e-10))
v.assert_true("numerical minimum agrees with the closed form", abs(num.x - kstar) < 1e-5)
v.check("14-06.11a", kstar)
kbest = min(range(1, 60), key=t)
v.check("14-06.11b", kbest)
v.check("14-06.11c", t(kbest))
v.assert_true("t(14) = 291.43 and t(15) = 291.67", round(t(14), 2) == 291.43 and round(t(15), 2) == 291.67)


def id_cost_per_element(body: str) -> int:
    """Cycles per element if branches resolve in ID (penalty 1; one stall if the instruction just before a
    branch writes one of its sources, two if that instruction is a load)."""
    def cycles(n):
        mem, syms, entry, size = build({"p.s": HEAD.format(n=n) + body}, text=0)
        words = [int.from_bytes(bytes(mem[a + k] for k in range(4)), "little") for a in range(0, size, 4)]
        data = {0x2000 + 4 * i + k: (val >> 8 * k) & 0xFF for i, val in enumerate(ARR) for k in range(4)}
        sim = Sim({**mem, **data}, entry)
        tr: list = []
        sim.run(trace=tr)
        pcs = [pc for pc, _ in tr] + [sim.pc]
        h = make_program.hazard_model(words, pcs)
        extra = 0
        for k in range(1, len(pcs)):
            w, prev = words[pcs[k] // 4], words[pcs[k - 1] // 4]
            if w & 0x7F == 0x63:
                rd = prev >> 7 & 31
                writes = prev & 0x7F in (0x33, 0x13, 0x03, 0x37, 0x17, 0x6F, 0x67)
                if writes and rd and rd in (w >> 15 & 31, w >> 20 & 31):
                    extra += 2 if prev & 0x7F == 0x03 else 1
        return len(pcs) + 4 + h["stalls"] + h["taken"] + extra
    return cycles(11) - cycles(10)


v.check("14-06.12a", per["rot"])
v.check("14-06.12b", id_cost_per_element(ROT))
v.check("14-06.12c", per["sched"])
v.check("14-06.12d", id_cost_per_element(ex5c))

sys.exit(v.finish())
