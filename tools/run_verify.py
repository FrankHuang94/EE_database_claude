#!/usr/bin/env python3
"""Run every verification script (courses/*/verify/*.py, checkpoints/**/verify*.py, capstones/**/verify*.py).

Each script must exit 0 on success. Usage:
    python tools/run_verify.py            # all scripts
    python tools/run_verify.py 07         # only scripts whose path contains "07"
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_scripts(filt: str | None):
    pats = ["courses/*/verify/*.py", "checkpoints/**/verify*.py", "capstones/**/verify*.py", "practitioner/**/verify*.py"]
    found = []
    for pat in pats:
        for p in sorted(ROOT.glob(pat)):
            if p.name.startswith("_"):
                continue
            if filt and filt not in str(p.relative_to(ROOT)):
                continue
            found.append(p)
    return found


def main() -> int:
    filt = sys.argv[1] if len(sys.argv) > 1 else None
    scripts = find_scripts(filt)
    env = dict(os.environ, PYTHONPATH=str(ROOT / "tools") + os.pathsep + os.environ.get("PYTHONPATH", ""),
               MPLBACKEND="Agg")
    failed = []
    for s in scripts:
        rel = s.relative_to(ROOT)
        r = subprocess.run([sys.executable, str(s)], cwd=s.parent, env=env, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        print(f"{'PASS' if r.returncode == 0 else 'FAIL'}  {rel}  —  {last}")
        if r.returncode != 0:
            failed.append(rel)
            print(r.stdout[-4000:])
            print(r.stderr[-4000:])
    print(f"\nverify: {len(scripts) - len(failed)}/{len(scripts)} scripts passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
