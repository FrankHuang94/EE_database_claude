#!/usr/bin/env python3
"""Figures for chapter 18-02 (bare-metal C and the build toolchain).

Run from anywhere:  python assets/figures/src/fig_18_02.py
Outputs
  assets/figures/18-02/memory-image.svg  flash and SRAM of the Lab 18-02 firmware (addresses from the linker script's
                                        rules for Example 18-02.2's sizes, not to scale), with the .data copy from
                                        its load address to its run address and the .bss zeroing done by the startup code
  assets/figures/18-02/code-size.svg     .text bytes of the lab firmware at -O0, -O1, -O2, -Os and -Oz (clang 18), read
                                        from the built ELF files; skipped with a message if the LLVM tools are missing
Uses labs/18-02-lab/bmbuild.py.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "courses" / "18-embedded-systems-and-microcontrollers" / "labs" / "18-02-lab"))
from plotstyle import PALETTE, save, use_style  # noqa: E402
import bmbuild as bb  # noqa: E402

OUT = "assets/figures/18-02"
use_style()
(ROOT / OUT).mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- memory image (Example 18-02.2's sizes)
L = bb.layout(0x08000000, 0x20000000, 0x20000, (16 + 98) * 4, 0x5E2A, 0x0A35, 0x01C2, 0x0D3D, 0x1000)
fig, ax = plt.subplots(figsize=(8.8, 4.8))


def block(x, y, h, label, color, addr=None, w=2.2):
    ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, alpha=0.35, edgecolor="black"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=8)
    if addr is not None:
        ax.text(x - 0.08, y, f"0x{addr:08X}", ha="right", va="center", fontsize=7, family="monospace")


# flash column (bottom = low address)
block(0.0, 0.0, 0.8, ".isr_vector\n(114 vectors)", PALETTE[0], 0x08000000)
block(0.0, 0.8, 2.6, ".text + .rodata\ncode and constants", PALETTE[1], 0x080001C8)
block(0.0, 3.4, 0.6, ".data initial values\n(load address)", PALETTE[2], L["_sidata"])
block(0.0, 4.0, 1.2, "free flash", "#ffffff", L["_sidata"] + 0x1C4)
ax.text(1.1, 5.45, "FLASH (0x0800 0000)", ha="center", fontsize=9, weight="bold")
# SRAM column
x2 = 5.2
block(x2, 0.0, 0.6, ".data\n(run address)", PALETTE[2], L["_sdata"])
block(x2, 0.6, 1.0, ".bss (zeroed)", PALETTE[3], L["_sbss"])
block(x2, 1.6, 2.4, "free SRAM\n(heap, if any)", "#ffffff", L["_ebss"])
block(x2, 4.0, 1.2, "main stack\n(grows down)", PALETTE[4], L["stack_bottom"])
ax.text(x2 - 0.08, 5.2, f"0x{L['_estack']:08X} = _estack", ha="right", va="center", fontsize=7, family="monospace")
ax.text(x2 + 1.1, 5.45, "SRAM (0x2000 0000)", ha="center", fontsize=9, weight="bold")
ax.annotate("", xy=(x2, 0.3), xytext=(2.2, 3.7), arrowprops=dict(arrowstyle="->", lw=1.4))
ax.text(3.0, 0.9, "Reset_Handler copies\n_sidata → _sdata … _edata", ha="center", fontsize=7.5)
ax.text(x2 + 2.35, 1.1, "← zeroed:\n_sbss … _ebss", ha="left", va="center", fontsize=7.5)
ax.text(x2 + 2.35, 4.6, "← SP starts at _estack\n(vector-table word 0)", ha="left", va="center", fontsize=7.5)
ax.set_xlim(-1.4, 10.4)
ax.set_ylim(-0.3, 5.8)
ax.axis("off")
ax.set_title("What the linker script places and the startup code prepares (not to scale)")
fig.tight_layout()
save(fig, f"{OUT}/memory-image.svg")

# ---------------------------------------------------------------- code size against optimization level
try:
    sizes = {}
    with tempfile.TemporaryDirectory() as d:
        for opt in ("-O0", "-O1", "-O2", "-Os", "-Oz"):
            sizes[opt] = bb.sections(bb.build(Path(d) / f"fw{opt}.elf", opt=opt))[".text"][0]
except FileNotFoundError as exc:
    print(f"fig_18_02: code-size figure skipped ({exc})")
else:
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    bars = ax.bar(list(sizes), list(sizes.values()), color=PALETTE[0], alpha=0.8)
    for b, v in zip(bars, sizes.values()):
        ax.text(b.get_x() + b.get_width() / 2, v + 20, str(v), ha="center", fontsize=8)
    ax.set_ylabel(".text bytes")
    ax.set_title("Lab 18-02 firmware, clang 18, Cortex-M4")
    ax.set_ylim(0, max(sizes.values()) * 1.2)
    fig.tight_layout()
    save(fig, f"{OUT}/code-size.svg")
