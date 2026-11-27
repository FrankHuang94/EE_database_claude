#!/usr/bin/env python3
"""Synthesize the three C2 FIR versions with Yosys and report area and timing against the C2 teaching library.

Flow: Yosys (`synth -flatten -noabc`) maps each RTL file to Yosys's generic gate library ($_AND_, $_XOR_, $_MUX_,
$_DFF_P_ and their variants), writes the netlist as JSON, and this script then
  - sums cell areas from the teaching library below, and
  - runs a static timing analysis on the gate graph: every register output and primary input launches at the
    clock-to-Q delay, every gate adds its intrinsic delay plus a fanout term, and every register data, enable or
    reset pin and every primary output must arrive a setup time before the next edge. The minimum period is the
    latest such arrival plus setup; the script also reports the source lines on the critical path.
The library is a teaching stand-in for a Liberty file: round numbers whose ratios follow static CMOS (an XOR or
mux costs about two NANDs; a flip-flop about seven). It is not any foundry's library, and its absolute values
should not be quoted as silicon results.

Yosys comes from PyPI as yowasp-yosys (the WebAssembly build, which needs no system install). Its built-in ABC
is not used: technology mapping and timing are done here, transparently.

Usage:  python synth.py           # synthesize and rewrite results.md
        python synth.py --check   # synthesize and compare with results.md (CI)
"""
from __future__ import annotations

import collections
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESIGNS = [("fir_direct", "direct form"), ("fir_transposed", "transposed form"),
           ("fir_pipelined", "transposed, pipelined products")]
# (area um^2, intrinsic delay ps) per generic cell; flip-flops: (area, clock-to-Q ps)
LIB = {
    "$_NOT_": (0.4, 12), "$_BUF_": (0.4, 12),
    "$_NAND_": (0.6, 18), "$_NOR_": (0.6, 18),
    "$_AND_": (0.8, 25), "$_OR_": (0.8, 25), "$_ANDNOT_": (0.8, 25), "$_ORNOT_": (0.8, 25),
    "$_XOR_": (1.2, 35), "$_XNOR_": (1.2, 35), "$_MUX_": (1.4, 35),
}
DFF_AREA, DFF_EXTRA_PIN_AREA, T_CQ, T_SETUP, T_FANOUT = 4.0, 0.6, 55, 35, 3
GATE_OUT = "Y"


def is_ff(cell_type):
    return re.match(r"^\$_(S?DFFE?|DFF|SDFF|SDFFE|SDFFCE|DFFE)_", cell_type) is not None


def synthesize(name, workdir):
    """workdir is a folder inside HERE: the WebAssembly Yosys sees only its working directory, so paths are relative."""
    out = workdir / f"{name}.json"
    rel = out.relative_to(HERE)
    script = f"read_verilog -sv {name}.v; synth -top {name} -flatten -noabc; opt_clean; write_json {rel}"
    exe = shutil.which("yowasp-yosys") or shutil.which("yosys")
    if exe is None:
        sys.exit("synth: needs yowasp-yosys (pip install yowasp-yosys) or yosys on the PATH")
    r = subprocess.run([exe, "-q", "-p", script], cwd=HERE, capture_output=True, text=True, timeout=600)
    if r.returncode != 0 or not out.exists():
        sys.exit(f"synth: yosys failed for {name}:\n{r.stdout}\n{r.stderr}")
    return json.loads(out.read_text(encoding="utf-8"))["modules"][name]


