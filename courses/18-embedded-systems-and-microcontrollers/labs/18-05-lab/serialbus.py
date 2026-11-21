"""Lab 18-05: arithmetic of GPIO pins and serial buses.

- UART: frame time and throughput, integer and fractional baud divisors and their error, and the clock-mismatch
  window of a receiver that samples each bit once at its centre (the model of hdl/uart_rx.v);
- SPI: maximum clock from the timing loop of a read;
- I2C: pull-up resistor range from the sink-current and rise-time limits, rise time, transaction length and time;
- GPIO: LED series resistor from worst-case output levels, and series resistors that limit injection current.
"""
from __future__ import annotations

import math


# ------------------------------------------------------------------ UART
def uart_frame_bits(data_bits=8, parity=False, stop_bits=1) -> int:
    return 1 + data_bits + (1 if parity else 0) + stop_bits


def uart_bytes_per_s(baud: float, frame_bits: int = 10) -> float:
    return baud / frame_bits


def baud_divisor(f_clk: float, baud: float, oversample: int = 16, frac_bits: int = 0) -> float:
    """Divisor f_clk / (oversample * baud), rounded to the nearest multiple of 2^-frac_bits."""
    exact = f_clk / (oversample * baud)
    q = 2 ** frac_bits
    return round(exact * q) / q


def baud_error(f_clk: float, baud: float, oversample: int = 16, frac_bits: int = 0) -> float:
    """Relative error of the achieved baud rate (negative = slower than requested)."""
    div = baud_divisor(f_clk, baud, oversample, frac_bits)
    return f_clk / (oversample * div) / baud - 1


def uart_ratio_window(frame_bits: int = 10, oversample: int = 16) -> tuple[float, float]:
    """Range of r = (sender bit time) / (receiver bit time) accepted by a receiver that detects the start edge
    within one tick (1/oversample bit) and samples bit k at (detection) + 1/2 + k bits, the stop bit being
    k = frame_bits - 1, in a continuous stream. Slow sender: sample k must not precede the sender's bit k,
    worst with zero detection delay; fast sender: it must precede the end of bit k, worst with a full tick."""
    k = frame_bits - 1
    r_max = (k + 0.5) / k
    r_min = (k + 0.5 + 1 / oversample) / (k + 1)
    return r_min, r_max


def uart_sender_rate_tolerance(frame_bits: int = 10, oversample: int = 16) -> tuple[float, float]:
    """The same window as sender baud-rate deviations: (most negative, most positive) relative error."""
    r_min, r_max = uart_ratio_window(frame_bits, oversample)
    return 1 / r_max - 1, 1 / r_min - 1


# ------------------------------------------------------------------ SPI
def spi_max_clock(t_sck_out: float, t_wire: float, t_co: float, t_setup: float) -> float:
    """Highest SCK when the controller samples MISO half a period after the edge that launched it:
    half period >= SCK output delay + wire + target clock-to-output + wire back + controller setup."""
    half = t_sck_out + t_wire + t_co + t_wire + t_setup
    return 1 / (2 * half)


# ------------------------------------------------------------------ I2C
def i2c_rp_min(vdd: float, vol_max: float = 0.4, iol: float = 3e-3) -> float:
    return (vdd - vol_max) / iol


def i2c_rp_max(t_rise_max: float, cb: float) -> float:
    """From t_r = 0.8473 Rp Cb (30% to 70% of VDD on an RC rise)."""
    return t_rise_max / (0.8473 * cb)


def rc_rise_30_70(rp: float, cb: float) -> float:
    return rp * cb * math.log(0.7 / 0.3)


def i2c_read_clocks(n_data: int, reg_addr_bytes: int = 1) -> int:
    """Clock periods for: START, address+W, register address, repeated START, address+R, n data bytes, STOP,
    counting 9 clocks per byte (8 bits and the acknowledge) and one period each for START, Sr and STOP."""
    return 9 * (1 + reg_addr_bytes + 1 + n_data) + 3


# ------------------------------------------------------------------ GPIO
def led_resistor_min(v_out_max: float, v_led: float, i_max: float) -> float:
    return (v_out_max - v_led) / i_max


def led_current(v_out: float, v_led: float, r: float) -> float:
    return (v_out - v_led) / r


def injection_resistor(v_in: float, vdd: float, v_diode: float, i_inj_max: float) -> float:
    """Series resistor keeping the current through the pin's clamp diode at or below i_inj_max."""
    return (v_in - vdd - v_diode) / i_inj_max


E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def e12_at_least(x: float) -> float:
    dec = 10 ** math.floor(math.log10(x))
    for m in E12 + [10.0]:
        if m * dec >= x * (1 - 1e-12):
            return m * dec
    return 10 * dec
