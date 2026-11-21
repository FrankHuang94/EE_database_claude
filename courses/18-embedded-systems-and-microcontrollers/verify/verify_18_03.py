#!/usr/bin/env python3
"""Verify every number in chapter 18-03 (interrupts, exceptions and timers), its problems and its lab.

Independent routes:
- response times by the fixed-point recurrence written here and by the lab's discrete-event simulator started at
  the critical instant (blocking and every request at t = 0);
- timer settings by exhaustive factor search; capture differences by modular arithmetic; PWM and watchdog figures
  by direct arithmetic;
- NVIC behaviour (implemented priority bits, preemption and tail-chaining order, masking, EXC_RETURN, the fault status
  and address registers) by building the lab firmware with clang 18 and running it on QEMU's Cortex-M4 board, and
  parsing what it reports;
- priority encodings by bit arithmetic.
"""
from __future__ import annotations

import math
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-03-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import irqtime as it  # noqa: E402
import fwrun  # noqa: E402

v = Verifier.from_files("18-03", ROOT / "chapters" / "18-03-interrupts-exceptions-timers.md",
                        ROOT / "solutions" / "18-03-solutions.md", LAB / "README.md")


def rta(c, b, hp):
    """R = c + b + sum ceil(R/T) C over hp = [(C, T)], iterated from c + b."""
    r = c + b
    while True:
        nxt = c + b + sum(math.ceil(r / t) * cj for cj, t in hp)
        if nxt == r:
            return r
        r = nxt


# ---------------------------------------------------------------- firmware on QEMU
try:
    code, out, elf = fwrun.build_and_run(Path(tempfile.mkdtemp(prefix="v1803_")))
except FileNotFoundError as exc:
    sys.exit(f"verify_18_03: {exc}")
v.assert_true("firmware passes every NVIC check on QEMU", code == 0 and "TEST PASSED" in out, out)
rep = {k: int(x, 16) for k, x in re.findall(r"^(\w+) (0x[0-9A-F]{8})$", out, re.M)}
v.check("Lab 18-03.a", fwrun.priority_bits(out))
v.check("Lab 18-03.b", rep["ORDER"])
v.check("Lab 18-03.c", rep["CFSR"])
v.check("Lab 18-03.d", rep["BFAR"])
v.check("Txt 18-03.e", rep["EXC_RETURN"])
v.assert_true("event log = IRQ0 in, IRQ1 (preempts), IRQ0 out, IRQ2 (tail-chains)", rep["ORDER"].to_bytes(4, "big") == bytes([1, 3, 2, 4]))
v.assert_true("CFSR bits 9 (PRECISERR) and 15 (BFARVALID) only; HFSR bit 30 (FORCED) only",
              rep["CFSR"] == (1 << 9) | (1 << 15) and rep["HFSR"] == 1 << 30)

# ---------------------------------------------------------------- text
v.check("Txt 18-03.a", 12 / 48e6 * 1e6)
v.check("Txt 18-03.b", 6 / 48e6 * 1e6)
v.check("Txt 18-03.c", it.systick_reload(168e6, 1e-3))
v.check("Txt 18-03.d", 2 ** 24 / 168e6 * 1e3)

# ---------------------------------------------------------------- Example 1
bytes_s = 115200 / 10
v.check("Ex 18-03.1a", 100 * it.cpu_load(bytes_s, 12 + 36 + 12, 48e6))
v.check("Ex 18-03.1b", 48e6 / 60)
v.check("Ex 18-03.1c", 100 * it.cpu_load(2e6, 60, 48e6))
v.check("Ex 18-03.1d", 24 / 48e6 * 1e6)

# ---------------------------------------------------------------- Example 2
v.check("Ex 18-03.2a", 2 ** 2)
v.check("Ex 18-03.2b", (2 << 6) | (1 << 4))
grp = lambda b: (b >> 6) & 3  # noqa: E731
v.assert_true("Example 2: 0x90 and 0xA0 share group 2 (no preemption); 0x50 is group 1 (preempts)",
              grp(0x90) == grp(0xA0) == 2 and (0x90 >> 4) & 3 == 1 and grp(0x50) == 1)

# ---------------------------------------------------------------- Example 3
irqs = [it.Irq("A", 5, 50, 0), it.Irq("B", 10, 200, 1), it.Irq("C", 20, 1000, 2)]
hp = {"A": [], "B": [(5, 50)], "C": [(5, 50), (10, 200)]}
cs = {"A": 5, "B": 10, "C": 20}
for blk, tags in ((8, "abc"), (30, "def")):
    sim = it.simulate(irqs, 3000, blocking_at=0.0, blocking_len=blk)
    for n, tg in zip("ABC", tags):
        r = rta(cs[n], blk, hp[n])
        v.check(f"Ex 18-03.3{tg}", r)
        v.assert_true(f"Example 3: simulator reproduces R_{n} = {r} with {blk} µs blocking", sim[n] == r and it.response_time(irqs, n, blk) == r)
v.check("Ex 18-03.3g", it.utilization(irqs))
v.assert_true("Example 3(c): with BASEPRI, A is unblocked: R_A = 5 µs", rta(5, 0, []) == 5)

