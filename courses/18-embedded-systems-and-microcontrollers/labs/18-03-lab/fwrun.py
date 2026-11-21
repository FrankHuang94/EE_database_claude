"""Lab 18-03: build and run the interrupt firmware in fw/ on QEMU, reusing Lab 18-02's toolchain wrapper."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "18-02-lab"))
import bmbuild as bb  # noqa: E402

FW = HERE / "fw"


def build_and_run(out_dir: Path, opt: str = "-O2") -> tuple[int, str, Path]:
    """Build fw/ and run it on QEMU mps2-an386; return (exit status, console output, ELF path)."""
    elf = bb.build(Path(out_dir) / f"irq{opt}.elf", opt=opt, fw_dir=FW)
    code, out = bb.run_qemu(elf)
    return code, out, elf


def priority_bits(output: str) -> int | None:
    m = re.search(r"NVIC priority bits: (\d+)", output)
    return int(m.group(1)) if m else None
