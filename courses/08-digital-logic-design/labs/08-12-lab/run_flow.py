#!/usr/bin/env python3
"""Run the open-source iCE40 flow (Yosys -> nextpnr-ice40 -> icepack) on the lab's designs.

Usage (from the repository root, after `pip install yowasp-yosys yowasp-nextpnr-ice40`):
    python courses/08-digital-logic-design/labs/08-12-lab/run_flow.py

For each design it synthesizes with Yosys (`synth_ice40`), places and routes for a Lattice iCE40
UltraPlus UP5K in the SG48 package with nextpnr-ice40 (fixed seed 1, a 12 MHz clock constraint), packs a
bitstream with icepack, and writes into reports/:
    <name>.json        nextpnr's report: achieved frequency, utilization, critical paths
    <name>_synth.txt   the lines of Yosys's log about FSM recoding and the final cell statistics
    seed_sweep.json    the gate-level adder's maximum frequency for placement seeds 1 to 8
The notebook and the verify script read these committed reports, so neither needs the tools.
The YoWASP packages are WebAssembly builds of the same tools, so results match native builds of the
same versions; a different version or seed can place and route differently.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
FSM_SRC = HERE.parent / "08-08-lab" / "fsm.v"

DESIGNS = {  # name: (yosys script, top module)
    "add_plus": ("read_verilog {d}; synth_ice40 -top bench_add_plus -json {j}", None),
    "add_rca": ("read_verilog {d}; synth_ice40 -top bench_add_rca -json {j}", None),
    "mul_dsp": ("read_verilog {d}; synth_ice40 -dsp -top bench_mul -json {j}", None),
    "mul_lut": ("read_verilog {d}; synth_ice40 -top bench_mul -json {j}", None),
    "fsm_auto": ("read_verilog {f}; synth_ice40 -top traffic -json {j}", None),
    "fsm_bin": ("read_verilog {f}; hierarchy -top traffic; proc; setattr -set fsm_encoding \"binary\" w:state; "
                "synth_ice40 -top traffic -json {j}", None),
}


def tool(name):
    for candidate in (name, "yowasp-" + name):
        path = shutil.which(candidate) or shutil.which(candidate, path=str(Path(sys.executable).parent))
        if path:
            return path
    sys.exit(f"{name} not found: pip install yowasp-yosys yowasp-nextpnr-ice40")


def main():
    yosys, nextpnr, icepack = tool("yosys"), tool("nextpnr-ice40"), tool("icepack")
    REPORTS.mkdir(exist_ok=True)
    work = HERE / "build"
    work.mkdir(exist_ok=True)
    for name, (script, _) in DESIGNS.items():
        j, asc, binf = work / f"{name}.json", work / f"{name}.asc", work / f"{name}.bin"
        ylog = work / f"{name}_yosys.log"
        cmd = script.format(d=HERE / "flow_designs.v", f=FSM_SRC, j=j)
        subprocess.run([yosys, "-q", "-l", str(ylog), "-p", cmd], check=True, stdout=subprocess.DEVNULL)
        subprocess.run([nextpnr, "--up5k", "--package", "sg48", "--json", str(j), "--asc", str(asc),
                        "--freq", "12", "--seed", "1", "--report", str(REPORTS / f"{name}.json")],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([icepack, str(asc), str(binf)], check=True)
        log = ylog.read_text()
        keep = [l for l in log.splitlines() if re.search(r"Recoding FSM|mapping auto encoding|existing encoding", l)]
        stats = log[log.rfind("Printing statistics"):]
        stats = stats[:stats.find("End of script")].rstrip() + "\n"     # drop run times, which vary
        (REPORTS / f"{name}_synth.txt").write_text("\n".join(keep) + "\n\n" + stats)
        rep = json.loads((REPORTS / f"{name}.json").read_text())
        fmax = next(iter(rep["fmax"].values()))["achieved"]
        used = {k: v["used"] for k, v in rep["utilization"].items() if v["used"]}
        print(f"{name:9s} {fmax:7.2f} MHz  {used}  bitstream {binf.stat().st_size} bytes")

    # placement-seed sweep for the gate-level adder: same netlist, seeds 1 to 8
    sweep = {}
    for seed in range(1, 9):
        rep = work / f"add_rca_seed{seed}.json"
        subprocess.run([nextpnr, "--up5k", "--package", "sg48", "--json", str(work / "add_rca.json"), "--freq", "12",
                        "--seed", str(seed), "--report", str(rep)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sweep[seed] = next(iter(json.loads(rep.read_text())["fmax"].values()))["achieved"]
    (REPORTS / "seed_sweep.json").write_text(json.dumps({"design": "add_rca", "fmax_mhz": sweep}, indent=1))
    print("seed sweep, add_rca:", {k: round(v, 2) for k, v in sweep.items()})


if __name__ == "__main__":
    main()