def analyze(mod, module_file):
    cells = mod["cells"]
    counts = collections.Counter(c["type"] for c in cells.values())
    area, ffs, ff_area = 0.0, 0, 0.0
    driver, fanout = {}, collections.Counter()
    for cname, c in cells.items():
        t = c["type"]
        if is_ff(t):
            ffs += 1
            a = DFF_AREA + DFF_EXTRA_PIN_AREA * (len(c["connections"]) - 3)   # C, D, Q plus E and/or R
            area += a
            ff_area += a
            driver[c["connections"]["Q"][0]] = ("ff", cname)
        elif t in LIB:
            area += LIB[t][0]
            driver[c["connections"][GATE_OUT][0]] = ("gate", cname)
        else:
            raise SystemExit(f"synth: cell type {t} is not in the teaching library")
        for pin, bits in c["connections"].items():
            if c["port_directions"][pin] == "input":
                for b in bits:
                    if isinstance(b, int):
                        fanout[b] += 1
    inputs = {b for p in mod["ports"].values() if p["direction"] == "input" for b in p["bits"] if isinstance(b, int)}
    memo, pred = {}, {}

    def arrival(bit):
        if not isinstance(bit, int):
            return 0.0                                   # constant
        if bit in memo:
            return memo[bit]
        d = driver.get(bit)
        if d is None:
            if bit not in inputs:
                raise SystemExit(f"synth: undriven net {bit}")
            memo[bit] = float(T_CQ)                      # a primary input is driven by an upstream register
            pred[bit] = None
        elif d[0] == "ff":
            memo[bit] = float(T_CQ)
            pred[bit] = None
        else:
            c = cells[d[1]]
            ins = [b for pin, bits in c["connections"].items() if c["port_directions"][pin] == "input" for b in bits]
            worst = max(ins, key=arrival)
            memo[bit] = arrival(worst) + LIB[c["type"]][1] + T_FANOUT * max(fanout[bit] - 1, 0)
            pred[bit] = (worst, d[1])
        return memo[bit]

    sys.setrecursionlimit(100000)
    endpoints = []
    for cname, c in cells.items():
        if is_ff(c["type"]):
            for pin, bits in c["connections"].items():
                if pin not in ("C", "Q"):
                    endpoints += [(arrival(b), b) for b in bits]
    for p in mod["ports"].values():
        if p["direction"] == "output":
            endpoints += [(arrival(b), b) for b in p["bits"]]
    worst_arr, worst_bit = max(endpoints, key=lambda e: e[0])
    path, b, depth = [], worst_bit, 0
    while isinstance(b, int) and pred.get(b):
        b, cname = pred[b]
        depth += 1
        src = cells[cname]["attributes"].get("src", "")
        for part in src.split("|"):                     # keep the design file's lines, not Yosys's techmap library
            m = re.match(rf"(?:.*/)?{re.escape(module_file)}:(\d+)", part)
            if m:
                path.append(int(m.group(1)))
    lines = sorted(set(path))
    return {"area": area, "ff_area": ff_area, "cells": sum(counts.values()), "ffs": ffs, "period": worst_arr + T_SETUP,
            "depth": depth, "lines": lines, "counts": counts}


def fmt_results(res):
    out = ["# C2 Reference · Synthesis Results", "",
           "Generated by [synth.py](synth.py): Yosys (generic gates) plus the C2 teaching library and a static timing "
           "analysis in Python. CI re-synthesizes every version and checks it against the answer key below. The design "
           "is discussed in [design-report.md](design-report.md).", "",
           "| Version | Cells | Flip-flops | Logic area (µm²) | Register area (µm²) | Area (µm²) | Gates on the critical "
           "path | Minimum period (ps) | Maximum clock (MHz) | Critical path (source lines) |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for (name, desc), r in zip(DESIGNS, res):
        lines = ", ".join(str(x) for x in r["lines"]) if r["lines"] else "—"
        out.append(f"| {desc} (`{name}.v`) | {r['cells']} | {r['ffs']} | {r['area'] - r['ff_area']:.1f} | "
                   f"{r['ff_area']:.1f} | {r['area']:.1f} | {r['depth']} | "
                   f"{r['period']:.0f} | {1e6 / r['period']:.0f} | {lines} |")
    out += ["", "Cell mix:", "", "| Version | " + " | ".join(t.strip('$_') for t in sorted(LIB)) + " | flip-flops |",
            "|---|" + "---|" * (len(LIB) + 1)]
    for (name, desc), r in zip(DESIGNS, res):
        out.append(f"| {desc} | " + " | ".join(str(r["counts"].get(t, 0)) for t in sorted(LIB)) + f" | {r['ffs']} |")
    out += ["", "<!-- answer-key -->", "", "| ID | Quantity | Value | Unit |", "|---|---|---|---|"]
    for (name, desc), r in zip(DESIGNS, res):
        k = name.replace("fir_", "")
        out += [f"| C2.{k}.cells | cells, {desc} | {r['cells']} | — |",
                f"| C2.{k}.ffs | flip-flops, {desc} | {r['ffs']} | — |",
                f"| C2.{k}.logic | logic area, {desc} | {r['area'] - r['ff_area']:.1f} | µm² |",
                f"| C2.{k}.regs | register area, {desc} | {r['ff_area']:.1f} | µm² |",
                f"| C2.{k}.area | area, {desc} | {r['area']:.1f} | µm² |",
                f"| C2.{k}.depth | gates on the critical path, {desc} | {r['depth']} | — |",
                f"| C2.{k}.period | minimum period, {desc} | {r['period']:.0f} | ps |",
                f"| C2.{k}.fmax | maximum clock, {desc} | {1e6 / r['period']:.0f} | MHz |"]
    return "\n".join(out) + "\n"


def main():
    with tempfile.TemporaryDirectory(dir=HERE, prefix=".synth-") as td:
        res = [analyze(synthesize(name, Path(td)), f"{name}.v") for name, _ in DESIGNS]
    text = fmt_results(res)
    target = HERE / "results.md"
    if "--check" in sys.argv:
        old = target.read_text(encoding="utf-8")
        if old != text:
            import difflib
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), text.splitlines(True), "results.md",
                                                       "re-synthesized"))
            print("synth: FAIL, results.md does not match a fresh synthesis")
            return 1
        print(f"synth: PASS, {len(res)} designs match results.md")
        return 0
    target.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
