#!/usr/bin/env python3
"""Verify every number in chapter 18-05 (GPIO, UART, SPI and I2C), its problems and its lab.

Independent routes:
- baud divisors and errors by direct arithmetic (exact fractions where it matters), cross-checked against the lab's
  serialbus module;
- the UART receiver's window from the sampling inequalities written out here for every bit of the frame (not only
  the last), and by running the lab's Verilog receiver under Icarus Verilog, both as published (tick 7) and with the
  sample point moved (tick 6);
- the UART driver by building the lab firmware with clang 18 and running it on QEMU's Cortex-M4 at -O2 and -O0;
- I2C rise times from the RC solution v(t) = VDD (1 - exp(-t/RC)), solved for the 30% and 70% crossings;
- SPI, GPIO, bus-occupancy and design numbers by direct arithmetic.
"""
from __future__ import annotations

import math
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAB = ROOT / "labs" / "18-05-lab"
sys.path.insert(0, str(HERE.parents[2] / "tools"))
sys.path.insert(0, str(LAB))
from eeverify import Verifier  # noqa: E402
import fwrun  # noqa: E402
import serialbus as sb  # noqa: E402

v = Verifier.from_files("18-05", ROOT / "chapters" / "18-05-gpio-uart-spi-i2c.md",
                        ROOT / "solutions" / "18-05-solutions.md", LAB / "README.md")

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def e12_up(x):
    vals = sorted(m * 10 ** d for d in range(-1, 7) for m in E12)
    return next(val for val in vals if val >= x * (1 - 1e-12))


def baud_err(f, baud, s=16, frac=0):
    q = 2 ** frac
    div = Fraction(round(Fraction(f) / (s * Fraction(baud)) * q), q)
    return div, float(Fraction(f) / (s * div) / Fraction(baud) - 1)


def window(n_bits, s_samp=0.5, tick=1 / 16, last_sampled=None, high_until=None):
    """Accepted range of r for a receiver sampling bit k at delta + s_samp + k (delta in [0, tick)), for bits
    0 .. last_sampled; each sampled bit k is held by the sender during [k r, (k + 1) r), except that the sampled
    stop bit may also land in later stop bits up to the end of bit high_until."""
    last = n_bits - 1 if last_sampled is None else last_sampled
    hi = last if high_until is None else high_until
    r_max = min((k + s_samp) / k for k in range(1, last + 1))
    lows = [(k + s_samp + tick) / (k + 1) for k in range(0, last)]
    lows.append((last + s_samp + tick) / (hi + 1))
    return max(lows), r_max


def rise_30_70(rc):
    t30 = brentq(lambda t: 1 - math.exp(-t / rc) - 0.3, 0, 10 * rc, xtol=1e-18)
    t70 = brentq(lambda t: 1 - math.exp(-t / rc) - 0.7, 0, 10 * rc, xtol=1e-18)
    return t70 - t30


K = rise_30_70(1.0)
v.assert_true("rise factor from the crossings equals ln(7/3)", abs(K - math.log(7 / 3)) < 1e-12)
v.assert_true("serialbus.rc_rise_30_70 matches", abs(sb.rc_rise_30_70(1.0, 1.0) - K) < 1e-12)


def i2c_clocks(n_data, reg=1):
    # START + (address+W) + register + Sr + (address+R) + data + STOP, 9 clocks a byte, 1 for each condition
    return 3 + 9 * (1 + reg + 1 + n_data)


def run_iverilog(rx_src: Path) -> tuple[float, float, str]:
    with tempfile.TemporaryDirectory(prefix="v1805_") as td:
        subprocess.run(["iverilog", "-g2012", "-o", f"{td}/sim", str(rx_src), str(LAB / "hdl" / "uart_rx_tb.v")],
                       check=True, capture_output=True, text=True)
        out = subprocess.run(["vvp", "-n", f"{td}/sim"], check=True, capture_output=True, text=True).stdout
    m = re.search(r"PASS RANGE r_min ([0-9.]+) r_max ([0-9.]+)", out)
    if not m:
        sys.exit(f"verify_18_05: no PASS RANGE in simulation output:\n{out}")
    return float(m.group(1)), float(m.group(2)), out


if not (shutil.which("iverilog") and shutil.which("vvp")):
    sys.exit("verify_18_05: iverilog and vvp are required (see SETUP.md)")

