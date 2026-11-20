#!/usr/bin/env python3
"""Verify every number in chapter 14-02, its problem set and its lab.

Independent routes:
- an RV32I encoder and decoder written from the format table, each word cross-checked against the
  LLVM assembler (llvm-mc) and each decode cross-checked against the LLVM disassembler;
- encodability limits (immediate, branch and jump ranges) by asking the assembler to accept or
  reject boundary cases;
- constant building by executing LUI + ADDI on a small RV32I instruction-set simulator, and by
  comparing with the assembler's own expansion of the `li` pseudo-instruction;
- code sizes from the .text sections of object files assembled by llvm-mc for four ISAs;
- dynamic instruction counts by running the LLVM-assembled RISC-V machine code on the simulator, and
  by interpreting the A64 and x86-64 listings instruction by instruction;
- multi-word addition by generating and executing the RV32I sequence on random operands;
- present values by discounting each year's cash flow, and the break-even volume by root finding.
"""
from __future__ import annotations

import glob
import math
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

ROOT = HERE.parent
LAB = ROOT / "labs" / "14-02-lab"
v = Verifier.from_files("14-02", ROOT / "chapters" / "14-02-isa-risc-v-arm-x86.md",
                        ROOT / "solutions" / "14-02-solutions.md", LAB / "README.md")


def tool(name: str) -> str:
    found = [g for pat in ("/usr/lib/llvm-*/bin/", "/opt/homebrew/opt/llvm/bin/", "/usr/local/opt/llvm/bin/")
             for g in sorted(glob.glob(pat + name))]
    path = shutil.which(name) or next(iter(found), None)
    if path is None:
        sys.exit(f"verify_14_02: {name} not found (install LLVM, e.g. `apt-get install llvm`)")
    return path


MC, SIZE, OBJCOPY = tool("llvm-mc"), tool("llvm-size"), tool("llvm-objcopy")
M32 = 0xFFFFFFFF

# --------------------------------------------------------------------------- the encoder (format table)
REG = {f"x{i}": i for i in range(32)}
REG.update(zero=0, ra=1, sp=2, gp=3, tp=4, t0=5, t1=6, t2=7, s0=8, s1=9, a0=10, a1=11, a2=12, a3=13,
           a4=14, a5=15, a6=16, a7=17)
OP = dict(OP=0x33, OPIMM=0x13, LOAD=0x03, STORE=0x23, BRANCH=0x63, JAL=0x6F, JALR=0x67, LUI=0x37,
          AUIPC=0x17)


def enc_r(f7, rs2, rs1, f3, rd, op):
    return f7 << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op


def enc_i(imm, rs1, f3, rd, op):
    assert -2048 <= imm <= 2047
    return (imm & 0xFFF) << 20 | rs1 << 15 | f3 << 12 | rd << 7 | op


def enc_s(imm, rs2, rs1, f3, op):
    assert -2048 <= imm <= 2047
    i = imm & 0xFFF
    return (i >> 5) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | (i & 0x1F) << 7 | op


def enc_b(imm, rs2, rs1, f3, op):
    assert imm % 2 == 0 and -4096 <= imm <= 4094
    i = imm & 0x1FFF
    return ((i >> 12) & 1) << 31 | ((i >> 5) & 0x3F) << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 \
        | ((i >> 1) & 0xF) << 8 | ((i >> 11) & 1) << 7 | op


def enc_u(imm20, rd, op):
    return (imm20 & 0xFFFFF) << 12 | rd << 7 | op


def enc_j(imm, rd, op):
    assert imm % 2 == 0 and -(1 << 20) <= imm <= (1 << 20) - 2
    i = imm & 0x1FFFFF
    return ((i >> 20) & 1) << 31 | ((i >> 1) & 0x3FF) << 21 | ((i >> 11) & 1) << 20 \
        | ((i >> 12) & 0xFF) << 12 | rd << 7 | op


R_OPS = dict(add=(0, 0), sub=(0x20, 0), sll=(0, 1), slt=(0, 2), sltu=(0, 3), xor=(0, 4), srl=(0, 5),
             sra=(0x20, 5), **{"or": (0, 6), "and": (0, 7)})
I_OPS = dict(addi=0, slti=2, sltiu=3, xori=4, ori=6, andi=7)
BR = dict(beq=0, bne=1, blt=4, bge=5, bltu=6, bgeu=7)


