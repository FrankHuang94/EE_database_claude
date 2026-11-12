#!/usr/bin/env python3
"""Execute every Jupyter notebook top to bottom and fail on the first error in any notebook.

Usage:
    python tools/run_notebooks.py              # execute all, do not modify files
    python tools/run_notebooks.py 07           # only notebooks whose path contains "07"
    python tools/run_notebooks.py --write      # also save outputs back into the notebooks
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    filt = args[0] if args else None
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ["PYTHONPATH"] = str(ROOT / "tools") + os.pathsep + os.environ.get("PYTHONPATH", "")
    nbs = [p for p in sorted(ROOT.glob("**/*.ipynb"))
           if ".ipynb_checkpoints" not in str(p) and "/site/" not in str(p) and "/docs/" not in str(p)]
    if filt:
        nbs = [p for p in nbs if filt in str(p.relative_to(ROOT))]
    failed = 0
    for nb_path in nbs:
        rel = nb_path.relative_to(ROOT)
        nb = nbformat.read(nb_path, as_version=4)
        client = NotebookClient(nb, timeout=900, kernel_name="python3",
                                resources={"metadata": {"path": str(nb_path.parent)}})
        try:
            client.execute()
            print(f"PASS  {rel}")
            if write:
                nbformat.write(nb, nb_path)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {rel}\n{str(e)[-3000:]}")
    print(f"\nnotebooks: {len(nbs) - failed}/{len(nbs)} executed cleanly")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
