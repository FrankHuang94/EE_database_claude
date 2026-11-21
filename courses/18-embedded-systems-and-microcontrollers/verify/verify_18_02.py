#!/usr/bin/env python3
"""Verify every number in chapter 18-02 (bare-metal C and the build toolchain), its problems and its lab.

Independent routes:
- section layouts by stepping a location counter section by section (written here, separately from the lab's
  `layout` model), and for the lab firmware against the symbol table that ld.lld actually writes;
- the firmware itself by cross-compiling it with clang 18 for the Cortex-M4 and running it on QEMU's mps2-an386
  board, including the two deliberately broken startup variants;
- the vector table by unpacking the raw .isr_vector bytes from the ELF file;
- the Example 18-02.5 listing by compiling poll.c afresh and comparing its disassembly with the published listing;
- register values by bit arithmetic and by running the host C test (which replays the race);
- the CMSIS-style struct of Problem 18-02.10 by compiling it with offsetof/sizeof checks for the target;
- costs, times and stack sizes by direct arithmetic.

Needs clang, ld.lld, the LLVM binary tools and qemu-system-arm (see the lab README).
"""
from __future__ import annotations

import math
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-02-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import bmbuild as bb  # noqa: E402

CH = ROOT / "chapters" / "18-02-bare-metal-c-and-toolchain.md"
v = Verifier.from_files("18-02", CH, ROOT / "solutions" / "18-02-solutions.md", LAB / "README.md")
TMP = Path(tempfile.mkdtemp(prefix="v1802_"))
KIB = 1024