def asm(line: str) -> int:
    """Encode one RV32I instruction from text with the functions above (independent of LLVM)."""
    m, _, rest = line.strip().partition(" ")
    a = [t.strip() for t in rest.split(",")]
    r = lambda t: REG[t]  # noqa: E731
    if m in R_OPS:
        f7, f3 = R_OPS[m]
        return enc_r(f7, r(a[2]), r(a[1]), f3, r(a[0]), OP["OP"])
    if m in I_OPS:
        return enc_i(int(a[2], 0), r(a[1]), I_OPS[m], r(a[0]), OP["OPIMM"])
    if m in ("slli", "srli", "srai"):
        sh = int(a[2], 0)
        top = 0x20 if m == "srai" else 0
        return enc_i(top << 5 | sh, r(a[1]), 1 if m == "slli" else 5, r(a[0]), OP["OPIMM"])
    if m in ("lw", "sw", "jalr"):
        off, base = re.fullmatch(r"(-?\w+)\((\w+)\)", a[1]).groups()
        if m == "lw":
            return enc_i(int(off, 0), r(base), 2, r(a[0]), OP["LOAD"])
        if m == "jalr":
            return enc_i(int(off, 0), r(base), 0, r(a[0]), OP["JALR"])
        return enc_s(int(off, 0), r(a[0]), r(base), 2, OP["STORE"])
    if m in BR:
        return enc_b(int(a[2], 0), r(a[1]), r(a[0]), BR[m], OP["BRANCH"])
    if m in ("lui", "auipc"):
        return enc_u(int(a[1], 0), r(a[0]), OP[m.upper()])
    if m == "jal":
        return enc_j(int(a[1], 0), r(a[0]), OP["JAL"])
    raise ValueError(line)


# --------------------------------------------------------------------------- the decoder
def sx(x, bits):
    return x - (1 << bits) if x >> (bits - 1) & 1 else x


def decode(w: int) -> dict:
    op, rd, f3, rs1, rs2, f7 = w & 0x7F, w >> 7 & 31, w >> 12 & 7, w >> 15 & 31, w >> 20 & 31, w >> 25
    d = dict(op=op, rd=rd, f3=f3, rs1=rs1, rs2=rs2, f7=f7)
    if op in (OP["OPIMM"], OP["LOAD"], OP["JALR"]):
        d.update(fmt="I", imm=sx(w >> 20, 12))
    elif op == OP["STORE"]:
        d.update(fmt="S", imm=sx((w >> 25) << 5 | (w >> 7 & 31), 12))
    elif op == OP["BRANCH"]:
        imm = (w >> 31 & 1) << 12 | (w >> 7 & 1) << 11 | (w >> 25 & 0x3F) << 5 | (w >> 8 & 0xF) << 1
        d.update(fmt="B", imm=sx(imm, 13))
    elif op in (OP["LUI"], OP["AUIPC"]):
        d.update(fmt="U", imm=w >> 12)
    elif op == OP["JAL"]:
        imm = (w >> 31 & 1) << 20 | (w >> 12 & 0xFF) << 12 | (w >> 20 & 1) << 11 | (w >> 21 & 0x3FF) << 1
        d.update(fmt="J", imm=sx(imm, 21))
    elif op == OP["OP"]:
        d.update(fmt="R", imm=None)
    else:
        raise ValueError(hex(w))
    return d


# --------------------------------------------------------------------------- LLVM helpers
def mc_encodings(src: str, triple="riscv32", mattr="-c") -> list[list[str]]:
    args = [MC, f"-triple={triple}", "-show-encoding"] + ([f"-mattr={mattr}"] if mattr else [])
    out = subprocess.run(args, input=src, capture_output=True, text=True, check=True).stdout
    return [[t.strip() for t in m.group(1).split(",")] for m in re.finditer(r"encoding: \[([^\]]*)\]", out)]


def mc_word(line: str) -> int:
    (e,) = mc_encodings(line)
    return int.from_bytes(bytes(int(t, 16) for t in e), "little")


def mc_accepts(line: str, triple="riscv32", mattr="-c") -> bool:
    args = [MC, f"-triple={triple}", f"-mattr={mattr}", "-show-encoding"]
    return subprocess.run(args, input=line, capture_output=True, text=True).returncode == 0


def mc_disasm(word: int) -> str:
    src = " ".join(f"0x{b:02x}" for b in word.to_bytes(4, "little"))
    out = subprocess.run([MC, "-triple=riscv32", "-mattr=-c", "-disassemble"], input=src,
                         capture_output=True, text=True, check=True).stdout
    return " ".join(out.split("\n")[-2].split()) if out.strip() else ""


def assemble(path: Path, triple: str, mattr: str | None = None) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        obj, raw = Path(td) / "a.o", Path(td) / "a.bin"
        args = [MC, f"-triple={triple}", "-filetype=obj", str(path), "-o", str(obj)]
        if mattr:
            args.insert(2, f"-mattr={mattr}")
        subprocess.run(args, check=True)
        size = subprocess.run([SIZE, "-A", str(obj)], capture_output=True, text=True, check=True).stdout
        n = int(next(ln.split()[1] for ln in size.splitlines() if ln.startswith(".text")))
        subprocess.run([OBJCOPY, "-O", "binary", "--only-section=.text", str(obj), str(raw)], check=True)
        code = raw.read_bytes()
    assert len(code) == n
    return code