# ---------------------------------------------------------------- Example 4
psc, arr = it.find_psc_arr(84e6, 20e3)
v.check("Ex 18-03.4a", arr)
v.assert_true("Example 4: PSC = 0 is the finest choice", psc == 0)
v.check("Ex 18-03.4b", it.pwm_resolution_bits(84e6, 20e3))
v.check("Ex 18-03.4c", 0.375 * (arr + 1))
v.check("Ex 18-03.4d", 84e6 / 20e3 / 2)
v.check("Ex 18-03.4e", it.pwm_resolution_bits(84e6, 20e3, center_aligned=True))
v.check("Ex 18-03.4f", 20e3 * 2 ** 16 / 1e9)

# ---------------------------------------------------------------- Example 5
v.check("Ex 18-03.5a", 84 - 1)
d5 = it.capture_delta(0xFFF0, 0x03D8)
v.check("Ex 18-03.5b", d5)
v.check("Ex 18-03.5c", 100 / d5)
v.check("Ex 18-03.5d", 1e6 / 2 ** 16)
v.assert_true("Example 5: 16-bit unsigned subtraction gives 0x03E8", (0x03D8 - 0xFFF0) & 0xFFFF == 0x03E8)

# ---------------------------------------------------------------- Example 6
v.check("Ex 18-03.6a", it.watchdog_timeout(64, 1000, 32e3))
v.check("Ex 18-03.6b", it.watchdog_timeout(64, 1000, 40e3))
v.check("Ex 18-03.6c", it.watchdog_timeout(64, 1000, 24e3))
v.assert_true("Example 6: 1.2 s loop is safe at the fast end; 1.8 s is not", 1.2 < it.watchdog_timeout(64, 1000, 40e3) < 1.8)

# ---------------------------------------------------------------- problems
v.check("18-03.1a", 16 + 45)
v.check("18-03.1b", (16 + 45) * 4)
v.check("18-03.1c", 15 * 4)
v.check("18-03.2a", 400e3 / 9)
v.check("18-03.2b", 100 * it.cpu_load(400e3 / 9, 80, 16e6))
v.check("18-03.3a", it.systick_reload(48e6, 10e-3))
v.check("18-03.3b", 2 ** 24 / 48e6 * 1e3)
v.check("18-03.3c", it.systick_reload(72e6, 1e-3))
v.check("18-03.4a", 2 ** 2)
v.check("18-03.4b", 2 ** 1)
v.check("18-03.4c", (1 << 6) | (1 << 5))
v.check("18-03.4d", 0x47 & 0xE0)
p6 = [it.Irq("A", 2, 20, 0), it.Irq("B", 4, 40, 1), it.Irq("C", 10, 100, 2), it.Irq("D", 15, 250, 3)]
v.check("18-03.6a", it.utilization(p6))
sim6 = it.simulate(p6, 5000, blocking_at=0.0, blocking_len=3)
hp6 = {"A": [], "B": [(2, 20)], "C": [(2, 20), (4, 40)], "D": [(2, 20), (4, 40), (10, 100)]}
for n, tg in zip("ABCD", "bcde"):
    r = rta({"A": 2, "B": 4, "C": 10, "D": 15}[n], 3, hp6[n])
    v.check(f"18-03.6{tg}", r)
    v.assert_true(f"Problem 6: simulator agrees for {n}", sim6[n] == r)
p7 = [it.Irq("A", 5, 50, 0), it.Irq("B", 25, 200, 1), it.Irq("C", 20, 1000, 2)]
r7 = rta(20, 8, [(5, 50), (25, 200)])
v.check("18-03.7a", r7)
v.check("Lab 18-03.e", it.simulate(p7, 3000, blocking_at=0.0, blocking_len=8)["C"])
psc8, arr8 = it.find_psc_arr(72e6, 1.0)
v.check("18-03.8a", psc8)
v.check("18-03.8b", arr8)
v.assert_true("Problem 8: no divisor of 72e6 between 1099 and 1124; 7199/9999 also exact",
              all(72_000_000 % p for p in range(1099, 1125)) and 7200 * 10000 == 72_000_000)
v.check("18-03.9a", 84e6 / 2 ** 10)
v.check("18-03.9b", 16e6 / 2 ** 8)
d10 = it.capture_delta(0xFFFFF000, 0x00002710, bits=32)
v.check("18-03.10a", d10)
v.check("18-03.10b", 60 / (2 * d10 * 1e-6))
need = 2 * 0.5 * 40e3
v.check("18-03.11a", need)
presc = min(p for p in (4, 8, 16, 32, 64, 128, 256) if need / p <= 4095)
v.check("18-03.11b", presc)
v.check("18-03.11c", need / presc)
v.check("18-03.11d", need / 24e3)
v.check("18-03.12a", 0x20030004 - (0x20000000 + 192 * 1024))
v.assert_true("Problem 12: the record's CFSR equals what the lab firmware measures for a precise bus error", rep["CFSR"] == 0x00008200)

sys.exit(v.finish())
