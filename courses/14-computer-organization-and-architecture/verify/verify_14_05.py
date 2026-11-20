#!/usr/bin/env python3
"""Verify every number in chapter 14-05, its problem set and its lab.

Independent routes:
- the control table of §3.3 is read from the lab's Verilog decoder (rv32_decoder.v) and compared with the
  chapter's table, so the text and the tested hardware cannot drift apart;
- immediates are derived by assembling instructions with single-bit immediates through llvm-mc and observing
  which instruction bit each immediate bit lands in, then counting multiplexer sources per output bit;
- path delays are recomputed from the chapter's own delay table (parsed from the Markdown);
- the test program is rebuilt with LLVM and checked against the committed program.hex, data.hex and
  expected.vh; it is executed on the Python RV32I simulator and on the Verilog core in Icarus Verilog, and the
  two register-write traces are compared entry by entry.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(HERE))
from eeverify import Verifier  # noqa: E402
from _rv32 import Sim, sx, tool  # noqa: E402

ROOT = HERE.parent
LAB = ROOT / "labs" / "14-05-lab"
CH = ROOT / "chapters" / "14-05-single-cycle-datapath.md"
sys.path.insert(0, str(LAB))
import make_program  # noqa: E402

v = Verifier.from_files("14-05", CH, ROOT / "solutions" / "14-05-solutions.md", LAB / "README.md")
chap = CH.read_text()

# --------------------------------------------------------------------------- control table: Verilog vs text
dec = (LAB / "rv32_decoder.v").read_text()
rows = {}
for m in re.finditer(r"7'b([01]{7}): begin (.*?)end\s*//\s*(.*)", dec):
    sig = dict(re.findall(r"(\w+) = \d+'[bd](\d+)", m.group(2)))
    rows[m.group(1)] = {k: int(val, 2) if len(val) > 1 and set(val) <= {"0", "1"} and "b" in m.group(2) else int(val) for k, val in sig.items()}
# re-parse values robustly (the regex above may mis-handle binary vs decimal widths)
rows = {}
for m in re.finditer(r"7'b([01]{7}): begin (.*?)end", dec):
    sig = {}
    for name, base, val in re.findall(r"(\w+) = \d+'([bd])(\d+)", m.group(2)):
        sig[name] = int(val, 2 if base == "b" else 10)
    rows[m.group(1)] = sig
defaults = dict(reg_write=0, a_sel=0, b_sel=0, imm_sel=0, mem_write=0, result_src=0, branch=0, jump=0, jalr=0, halt=0, alu_op=0)
ctl = {op: {**defaults, **sig} for op, sig in rows.items()}

table = {}
sec = chap[chap.index("| Opcode | Class | RegWrite"):]
for line in sec.splitlines()[2:]:
    if not line.startswith("| 0") and not line.startswith("| 1"):
        break
    c = [x.strip() for x in line.strip("|").split("|")]
    table[c[0]] = c
ASEL = {"rs1": 0, "PC": 1, "0": 2}
BSEL = {"rs2": 0, "imm": 1}
IMM = {"I": 0, "S": 1, "B": 2, "U": 3, "J": 4}
RES = {"ALU": 0, "memory": 1, "PC + 4": 2}
ALUOP = {"add": 0, "subtract": 1, "funct": 2}
ok = len(table) == 9
for op, c in table.items():
    h = ctl[op]
    exp = dict(reg_write=int(c[2]), mem_write=int(c[6]), branch=int(c[8]), jump=int(c[9]), jalr=int(c[10]))
    if c[3] != "—":
        exp["a_sel"] = ASEL[c[3]]
    if c[4] != "—":
        exp["b_sel"] = BSEL[c[4]]
    if c[5] != "—":
        exp["imm_sel"] = IMM[c[5]]
    if c[7] != "—":
        exp["result_src"] = RES[c[7]]
    if c[11] != "—":
        exp["alu_op"] = ALUOP[c[11]]
    bad = {k: (val, h[k]) for k, val in exp.items() if h[k] != val}
    if bad:
        ok = False
        print(f"  table/decoder mismatch for {op} ({c[1]}): {bad}")
v.assert_true("the chapter's control table matches rv32_decoder.v for all nine opcodes", ok)

SW, JAL, LUI, BR, LW = "0100011", "1101111", "0110111", "1100011", "0000011"
v.check("Ex 14-05.2a", ctl[SW]["reg_write"])
v.check("Ex 14-05.2b", ctl[SW]["mem_write"])
v.check("Ex 14-05.2c", ctl[JAL]["result_src"])
v.check("Ex 14-05.2d", ctl[LUI]["a_sel"])
v.check("Ex 14-05.2e", ctl[BR]["imm_sel"])
v.check("14-05.1a", ctl[LW]["result_src"])
v.check("14-05.1b", ctl[LW]["b_sel"])
v.check("14-05.1c", ctl[BR]["reg_write"])
v.check("14-05.1d", ctl[BR]["branch"])

# --------------------------------------------------------------------------- Example 1 and Problem 3 on the Python simulator
add_w = 0x007302B3
mem = {0x100 + k: (add_w >> 8 * k) & 0xFF for k in range(4)}
mem.update({0x104 + k: b for k, b in enumerate((0x73, 0x00, 0x10, 0x00))})  # ebreak
s = Sim(mem, 0x100, regs={6: 12, 7: 30})
s.run()
v.check("Ex 14-05.1a", 12)
v.check("Ex 14-05.1b", 30)
v.check("Ex 14-05.1c", s.x[5])
v.check("Ex 14-05.1d", s.pc)
lw_w = 0xFFC52303
mem = {0x200 + k: (lw_w >> 8 * k) & 0xFF for k in range(4)}
mem.update({0x204 + k: b for k, b in enumerate((0x73, 0x00, 0x10, 0x00))})
mem.update({0x1FFC + k: (0x12345678 >> 8 * k) & 0xFF for k in range(4)})
s = Sim(mem, 0x200, regs={10: 0x2000})
s.run()
v.check("14-05.3a", (0x2000 - 4) & 0xFFFFFFFF)
v.check("14-05.3b", s.x[6])
v.check("14-05.3c", s.pc)

# --------------------------------------------------------------------------- immediates, by assembling single-bit immediates
mc = tool("llvm-mc")


def enc(line: str) -> int:
    out = subprocess.run([mc, "-triple=riscv32", "-mattr=-c", "-show-encoding"], input=line, capture_output=True, text=True, check=True).stdout
    toks = re.search(r"encoding: \[([^\]]*)\]", out).group(1).split(",")
    return int.from_bytes(bytes(int(t, 16) for t in toks), "little")


TEMPL = {"I": ("addi x0, x0, {}", range(0, 11)), "S": ("sw x0, {}(x0)", range(0, 11)), "B": ("beq x0, x0, {}", range(1, 12)),
         "U": ("lui x0, {}", range(12, 31)), "J": ("jal x0, {}", range(1, 20))}


def source_map(fmt: str) -> dict:
    """Map each immediate output bit to its source: an instruction bit, 'z' (zero) or 's' (sign, bit 31)."""
    tmpl, rng = TEMPL[fmt]
    base = enc(tmpl.format(0))
    m = {}
    for i in rng:
        val = (1 << i) if fmt != "U" else (1 << (i - 12))
        w = enc(tmpl.format(val)) ^ base
        assert bin(w).count("1") == 1, (fmt, i)
        m[i] = w.bit_length() - 1
    top = {"I": 11, "S": 11, "B": 12, "U": 31, "J": 20}[fmt]
    for i in range(32):
        if i not in m:
            m[i] = "s" if i >= top else "z"
    if fmt == "U":
        m[31] = 31
    return m


fmts = {f: source_map(f) for f in "ISBUJ"}
v.assert_true("immediate sign bits all come from instruction bit 31", all(fmts[f][31] in ("s", 31) for f in fmts))
widths = [len({("s" if fmts[f][i] in ("s", 31) else fmts[f][i]) for f in fmts}) for i in range(32)]
v.check("Ex 14-05.5a", sum(widths))
v.check("Ex 14-05.5b", max(widths))
naive = dict(fmts)
naive["B"] = {i: ("z" if i == 0 else 7 + i - 1 if i <= 5 else 25 + i - 6 if i <= 11 else "s") for i in range(32)}
naive["J"] = {i: ("z" if i == 0 else 12 + i - 1 if i <= 19 else "s") for i in range(32)}
nw = [len({("s" if naive[f][i] in ("s", 31) else naive[f][i]) for f in naive}) for i in range(32)]
v.check("Ex 14-05.5c", sum(nw))
v.check("Ex 14-05.5d", max(nw))


def imm_of(word: int, fmt: str) -> int:
    m = fmts[fmt]
    val = 0
    for i in range(32):
        src = m[i]
        bit = (word >> 31) & 1 if src == "s" else 0 if src == "z" else (word >> src) & 1
        val |= bit << i
    return val


v.check("14-05.2a", imm_of(0xFFC52303, "I"))
v.check("14-05.2b", imm_of(0x00512623, "S"))
v.check("14-05.2c", imm_of(0xFE051CE3, "B"))
v.check("14-05.2d", imm_of(0x001000EF, "J"))

# --------------------------------------------------------------------------- timing from the chapter's delay table
dl = {}
for name, val in re.findall(r"^\| ([^|]+?) \| ([\d ps,;]+?) \|$", chap[chap.index("| Element | Delay |"):chap.index("The **load** is")], re.M):
    dl[name.strip()] = [int(x) for x in re.findall(r"(\d+) ps", val)]
t_cq, t_su = dl["Register clock-to-Q ($t_{\\text{clk-q}}$) and setup ($t_{\\text{setup}}$)"]
t_im = dl["Instruction memory read"][0]
t_rf, t_rfsu = dl["Register file read; write setup"]
t_ig, t_mux, t_alu = dl["Immediate generator"][0], dl["Multiplexer"][0], dl["ALU"][0]
t_add, t_cmp = dl["Adder (PC + 4, target)"][0], dl["Branch comparator"][0]
t_dm, t_dmsu = dl["Data memory read; write setup"]


def paths(t_im=t_im, t_dm=t_dm):
    front = t_cq + t_im + max(t_rf, t_ig)
    return dict(R=front + t_mux + t_alu + t_mux + t_rfsu,
                lw=front + t_mux + t_alu + t_dm + t_mux + t_rfsu,
                sw=front + t_mux + t_alu + t_dmsu,
                br=max(t_cq + t_im + t_rf + t_cmp, t_cq + t_im + t_ig + t_add) + t_mux + t_su,
                jal=max(t_cq + t_im + t_ig + t_add + t_mux + t_su, t_cq + t_add + t_mux + t_rfsu),
                jalr=front + t_mux + t_alu + t_mux + t_su,
                lui=t_cq + t_im + t_ig + t_mux + t_alu + t_mux + t_rfsu)


P = paths()
v.check("Ex 14-05.3a", P["R"])
v.check("Ex 14-05.3b", P["lw"])
v.check("Ex 14-05.3c", P["sw"])
v.check("Ex 14-05.3d", P["br"])
v.check("Ex 14-05.3e", P["jal"])
T = max(P.values())
v.check("Ex 14-05.3f", T)
v.check("Ex 14-05.3g", 1e3 / T)
v.assert_true("JALR 530 ps and LUI 480 ps, as Example 6 assumes", P["jalr"] == 530 and P["lui"] == 480)
mix = dict(lw=0.25, sw=0.10, R=0.45, br=0.15, jal=0.05)
avg = sum(f * P[k] for k, f in mix.items())
v.check("Ex 14-05.4a", avg)
v.check("Ex 14-05.4b", 100 * avg / T)
v.check("Ex 14-05.4c", T / avg)

P4 = paths(t_dm=120)
v.check("14-05.4a", P4["lw"])
v.check("14-05.4b", max(P4.values()))
v.check("14-05.4c", 1e3 / max(P4.values()))
v.assert_true("with a 120 ps data memory the next-longest paths are R-type and JALR at 530 ps", sorted(P4.values())[-2] == 530)
P5 = paths(t_im=300)
v.check("14-05.5a", max(P5.values()))
v.check("14-05.5b", 1e3 / max(P5.values()))
mix6 = dict(lw=0.20, sw=0.10, R=0.50, br=0.15, jal=0.05)
avg6 = sum(f * P[k] for k, f in mix6.items())
v.check("14-05.6a", avg6)
v.check("14-05.6b", 100 * avg6 / T)

# Problem 7: a stuck RegWrite, from the encodings and the core's ALU behaviour
sw_w, beq_w = enc("sw x5, 12(x2)"), enc("beq x1, x2, 16")
v.check("14-05.7a", sw_w >> 7 & 31)
v.check("14-05.7b", 0x3FF0 + sx(imm_of(sw_w, "S"), 32))
v.check("14-05.7c", beq_w >> 7 & 31)
v.check("14-05.7d", 5 - 5)
v.assert_true("the core's decoder drives ResultSrc = ALU for stores and ALUOp = subtract for branches",
              ctl[SW]["result_src"] == 0 and ctl[BR]["alu_op"] == 1)

cpi8 = 0.25 * 5 + 0.10 * 4 + 0.45 * 4 + 0.15 * 3 + 0.05 * 3
v.check("14-05.8a", cpi8)
v.check("14-05.8b", cpi8 * 250)
v.check("14-05.8c", cpi8 * 250 / T)

# --------------------------------------------------------------------------- the lab program: rebuild, simulate, run the Verilog
with tempfile.TemporaryDirectory() as td:
    gen = make_program.generate(Path(td))
    same = all((Path(td) / f).read_text() == (LAB / f).read_text() for f in ("program.hex", "data.hex", "expected.vh"))
v.assert_true("committed program.hex, data.hex and expected.vh are up to date", same)
n = gen["count"]
words = gen["words"]
v.check("Ex 14-05.6a", n)
v.check("Ex 14-05.6b", n * T / 1e6)
v.check("Ex 14-05.6c", gen["fib"])
v.assert_true("sum = 115 = sum of 7i - 20", gen["sum"] == sum(make_program.ARRAY) == 115)
v.assert_true("cycles = (6n + 4) + (21F(11) - 18) + 8 = 64 + 1851 + 8", n == 64 + 1851 + 8)

mem = {4 * i + k: (w >> 8 * k) & 0xFF for i, w in enumerate(words) for k in range(4)}
mem.update({0x2000 + 4 * i + k: ((val & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, val in enumerate(make_program.ARRAY) for k in range(4)})
sim = Sim(mem, 0)
tr: list = []
sim.run(trace=tr)
CLS = {0x33: "R", 0x13: "I", 0x03: "lw", 0x23: "sw", 0x63: "br", 0x6F: "jal", 0x67: "jalr", 0x37: "lui", 0x17: "auipc"}
mixc = Counter(CLS[words[pc // 4] & 0x7F] for pc, _ in tr)
v.assert_true("dynamic mix as stated in Example 6", dict(mixc) == dict(I=729, lw=274, sw=266, jal=188, br=188, jalr=178, R=98, lui=2))
dl6 = dict(R=P["R"], I=P["R"], lw=P["lw"], sw=P["sw"], br=P["br"], jal=P["jal"], jalr=P["jalr"], lui=P["lui"], auipc=P["lui"])
var_ns = sum(dl6[k] * c for k, c in mixc.items()) / 1e3
v.check("Ex 14-05.6d", var_ns)
v.check("Ex 14-05.6e", n * T / 1e3 / var_ns)

prog15 = (LAB / "program.s").read_text().replace("    li   a0, 10\n    call fib", "    li   a0, 15\n    call fib")
assert prog15 != (LAB / "program.s").read_text()
with tempfile.TemporaryDirectory() as td:
    (Path(td) / "program.s").write_text(prog15)
    from _rv32 import build
    m15, _, e15, _ = build({"program.s": prog15}, text=0)
    m15.update({0x2000 + 4 * i + k: ((val & 0xFFFFFFFF) >> 8 * k) & 0xFF for i, val in enumerate(make_program.ARRAY) for k in range(4)})
    s15 = Sim(m15, e15)
    n15 = s15.run()
v.assert_true("fib(15) stored as 610", int.from_bytes(bytes(s15.mem[0x104 + k] for k in range(4)), "little") == 610)
v.check("14-05.9a", n15)
v.check("14-05.9b", n15 * T / 1e6)
v.assert_true("20781 = 1923 - 1851 + 20709", n15 == 1923 - 1851 + 21 * 987 - 18)

v.check("14-05.10a", 2 * 2)
v.check("14-05.10b", 2)
v.check("14-05.10c", ((2 * 2 + 2) / 3) ** 2)
v.check("14-05.10d", ((2 * 4 + 4) / 3) ** 2)
v.check("14-05.11a", 0)
v.check("14-05.11b", 2)
e_all = 10 + 6 + 0.1 + 20
e_gate = 10 + 6 + 0.1 + 0.35 * 20
v.check("14-05.12a", e_all)
v.check("14-05.12b", e_gate)
v.check("14-05.12c", 100 * (e_all - e_gate) / e_all)

# Icarus Verilog: run the testbench and compare the register-write trace with the Python simulator
wtrace: list = []
Sim(mem, 0).run(wtrace=wtrace)
if shutil.which("iverilog") and shutil.which("vvp"):
    with tempfile.TemporaryDirectory() as td:
        for f in LAB.glob("*"):
            if f.suffix in (".v", ".hex", ".vh"):
                shutil.copy(f, td)
        srcs = ["rv32_single_tb.v", "rv32_single.v", "rv32_decoder.v", "rv32_immgen.v", "rv32_alu.v", "rv32_regfile.v"]
        subprocess.run(["iverilog", "-g2012", "-o", "sim.vvp", *srcs], cwd=td, check=True)
        out = subprocess.run(["vvp", "-n", "sim.vvp", "+trace"], cwd=td, capture_output=True, text=True, check=True).stdout
        vtrace = [tuple(int(t, 16) if i != 1 else int(t) for i, t in enumerate(line.split())) for line in (Path(td) / "trace.txt").read_text().splitlines()]
    v.assert_true("Verilog testbench prints TEST PASSED", "TEST PASSED" in out and "ERROR" not in out)
    v.assert_true(f"Verilog and Python register-write traces match ({len(wtrace)} writes)", vtrace == wtrace)
    m = re.search(r"sum = (\d+), fib\(10\) = (\d+), (\d+) cycles", out)
    v.check("Lab 14-05.a", int(m.group(3)))
    v.check("Lab 14-05.b", len(vtrace))
    v.check("Lab 14-05.c", int(m.group(1)))
else:
    print("  note: iverilog not found; the trace comparison runs in the CI hdl job (TEST PASSED) only")
    v.check("Lab 14-05.a", n)
    v.check("Lab 14-05.b", len(wtrace))
    v.check("Lab 14-05.c", gen["sum"])
v.check("Lab 14-05.d", n * T / 1e6)

sys.exit(v.finish())