def up4(x: int) -> int:
    return -(-x // 4) * 4


def step_layout(flash0, ram0, ram_len, n_irq, text, rodata, data, bss, stack):
    """Location-counter walk of the chapter's linker script (independent of bmbuild.layout)."""
    lc = flash0
    lc += (16 + n_irq) * 4           # .isr_vector
    lc = up4(lc)
    lc += text
    lc += rodata
    lc = up4(lc)                     # . = ALIGN(4); _etext = .
    etext = lc
    sdata = ram0
    edata = up4(sdata + data)
    ebss = up4(edata + bss)
    estack = ram0 + ram_len
    return dict(etext=etext, edata=edata, ebss=ebss, estack=estack, bottom=estack - stack,
                free=estack - stack - ebss, flash=etext - flash0 + (edata - sdata))


# ---------------------------------------------------------------- tools present?
for t in ("clang", "ld.lld", "llvm-size", "llvm-nm", "llvm-objdump", "qemu-system-arm"):
    try:
        bb.tool(t)
    except FileNotFoundError as exc:
        sys.exit(f"verify_18_02: {exc}")
clang_ver = subprocess.run([bb.tool("clang"), "--version"], capture_output=True, text=True).stdout.splitlines()[0]
v.assert_true(f"toolchain is clang 18 (published layouts and listings depend on it): {clang_ver}", "version 18." in clang_ver)

# ---------------------------------------------------------------- text: field count, sizes by optimization level, frames
v.check("Txt 18-02.a", sum(1 for w in range(1, 33) for lsb in range(0, 33 - w)))
sizes = {}
for opt in ("-O0", "-O1", "-O2", "-Os", "-Oz"):
    elf = bb.build(TMP / f"fw{opt}.elf", opt=opt)
    sizes[opt] = bb.sections(elf)[".text"][0]
    code, out = bb.run_qemu(elf)
    v.assert_true(f"firmware built at {opt} passes on QEMU", code == 0 and "TEST PASSED" in out, out)
for tag, opt in zip("bcdef", ("-O0", "-O1", "-O2", "-Os", "-Oz")):
    v.check(f"Txt 18-02.{tag}", sizes[opt])
v.check("Txt 18-02.g", 100 * (1 - sizes["-Oz"] / sizes["-O2"]))
v.check("Txt 18-02.h", 8 * 4)                       # R0-R3, R12, LR, PC, xPSR
v.check("Txt 18-02.i", (8 + 16 + 1 + 1) * 4)        # + S0-S15, FPSCR, reserved word
elf = bb.build(TMP / "fw.elf", mapfile=TMP / "fw.map")
secs = bb.sections(elf)
v.check("Txt 18-02.j", secs[".ARM.exidx"][0])
v.assert_true("the unwind index holds only EXIDX_CANTUNWIND entries (value 1)",
              all(w == 1 for w in struct.unpack("<6I", bb.section_bytes(elf, ".ARM.exidx"))[1::2]))
v.assert_true("-O2 unrolls the startup copy loop: four ldr/str pairs in Reset_Handler",
              sum(1 for i in bb.disassemble(elf, "Reset_Handler") if i.startswith("ldr")) == 4)

# ---------------------------------------------------------------- Example 1
flash1 = 23456 + 1204
ram1 = 1204 + 9872 + 4 * KIB + 8 * KIB
slot = (256 - 16) * KIB // 2
v.check("Ex 18-02.1a", flash1)
v.check("Ex 18-02.1b", 100 * flash1 / (256 * KIB))
v.check("Ex 18-02.1c", ram1)
v.check("Ex 18-02.1d", 100 * ram1 / (64 * KIB))
v.check("Ex 18-02.1e", slot)
v.check("Ex 18-02.1f", 100 * flash1 / slot)

# ---------------------------------------------------------------- Example 2 (and the lab's model agrees)
L2 = step_layout(0x08000000, 0x20000000, 0x20000, 98, 0x5E2A, 0x0A35, 0x01C2, 0x0D3D, 0x1000)
v.check("Ex 18-02.2a", L2["etext"])
v.check("Ex 18-02.2b", L2["edata"])
v.check("Ex 18-02.2c", L2["ebss"])
v.check("Ex 18-02.2d", L2["estack"])
v.check("Ex 18-02.2e", L2["bottom"])
v.check("Ex 18-02.2f", L2["free"])
v.check("Ex 18-02.2g", L2["flash"])
M2 = bb.layout(0x08000000, 0x20000000, 0x20000, (16 + 98) * 4, 0x5E2A, 0x0A35, 0x01C2, 0x0D3D, 0x1000)
v.assert_true("bmbuild.layout agrees with the location-counter walk",
              (M2["_sidata"], M2["_edata"], M2["_ebss"], M2["free_ram"], M2["flash_used"]) ==
              (L2["etext"], L2["edata"], L2["ebss"], L2["free"], L2["flash"]))
v.assert_true("Example 2: the ASSERT holds", L2["ebss"] + 0x1000 <= L2["estack"])

# ---------------------------------------------------------------- Example 3
reg = 0x00008C31
mask = ((1 << 4) - 1) << 8
cleared = reg & ~mask & 0xFFFFFFFF
new = cleared | ((6 << 8) & mask)
snapshot = reg
hw = reg | 0x8                      # the handler runs between main's load and store
hw = (snapshot & ~mask) | (6 << 8)  # main stores its stale computation
v.check("Ex 18-02.3a", mask)
v.check("Ex 18-02.3b", cleared)
v.check("Ex 18-02.3c", new)
v.check("Ex 18-02.3d", hw)
v.check("Ex 18-02.3e", new | 0x8)
v.assert_true("race loses the handler's bit 3", hw & 0x8 == 0)

# ---------------------------------------------------------------- Example 4
cyc4 = math.ceil(6 * KIB / 4) * 7 + math.ceil(40 * KIB / 4) * 4
v.check("Ex 18-02.4a", cyc4)
v.check("Ex 18-02.4b", cyc4 / 4e6 * 1e3)
v.check("Ex 18-02.4c", cyc4 / 48e6 * 1e3)
e4 = 3.0 * 1.0e-3 * cyc4 / 4e6
v.check("Ex 18-02.4d", e4 * 1e6)
v.check("Ex 18-02.4e", (e4 / 1.0) / (3e-6 * 1.8))   # one wake per second vs 3 uA at 1.8 V
v.assert_true("Example 4: zeroing is 79% of the cycles; lab model agrees", round(100 * 10240 * 4 / cyc4) == 79 and bb.startup_cycles(6 * KIB, 40 * KIB, 7, 4) == cyc4)

# ---------------------------------------------------------------- Example 5: compile and compare with the published listing
o2 = bb.compile_object("poll.c", TMP / "poll_O2.o", opt="-O2")
o0 = bb.compile_object("poll.c", TMP / "poll_O0.o", opt="-O0")
plain2, vol2 = bb.disassemble(o2, "wait_plain"), bb.disassemble(o2, "wait_volatile")
plain0 = bb.disassemble(o0, "wait_plain")
v.check("Ex 18-02.5a", len(plain2))
v.check("Ex 18-02.5b", sum(1 for i in vol2 if i.startswith("ldr")))
v.check("Ex 18-02.5c", sum(1 for i in plain0 if i.startswith("ldr")))
text = CH.read_text(encoding="utf-8")
block = re.search(r"```text\n(wait_plain:\n.*?)```", text, re.S).group(1)
pub = {}
cur = None
for line in block.splitlines():
    if line.endswith(":"):
        cur = line[:-1]
        pub[cur] = []
    elif line.strip():
        pub[cur].append(line.split()[0])
v.assert_true("published -O2 listing matches the fresh disassembly (mnemonics, in order)",
              pub["wait_plain"] == [i.split()[0] for i in plain2] and pub["wait_volatile"] == [i.split()[0] for i in vol2],
              f"{pub} vs {plain2} {vol2}")

# ---------------------------------------------------------------- Example 6
hal6, reg6 = 2 * 58 + 8, 2 * 27 + 8
v.check("Ex 18-02.6a", hal6)
v.check("Ex 18-02.6b", reg6)
v.check("Ex 18-02.6c", round((1.05 - 0.92) * 1.2e6 * 3, 6))
v.check("Ex 18-02.6d", 4 * 20000)
v.check("Ex 18-02.6e", 64 - reg6)
v.check("Ex 18-02.6f", 100 * (64 - reg6) / 64)
v.check("Ex 18-02.6g", 2 * 27 * 1.1 + 8)
v.check("Ex 18-02.6h", 128 - hal6)
v.check("Ex 18-02.6i", 128 - reg6)
v.check("Ex 18-02.6j", 100 * (128 - reg6) / 128)
v.assert_true("Example 6: HAL on 128 KiB also leaves 3.1%", round(100 * (128 - hal6) / 128, 1) == 3.1 and 2 * 27 * 1.1 + 8 > 64)

# ---------------------------------------------------------------- lab: the firmware image
sym = bb.symbols(elf)
vt = bb.vector_table(elf)
v.check("Lab 18-02.a", vt[0])
v.check("Lab 18-02.b", vt[1])
v.assert_true("word 0 is _estack; word 1 is Reset_Handler + 1 (Thumb)", vt[0] == sym["_estack"] and vt[1] == sym["Reset_Handler"] + 1)
v.assert_true("handlers 2..15 are odd or zero", all(w == 0 or w & 1 for w in vt[2:]))
v.check("Lab 18-02.c", secs[".data"][0])
v.check("Lab 18-02.d", secs[".bss"][0])
v.check("Lab 18-02.e", sym["_sidata"])
v.check("Lab 18-02.f", sym["_ebss"])
v.assert_true("lab: _sidata = _etext + the unwind index; .data and .bss addresses as the script says",
              sym["_sidata"] == sym["_etext"] + secs[".ARM.exidx"][0] and sym["_sdata"] == 0x20000000
              and sym["_edata"] == up4(0x20000000 + secs[".data"][0]) and sym["_ebss"] == up4(sym["_sbss"] + secs[".bss"][0]))
v.assert_true("lab: objects in the expected sections",
              0x20000000 <= sym["magic"] < sym["_edata"] and sym["_sbss"] <= sym["zeros"] < sym["_ebss"] and sym["squares"] < sym["_etext"])
v.assert_true("lab: berkeley text = vectors + .text + unwind index", bb.berkeley(elf)["text"] == secs[".isr_vector"][0] + secs[".text"][0] + secs[".ARM.exidx"][0])
code_d, out_d = bb.run_qemu(bb.build(TMP / "nodata.elf", defines=("LAB_SKIP_DATA_COPY",)))
code_b, out_b = bb.run_qemu(bb.build(TMP / "nobss.elf", defines=("LAB_SKIP_BSS_ZERO",)))
v.check("Lab 18-02.g", code_d)
v.assert_true("without the .data copy the .data checks fail", "FAIL: .data initial value" in out_d)
v.assert_true("without the .bss loop QEMU still passes (its SRAM starts at zero)", code_b == 0 and "TEST PASSED" in out_b)
cc = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
exe = TMP / "regbits_test"
r = subprocess.run([cc, "-std=c17", "-O1", "-Wall", "-Wextra", "-Werror", "-o", str(exe), str(LAB / "host" / "regbits_test.c")], capture_output=True, text=True)
out = subprocess.run([str(exe)], capture_output=True, text=True).stdout if r.returncode == 0 else r.stderr
m = re.search(r"(\d+) field cases checked", out)
v.check("Lab 18-02.h", int(m.group(1)) if m else -1)
v.assert_true("host test passes (field helpers, worked values, the race replay)", "TEST PASSED" in out, out)

# ---------------------------------------------------------------- problems
v.check("18-02.2a", 41220 + 2312)
v.check("18-02.2b", 100 * (41220 + 2312) / (128 * KIB))
v.check("18-02.2c", 2312 + 18004 + 2 * KIB)
v.check("18-02.2d", 100 * (2312 + 18004 + 2 * KIB) / (32 * KIB))
v.check("18-02.2e", 32 * KIB - (2312 + 18004 + 2 * KIB))
v.check("18-02.3a", (16 + 82) * 4)
v.check("18-02.3b", (16 + 37) * 4)
x = 0x12345678
x = (x & ~(0xF << 16)) | (0xA << 16)
x &= ~(1 << 31) & 0xFFFFFFFF
x |= 1 << 2
v.check("18-02.4a", x)
v.check("18-02.4b", (0x12345678 >> 20) & 0xFF)
v.check("18-02.4c", 32 * 33 // 2)
frac = (3 / 48e6) / 10e-6
v.check("18-02.5a", frac)
v.check("18-02.5b", 2000 * 3600 * frac)
L6 = step_layout(0x0, 0x20000000, 0x8000, 32, 0x2F1C, 0x0412, 0x0099, 0x0721, 0x800)
v.check("18-02.6a", L6["etext"])
v.check("18-02.6b", L6["edata"])
v.check("18-02.6c", L6["ebss"])
v.check("18-02.6d", L6["bottom"])
v.check("18-02.6e", L6["free"])
v.check("18-02.6f", L6["flash"])
v.check("18-02.7a", L6["etext"] + (L6["edata"] - 0x20000000))
v.check("18-02.8a", (768 * 6 + 6144 * 3) / 16e6 * 1e6)
v.check("18-02.8b", 768 * 6 / 16e6 * 1e6)
# Problem 10: compile the struct for the target and read offsetof/sizeof back from a static assertion build
src10 = TMP / "uart.c"
src10.write_text("""#include <stdint.h>
#include <stddef.h>
typedef struct { volatile uint32_t CR; volatile const uint32_t SR; volatile uint32_t DR; uint32_t RESERVED[5]; volatile uint32_t BRR; } uart_t;
_Static_assert(offsetof(uart_t, BRR) == 0x20, "BRR offset");
_Static_assert(sizeof(uart_t) == 36, "size");
""")
r10 = subprocess.run([bb.tool("clang"), *bb.TARGET, "-ffreestanding", "-c", str(src10), "-o", str(TMP / "uart.o")], capture_output=True, text=True)
v.assert_true("Problem 10: struct offsets and size confirmed by the target compiler", r10.returncode == 0, r10.stderr)
v.check("18-02.10a", 0x40013800 + 0x20)
v.check("18-02.10b", 9 * 4)
v.check("18-02.11a", 100 * (sizes["-O2"] / sizes["-Os"] - 1))
v.assert_true("Problem 11: -O1, -Os, -Oz fit 1.3 KiB; -O0 and -O2 do not",
              [o for o, s in sizes.items() if s <= 1.3 * KIB] == ["-O1", "-Os", "-Oz"])
hal12, reg12 = 2 * 46 + 4, 2 * 30 + 4
v.check("18-02.12a", hal12)
v.check("18-02.12b", reg12)
v.check("18-02.12c", 100 * (128 - hal12) / 128)
v.check("18-02.12d", 100 * (128 - reg12) / 128)
v.check("18-02.12e", round(0.99 * 300000 * 4, 6))
v.check("18-02.12f", 3 * 20000)
v.assert_true("Problem 12: neither build leaves 20% free on 64 KiB; both do on 128 KiB",
              hal12 > 0.8 * 64 and reg12 > 0.8 * 64 and hal12 <= 0.8 * 128 and reg12 <= 0.8 * 128)
calls = 64 + 120 + 248 + 56
v.check("18-02.13a", calls + (32 + 96) + (32 + 40))
s13 = calls + (104 + 96) + (104 + 40)
v.check("18-02.13b", s13)
v.check("18-02.13c", math.ceil(s13 * 1.25 / 8) * 8)

shutil.rmtree(TMP, ignore_errors=True)
# prose numbers outside the answer keys (audit)
v.assert_true("Example 4: .bss is 6.7 times .data", round(40 / 6, 1) == 6.7)
v.assert_true("Example 6(d): 64 - 8 - 27 = 29 KiB free is 45% of 64 KiB", round(100 * (64 - 8 - 27) / 64) == 45)
v.assert_true("Example 6(d): both cheap combinations fill 97% of their flash", round(100 * 124 / 128) == 97 and round(100 * 62 / 64) == 97)
v.assert_true("Solution 5(c): one race in 160 of 2000 interrupts a second is 12.5 a second", 2000 / 160 == 12.5)
sys.exit(v.finish())
