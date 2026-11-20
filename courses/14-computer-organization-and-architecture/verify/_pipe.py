"""Run programs on the five-stage pipelined Verilog core of Lab 14-06 (Icarus Verilog) and on the cycle model.

Not a verify script (run_verify skips `_*.py`). Used by verify_14_06.py and later chapters' scripts.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent / "labs" / "14-06-lab"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LAB))
from _rv32 import Sim, build  # noqa: E402
import make_program  # noqa: E402

SRCS = ["rv32_pipe_tb.v", "rv32_pipe.v", "rv32_decoder.v", "rv32_immgen.v", "rv32_alu.v", "rv32_regfile.v"]


def have_iverilog() -> bool:
    return bool(shutil.which("iverilog") and shutil.which("vvp"))


def run(asm: str, array: list[int] | None = None) -> dict:
    """Assemble `asm` (must define _start and end with EBREAK), run it on the Python simulator and the cycle model,
    and, if Icarus is available, on the Verilog pipeline. Returns model counts, Verilog counts and trace agreement."""
    mem, syms, entry, size = build({"p.s": asm}, text=0)
    words = [int.from_bytes(bytes(mem[a + k] for k in range(4)), "little") for a in range(0, size, 4)]
    arr = array or []
    data = {0x2000 + 4 * i + k: (v & 0xFFFFFFFF) >> 8 * k & 0xFF for i, v in enumerate(arr) for k in range(4)}
    sim = Sim({**mem, **data}, entry)
    tr: list = []
    wt: list = []
    n = sim.run(trace=tr, wtrace=wt)
    pcs = [pc for pc, _ in tr] + [sim.pc]
    h = make_program.hazard_model(words, pcs)
    out = dict(instr=n + 1, model_cycles=n + 1 + 4 + h["stalls"] + 2 * h["taken"], stalls=h["stalls"], taken=h["taken"],
               sim=sim, writes=len(wt))
    if not have_iverilog():
        return out
    rd = lambda a: int.from_bytes(bytes(sim.mem.get(a + k, 0) for k in range(4)), "little")  # noqa: E731
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for f in SRCS[1:]:
            shutil.copy(LAB / f, td)
        shutil.copy(LAB / SRCS[0], td)
        (td / "program.hex").write_text("".join(f"{w:08x}\n" for w in words + [0x00100073] * (1024 - len(words))))
        dw = [0] * 0x1000
        for i, v in enumerate(arr):
            dw[0x2000 // 4 + i] = v & 0xFFFFFFFF
        (td / "data.hex").write_text("".join(f"{w:08x}\n" for w in dw))
        (td / "expected.vh").write_text(
            f"`define EXPECT_SUM 32'd{rd(0x100)}\n`define EXPECT_FIB 32'd{rd(0x104)}\n`define EXPECT_INSTR {n + 1}\n"
            f"`define EXPECT_WRITES {len(wt)}\n`define EXPECT_STALLS {h['stalls']}\n`define EXPECT_FLUSHES {h['taken']}\n"
            f"`define EXPECT_CYCLES {out['model_cycles']}\n")
        subprocess.run(["iverilog", "-g2012", "-I", ".", "-o", "s.vvp", *SRCS], cwd=td, check=True)
        res = subprocess.run(["vvp", "-n", "s.vvp", "+trace"], cwd=td, capture_output=True, text=True).stdout
        vt = [(int(a, 16), int(b), int(c, 16)) for a, b, c in (ln.split() for ln in (td / "trace.txt").read_text().splitlines())]
    m = re.search(r"(\d+) cycles for (\d+) instructions .*?, (\d+) load-use stalls, (\d+) flushes", res)
    out.update(verilog_passed="TEST PASSED" in res and "ERROR" not in res, trace_match=vt == wt,
               cycles=int(m.group(1)), v_stalls=int(m.group(3)), v_flushes=int(m.group(4)), report=res)
    return out