# ---------------------------------------------------------------- firmware on QEMU
for opt in ("-O2", "-O0"):
    try:
        code, out, _ = fwrun.build_and_run(Path(tempfile.mkdtemp(prefix="v1805_")), opt)
    except FileNotFoundError as exc:
        sys.exit(f"verify_18_05: {exc}")
    v.assert_true(f"UART firmware passes on QEMU at {opt}", code == 0 and "TEST PASSED" in out, out)
    v.assert_true(f"UART0 printed its greeting at {opt}", "hello from the CMSDK UART" in out, out)
    m = re.search(r"UART0 BAUDDIV (\d+)", out)
    mb = re.search(r"UART0 actual baud (\d+)", out)
    v.assert_true(f"firmware reported divisor and baud at {opt}", bool(m and mb), out)
fw_div, fw_baud = int(m.group(1)), int(mb.group(1))
v.check("Lab 18-05.e", fw_div)
v.check("Lab 18-05.f", fw_baud)
v.assert_true("driver's divisor is the nearest integer", fw_div == round(25e6 / 115200))
v.check("Lab 18-05.g", 100 * (25e6 / fw_div / 115200 - 1))

# ---------------------------------------------------------------- Verilog receiver
lo7, hi7, out7 = run_iverilog(LAB / "hdl" / "uart_rx.v")
v.assert_true("published receiver's testbench prints TEST PASSED", "TEST PASSED" in out7, out7[-400:])
src = (LAB / "hdl" / "uart_rx.v").read_text()
needle = "tick == 4'd7) begin"
v.assert_true("start-bit comparison found once in uart_rx.v", src.count(needle) == 1)
with tempfile.TemporaryDirectory(prefix="v1805_rx6_") as td:
    rx6 = Path(td) / "uart_rx6.v"
    rx6.write_text(src.replace(needle, "tick == 4'd6) begin"))
    lo6, hi6, _ = run_iverilog(rx6)


def grid_window(lo, hi):
    grid = [round(0.940 + 0.0025 * k, 4) for k in range(53)]
    inside = [g for g in grid if lo - 1e-12 <= g <= hi + 1e-12]
    return inside[0], inside[-1]


# ---------------------------------------------------------------- text and Example 1 (LED)
v.check("Txt 18-05.a", 115200 / 10)
v.check("Txt 18-05.b", K)
r_led = (3.3 - 2.0) / 6e-3
v.check("Ex 18-05.1a", r_led)
v.check("Ex 18-05.1b", e12_up(r_led))
v.assert_true("serialbus E12 agrees", sb.e12_at_least(r_led) == e12_up(r_led))
v.check("Ex 18-05.1c", 1e3 * (3.3 - 0.4 - 2.0) / 220)
v.check("Ex 18-05.1d", 1e3 * (3.3 - 2.0) / 220)
v.check("Ex 18-05.1e", 80 / 6)

# ---------------------------------------------------------------- Example 2 (divisors)
v.check("Ex 18-05.2a", 16e6 / (16 * 115200))
d_int, e_int = baud_err(16_000_000, 115200)
v.check("Ex 18-05.2b", float(d_int))
v.check("Ex 18-05.2c", 16e6 / (16 * float(d_int)))
v.check("Ex 18-05.2d", 100 * e_int)
d_fr, e_fr = baud_err(16_000_000, 115200, frac=4)
v.check("Ex 18-05.2e", float(d_fr))
v.check("Ex 18-05.2f", 16e6 / (16 * float(d_fr)))
v.check("Ex 18-05.2g", 100 * e_fr)
v.assert_true("serialbus baud_error agrees", abs(sb.baud_error(16e6, 115200) - e_int) < 1e-12
              and abs(sb.baud_error(16e6, 115200, 16, 4) - e_fr) < 1e-12)
v.assert_true("14.7456 MHz = 128 x 115 200", 14_745_600 == 128 * 115200)
r_tx = 1.01 * 115200 / (16e6 / (16 * 9))      # MCU sends, peer 1% fast receives
r_rx = (16e6 / (16 * 9)) / (1.01 * 115200)      # peer 1% fast sends, MCU receives
v.assert_true("integer divisor: MCU TX inside r_max, MCU RX below r_min (fails)",
              round(r_tx, 3) == 1.047 and r_tx < 9.5 / 9 and r_rx < (9.5 + 1 / 16) / 10)
v.check("Ex 18-05.2h", r_rx)

