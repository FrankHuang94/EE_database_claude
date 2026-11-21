"""Lab 18-04: build and run the ring-buffer firmware in fw/ on QEMU, reusing Lab 18-02's toolchain wrapper."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "18-02-lab"))
import bmbuild as bb  # noqa: E402

FW = HERE / "fw"


def build_and_run(out_dir: Path, opt: str = "-O2") -> tuple[int, str, Path]:
    elf = bb.build(Path(out_dir) / f"ring{opt}.elf", opt=opt, fw_dir=FW)
    code, out = bb.run_qemu(elf, timeout=60)
    return code, out, elf
