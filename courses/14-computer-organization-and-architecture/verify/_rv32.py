"""Shared RV32I toolkit for Course 14 verify scripts (not a verify script itself: run_verify skips `_*.py`).

- `tool(name)`: locate an LLVM tool (llvm-mc, ld.lld, clang, ...) on PATH, in /usr/lib/llvm-*/bin or in Homebrew.
- `build(...)`: assemble/compile sources with LLVM, link them with ld.lld at a fixed address, and return the
  linked ELF's loadable image and symbol table (parsed here from the ELF file itself).
- `Sim`: an RV32IM instruction-set simulator written from the specification's instruction descriptions. It
  counts instructions, records the lowest stack pointer, counts calls per target, and stops on EBREAK/ECALL.
"""
from __future__ import annotations

import glob
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

M32 = 0xFFFFFFFF


def tool(name: str) -> str:
    found = [g for pat in ("/usr/lib/llvm-*/bin/", "/opt/homebrew/opt/llvm/bin/", "/usr/local/opt/llvm/bin/")
             for g in sorted(glob.glob(pat + name))]
    path = shutil.which(name) or next(iter(found), None)
    if path is None:
        sys.exit(f"{name} not found (install LLVM: `apt-get install llvm clang lld`)")
    return path


def sx(x: int, bits: int) -> int:
    return x - (1 << bits) if x >> (bits - 1) & 1 else x