# ---------------------------------------------------------------- Example 3 (window, theory and simulation)
rmin16, rmax = window(10)
rmin8, rmax8 = window(10, tick=1 / 8)
v.check("Ex 18-05.3a", rmax)
v.check("Ex 18-05.3b", rmin16)
v.check("Ex 18-05.3c", rmin8)
v.assert_true("8x does not change r_max", rmax8 == rmax)
v.check("Ex 18-05.3d", 100 * (1 / rmax - 1))
v.check("Ex 18-05.3e", 100 * (1 / rmin16 - 1))
v.check("Ex 18-05.3f", 100 * (1 / rmin8 - 1))
v.assert_true("serialbus window agrees", all(abs(a - b) < 1e-12 for a, b in
                                              zip(sb.uart_ratio_window(10, 16), (rmin16, rmax))))
v.check("Ex 18-05.3g", lo7)
v.check("Ex 18-05.3h", hi7)
v.assert_true("simulated window is the grid inside the derived one", grid_window(rmin16, rmax) == (lo7, hi7))
v.assert_true("ATmega328P Rfast 104.58% matches the fast limit", abs(100 / rmin16 - 104.58) < 0.005)

# ---------------------------------------------------------------- Example 4 (SPI)
v.check("Ex 18-05.4a", 1e-6 / (2 * (2 + 1 + 15 + 1 + 5) * 1e-9))
v.check("Ex 18-05.4b", 1e-6 / (2 * (2 + 1 + 3 + 15 + 3 + 1 + 5) * 1e-9))
v.assert_true("serialbus spi_max_clock agrees", abs(sb.spi_max_clock(2e-9, 1e-9, 15e-9, 5e-9) - 1 / 48e-9) < 1)

# ---------------------------------------------------------------- Example 5 (I2C pull-ups)
v.check("Ex 18-05.5a", (3.3 - 0.4) / 3e-3)
v.check("Ex 18-05.5b", 300e-9 / (K * 200e-12))
v.check("Ex 18-05.5c", 1e9 * rise_30_70(1500 * 200e-12))
v.check("Ex 18-05.5d", (3.3 - 0.4) / 20e-3)
v.check("Ex 18-05.5e", 120e-9 / (K * 550e-12))
t47 = rise_30_70(4700 * 200e-12)
v.check("Ex 18-05.5f", 1e9 * t47)
v.assert_true("4.7 kOhm at 200 pF meets 1000 ns but not 300 ns", 300e-9 < t47 < 1000e-9)

# ---------------------------------------------------------------- Example 6 (I2C read)
n6 = i2c_clocks(2)
v.check("Ex 18-05.6a", n6)
v.assert_true("serialbus i2c_read_clocks agrees", sb.i2c_read_clocks(2) == n6)
v.check("Ex 18-05.6b", n6 * 2.5)
v.check("Ex 18-05.6c", 100 * 16 / n6)
v.check("Ex 18-05.6d", 1 / (n6 * 2.5e-6))
v.assert_true("I3C clock / 400 kHz is about 30", 25 < 12.5e6 / 400e3 < 35)

# ---------------------------------------------------------------- Problem 1
v.check("18-05.1a", 0.7 * 1.8)
v.check("18-05.1b", 0.3 * 1.8)
v.check("18-05.1c", 0.7 * 3.3)
v.check("18-05.1d", 0.3 * 3.3)
v.check("18-05.1e", 1.8 - 0.4)
v.check("18-05.1f", 0.3 * 1.8 - 0.4)
v.assert_true("sensor high fails the MCU threshold", 1.8 - 0.4 < 0.7 * 3.3)
v.assert_true("MCU levels meet the sensor thresholds", 3.3 - 0.4 > 0.7 * 1.8 and 0.4 < 0.3 * 1.8)

# ---------------------------------------------------------------- Problem 2
v.check("18-05.2a", 9600 / sb.uart_frame_bits(8, True, 1))
v.assert_true("8E1 frame is 11 bits", sb.uart_frame_bits(8, True, 1) == 11)
v.check("18-05.2b", 100 * 8 / 11)
v.check("18-05.2c", 1e3 * 1024 * 10 / 115200)
v.check("18-05.2d", 1e6 / 10)
v.check("18-05.2e", 1e6 / (1e6 / 10))

# ---------------------------------------------------------------- Problem 3 (SPI)
MODES = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}


def spi_mode(idle_high, capture_rising):
    cpol = 1 if idle_high else 0
    first_edge_rising = not idle_high
    cpha = 0 if capture_rising == first_edge_rising else 1
    return MODES[(cpol, cpha)]


