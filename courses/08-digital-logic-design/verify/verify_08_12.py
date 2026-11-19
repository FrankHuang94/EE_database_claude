#!/usr/bin/env python3
"""Verify every number in chapter 08-12 (FPGA implementation flow), its solutions and lab.

The measured values come from the lab's committed nextpnr reports (labs/08-12-lab/reports/, produced by
run_flow.py with Yosys 0.71 and nextpnr-ice40 0.11.1). This script reads them directly, checks that each
critical path's segments add up to the reported maximum frequency, and recomputes every derived number
(utilizations, periods, slacks, ratios, path shares, counts) from the raw report values. Device constants
(5280 logic cells, 8 DSP blocks, 39 I/O, the 140 ms and 50 ms configuration times) are from the iCE40
UltraPlus data sheet (R-159, R-160); the bitstream size is the measured file size recorded below.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
from eeverify import Verifier  # noqa: E402

COURSE = HERE.parent
REPORTS = COURSE / "labs" / "08-12-lab" / "reports"
v = Verifier.from_files("08-12", COURSE / "chapters" / "08-12-fpga-implementation-flow.md",
                        COURSE / "solutions" / "08-12-solutions.md",
                        COURSE / "labs" / "08-12-lab" / "README.md")
CELLS, DSPS, IOS = 5280, 8, 39
BITSTREAM_BYTES = 104090          # every UP5K bitstream written by run_flow.py (icepack output size)


def load(name):
    r = json.loads((REPORTS / f"{name}.json").read_text())
    fmax = next(iter(r["fmax"].values()))["achieved"]
    used = {k: v["used"] for k, v in r["utilization"].items()}
    path = r["critical_paths"][0]["path"]
    parts = {}
    for seg in path:
        parts[seg["type"]] = parts.get(seg["type"], 0.0) + seg["delay"]
    hops = {t: sum(1 for seg in path if seg["type"] == t) for t in ("logic", "routing")}
    return dict(fmax=fmax, cells=used["ICESTORM_LC"], dsp=used.get("ICESTORM_DSP", 0), io=used["SB_IO"],
                parts=parts, total=sum(parts.values()), hops=hops)


R = {n: load(n) for n in ("add_plus", "add_rca", "mul_dsp", "mul_lut", "fsm_auto", "fsm_bin")}
v.assert_true("every critical path's segments add up to 1000/fmax",
              all(abs(r["total"] - 1000 / r["fmax"]) < 0.005 for r in R.values()))
v.assert_true("the automatic FSM was recoded one-hot and the forced one kept binary",
              "one-hot" in (REPORTS / "fsm_auto_synth.txt").read_text()
              and "packed binary" in (REPORTS / "fsm_bin_synth.txt").read_text())
v.assert_true("the measured table of chapter 3.7 matches the reports",
              [(R[n]["cells"], R[n]["dsp"], round(R[n]["fmax"], 2)) for n in R]
              == [(175, 0, 52.09), (214, 0, 17.44), (79, 1, 100.88), (765, 0, 26.10), (29, 0, 79.23), (37, 0, 54.20)])


def slack(n, f_req):
    return 1000 / f_req - R[n]["total"]


# ================================================================= chapter
v.check("Ex 08-12.1a", 100 * R["add_rca"]["cells"] / CELLS)
v.check("Ex 08-12.1b", 100 * R["fsm_auto"]["cells"] / CELLS)
v.check("Ex 08-12.1c", 100 * R["fsm_auto"]["io"] / IOS)
v.check("Ex 08-12.1d", CELLS // R["mul_lut"]["cells"])
v.check("Ex 08-12.2a", R["add_plus"]["total"])
v.check("Ex 08-12.2b", R["add_rca"]["total"])
v.check("Ex 08-12.2c", slack("add_plus", 12))
v.check("Ex 08-12.2d", slack("add_rca", 12))
v.check("Ex 08-12.2e", slack("add_plus", 48))
v.check("Ex 08-12.2f", slack("add_rca", 48))
pr = R["add_rca"]["parts"]
v.check("Ex 08-12.3a", R["add_rca"]["total"])
v.check("Ex 08-12.3b", 100 * pr["routing"] / R["add_rca"]["total"])
v.check("Ex 08-12.3c", R["add_rca"]["hops"]["logic"])
v.check("Ex 08-12.3d", R["add_rca"]["hops"]["routing"])
v.check("Ex 08-12.3e", pr["logic"] / R["add_rca"]["hops"]["logic"])
v.check("Ex 08-12.3f", pr["routing"] / R["add_rca"]["hops"]["routing"])
v.check("Ex 08-12.4a", R["add_rca"]["cells"] - R["add_plus"]["cells"])
v.check("Ex 08-12.4b", 100 * (R["add_rca"]["cells"] - R["add_plus"]["cells"]) / R["add_rca"]["cells"])
v.check("Ex 08-12.4c", R["add_plus"]["fmax"] / R["add_rca"]["fmax"])
v.check("Ex 08-12.5a", R["mul_lut"]["cells"] - R["mul_dsp"]["cells"])
v.check("Ex 08-12.5b", 100 * (R["mul_lut"]["cells"] - R["mul_dsp"]["cells"]) / CELLS)
v.check("Ex 08-12.5c", R["mul_dsp"]["fmax"] / R["mul_lut"]["fmax"])
v.check("Ex 08-12.5d", DSPS // R["mul_dsp"]["dsp"])
v.check("Ex 08-12.5e", CELLS // R["mul_lut"]["cells"])
v.check("Ex 08-12.5f", R["mul_dsp"]["parts"]["routing"])
v.check("Ex 08-12.5g", R["mul_dsp"]["total"])
import re  # noqa: E402
fsm_src = (COURSE / "labs" / "08-08-lab" / "fsm.v").read_text()
traffic = fsm_src[fsm_src.index("module traffic"):]
n_states = len(re.findall(r"\b[A-Z_0-9]+\s*=\s*3'd\d", traffic[:traffic.index("reg ")]))
v.assert_true("the traffic controller declares six states (NS_G, NS_Y, RED1, EW_G, EW_Y, RED2)", n_states == 6)
v.check("Ex 08-12.6a", n_states)
v.check("Ex 08-12.6b", math.ceil(math.log2(n_states)))
v.check("Ex 08-12.6c", R["fsm_bin"]["cells"] - R["fsm_auto"]["cells"])
v.check("Ex 08-12.6d", 100 * (R["fsm_bin"]["cells"] - R["fsm_auto"]["cells"]) / R["fsm_auto"]["cells"])
v.check("Ex 08-12.6e", R["fsm_auto"]["fmax"] / R["fsm_bin"]["fmax"])
bits = BITSTREAM_BYTES * 8
v.check("Ex 08-12.7a", bits)
v.check("Ex 08-12.7b", 100 * CELLS * 16 / bits)
v.check("Ex 08-12.7c", bits / 0.140 / 1e6)
v.check("Ex 08-12.7d", bits / 0.050 / 1e6)

# ================================================================= solutions
v.check("08-12.2a", 100 * R["fsm_bin"]["cells"] / CELLS)
v.check("08-12.2b", 100 * R["mul_dsp"]["cells"] / CELLS)
v.check("08-12.2c", 100 * R["mul_dsp"]["dsp"] / DSPS)
v.check("08-12.3a", R["fsm_bin"]["total"])
v.check("08-12.3b", slack("fsm_bin", 48))
v.check("08-12.3c", R["fsm_auto"]["total"])
v.check("08-12.3d", slack("fsm_auto", 48))
pm = R["mul_lut"]["parts"]
v.check("08-12.4a", R["mul_lut"]["total"])
v.check("08-12.4b", 1000 / R["mul_lut"]["total"])
v.check("08-12.4c", 100 * pm["routing"] / R["mul_lut"]["total"])
v.check("08-12.4d", 100 * pm["logic"] / R["mul_lut"]["total"])
half = R["add_rca"]["total"] - pr["routing"] / 2
v.check("08-12.5a", half)
v.check("08-12.5b", 1000 / half)
over = pm["clk-to-q"] + pm["setup"]
p6 = (R["mul_lut"]["total"] - over) / 2 + over
v.check("08-12.6a", p6)
v.check("08-12.6b", 1000 / p6)
v.check("08-12.7a", sum(1 for r in R.values() if r["fmax"] >= 48))
v.check("08-12.7b", sum(1 for r in R.values() if r["fmax"] < 48))
sweep = list(json.loads((REPORTS / "seed_sweep.json").read_text())["fmax_mhz"].values())
v.assert_true("seed 1 of the sweep equals the main run", abs(sweep[0] - R["add_rca"]["fmax"]) < 1e-9)
v.check("08-12.8a", max(sweep))
v.check("08-12.8b", min(sweep))
v.check("08-12.8c", sum(sweep) / len(sweep))
v.check("08-12.8d", 100 * (max(sweep) - min(sweep)) / min(sweep))
v.check("08-12.8e", sum(1 for x in sweep if x == max(sweep)))
v.check("08-12.9a", (128 * 1024) // BITSTREAM_BYTES)
v.check("08-12.9b", (512 * 1024) // BITSTREAM_BYTES)
v.check("08-12.10a", DSPS * R["mul_dsp"]["fmax"] * 1e6)
v.check("08-12.10b", (CELLS // R["mul_lut"]["cells"]) * R["mul_lut"]["fmax"] * 1e6)
v.check("08-12.10c", DSPS * R["mul_dsp"]["fmax"] / ((CELLS // R["mul_lut"]["cells"]) * R["mul_lut"]["fmax"]))
v.check("08-12.11a", bits / 12e6 * 1e3)
v.check("08-12.11b", bits / 48e6 * 1e3)

# ================================================================= lab
v.check("Lab 08-12.a", R["add_plus"]["fmax"] / R["add_rca"]["fmax"])
v.check("Lab 08-12.b", 100 * pr["routing"] / R["add_rca"]["total"])
v.check("Lab 08-12.c", sum(1 for r in R.values() if r["fmax"] >= 48))
v.check("Lab 08-12.d", sum(1 for r in R.values() if r["fmax"] >= 96))
v.check("Lab 08-12.e", R["mul_lut"]["hops"]["logic"])
v.check("Lab 08-12.f", slack("mul_dsp", 96))
v.check("Lab 08-12.g", 3000)

v.check("08-12.13a", 1000 / 48)
v.check("08-12.13b", 1000 / 12 - 20)
v.finish()