# --------------------------------------------------------------------------- ELF32 reading
def read_elf(path: Path) -> tuple[dict[int, int], dict[str, int], int]:
    """Return (memory bytes {addr: byte}, symbols {name: value}, entry) from a little-endian ELF32 file."""
    b = Path(path).read_bytes()
    assert b[:4] == b"\x7fELF" and b[4] == 1 and b[5] == 1, "expected little-endian ELF32"
    (e_type, e_machine, _, e_entry, e_phoff, e_shoff, _, _, e_phentsize, e_phnum, e_shentsize, e_shnum,
     e_shstrndx) = struct.unpack_from("<HHIIIIIHHHHHH", b, 16)
    mem: dict[int, int] = {}
    for i in range(e_phnum):
        p_type, p_offset, p_vaddr, _, p_filesz, p_memsz, _, _ = struct.unpack_from("<IIIIIIII", b, e_phoff + i * e_phentsize)
        if p_type == 1:  # PT_LOAD
            for k in range(p_memsz):
                mem[p_vaddr + k] = b[p_offset + k] if k < p_filesz else 0
    sections = [struct.unpack_from("<IIIIIIIIII", b, e_shoff + i * e_shentsize) for i in range(e_shnum)]
    syms: dict[str, int] = {}
    for sh in sections:
        if sh[1] == 2:  # SHT_SYMTAB
            strtab = sections[sh[6]]
            for k in range(sh[5] // 16):
                st_name, st_value, _, _, _, _ = struct.unpack_from("<IIIBBH", b, sh[4] + 16 * k)
                if st_name:
                    s0 = strtab[4] + st_name
                    name = b[s0:b.index(b"\0", s0)].decode()
                    syms[name] = st_value
    return mem, syms, e_entry


# --------------------------------------------------------------------------- building with LLVM
START = """    .text
    .globl _start
_start:
    li   sp, 0x80000
{body}
    ebreak
"""


def build(sources: dict[str, str], relax: bool = True, opt: str = "-O2", text: int = 0x10000,
          keep: Path | None = None, m: bool = False) -> tuple[dict[int, int], dict[str, int], int, int]:
    """Build {filename: source} (.s assembled by llvm-mc, .c compiled by clang) for RV32I (RV32IM if `m`)
    with the ILP32 ABI, and link.

    Returns (memory, symbols, entry, text_size_bytes)."""
    mc, clang, lld, size = tool("llvm-mc"), tool("clang"), tool("ld.lld"), tool("llvm-size")
    with tempfile.TemporaryDirectory() as td:
        td = Path(keep) if keep else Path(td)
        td.mkdir(parents=True, exist_ok=True)
        objs = []
        attr = "-c," + ("+relax" if relax else "-relax") + (",+m" if m else "")
        for name, src in sources.items():
            (td / name).write_text(src)
            obj = td / (name + ".o")
            if name.endswith(".s"):
                subprocess.run([mc, "-triple=riscv32", f"-mattr={attr}", "-filetype=obj", str(td / name), "-o", str(obj)], check=True)
            else:
                subprocess.run([clang, "--target=riscv32", "-march=rv32im" if m else "-march=rv32i", "-mabi=ilp32", opt, "-ffreestanding", "-nostdlib",
                                "-fno-builtin", "-fno-pic", "-mrelax" if relax else "-mno-relax", "-c", str(td / name), "-o", str(obj)], check=True)
            objs.append(str(obj))
        elf = td / "prog.elf"
        subprocess.run([lld, "-m", "elf32lriscv", f"-Ttext={text:#x}", "-e", "_start"] + ([] if relax else ["--no-relax"])
                       + objs + ["-o", str(elf)], check=True)
        out = subprocess.run([size, "-A", str(elf)], capture_output=True, text=True, check=True).stdout
        tsize = int(next(ln.split()[1] for ln in out.splitlines() if ln.startswith(".text")))
        mem, syms, entry = read_elf(elf)
    return mem, syms, entry, tsize


# --------------------------------------------------------------------------- the simulator
class Sim:
    """RV32I simulator. `run()` executes from `pc` until EBREAK or ECALL and returns the instruction count."""

    def __init__(self, mem: dict[int, int], pc: int, regs: dict[int, int] | None = None):
        self.mem = dict(mem)
        self.x = [0] * 32
        for r, val in (regs or {}).items():
            self.x[r] = val & M32
        self.pc = pc
        self.count = 0
        self.min_sp = None
        self.calls: dict[int, int] = {}  # target address -> number of calls (jal/jalr with rd = ra)

    def load(self, a: int, n: int) -> int:
        return int.from_bytes(bytes(self.mem.get((a + i) & M32, 0) for i in range(n)), "little")

    def store(self, a: int, val: int, n: int) -> None:
        for i in range(n):
            self.mem[(a + i) & M32] = val >> 8 * i & 0xFF

    def run(self, limit: int = 10**7, trace: list | None = None) -> int:
        """Execute until EBREAK/ECALL. If `trace` is a list, append (pc, sp) after every instruction."""
        x = self.x
        s = lambda u: sx(u, 32)  # noqa: E731
        while True:
            assert self.count < limit, "instruction limit reached"
            pc = self.pc
            w = self.load(pc, 4)
            op, rd, f3, rs1, rs2, f7 = w & 0x7F, w >> 7 & 31, w >> 12 & 7, w >> 15 & 31, w >> 20 & 31, w >> 25
            a, b = x[rs1], x[rs2]
            nxt, res = pc + 4, None
            if op == 0x37:  # LUI
                res = w & 0xFFFFF000
            elif op == 0x17:  # AUIPC
                res = pc + (w & 0xFFFFF000)
            elif op == 0x6F:  # JAL
                imm = sx((w >> 31 & 1) << 20 | (w >> 12 & 0xFF) << 12 | (w >> 20 & 1) << 11 | (w >> 21 & 0x3FF) << 1, 21)
                res, nxt = pc + 4, pc + imm
            elif op == 0x67:  # JALR
                res, nxt = pc + 4, (a + sx(w >> 20, 12)) & ~1
            elif op == 0x63:  # branches
                imm = sx((w >> 31 & 1) << 12 | (w >> 7 & 1) << 11 | (w >> 25 & 0x3F) << 5 | (w >> 8 & 0xF) << 1, 13)
                take = {0: a == b, 1: a != b, 4: s(a) < s(b), 5: s(a) >= s(b), 6: a < b, 7: a >= b}[f3]
                if take:
                    nxt = pc + imm
            elif op == 0x03:  # loads
                addr = (a + sx(w >> 20, 12)) & M32
                n = {0: 1, 1: 2, 2: 4, 4: 1, 5: 2}[f3]
                v = self.load(addr, n)
                res = sx(v, 8 * n) & M32 if f3 in (0, 1) else v
            elif op == 0x23:  # stores
                addr = (a + sx((w >> 25) << 5 | rd, 12)) & M32
                self.store(addr, b, {0: 1, 1: 2, 2: 4}[f3])
            elif op == 0x33 and f7 == 1:  # M extension
                sa, sb = s(a), s(b)
                if f3 == 0:
                    res = a * b
                elif f3 in (1, 2, 3):  # MULH, MULHSU, MULHU: upper 32 bits of the 64-bit product
                    res = ({1: sa * sb, 2: sa * b, 3: a * b}[f3] >> 32) & M32
                elif f3 == 4:  # DIV: round toward zero; /0 -> all ones; overflow -> dividend
                    res = M32 if b == 0 else (a if (sa == -2**31 and sb == -1) else int(abs(sa) // abs(sb)) * (1 if (sa < 0) == (sb < 0) else -1))
                elif f3 == 5:  # DIVU
                    res = M32 if b == 0 else a // b
                elif f3 == 6:  # REM: sign of the dividend; /0 -> dividend; overflow -> 0
                    res = a if b == 0 else (0 if (sa == -2**31 and sb == -1) else (abs(sa) % abs(sb)) * (1 if sa >= 0 else -1))
                else:  # REMU
                    res = a if b == 0 else a % b
            elif op in (0x13, 0x33):  # OP-IMM, OP
                y = sx(w >> 20, 12) & M32 if op == 0x13 else b
                sh = y & 31
                alt = (w >> 30) & 1 and (op == 0x33 or f3 == 5)
                res = {0: (a - y) if (alt and op == 0x33) else (a + y), 1: a << sh, 2: int(s(a) < s(y)), 3: int(a < y),
                       4: a ^ y, 5: (s(a) >> sh) if alt else (a >> sh), 6: a | y, 7: a & y}[f3]
            elif op == 0x0F:  # FENCE: no effect here
                pass
            elif op == 0x73:  # ECALL / EBREAK: stop (not counted)
                return self.count
            else:
                raise ValueError(f"illegal instruction {w:#010x} at {pc:#x}")
            if op in (0x6F, 0x67) and rd == 1:
                self.calls[nxt & M32] = self.calls.get(nxt & M32, 0) + 1
            if res is not None and rd:
                x[rd] = res & M32
            self.pc = nxt & M32
            self.count += 1
            if trace is not None:
                trace.append((pc, x[2]))
            if rd == 2 and res is not None:
                self.min_sp = x[2] if self.min_sp is None else min(self.min_sp, x[2])


def run_function(sources: dict[str, str], call: str, args: list[int] = (), relax: bool = True, opt: str = "-O2",
                 data: dict[int, int] | None = None, m: bool = False):
    """Link the sources with a start-up stub that calls `call(args...)`, run it, and return a result dict:
    value (a0 as signed), count (instructions executed inside the call, excluding the stub), max stack depth
    in bytes below the initial sp, calls per symbol, text size and symbols."""
    body = "\n".join(f"    li   a{i}, {v}" for i, v in enumerate(args)) + f"\n    call {call}"
    srcs = {"start.s": START.format(body=body), **sources}
    mem, syms, entry, tsize = build(srcs, relax=relax, opt=opt, m=m)
    if data:
        mem.update(data)
    sim = Sim(mem, entry)
    n = sim.run()
    stub = _stub_len(mem, entry)  # instructions of the start-up stub up to and including the call
    inv = {v: k for k, v in syms.items()}
    calls = {inv.get(t, hex(t)): c for t, c in sim.calls.items()}
    return dict(value=sx(sim.x[10], 32), count=n - stub, depth=0x80000 - (sim.min_sp if sim.min_sp is not None else 0x80000),
                calls=calls, text=tsize, syms=syms, sim=sim)


def _stub_len(mem: dict[int, int], entry: int) -> int:
    """Instructions the start-up stub executes before control reaches the callee (up to and including the call)."""
    n, pc = 0, entry
    while True:
        w = int.from_bytes(bytes(mem.get(pc + i, 0) for i in range(4)), "little")
        n += 1
        if (w & 0x7F) in (0x6F, 0x67) and (w >> 7 & 31) == 1:  # the jal/jalr that makes the call
            return n
        pc += 4
