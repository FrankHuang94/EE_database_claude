#!/usr/bin/env python3
"""Verify every number in chapter 14-03, its problem set and its lab.

Independent routes:
- every ```asm listing in the chapter, problems and solutions is taken verbatim from the Markdown,
  assembled by llvm-mc, linked by ld.lld behind a start-up stub, and executed on the RV32I simulator in
  _rv32.py, which counts instructions, calls and stack depth; results are checked against C semantics;
- the closed-form counts (21F(n+1) - 18, 12n + 2, 3L + 7, 15n + 10, ...) are checked against those runs
  for many n, not only the published ones;
- linking: object files are inspected for their relocations, and the two-file programs are linked with
  and without relaxation to read addresses, sizes and encodings from the ELF;
- structure layouts are compiled by clang for ILP32 (riscv32), LP64 (riscv64) and x86-64 and read back;
- claims about clang 18's output are checked by compiling and running it.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(HERE))
from eeverify import Verifier, markdown_code_blocks  # noqa: E402
from _rv32 import M32, Sim, build, run_function, sx, tool  # noqa: E402

ROOT = HERE.parent
CH = ROOT / "chapters" / "14-03-assembly-and-the-compilation-stack.md"
PR = ROOT / "problems" / "14-03-problems.md"
SO = ROOT / "solutions" / "14-03-solutions.md"
LAB = ROOT / "labs" / "14-03-lab"
v = Verifier.from_files("14-03", CH, SO, LAB / "README.md")


# --------------------------------------------------------------------------- listings from the Markdown
def asm_blocks(*paths: Path) -> dict[str, str]:
    """Map every label defined in an ```asm block to that block's source."""
    out = {}
    for p in paths:
        for lang, code, _, _ in markdown_code_blocks(p):
            if lang != "asm":
                continue
            for lab in re.findall(r"^([A-Za-z_]\w*):", code, re.M):
                out[lab] = code
    return out


BLK = asm_blocks(CH, PR, SO)


def src(*labels: str) -> dict[str, str]:
    """Assembly sources for the blocks defining `labels`. Only the requested entry points are made global:
    llvm-mc emits a branch to a global (preemptible) symbol as a long-branch sequence, which would add an
    instruction to every taken branch, so branch targets inside a block must stay local."""
    files, seen = {}, {}
    for lab in labels:
        seen.setdefault(BLK[lab], []).append(lab)
    for i, (code, labs) in enumerate(seen.items()):
        files[f"blk{i}.s"] = "    .text\n" + "".join(f"    .globl {n}\n" for n in labs) + code
    return files


def words(addr: int, vals: list[int]) -> dict[int, int]:
    return {addr + 4 * i + k: (val & M32) >> 8 * k & 0xFF for i, val in enumerate(vals) for k in range(4)}


def read_words(sim: Sim, addr: int, n: int) -> list[int]:
    return [sx(sim.load(addr + 4 * i, 4), 32) for i in range(n)]


def fibs(n):
    F = [0, 1]
    while len(F) <= n + 1:
        F.append(F[-1] + F[-2])
    return F


ARR = 0x20000

# =========================================================================== Chapter examples
# Ex 1
a0 = [10 * i for i in range(8)]
r = run_function(src("update"), "update", [ARR, 5, 7], data=words(ARR, a0))
v.assert_true("update stores a[4] + k into a[5]", read_words(r["sim"], ARR, 8) == a0[:5] + [a0[4] + 7] + a0[6:])
v.check("Ex 14-03.1a", 4 * 5)
v.check("Ex 14-03.1b", ARR + 4 * 5)
v.check("Ex 14-03.1c", r["count"])

# Ex 2
base = list(range(-50, 50))
ri = run_function(src("inc_idx"), "inc_idx", [ARR, 100, 3], data=words(ARR, base))
rp = run_function(src("inc_ptr"), "inc_ptr", [ARR, 100, 3], data=words(ARR, base))
v.assert_true("both loops add k to every element", read_words(ri["sim"], ARR, 100) == [b + 3 for b in base] == read_words(rp["sim"], ARR, 100))
v.assert_true("index count is 8n + 3 and pointer count 5n + 4 for n = 0..20",
              all(run_function(src("inc_idx"), "inc_idx", [ARR, n, 1], data=words(ARR, [0] * n))["count"] == 8 * n + 3
                  and run_function(src("inc_ptr"), "inc_ptr", [ARR, n, 1], data=words(ARR, [0] * n))["count"] == 5 * n + 4
                  for n in (0, 1, 2, 7, 20)))
v.check("Ex 14-03.2a", ri["count"])
v.check("Ex 14-03.2b", rp["count"])
v.check("Ex 14-03.2c", ri["count"] / rp["count"])

# Ex 3
r = run_function(src("max3"), "max3", [3, 9, 4])
v.check("Ex 14-03.3a", r["depth"])
v.assert_true("max3 saves ra and s0", re.search(r"sw\s+ra", BLK["max3"]) and re.search(r"sw\s+s0", BLK["max3"]) and len(re.findall(r"^\s+sw\s", BLK["max3"], re.M)) == 2)
v.check("Ex 14-03.3b", len(re.findall(r"^\s+sw\s", BLK["max3"], re.M)))
v.check("Ex 14-03.3c", r["count"])
v.check("Ex 14-03.3d", r["value"])
v.assert_true("max3 is correct on many inputs", all(run_function(src("max3"), "max3", list(t))["value"] == max(t)
                                                      for t in ((1, 2, 3), (3, 2, 1), (-5, -9, -7), (0, 0, 0), (2, 9, 9))))

# Ex 4
r = run_function(src("fib"), "fib", [10])
F = fibs(30)
v.check("Ex 14-03.4a", r["value"])
v.check("Ex 14-03.4b", r["calls"]["fib"])
v.check("Ex 14-03.4c", r["count"])
v.check("Ex 14-03.4d", r["depth"])
ok = True
for n in range(0, 16):
    rn = run_function(src("fib"), "fib", [n])
    ok &= rn["value"] == F[n] and rn["count"] == 21 * F[n + 1] - 18 and rn["calls"]["fib"] == 2 * F[n + 1] - 1 \
        and rn["depth"] == 16 * max(n - 1, 0)
v.assert_true("fib: value, 21F(n+1) - 18 instructions, 2F(n+1) - 1 calls, 16(n-1) bytes for n = 0..15", ok)

# Ex 5: two-file link, with and without relaxation
MAIN = "    .text\n    .globl _start\n_start:\n    li   a0, 10\n    call fib\n    ebreak\n"
FIBSRC = src("fib")["blk0.s"]
mc = tool("llvm-mc")


def relocs(source: str, kind="R_RISCV_CALL_PLT") -> int:
    with tempfile.TemporaryDirectory() as td:
        p, o = Path(td) / "x.s", Path(td) / "x.o"
        p.write_text(source)
        subprocess.run([mc, "-triple=riscv32", "-mattr=-c,+relax", "-filetype=obj", str(p), "-o", str(o)], check=True)
        out = subprocess.run([tool("llvm-objdump"), "-r", str(o)], capture_output=True, text=True, check=True).stdout
    return len(re.findall(kind + r"\b", out))


v.check("Ex 14-03.5a", relocs(MAIN))
v.check("Ex 14-03.5b", relocs(FIBSRC))
v.assert_true("each call also carries R_RISCV_RELAX", relocs(MAIN, "R_RISCV_RELAX") == 1 and relocs(FIBSRC, "R_RISCV_RELAX") == 2)
memN, symN, _, sizeN = build({"main.s": MAIN, "fib.s": FIBSRC}, relax=False)
memR, symR, _, sizeR = build({"main.s": MAIN, "fib.s": FIBSRC}, relax=True)
word = lambda mem, a: int.from_bytes(bytes(mem[a + i] for i in range(4)), "little")  # noqa: E731
au, jr = word(memN, 0x10004), word(memN, 0x10008)
v.assert_true("unrelaxed call is auipc ra + jalr ra", au & 0x7F == 0x17 and jr & 0x7F == 0x67 and (au >> 7) & 31 == 1 and (jr >> 7) & 31 == 1)
v.check("Ex 14-03.5c", au >> 12)
v.check("Ex 14-03.5d", sx(jr >> 20, 12))
v.assert_true("unrelaxed target is fib at 0x10010", symN["fib"] == 0x10010 == 0x10004 + (au & 0xFFFFF000) + sx(jr >> 20, 12))
v.check("Ex 14-03.5e", sizeN)
jl = word(memR, 0x10004)
joff = sx((jl >> 31 & 1) << 20 | (jl >> 12 & 0xFF) << 12 | (jl >> 20 & 1) << 11 | (jl >> 21 & 0x3FF) << 1, 21)
v.assert_true("relaxed call is one JAL to fib at 0x1000C", jl & 0x7F == 0x6F and symR["fib"] == 0x1000C == 0x10004 + joff)
v.check("Ex 14-03.5f", joff)
v.check("Ex 14-03.5g", sizeR)
v.check("Ex 14-03.5h", sizeN - sizeR)
v.check("Ex 14-03.5i", run_function(src("fib"), "fib", [10], relax=False)["count"])
v.check("Ex 14-03.5j", run_function(src("fib"), "fib", [10], relax=False)["count"]
        - run_function(src("fib"), "fib", [10])["count"])
fib6 = run_function(src("fib"), "fib", [6])
v.check("Fig 14-03.a", fib6["count"])
v.check("Fig 14-03.b", fib6["calls"]["fib"])
v.check("Fig 14-03.c", fib6["depth"])

# Ex 6 and Problems 10, 14: structure layouts compiled by clang for three ABIs
LAYOUT_C = r"""
#include <stddef.h>
struct A  { char c; int i; short s; double d; };
struct Ar { double d; int i; short s; char c; };
struct P  { char c; long l; };
struct S1 { char a; double b; char c; int d; };
struct S1r { double b; int d; char a; char c; };
struct S2 { short s; char c[3]; };
struct S3 { char *p; char c; };
struct V1 { int id; int flags; double balance; };
struct V2 { int id; short region; int flags; double balance; };
int vals[] = {
  sizeof(struct A), offsetof(struct A, i), offsetof(struct A, s), offsetof(struct A, d),
  sizeof(struct Ar), sizeof(struct P),
  sizeof(struct S1), offsetof(struct S1, b), offsetof(struct S1, c), offsetof(struct S1, d), sizeof(struct S1r),
  sizeof(struct S2), sizeof(struct S3),
  sizeof(struct V1), offsetof(struct V1, flags), offsetof(struct V1, balance),
  sizeof(struct V2), offsetof(struct V2, region), offsetof(struct V2, flags), offsetof(struct V2, balance),
};
"""
KEYS = ["A", "A.i", "A.s", "A.d", "Ar", "P", "S1", "S1.b", "S1.c", "S1.d", "S1r", "S2", "S3", "V1", "V1.flags", "V1.balance",
        "V2", "V2.region", "V2.flags", "V2.balance"]


def layout(target: list[str]) -> dict[str, int]:
    out = subprocess.run([tool("clang")] + target + ["-ffreestanding", "-O0", "-S", "-x", "c", "-", "-o", "-"],
                         input=LAYOUT_C, capture_output=True, text=True, check=True).stdout
    body = out[out.index("vals:"):]
    nums = [int(m) for m in re.findall(r"^\s*\.(?:word|long)\s+(-?\d+)", body, re.M)][:len(KEYS)]
    return dict(zip(KEYS, nums))


L32 = layout(["--target=riscv32", "-march=rv32i", "-mabi=ilp32"])
L64 = layout(["--target=riscv64", "-march=rv64i", "-mabi=lp64"])
LX = layout(["--target=x86_64-linux-gnu"])
v.assert_true("struct A offsets 0, 4, 8, 16 under ILP32", (L32["A.i"], L32["A.s"], L32["A.d"]) == (4, 8, 16))
v.check("Ex 14-03.6a", L32["A.d"])
v.check("Ex 14-03.6b", L32["A"])
v.check("Ex 14-03.6c", L32["Ar"])
v.check("Ex 14-03.6d", L32["P"])
v.check("Ex 14-03.6e", L64["P"])
v.assert_true("x86-64 (LP64) agrees with RV64 on every layout", LX == L64)

# claims about clang 18 (chapter §3.6 and lab)
clang_ver = subprocess.run([tool("clang"), "--version"], capture_output=True, text=True).stdout
CINC = "void inc(int *a, int n, int k) { for (int i = 0; i < n; i++) a[i] += k; }\n"
CFIB = "int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }\n"
c0 = run_function({"inc.c": CINC}, "inc", [ARR, 100, 3], opt="-O0", data=words(ARR, base))
c2 = run_function({"inc.c": CINC}, "inc", [ARR, 100, 3], opt="-O2", data=words(ARR, base))
f0 = run_function({"fib.c": CFIB}, "fib", [10], opt="-O0")
f2 = run_function({"fib.c": CFIB}, "fib", [10], opt="-O2")
v.assert_true("compiled code is correct", read_words(c0["sim"], ARR, 100) == read_words(c2["sim"], ARR, 100) == [b + 3 for b in base]
              and f0["value"] == f2["value"] == 55)
v.assert_true("-O0 executes more than three times as many instructions as -O2 (inc loop)", c0["count"] > 3 * c2["count"])
v.assert_true("-O2 fib makes fewer calls than -O0", f2["calls"]["fib"] < f0["calls"]["fib"] == 177)
if re.search(r"clang version 18\.", clang_ver):
    v.check("Txt 14-03.a", c2["count"])
    v.check("Txt 14-03.b", c0["count"])
    v.assert_true("clang 18: -O2 fib(10) makes 89 calls (about half of 177)", f2["calls"]["fib"] == 89)
    hand15 = run_function(src("fib"), "fib", [15])["count"]
    o0_15 = run_function({"fib.c": CFIB}, "fib", [15], opt="-O0")["count"]
    o2_15 = run_function({"fib.c": CFIB}, "fib", [15], opt="-O2")
    v.assert_true("clang 18, fib(15): -O0 about twice the hand count; -O2 half the calls (987) but about 8% more instructions",
                  1.9 < o0_15 / hand15 < 2.2 and o2_15["calls"]["fib"] == 987 and 1.07 < o2_15["count"] / hand15 < 1.09)
else:
    v.assert_true("clang 18 is required to check Txt 14-03.a and Txt 14-03.b (version-specific counts)", False,
                  clang_ver.splitlines()[0])

# =========================================================================== Problems
v.check("14-03.1a", len(["ra", "s0", "s1", "s2"]))
v.check("14-03.1b", -(-4 * 4 // 16) * 16)

r = run_function(src("pick"), "pick", [ARR, 6], data=words(ARR, list(range(100, 110))))
v.assert_true("pick returns a[3] + a[i]", r["value"] == 103 + 106)
v.check("14-03.2a", 3 * 4)
v.check("14-03.2b", r["count"] - 1)


def mc_count(line: str) -> int:
    out = subprocess.run([mc, "-triple=riscv32", "-mattr=-c", "-show-encoding"], input=line, capture_output=True, text=True, check=True).stdout
    return sum(len(m.group(1).split(",")) for m in re.finditer(r"encoding: \[([^\]]*)\]", out)) // 4


v.check("14-03.3a", mc_count("li a0, 100"))
v.check("14-03.3b", mc_count("li a0, 0x12345678"))
v.check("14-03.3c", mc_count("call f"))
expand = subprocess.run([mc, "-triple=riscv32", "-mattr=-c", "-riscv-no-aliases"],
                        input="not a0, a1\nneg a0, a1\nseqz a0, a1\nbgt a0, a1, 8\nret\n", capture_output=True, text=True, check=True).stdout
v.assert_true("pseudo-instruction expansions as tabulated",
              all(re.search(p, expand) for p in (r"xori\s+a0, a1, -1", r"sub\s+a0, zero, a1", r"sltiu\s+a0, a1, 1", r"blt\s+a1, a0, 8", r"jalr\s+zero, 0\(ra\)")))

v.check("14-03.4a", -(-(3 * 4 + 6 * 4) // 16) * 16)
v.check("14-03.4b", -(-(3 * 4 + 6 * 4) // 16) * 16 - (3 * 4 + 6 * 4))

r1, r2 = run_function(src("abs"), "abs", [-7]), run_function(src("abs"), "abs", [-2147483648])
v.assert_true("abs is correct on a sweep", all(run_function(src("abs"), "abs", [x])["value"] == abs(x) for x in (0, 1, -1, 12345, -98765, 2147483647)))
v.check("14-03.5a", r1["count"])
v.check("14-03.5b", r1["value"])
v.check("14-03.5c", r2["value"])


def cstring(s: str) -> dict[int, int]:
    return {ARR + i: b for i, b in enumerate(s.encode() + b"\0")}


r = run_function(src("strlen"), "strlen", [ARR], data=cstring("hello"))
v.assert_true("strlen('hello') = 5", r["value"] == 5)
v.assert_true("strlen count is 3L + 7 for L = 0..12", all(run_function(src("strlen"), "strlen", [ARR], data=cstring("x" * L))["count"] == 3 * L + 7 for L in range(13)))
v.check("14-03.6a", r["count"])

rb = run_function(src("g", "sum2"), "sum2", [3, 4])
rf = run_function(src("g", "sum2_fixed"), "sum2_fixed", [3, 4])
v.check("14-03.7a", rb["value"])
v.check("14-03.7b", (2 * 3 + 1) + (2 * 4 + 1))
v.assert_true("fixed sum2 returns 16 and is correct on a sweep", rf["value"] == 16 and all(
    run_function(src("g", "sum2_fixed"), "sum2_fixed", [x, y])["value"] == 2 * x + 1 + 2 * y + 1 for x, y in ((0, 0), (-5, 9), (100, -3))))
v.check("14-03.7c", rf["count"])
v.assert_true("fixed frame is 16 bytes", rf["depth"] == 16)

r = run_function(src("sumto"), "sumto", [100])
rl = run_function(src("sumto_loop"), "sumto_loop", [100])
v.assert_true("both sums equal 5050", r["value"] == rl["value"] == 5050)
v.assert_true("recursive count 12n + 2, depth 16n; loop 3n + 4 (n = 0..30)", all(
    run_function(src("sumto"), "sumto", [n])["count"] == 12 * n + 2 and run_function(src("sumto"), "sumto", [n])["depth"] == 16 * n
    and run_function(src("sumto_loop"), "sumto_loop", [n])["count"] == 3 * n + 4 for n in (0, 1, 2, 5, 30)))
v.check("14-03.8a", r["count"])
v.check("14-03.8b", r["depth"])
v.check("14-03.8c", rl["count"])
v.check("14-03.8d", r["count"] / rl["count"])
v.check("14-03.8e", 8 * 1024 // 16)
v.assert_true("sumto(512) uses exactly 8 KiB", run_function(src("sumto"), "sumto", [512])["depth"] == 8192)

r = run_function(src("fib"), "fib", [20])
ri = run_function(src("fibi"), "fibi", [20])
v.assert_true("fib(20) = fibi(20) = 6765", r["value"] == ri["value"] == 6765)
v.assert_true("fibi count 5n + 5 (n = 0..25)", all(run_function(src("fibi"), "fibi", [n])["count"] == 5 * n + 5
                                                   and run_function(src("fibi"), "fibi", [n])["value"] == F[n] for n in (0, 1, 2, 9, 25)))
v.check("14-03.9a", r["calls"]["fib"])
v.check("14-03.9b", r["count"])
v.check("14-03.9c", r["depth"])
v.check("14-03.9d", ri["count"])
v.check("14-03.9e", r["count"] / ri["count"])

v.assert_true("S1 offsets b 8, c 16, d 20", (L32["S1.b"], L32["S1.c"], L32["S1.d"]) == (8, 16, 20))
v.check("14-03.10a", L32["S1"])
v.check("14-03.10b", L32["S1r"])
v.check("14-03.10c", L32["S2"])
v.check("14-03.10d", L32["S3"])
v.check("14-03.10e", L64["S3"])

# Problem 11: the two-file link of the problem, built for real
A_S = """    .text
    .globl _start
_start:
    li   sp, 0x80000
    li   a0, 3
    li   a1, 4
    nop
    call g
    ebreak
    nop
    nop
    nop
"""
B_S = """    .text
    nop
    nop
    .globl g
g:
    add  a0, a0, a1
    ret
"""
mN, sN, _, _ = build({"a.s": A_S, "b.s": B_S}, relax=False)
mR, sR, _, _ = build({"a.s": A_S, "b.s": B_S}, relax=True)
v.assert_true("a.o text is 40 bytes with the AUIPC at offset 0x10", word(mN, 0x10010) & 0x7F == 0x17
              and len(re.findall(r"^\s+(?:li|nop|call|ebreak)\b", A_S, re.M)) + 1 == 10)
v.check("14-03.11a", sN["g"])
au, jr = word(mN, 0x10010), word(mN, 0x10014)
v.check("14-03.11b", au >> 12)
v.check("14-03.11c", sx(jr >> 20, 12))
v.check("14-03.11d", au)
v.check("14-03.11e", jr)
v.check("14-03.11f", sR["g"])
jl = word(mR, 0x10010)
v.check("14-03.11g", sx((jl >> 31 & 1) << 20 | (jl >> 12 & 0xFF) << 12 | (jl >> 20 & 1) << 11 | (jl >> 21 & 0x3FF) << 1, 21))
v.check("14-03.11h", jl)
sims = [Sim(m, 0x10000) for m in (mN, mR)]
for sm in sims:
    sm.run()
v.assert_true("both linked versions return 3 + 4", all(sm.x[10] == 7 for sm in sims))

# Problem 12: caller- against callee-saved, measured
LOOPS = """
h:      addi a0, a0, 1
        ret
loopT:  addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s1, 8(sp)
        li   s1, 100
        li   t3, 7              # the value lives in a temporary
1:      sw   t3, 4(sp)          # caller saves it around the call
        call h
        lw   t3, 4(sp)
        addi s1, s1, -1
        bnez s1, 1b
        mv   a0, t3
        lw   ra, 12(sp)
        lw   s1, 8(sp)
        addi sp, sp, 16
        ret
loopS:  addi sp, sp, -16
        sw   ra, 12(sp)
        sw   s1, 8(sp)
        sw   s0, 4(sp)          # callee-saved: saved once
        li   s1, 100
        li   s0, 7
2:      call h
        addi s1, s1, -1
        bnez s1, 2b
        mv   a0, s0
        lw   ra, 12(sp)
        lw   s1, 8(sp)
        lw   s0, 4(sp)          # and restored once
        addi sp, sp, 16
        ret
"""
srcL = {"loops.s": "    .text\n    .globl loopT\n    .globl loopS\n" + LOOPS}
rT, rS = run_function(srcL, "loopT"), run_function(srcL, "loopS")
base_count = run_function(srcL, "loopS")["count"] - 2  # the same loop with no saving at all
v.assert_true("both keep the value", rT["value"] == rS["value"] == 7)
v.check("14-03.12a", rT["count"] - base_count)
v.check("14-03.12b", rS["count"] - base_count)
HT = "    .text\n    .globl ht\nht:  add t0, a0, a0\n    add t1, t0, a0\n    add t2, t1, a0\n    mv a0, t2\n    ret\n"
HS = ("    .text\n    .globl hs\nhs:  addi sp, sp, -16\n    sw s0, 12(sp)\n    sw s1, 8(sp)\n    sw s2, 4(sp)\n"
      "    add s0, a0, a0\n    add s1, s0, a0\n    add s2, s1, a0\n    mv a0, s2\n"
      "    lw s0, 12(sp)\n    lw s1, 8(sp)\n    lw s2, 4(sp)\n    addi sp, sp, 16\n    ret\n")
rht, rhs = run_function({"ht.s": HT}, "ht", [5]), run_function({"hs.s": HS}, "hs", [5])
v.assert_true("both h versions compute 4x", rht["value"] == rhs["value"] == 20)
v.check("14-03.12c", rhs["count"] - rht["count"])

# Problem 13
r = run_function(src("inc_o0"), "inc_o0", [ARR, 100, 3], data=words(ARR, base))
v.assert_true("inc_o0 is correct", read_words(r["sim"], ARR, 100) == [b + 3 for b in base])
v.assert_true("inc_o0 count is 15n + 10 (n = 0..20)", all(run_function(src("inc_o0"), "inc_o0", [ARR, n, 1], data=words(ARR, [0] * n))["count"] == 15 * n + 10
                                                          for n in (0, 1, 5, 20)))
v.check("14-03.13a", r["count"])
v.check("14-03.13b", r["count"] / rp["count"])
loop_body = BLK["inc_o0"].split("1:")[1].split("2:")[0]
v.check("14-03.13c", len(re.findall(r"^\s*(?:lw|sw)\s", loop_body, re.M)))
v.check("14-03.13d", len(re.findall(r"^\s*(?:lw|sw)\s", BLK["inc_ptr"].split("loop2:")[1], re.M)))

v.assert_true("version 1 layout 0, 4, 8; size 16", (L32["V1.flags"], L32["V1.balance"], L32["V1"]) == (4, 8, 16) and L32["V2.region"] == 4)
v.check("14-03.14a", L32["V2.flags"])
v.check("14-03.14b", L32["V2.balance"])
v.check("14-03.14c", L32["V2"])

# =========================================================================== Lab
labfib = (LAB / "fib.s").read_text()
v.assert_true("lab fib.s matches the chapter listing", re.sub(r"\s+", " ", labfib.split("fib:", 1)[1]).strip()
              == re.sub(r"\s+", " ", BLK["fib"].split("fib:", 1)[1]).strip())
r = run_function({"fib.s": labfib}, "fib", [15])
v.check("Lab 14-03.a", r["value"])
v.check("Lab 14-03.b", r["count"])
v.check("Lab 14-03.c", r["calls"]["fib"])
v.check("Lab 14-03.d", r["depth"])
v.assert_true("lab count equals 21F(16) - 18", r["count"] == 21 * F[16] - 18)

sys.exit(v.finish())
