#!/usr/bin/env python3
"""Run every ngspice netlist that declares expectations, and check the measured results.

A netlist opts in by containing one or more EXPECT comment lines:

    * EXPECT <meas_name> <value> [rtol=1e-3] [atol=...]
    * EXPECT <meas_name> key:<relative/path.md>#<ANSWER-KEY-ID> [scale=1e-3] [rtol=2e-3]

(Write spaces in an answer-key ID as underscores, e.g. #Ex_07-02.2e for 'Ex 07-02.2e'.)

The first form compares a `.meas` result with a literal value. The second form
links the simulation to a published answer: it reads the value from the answer-key
table in the given Markdown file (path relative to the netlist), multiplies it by
`scale` (e.g. 1e-3 when the key is in ms and the simulator reports seconds), and
compares. Default rtol is 1e-3. Netlists are run with `ngspice -b`.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from eeverify import load_answer_key  # noqa: E402

EXPECT_RE = re.compile(r"^\*\s*EXPECT\s+(\S+)\s+(\S+)(.*)$", re.IGNORECASE)
MEAS_RE = re.compile(r"^\s*([A-Za-z_][\w]*)\s*=\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)")


def parse_opts(s: str) -> dict:
    return {k: float(v) for k, v in re.findall(r"(\w+)=([-+\d.eE]+)", s)}


def expected_value(spec: str, netlist: Path) -> float:
    if spec.startswith("key:"):
        rel, ident = spec[4:].split("#", 1)
        key = load_answer_key((netlist.parent / rel).resolve())
        if ident not in key and ident.replace("_", " ") in key:
            ident = ident.replace("_", " ")  # IDs with spaces are written with underscores in netlists
        if ident not in key:
            raise KeyError(f"{ident} not in {rel}")
        pub = key[ident][0]
        if pub.kind != "real":
            raise ValueError(f"{ident} is not a real number")
        return pub.parts[0].value
    return float(spec)


def run_one(netlist: Path) -> list[str]:
    expects = []
    for line in netlist.read_text(encoding="utf-8").splitlines():
        m = EXPECT_RE.match(line)
        if m:
            expects.append((m.group(1).lower(), m.group(2), parse_opts(m.group(3))))
    if not expects:
        return []
    r = subprocess.run(["ngspice", "-b", netlist.name], cwd=netlist.parent, capture_output=True, text=True,
                       timeout=300)
    out = r.stdout + r.stderr
    errors = []
    if r.returncode != 0:
        errors.append(f"ngspice exited with code {r.returncode}")
    if re.search(r"^\s*Error", out, re.MULTILINE | re.IGNORECASE):
        errors.append("ngspice reported an error")
    measured = {}
    for line in out.splitlines():
        m = MEAS_RE.match(line)
        if m:
            measured[m.group(1).lower()] = float(m.group(2))
    for name, spec, opts in expects:
        try:
            exp = expected_value(spec, netlist) * opts.get("scale", 1.0)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: bad expectation ({e})")
            continue
        if name not in measured:
            errors.append(f"{name}: no measurement found in ngspice output")
            continue
        got = measured[name]
        rtol = opts.get("rtol", 1e-3)
        atol = opts.get("atol", 0.0)
        ok = abs(got - exp) <= max(atol, rtol * abs(exp))
        print(f"    {'ok  ' if ok else 'FAIL'} {name}: simulated {got:.6g}, expected {exp:.6g} (rtol {rtol:g})")
        if not ok:
            errors.append(f"{name}: simulated {got:.6g} vs expected {exp:.6g}")
    if errors:
        print(out[-3000:])
    return errors


def main() -> int:
    if not shutil.which("ngspice"):
        print("ngspice not found on PATH")
        return 1
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    nets = [p for p in sorted(ROOT.glob("**/*.cir")) if "/site/" not in str(p) and "/docs/" not in str(p)]
    if filt:
        nets = [p for p in nets if filt in str(p.relative_to(ROOT))]
    total = failed = 0
    for n in nets:
        if "EXPECT" not in n.read_text(encoding="utf-8"):
            continue
        total += 1
        print(f"  {n.relative_to(ROOT)}")
        errs = run_one(n)
        if errs:
            failed += 1
            print("FAIL  " + "; ".join(errs))
    print(f"\nspice: {total - failed}/{total} netlists passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