v.check("18-05.3d", spi_mode(True, True))
v.check("18-05.3e", spi_mode(False, True))   # output changes on falling, so capture on rising
v.check("18-05.3a", 1e6 * (1 + 3 + 256) * 8 / 10e6)
v.check("18-05.3b", 100 * 256 / 260)
v.check("18-05.3c", 1e6 * (1 + 3 + 1 + 256) * 8 / 40e6)

# ---------------------------------------------------------------- Problem 4 (I2C addressing and arbitration)
v.check("18-05.4a", (0x48 << 1) | 0)
v.check("18-05.4b", (0x48 << 1) | 1)
a_bits, b_bits = format(0x48, "07b"), format(0x4C, "07b")
first_diff = next(i for i in range(7) if a_bits[i] != b_bits[i])
v.assert_true("B sends the 1 at the first difference (so B loses)", b_bits[first_diff] == "1")
v.check("18-05.4c", first_diff + 1)
usable = [a for a in range(128) if (a >> 3) not in (0b0000, 0b1111)]
v.check("18-05.4d", len(usable))

# ---------------------------------------------------------------- Problem 5 (divisors from 48 MHz)
d5, e5 = baud_err(48_000_000, 1_000_000)
v.check("18-05.5a", float(d5))
v.check("18-05.5b", 100 * e5)
v.check("18-05.5c", 48e6 / (16 * 921600))
d5b, e5b = baud_err(48_000_000, 921600)
v.assert_true("nearest integer is 3", d5b == 3)
v.check("18-05.5d", 100 * e5b)
d5c, e5c = baud_err(48_000_000, 921600, frac=4)
v.check("18-05.5e", float(d5c))
v.check("18-05.5f", 48e6 / (16 * float(d5c)))
v.check("18-05.5g", 100 * e5c)
v.check("18-05.5h", 48e6 / (8 * 921600))
d5d, e5d = baud_err(48_000_000, 921600, s=8)
v.check("18-05.5i", float(d5d))
v.check("18-05.5j", 48e6 / (8 * float(d5d)))
v.check("18-05.5k", 100 * e5d)
bauddiv = (48_000_000 + 921600 // 2) // 921600
v.assert_true("integer rounding expression gives the nearest integer", bauddiv == round(48e6 / 921600))
v.check("18-05.5l", bauddiv)
v.check("18-05.5m", 100 * (48e6 / bauddiv / 921600 - 1))
v.assert_true("cycles-per-bit divisor equals 16x with 4 fraction bits", Fraction(bauddiv, 16) == d5c)
v.assert_true("the sum fits in 32 bits", 48_000_000 + 921600 // 2 < 2 ** 32)

# ---------------------------------------------------------------- Problem 6 (clock budget)
v.check("18-05.6a", 1.015 / 0.985)
v.check("18-05.6b", 0.985 / 1.015)
v.check("18-05.6c", 100 * (1 / (1.015 / 0.985) - 1))
v.check("18-05.6d", 100 * (1 / (0.985 / 1.015) - 1))
v.assert_true("oscillator-only range is inside the 16x window", rmin16 < 0.985 / 1.015 and 1.015 / 0.985 < rmax)
tx = 1 + e_int
r6 = 1.015 / (0.985 * tx)
v.check("18-05.6e", r6)
v.assert_true("integer divisor plus 1.5% oscillators fails", r6 > rmax)
v.assert_true("other extreme is fine", rmin16 < 0.985 / (1.015 * tx) < rmax)
x6 = brentq(lambda x: (1 + x) / ((1 - x) * tx) - rmax, 0, 0.05, xtol=1e-15)
v.check("18-05.6f", 100 * x6)

# ---------------------------------------------------------------- Problem 7 (frame formats)
rmin_e, rmax_e = window(11)
v.check("18-05.7a", rmax_e)
v.check("18-05.7b", rmin_e)
v.check("18-05.7c", 100 * (1 / rmax_e - 1))
v.check("18-05.7d", 100 * (1 / rmin_e - 1))
v.assert_true("serialbus 8E1 window agrees", all(abs(a - b) < 1e-12 for a, b in
                                                 zip(sb.uart_ratio_window(11, 16), (rmin_e, rmax_e))))
rmin_n2, rmax_n2 = window(11, last_sampled=9, high_until=10)
v.assert_true("8N2 leaves r_max unchanged", abs(rmax_n2 - rmax) < 1e-15)
v.assert_true("8N2 stop-bit sample bound is about 0.869", abs((9.5 + 1 / 16) / 11 - 0.869) < 5e-4)
v.check("18-05.7e", rmin_n2)
v.assert_true("8N2 binding bit is the last data bit", abs(rmin_n2 - (8.5 + 1 / 16) / 9) < 1e-15)
v.check("18-05.7f", 100 * (1 / rmin_n2 - 1))

# ---------------------------------------------------------------- Problem 8 (5 V input)
r8 = (5 - 3.3 - 0.3) / 2e-3
v.check("18-05.8a", r8)
v.assert_true("serialbus injection_resistor agrees", abs(sb.injection_resistor(5, 3.3, 0.3, 2e-3) - r8) < 1e-9)
r8e = e12_up(r8)
v.check("18-05.8b", r8e)
v.check("18-05.8c", 1e3 * (5 - 3.6) / r8e)
v.check("18-05.8d", 1e9 * r8e * 10e-12)
v.check("18-05.8e", 1e6 / 115200)

# ---------------------------------------------------------------- Problem 9 (pull-ups for a real bus)
cb9 = 10 * 10e-12 + 30e-12
v.check("18-05.9a", cb9 * 1e12)
v.check("18-05.9b", 2.9 / 3e-3)
v.check("18-05.9c", 300e-9 / (K * cb9))
t9a, t9b = rise_30_70(4700 * cb9), rise_30_70(2200 * cb9)
v.check("18-05.9d", 1e9 * t9a)
v.check("18-05.9e", 1e9 * t9b)
v.assert_true("4.7k fails and 2.2k passes 300 ns; 2.2k above R_p min", t9a > 300e-9 > t9b and 2200 > 2.9 / 3e-3)
v.check("18-05.9f", 1e3 * 3.3 / 2200)
v.check("18-05.9g", 1e3 * 3.3 ** 2 / 2200)

# ---------------------------------------------------------------- Problem 10 (SPI timing)
half10 = 1.5 + 0.5 + 8 + 0.5 + 4
v.check("18-05.10a", 1e3 / (2 * half10))
v.assert_true("controller rating limits (a)", 1e3 / (2 * half10) > 32)
v.check("18-05.10b", 1e3 / half10)
v.check("18-05.10c", 1e3 / (2 * (half10 + 6)))
v.assert_true("translators make the loop the limit", 1e3 / (2 * (half10 + 6)) < 32)

# ---------------------------------------------------------------- Problem 11 (bus occupancy)
n11 = i2c_clocks(6)
v.check("18-05.11a", n11)
v.check("18-05.11b", n11 * 2.5)
v.check("18-05.11c", 100 * 6 * 200 * n11 / 400e3)
v.check("18-05.11d", 100 * 6 * 200 * n11 / 1e6)
v.check("18-05.11e", 100 * 6 * 200 * n11 / 12.5e6)
nmax = 0.5 / (200 * n11 / 400e3)
v.assert_true("sensor limit before rounding is 11.9", abs(nmax - 11.9) < 0.05)
v.assert_true("limit is not an integer", nmax != int(nmax))
v.check("18-05.11f", math.floor(nmax))

# ---------------------------------------------------------------- Problem 12 (wearable)
v.check("18-05.12a", 1600 * 12)
v.check("18-05.12b", 1600 * 12 * 8 / 1e3)
n12 = i2c_clocks(12)
v.check("18-05.12c", n12)
v.check("18-05.12d", n12 * 2.5)
v.check("18-05.12e", 100 * 1600 * n12 / 400e3)
n12f = i2c_clocks(32 * 12)
v.check("18-05.12f", n12f)
v.assert_true("FIFO read takes 8.715 ms", abs(n12f / 400e3 - 8.715e-3) < 1e-9)
v.assert_true("32 samples at 1600 Hz is 20 ms", abs(32 / 1600 - 0.020) < 1e-15)
v.check("18-05.12g", 100 * (n12f / 400e3) / (32 / 1600))
t_spi = (1 + 12) * 8 / 8e6
v.check("18-05.12h", 1e6 * t_spi)
v.check("18-05.12i", 100 * 1600 * t_spi)
pins = {"SCK": 1, "MOSI": 1, "MISO": 1, "CS_IMU": 1, "CS_FLASH": 1, "INT_IMU": 1,
        "TX": 1, "RX": 1, "RTS": 1, "CTS": 1, "SCL": 1, "SDA": 1}
v.check("18-05.12j", sum(pins.values()))

# ---------------------------------------------------------------- Problem 13 (sample point)
rmin_7, rmax_7 = window(10, s_samp=7 / 16)
v.check("18-05.13a", rmax_7)
v.check("18-05.13b", rmin_7)
v.check("18-05.13c", 100 * (1 / rmax_7 - 1))
v.check("18-05.13d", 100 * (1 / rmin_7 - 1))
v.assert_true("s = 7/16 tolerates more than s = 8/16 symmetrically",
              min(1 - 1 / rmax_7, 1 / rmin_7 - 1) > min(1 - 1 / rmax, 1 / rmin16 - 1))


def tol_gap(s):
    lo, hi = window(10, s_samp=s)
    return (1 - 1 / hi) - (1 / lo - 1)


s_star = brentq(tol_gap, 0.3, 0.6, xtol=1e-15)
v.check("18-05.13e", s_star)
v.assert_true("s* is 7.48 sixteenths", abs(16 * s_star - 7.48) < 0.005)
lo_s, hi_s = window(10, s_samp=s_star)
v.check("18-05.13f", 100 * (1 - 1 / hi_s))
v.assert_true("with zero detection delay the balance is s = 0.5 at 1/19",
              abs(window(10, s_samp=0.5, tick=0)[0] - 0.95) < 1e-15 and abs(1 / 0.95 - 1 - 1 / 19) < 1e-15)
v.check("18-05.13g", lo6)
v.check("18-05.13h", hi6)
v.assert_true("tick-6 simulation is the grid inside the derived window", grid_window(rmin_7, rmax_7) == (lo6, hi6))
v.check("Lab 18-05.c", lo6)
v.check("Lab 18-05.d", hi6)
v.assert_true("tick 6 moves the window by 1/144 and 1/160",
              abs((rmax - rmax_7) - 1 / 144) < 1e-15 and abs((rmin16 - rmin_7) - 1 / 160) < 1e-15)

# ---------------------------------------------------------------- lab: divisor table and pull-up closure
v.check("Lab 18-05.a", 100 * baud_err(16_000_000, 9600)[1])
v.assert_true("16 MHz, 9600 baud divisor is 104", baud_err(16_000_000, 9600)[0] == 104)
v.assert_true("48 MHz gives +0.16% at 9600 and 115 200", all(abs(100 * baud_err(48_000_000, b)[1] - 0.16) < 0.005
                                                          for b in (9600, 115200)))
v.assert_true("14.7456 MHz exact at 9600 and 115 200", all(baud_err(14_745_600, b)[1] == 0 for b in (9600, 115200)))
v.assert_true("14.7456 MHz 16x divisor for 1 Mbaud is below 1", 14.7456e6 / (16 * 1e6) < 1)
v.check("Lab 18-05.b", 100 * baud_err(14_745_600, 1_000_000)[1])
for ident, tr, iol in (("Lab 18-05.h", 1000e-9, 3e-3), ("Lab 18-05.i", 300e-9, 3e-3), ("Lab 18-05.j", 120e-9, 20e-3)):
    rp_min = (3.3 - 0.4) / iol
    c_close = brentq(lambda c: tr / (K * c) - rp_min, 1e-13, 1e-8, xtol=1e-20)
    v.check(ident, c_close * 1e12)
v.assert_true("only fast mode closes below its specification limit",
              300e-9 / (K * 2.9 / 3e-3) < 400e-12 and 1000e-9 / (K * 2.9 / 3e-3) > 400e-12
              and 120e-9 / (K * 2.9 / 20e-3) > 550e-12)
v.assert_true("Example 18-05.4's other delays sum to 9 ns", 2 + 1 + 1 + 5 == 9)
v.assert_true("100 characters at 115 200 baud take about 8.7 ms",
              abs(100 * 10 / 115200 - 8.7e-3) < 0.05e-3 and abs(10 / 115200 - 86.8e-6) < 0.05e-6)

v.assert_true("Example 1 caution: a 1.8 V LED with 220 ohm from 3.3 V draws 6.8 mA", round((3.3 - 1.8) / 220 * 1e3, 1) == 6.8)
v.assert_true("Q6: I3C SDR data about 30x fast mode and 12x fast-mode plus", round(11 / (0.4 * 8 / 9)) == 31 and round(11 / (1.0 * 8 / 9)) == 12)
sys.exit(v.finish())
