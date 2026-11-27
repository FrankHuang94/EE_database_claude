#!/usr/bin/env python3
"""Build and run the C2 testbench with Verilator (the brief's Route 1 asks for a passing Verilator testbench).

Icarus runs the same testbench in tools/run_hdl.py; this script checks that it also passes under Verilator's
timing-aware simulation. It builds in a temporary folder and exits non-zero unless the run prints TEST PASSED.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = ["fir_tb.v", "fir_direct.v", "fir_transposed.v", "fir_pipelined.v"]


def main():
    if shutil.which("verilator") is None:
        sys.exit("sim_verilator: verilator is not on the PATH")
    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        for f in SOURCES + ["stim.hex", "expected.hex"]:
            shutil.copy(HERE / f, work / f)
        build = subprocess.run(["verilator", "--binary", "--timing", "-Wall", "-Wno-fatal", "--top-module", "fir_tb",
                                *SOURCES, "-o", "fir_sim"], cwd=work, capture_output=True, text=True, timeout=900)
        if build.returncode != 0:
            print(build.stdout[-3000:], build.stderr[-3000:])
            sys.exit("sim_verilator: build failed")
        run = subprocess.run([str(work / "obj_dir" / "fir_sim")], cwd=work, capture_output=True, text=True, timeout=300)
        print(run.stdout.strip())
        if "TEST PASSED" not in run.stdout:
            sys.exit("sim_verilator: FAIL")
    print("sim_verilator: PASS")


if __name__ == "__main__":
    main()
