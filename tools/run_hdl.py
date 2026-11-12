#!/usr/bin/env python3
"""Compile and run every self-checking Verilog/SystemVerilog testbench.

Convention: a testbench file is named `*_tb.v` or `*_tb.sv`. It is compiled with
every non-testbench `.v`/`.sv` file in the same directory using Icarus Verilog
(`iverilog -g2012`), then run with `vvp`. It passes if the output contains
`TEST PASSED` and contains neither `TEST FAILED` nor `ERROR`.

Design (non-testbench) files are also linted with `verilator --lint-only -Wall`
when Verilator is available; lint warnings are reported but do not fail the run
unless --strict-lint is given.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    strict = "--strict-lint" in sys.argv
    if not shutil.which("iverilog"):
        print("iverilog not found on PATH")
        return 1
    tbs = sorted([*ROOT.glob("**/*_tb.v"), *ROOT.glob("**/*_tb.sv")])
    tbs = [t for t in tbs if "/site/" not in str(t) and "/docs/" not in str(t)]
    failed = 0
    for tb in tbs:
        d = tb.parent
        designs = sorted(p for p in [*d.glob("*.v"), *d.glob("*.sv")] if not p.stem.endswith("_tb"))
        rel = tb.relative_to(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "sim.vvp"
            c = subprocess.run(["iverilog", "-g2012", "-o", str(exe), str(tb), *map(str, designs)],
                               capture_output=True, text=True)
            if c.returncode != 0:
                failed += 1
                print(f"FAIL  {rel} (compile)\n{c.stderr}")
                continue
            r = subprocess.run(["vvp", "-n", str(exe)], cwd=d, capture_output=True, text=True, timeout=300)
            out = r.stdout + r.stderr
            ok = "TEST PASSED" in out and "TEST FAILED" not in out and "ERROR" not in out
            print(f"{'PASS' if ok else 'FAIL'}  {rel}")
            if not ok:
                failed += 1
                print(out[-3000:])
        if shutil.which("verilator") and designs:
            lint = subprocess.run(["verilator", "--lint-only", "-Wall", *map(str, designs)],
                                  capture_output=True, text=True)
            if lint.returncode != 0:
                print(f"  lint warnings in {d.relative_to(ROOT)}:\n{lint.stderr[-2000:]}")
                if strict:
                    failed += 1
    print(f"\nhdl: {len(tbs) - failed}/{len(tbs)} testbenches passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