# --------------------------------------------------------------------------- an RV32I simulator
HALT = 0xFFFFFFF0


def run_rv32(code: bytes, regs: dict | None = None, mem: dict | None = None, base=0x1000, limit=10**6):
    """Execute RV32I machine code (no compressed instructions) until a jump to HALT. Returns (x, n)."""
    x = [0] * 32
    for k, val in (regs or {}).items():
        x[REG[k]] = val & M32
    x[1] = HALT
    mem = dict(mem or {})
    for i, b in enumerate(code):
        mem[base + i] = b
    rd_word = lambda a: int.from_bytes(bytes(mem.get(a + i, 0) for i in range(4)), "little")  # noqa: E731
    pc, n = base, 0
    while pc != HALT:
        assert n < limit
        w = rd_word(pc)
        d = decode(w)
        op, imm, a, b = d["op"], d["imm"], x[d["rs1"]], x[d["rs2"]]
        s = lambda u: sx(u, 32)  # noqa: E731
        nxt, res = pc + 4, None
        if op == OP["LUI"]:
            res = imm << 12
        elif op == OP["AUIPC"]:
            res = pc + (imm << 12)
        elif op == OP["JAL"]:
            res, nxt = pc + 4, pc + imm
        elif op == OP["JALR"]:
            res, nxt = pc + 4, (a + imm) & ~1
        elif op == OP["BRANCH"]:
            take = {0: a == b, 1: a != b, 4: s(a) < s(b), 5: s(a) >= s(b), 6: a < b, 7: a >= b}[d["f3"]]
            nxt = pc + imm if take else nxt
        elif op == OP["LOAD"]:
            assert d["f3"] == 2
            res = rd_word((a + imm) & M32)
        elif op == OP["STORE"]:
            for i in range(4):
                mem[(a + imm + i) & M32] = b >> 8 * i & 0xFF
        elif op in (OP["OPIMM"], OP["OP"]):
            f3, alt = d["f3"], d["f7"] == 0x20
            y = imm & M32 if op == OP["OPIMM"] else b
            sh = y & 31
            res = {0: (a - y) if (alt and op == OP["OP"]) else (a + y), 1: a << sh, 2: int(s(a) < s(y)),
                   3: int(a < y), 4: a ^ y, 5: (s(a) >> sh) if alt else (a >> sh), 6: a | y, 7: a & y}[f3]
        if res is not None and d["rd"]:
            x[d["rd"]] = res & M32
        pc, n = nxt & M32, n + 1
    return x, n


# --------------------------------------------------------------------------- A64 and x86-64 interpreters
def listing(path: Path, comment: str) -> tuple[list, dict]:
    prog, labels = [], {}
    for ln in path.read_text().splitlines():
        ln = ln.split(comment)[0].strip()
        if not ln:
            continue
        if ln.endswith(":"):
            labels[ln[:-1]] = len(prog)
            continue
        m, _, rest = ln.partition(" ")
        prog.append((m, [t.strip() for t in re.split(r",(?![^\[]*\])", rest)] if rest else []))
    return prog, labels


def run_a64(path: Path, arr: list[int]):
    prog, lab = listing(path, "//")
    mem = {0x1000 + 4 * i: v_ for i, v_ in enumerate(arr)}
    R = {"x0": 0x1000, "x1": len(arr)}
    get = lambda r: 0 if r in ("wzr", "xzr") else R.get("x" + r[1:], 0)  # noqa: E731
    put = lambda r, val: R.__setitem__("x" + r[1:], val & (M32 if r[0] == "w" else 2**64 - 1))  # noqa: E731
    pc, n = 0, 0
    while True:
        m, a = prog[pc]
        n += 1
        pc += 1
        if m == "ret":
            return sx(R["x0"] & M32, 32), n
        if m == "mov":
            put(a[0], get(a[1]))
        elif m in ("cbz", "cbnz"):
            if (get(a[0]) == 0) == (m == "cbz"):
                pc = lab[a[1]]
        elif m == "b":
            pc = lab[a[0]]
        elif m == "ldr":  # post-index: ldr wD, [xN], #imm
            base = a[1].strip("[]")
            put(a[0], mem[get(base)])
            put(base, get(base) + int(a[2].lstrip("#")))
        elif m == "add":
            put(a[0], get(a[1]) + get(a[2]))
        elif m == "sub":
            put(a[0], get(a[1]) - int(a[2].lstrip("#")))
        else:
            raise ValueError(m)


def run_x86(path: Path, arr: list[int]):
    prog, lab = listing(path, "#")
    mem = {0x1000 + 4 * i: v_ for i, v_ in enumerate(arr)}
    R, zf = {"rdi": 0x1000, "rsi": len(arr), "rax": 0}, False
    pc, n = 0, 0
    while True:
        m, a = prog[pc]
        n += 1
        pc += 1
        if m == "ret":
            return sx(R["rax"] & M32, 32), n
        if m == "xorl":
            R["rax"] = 0
        elif m == "testq":
            zf = R[a[0][1:]] == 0
        elif m in ("je", "jne"):
            if zf == (m == "je"):
                pc = lab[a[0]]
        elif m == "jmp":
            pc = lab[a[0]]
        elif m == "addl":  # addl (%rdi), %eax
            R["rax"] = (R["rax"] + mem[R["rdi"]]) & M32
        elif m == "addq":
            R[a[1][1:]] += int(a[0].lstrip("$"))
        elif m == "decq":
            R[a[0][1:]] -= 1
            zf = R[a[0][1:]] == 0
        else:
            raise ValueError(m)


# =========================================================================== Chapter examples
# Ex 1 and 2: encode and decode, cross-checked with LLVM
w_add, w_sub = asm("add x5, x6, x7"), asm("sub x5, x6, x7")
v.check("Ex 14-02.1a", w_add)
v.check("Ex 14-02.1b", w_sub)
v.assert_true("add/sub encodings match llvm-mc", w_add == mc_word("add x5, x6, x7") and w_sub == mc_word("sub x5, x6, x7"))
v.assert_true("add stored little-endian as B3 02 73 00", w_add.to_bytes(4, "little") == bytes([0xB3, 0x02, 0x73, 0x00]))
d = decode(0xFE051CE3)
v.check("Ex 14-02.2a", d["imm"])
v.assert_true("0xFE051CE3 is BNE x10, x0", d["fmt"] == "B" and d["f3"] == 1 and d["rs1"] == 10 and d["rs2"] == 0)
v.assert_true("LLVM disassembles 0xFE051CE3 as bnez a0, -8", mc_disasm(0xFE051CE3) == "bnez a0, -8")


# Ex 3: constants
def split_const(C):
    hi = ((C + 0x800) >> 12) & 0xFFFFF
    lo = sx((C - (hi << 12)) & 0xFFF, 12)
    return hi, lo


def build_and_run(C):
    hi, lo = split_const(C)
    prog = ([asm(f"lui x5, {hi}")] if hi else []) + [asm(f"addi x5, {'x5' if hi else 'x0'}, {lo}"), asm("jalr x0, 0(x1)")]
    x, _ = run_rv32(b"".join(w.to_bytes(4, "little") for w in prog))
    return x[5], len(prog) - 1


hi, lo = split_const(0xDEADBEEF)
v.check("Ex 14-02.3a", lo)
v.check("Ex 14-02.3b", hi)
v.check("Ex 14-02.3c", asm(f"lui x5, {hi}"))
v.check("Ex 14-02.3d", asm(f"addi x5, x5, {lo}"))
v.assert_true("LUI/ADDI for 0xDEADBEEF match llvm-mc", asm(f"lui x5, {hi}") == mc_word("lui x5, 0xDEADC") and asm(f"addi x5, x5, {lo}") == mc_word("addi x5, x5, -273"))
v.assert_true("simulator: lui+addi builds 0xDEADBEEF", build_and_run(0xDEADBEEF)[0] == 0xDEADBEEF)
naive = ((0xDEADBEEF >> 12) << 12) + sx(0xEEF, 12)
v.assert_true("unrounded upper part gives 0xDEADAEEF", naive & M32 == 0xDEADAEEF)
v.assert_true("llvm-mc li expansion matches the split", [int.from_bytes(bytes(int(t, 16) for t in e), "little") for e in mc_encodings("li x5, 0xDEADBEEF")] == [asm(f"lui x5, {hi}"), asm(f"addi x5, x5, {lo}")])

# Ex 4: ranges, by asking the assembler
v.check("Ex 14-02.4a", 4094)
v.assert_true("beq accepts +4094 and -4096", mc_accepts("beq x5, x6, 4094") and mc_accepts("beq x5, x6, -4096"))
v.assert_true("beq rejects +4096 and -4098", not mc_accepts("beq x5, x6, 4096") and not mc_accepts("beq x5, x6, -4098"))
v.assert_true("encoder agrees at the branch limits", asm("beq x5, x6, 4094") == mc_word("beq x5, x6, 4094") and asm("beq x5, x6, -4096") == mc_word("beq x5, x6, -4096"))
v.check("Ex 14-02.4b", -4096 // 4)
v.assert_true("1500-instruction loop is out of branch range", -1500 * 4 < -4096)
v.assert_true("jal accepts +1048574 and -1048576, rejects +1048576", mc_accepts("jal x1, 1048574") and mc_accepts("jal x1, -1048576") and not mc_accepts("jal x1, 1048576"))
v.check("Ex 14-02.4c", 2**20 / 2**20)
v.assert_true("addi accepts -2048..2047 only", mc_accepts("addi x5, x5, 2047") and mc_accepts("addi x5, x5, -2048") and not mc_accepts("addi x5, x5, 2048") and not mc_accepts("addi x5, x5, -2049"))

# Ex 5: code size from object files
sizes = {"rv32i": len(assemble(LAB / "sum_rv32.s", "riscv32", "-c,-relax")),
         "rv32ic": len(assemble(LAB / "sum_rv32.s", "riscv32", "+c,-relax")),
         "a64": len(assemble(LAB / "sum_a64.s", "aarch64")),
         "x86": len(assemble(LAB / "sum_x86.s", "x86_64"))}
v.check("Ex 14-02.5a", sizes["rv32i"])
v.check("Ex 14-02.5b", sizes["rv32ic"])
v.check("Ex 14-02.5c", sizes["a64"])
v.check("Ex 14-02.5d", sizes["x86"])
v.check("Ex 14-02.5e", 100 * (1 - sizes["rv32ic"] / sizes["rv32i"]))
counts = {k: len(listing(LAB / f, c)[0]) for k, f, c in (("rv", "sum_rv32.s", "#"), ("a64", "sum_a64.s", "//"), ("x86", "sum_x86.s", "#"))}
v.assert_true("instruction counts 9, 8, 8", (counts["rv"], counts["a64"], counts["x86"]) == (9, 8, 8))
rvc_len = [len(e) for e in mc_encodings((LAB / "sum_rv32.s").read_text(), mattr="+c")]
x86_len = [len(e) for e in mc_encodings((LAB / "sum_x86.s").read_text(), triple="x86_64", mattr=None)]
v.assert_true("8 of the 9 RISC-V instructions compress; lw t1, 0(a0) does not", rvc_len.count(2) == 8 and rvc_len[2] == 4)
v.assert_true("x86 lengths are 1-3 bytes except one 4-byte addq", sorted(x86_len) == [1, 2, 2, 2, 2, 3, 3, 4] and x86_len[4] == 4)
chap = (ROOT / "chapters" / "14-02-isa-risc-v-arm-x86.md").read_text()
for k, f, c in (("rv", "sum_rv32.s", "#"), ("a64", "sum_a64.s", "//"), ("x86", "sum_x86.s", "#")):
    for m, a in listing(LAB / f, c)[0]:
        v.assert_true(f"chapter listing has '{m} {', '.join(a)}'", re.search(re.escape(m) + r"\s+" + r",\s*".join(map(re.escape, a)) if a else re.escape(m), chap) is not None)


# Ex 6: register count against immediate width
def imm_bits(R):
    return 32 - 7 - 3 - 2 * int(math.log2(R))


v.check("Ex 14-02.6a", imm_bits(16))
v.check("Ex 14-02.6b", imm_bits(32))
v.check("Ex 14-02.6c", imm_bits(64))
v.assert_true("I-type fields with 32 registers fill 32 bits", 12 + 5 + 3 + 5 + 7 == 32)

# =========================================================================== Problems
for ID, line in (("14-02.1a", "addi x10, x10, -1"), ("14-02.1b", "srai x5, x5, 3"), ("14-02.6a", "beq x5, x6, 16"),
                 ("14-02.6b", "bge x10, x11, -32"), ("14-02.8e", "auipc x6, 0x301"), ("14-02.8f", "jalr x1, -256(x6)")):
    w = asm(line)
    v.check(ID, w)
    v.assert_true(f"{line} matches llvm-mc", w == mc_word(line))

d = decode(0xFFC52303)
v.check("14-02.2a", d["rd"])
v.check("14-02.2b", d["rs1"])
v.check("14-02.2c", d["imm"])
v.assert_true("0xFFC52303 is LW (I format)", d["fmt"] == "I" and d["op"] == 0x03 and d["f3"] == 2)
v.assert_true("LLVM disassembles 0xFFC52303 as lw t1, -4(a0)", mc_disasm(0xFFC52303) == "lw t1, -4(a0)")
x, _ = run_rv32(b"".join(asm(s_).to_bytes(4, "little") for s_ in ("lw x6, -4(x10)", "jalr x0, 0(x1)")),
                regs={"a0": 0x2000}, mem={0x1FFC + i: b for i, b in enumerate((0x78, 0x56, 0x34, 0x12))})
v.assert_true("simulator loads the word at 0x1FFC", x[6] == 0x12345678)
v.check("14-02.2d", (0x2000 + d["imm"]) & M32)

v.check("14-02.3a", 2047)
v.assert_true("addi x5, x5, 3000 is rejected", not mc_accepts("addi x5, x5, 3000"))
x, _ = run_rv32(b"".join(asm(s_).to_bytes(4, "little") for s_ in ("addi x5, x0, -1", "lui x6, 0xFFFFF", "addi x0, x5, 7", "jalr x0, 0(x1)")))
v.check("14-02.3b", x[5])
v.check("14-02.3c", sx(x[6], 32))
v.assert_true("x0 stays zero after addi x0, x5, 7", x[0] == 0)

b_ = asm("add x5, x6, x7").to_bytes(4, "little")
v.check("14-02.4a", b_[0])
v.check("14-02.4b", b_[3])
v.check("14-02.4c", int.from_bytes(b_, "big"))

for C, (ih, il) in ((0x12345678, ("14-02.5a", "14-02.5b")), (0x00000800, ("14-02.5c", "14-02.5d")),
                    (0xFFFFF800, ("14-02.5e", "14-02.5f")), (0x7FFFF800, ("14-02.5h", "14-02.5i"))):
    hi, lo = split_const(C)
    v.check(ih, hi)
    v.check(il, lo)
    val, ninstr = build_and_run(C)
    v.assert_true(f"simulator rebuilds {C:#010x} in {ninstr} instruction(s)", val == C)
    v.assert_true(f"llvm-mc li {C:#010x} uses {ninstr} instruction(s)", len(mc_encodings(f"li x5, {C:#x}")) == ninstr)
v.check("14-02.5g", build_and_run(0xFFFFF800)[1])

d = decode(0x001000EF)
v.assert_true("0x001000EF is JAL x1", d["fmt"] == "J" and d["rd"] == 1)
v.assert_true("LLVM disassembles 0x001000EF as jal 2048", mc_disasm(0x001000EF) in ("jal 2048", "jal ra, 2048"))
pc0 = 0x00010040
v.check("14-02.7a", d["imm"])
v.check("14-02.7b", pc0 + d["imm"])
v.check("14-02.7c", pc0 + 4)

v.check("14-02.8a", 4096 // 4)
v.check("14-02.8b", 4096 // 2)
v.assert_true("JAL cannot reach +0x00300F00", 0x00300F00 > 2**20 - 2 and not mc_accepts("jal x1, 3149568"))
hi, lo = split_const(0x00300F00)
v.check("14-02.8c", hi)
v.check("14-02.8d", lo)
# run the call: auipc + jalr from 0x1000 must land at 0x1000 + 0x300F00, where a 'jalr x0, 0(x1)' returns
far = 0x1000 + 0x00300F00
code = b"".join(asm(s_).to_bytes(4, "little") for s_ in ("auipc x6, 0x301", "jalr x1, -256(x6)", "addi x7, x0, 1", "jalr x0, 0(x9)"))
ret = asm("addi x8, x0, 42").to_bytes(4, "little") + asm("jalr x0, 0(x1)").to_bytes(4, "little")
x, n = run_rv32(code, regs={"x9": HALT}, mem={far + i: b for i, b in enumerate(ret)})
v.assert_true("auipc+jalr reaches the far function and returns", x[8] == 42 and x[7] == 1 and n == 6)

# Problem 9 and lab: dynamic counts
random.seed(1402)
arr = [random.randint(-1000, 1000) for _ in range(1000)]
mem = {}
for i, val in enumerate(arr):
    for k in range(4):
        mem[0x10000 + 4 * i + k] = (val & M32) >> 8 * k & 0xFF


def rv_count(f, a):
    m = {}
    for i, val in enumerate(a):
        for k in range(4):
            m[0x10000 + 4 * i + k] = (val & M32) >> 8 * k & 0xFF
    x, n = run_rv32(assemble(LAB / f, "riscv32", "-c,-relax"), regs={"a0": 0x10000, "a1": len(a)}, mem=m)
    return sx(x[10], 32), n


res = {}
for key, f in (("rv", "sum_rv32.s"), ("rvr", "sum_rv32_rot.s")):
    res[key] = rv_count(f, arr)
for key, f, fn in (("a64", "sum_a64.s", run_a64), ("a64r", "sum_a64_rot.s", run_a64),
                   ("x86", "sum_x86.s", run_x86), ("x86r", "sum_x86_rot.s", run_x86)):
    res[key] = fn(LAB / f, arr)
v.assert_true("all six versions return the correct sum", all(r[0] == sum(arr) for r in res.values()))
for ID, key in (("14-02.9a", "rv"), ("14-02.9b", "a64"), ("14-02.9c", "x86"), ("14-02.9d", "rvr"),
                ("14-02.9e", "a64r"), ("14-02.9f", "x86r")):
    v.check(ID, res[key][1])
v.check("14-02.9g", 100 * (res["rv"][1] - res["rvr"][1]) / res["rv"][1])
v.assert_true("empty array: 4 instructions in every version", all(rv_count(f, [])[1] == 4 for f in ("sum_rv32.s", "sum_rv32_rot.s"))
              and all(fn(LAB / f, [])[1] == 4 for f, fn in (("sum_a64.s", run_a64), ("sum_a64_rot.s", run_a64), ("sum_x86.s", run_x86), ("sum_x86_rot.s", run_x86))))
v.assert_true("rotation leaves code size unchanged", len(assemble(LAB / "sum_rv32_rot.s", "riscv32", "-c,-relax")) == 36
              and len(assemble(LAB / "sum_rv32_rot.s", "riscv32", "+c,-relax")) == 20 and len(assemble(LAB / "sum_x86_rot.s", "x86_64")) == 19
              and len(assemble(LAB / "sum_a64_rot.s", "aarch64")) == 32)
prob = (ROOT / "problems" / "14-02-problems.md").read_text()
for f, c in (("sum_rv32_rot.s", "#"), ("sum_a64_rot.s", "//"), ("sum_x86_rot.s", "#")):
    for m, a in listing(LAB / f, c)[0]:
        v.assert_true(f"problem listing has '{m} {', '.join(a)}'", re.search(re.escape(m) + r"\s+" + r",\s*".join(map(re.escape, a)) if a else re.escape(m), prob) is not None)


# Problem 10: fetch windows
def complete_in(lengths, window=16):
    ends, t = [], 0
    for L in lengths:
        t += L
        ends.append(t)
    return sum(e <= window for e in ends)


v.assert_true("problem's x86 and RV32IC lengths match the assembler", x86_len == [2, 3, 2, 2, 4, 3, 2, 1] and rvc_len == [2, 2, 4, 2, 2, 2, 2, 2, 2])
v.check("14-02.10a", complete_in(x86_len))
v.check("14-02.10b", complete_in([4] * 9))
v.check("14-02.10c", complete_in(rvc_len))

# Problem 11
v.check("14-02.11a", 48 * (1 - 0.28))
v.check("14-02.11b", 100 * (1 - 32 / 48))
v.check("14-02.11c", 48 * sizes["rv32ic"] / sizes["rv32i"])
v.assert_true("at the spec's 25-30% saving the code still does not fit", 48 * (1 - 0.30) > 32)

# Problem 12
v.check("14-02.12a", 2 ** (7 + 3))
v.check("14-02.12b", 32 - 7 - 3 * 6)
v.check("14-02.12c", 2 ** (32 - 7 - 3 * 6))
v.check("14-02.12d", 2**3)
v.check("14-02.12e", 16 - 2 * 5)
v.assert_true("C.ADD (CR format) is funct4 + two 5-bit registers + 2-bit op", 4 + 5 + 5 + 2 == 16)


# Problem 13: multi-word addition, generated and executed
def mw_add_program(n):
    """a in x2.., b in x10.., sum in x18..; carry x26, temporary x27, partial carries x28 and x29."""
    A, B, S = (list(range(k, k + n)) for k in (2, 10, 18))
    p = [f"add x{S[0]}, x{A[0]}, x{B[0]}", f"sltu x26, x{S[0]}, x{A[0]}"]
    for i in range(1, n):
        p.append(f"add x27, x{A[i]}, x{B[i]}")
        if i < n - 1:
            p += [f"sltu x28, x27, x{A[i]}", f"add x{S[i]}, x27, x26", f"sltu x29, x{S[i]}, x27", "or x26, x28, x29"]
        else:
            p.append(f"add x{S[i]}, x27, x26")
    return p


def mw_count(n):
    return len(mw_add_program(n))


ok = True
for n in (2, 3, 4, 8):
    prog_ = mw_add_program(n) + ["jalr x0, 0(x1)"]
    code = b"".join(asm(s_).to_bytes(4, "little") for s_ in prog_)
    for _ in range(300):
        a = [random.getrandbits(32) for _ in range(n)]
        b = [random.getrandbits(32) for _ in range(n)]
        if random.random() < 0.3:  # force long carry chains
            a = [M32] * n
        regs = {f"x{2 + i}": a[i] for i in range(n)} | {f"x{10 + i}": b[i] for i in range(n)}
        x, steps = run_rv32(code, regs=regs)
        ok &= steps == mw_count(n) + 1
        got = sum(x[18 + i] << 32 * i for i in range(n))
        A_ = sum(a[i] << 32 * i for i in range(n))
        B_ = sum(b[i] << 32 * i for i in range(n))
        ok &= got == (A_ + B_) % 2 ** (32 * n)
v.assert_true("generated multi-word adds are correct on random and all-ones operands", ok)
v.assert_true("instruction count is 5n - 6 for n = 2..16", all(mw_count(n) == 5 * n - 6 for n in range(2, 17)))
v.check("14-02.13a", mw_count(2))
v.check("14-02.13b", mw_count(8))
v.check("14-02.13c", 1 + (8 - 1))
v.check("14-02.13d", mw_count(8) / 8)
v.assert_true("llvm-mc accepts the x86 add/adc pair", mc_accepts("addl %ebx, %eax\nadcl %edx, %ecx", triple="x86_64", mattr=""))
v.assert_true("carry rule s < a exhaustively on 8-bit words", all(((a + b) % 256 < a) == (a + b >= 256) for a in range(256) for b in range(256)))
v.assert_true("two partial carries never both occur (8-bit, exhaustive)", all(not ((a + b) % 256 < a and ((a + b) % 256 + 1) % 256 < (a + b) % 256) for a in range(256) for b in range(256)))


# Problem 14: present values by discounting each year's flows
def pv(flows, r=0.10):
    return sum(cf / (1 + r) ** t for t, cf in flows)


def pv_L(V):  # V in millions of units a year; $M
    return pv([(0, 1.5)] + [(t, V * 0.015 * 2.00) for t in range(1, 6)])


pv_O = pv([(0, 6.0)] + [(t, 0.5) for t in range(1, 6)])
v.check("14-02.14a", pv_L(40))
v.check("14-02.14b", pv_O)
v.check("14-02.14c", pv_O - pv_L(40))
v.check("14-02.14d", brentq(lambda V: pv_L(V) - pv_O, 1, 500, xtol=1e-12))
v.check("14-02.14e", pv_L(80))
v.check("14-02.14f", pv_L(80) - pv_O)

# Practitioner lens: derived figures from the Arm 20-F (R-204)
v.assert_true("royalty share of FY2026 revenue rounds to 53%", round(100 * 2613 / 4920) == 53 and 2613 + 2307 == 4920)
v.assert_true("related-party licence growth exceeds the whole licence growth", (1009 - 418) > (2307 - 1839))

# =========================================================================== Lab
v.check("Lab 14-02.a", asm("sw x5, 12(x2)"))
v.assert_true("sw x5, 12(x2) matches llvm-mc", asm("sw x5, 12(x2)") == mc_word("sw x5, 12(x2)"))
need = sum(1 for low in range(4096) if split_const(low)[0] != 0)  # rounding needed iff hi rounds up
v.check("Lab 14-02.b", 100 * need / 4096)
random.seed(14021)
v.assert_true("2000 random constants rebuilt exactly", all(build_and_run(C)[0] == C for C in (random.getrandbits(32) for _ in range(2000))))
arr100 = list(range(1, 101))
s1, n1 = rv_count("sum_rv32.s", arr100)
s2, n2 = rv_count("sum_rv32_rot.s", arr100)
v.assert_true("both loops return the same sum", s1 == s2)
v.check("Lab 14-02.c", s1)
v.check("Lab 14-02.d", n1)
v.check("Lab 14-02.e", n2)

# encoder/decoder round trip over a broad instruction list
lines = ["add x5, x6, x7", "sub x31, x1, x2", "sltu x15, x14, x10", "or x31, x29, x30", "and x1, x2, x3",
         "sra x4, x5, x6", "addi x1, x2, -2048", "addi x1, x2, 2047", "slti x3, x4, -1", "xori x5, x6, 255",
         "slli x7, x8, 31", "srli x9, x10, 1", "srai x11, x12, 17", "lw x13, 2047(x14)", "lw x15, -2048(x16)",
         "sw x17, -1(x18)", "sw x19, 1024(x20)", "beq x1, x2, -4096", "bne x3, x4, 4094", "blt x5, x6, 2",
         "bltu x7, x8, -2", "bgeu x9, x10, 2048", "lui x11, 0xFFFFF", "auipc x12, 0x80000",
         "jal x1, -1048576", "jal x0, 1048574", "jalr x1, 2047(x31)"]
v.assert_true(f"{len(lines)} encodings match llvm-mc", all(asm(s_) == mc_word(s_) for s_ in lines))


def text_imm(line):
    m = re.search(r"(-?(?:0x[0-9A-Fa-f]+|\d+))(?:\(\w+\))?\s*$", line)
    return int(m.group(1), 0)


rt = True
for s_ in lines:
    d = decode(asm(s_))
    if d["fmt"] == "R":
        continue
    want = text_imm(s_)
    got = d["imm"] & 31 if s_.split()[0] in ("slli", "srli", "srai") else d["imm"]
    rt &= got == (want & 0xFFFFF if d["fmt"] == "U" else want)
v.assert_true("decoder recovers every immediate from its encoding", rt)
v.assert_true("canonical NOP is 0x00000013", asm("addi x0, x0, 0") == 0x00000013 == mc_word("nop"))

sys.exit(v.finish())
