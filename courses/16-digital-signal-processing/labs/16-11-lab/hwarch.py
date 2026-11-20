"""DSP-hardware toolkit for Lab 16-11: MAC sizing, folding, iteration bounds, look-ahead, CSD and CORDIC.

Functions
- mac_widths(bx, bc, taps)            (product bits, accumulator bits) for bx-bit data, bc-bit coefficients, taps terms
- units_needed(mults_per_output, fs, f_clk)   multipliers needed when each runs at f_clk (time-multiplexed)
- iteration_bound(loops)              max over loops of (total delay of operations in the loop / registers in the loop);
                                      loops is a list of (computation_time, registers)
- iir1(a, x), iir1_lookahead2(a, x)   y[n] = a y[n-1] + x[n] and its look-ahead form
                                      y[n] = a^2 y[n-2] + x[n] + a x[n-1], which must agree exactly
- csd(value, frac_bits)               canonical signed-digit form of round(value * 2^frac_bits): list of (sign, shift)
- csd_adders(value, frac_bits)        adders/subtractors needed for a shift-and-add constant multiplier (nonzero digits - 1)
- cordic_gain(n)                      K_n = prod sqrt(1 + 2^(-2i)), i = 0..n-1
- cordic_rotate(theta, n)             floating-point CORDIC in rotation mode: (cos, sin) after n iterations
- cordic_vector(x, y, n)              floating-point CORDIC in vectoring mode: (magnitude, angle)
- ANGLE_BITS, FRAC, cordic_fixed(theta_code, n=14)   bit-exact model of cordic.v: 16-bit binary angle (2^15 = pi),
                                      x, y in Q2.14 starting from x0 = round(2^14 / K_n), arithmetic right shifts;
                                      returns (x, y, z) integers
"""
from __future__ import annotations

import math

import numpy as np

ANGLE_BITS = 16
FRAC = 14


def mac_widths(bx, bc, taps):
    prod = bx + bc
    return prod, prod + math.ceil(math.log2(taps))


def units_needed(mults_per_output, fs, f_clk):
    return math.ceil(mults_per_output * fs / f_clk)


def iteration_bound(loops):
    return max(t / r for t, r in loops)


def iir1(a, x):
    y, prev = [], 0.0
    for xn in x:
        prev = a * prev + xn
        y.append(prev)
    return np.array(y)


def iir1_lookahead2(a, x):
    y = [0.0, 0.0]
    xp = 0.0
    out = []
    for xn in x:
        yn = a * a * y[-2] + xn + a * xp
        out.append(yn)
        y.append(yn)
        xp = xn
    return np.array(out)


def csd(value, frac_bits):
    n = int(round(value * 2**frac_bits))
    digits, k = [], 0
    while n != 0:
        if n & 1:
            d = 2 - (n & 3)  # +1 if n % 4 == 1, -1 if n % 4 == 3
            n -= d
            digits.append((d, k - frac_bits))
        n >>= 1
        k += 1
    return digits


def csd_adders(value, frac_bits):
    return max(len(csd(value, frac_bits)) - 1, 0)


def cordic_gain(n):
    return math.prod(math.sqrt(1 + 2.0 ** (-2 * i)) for i in range(n))


def cordic_rotate(theta, n):
    x, y, z = 1 / cordic_gain(n), 0.0, theta
    for i in range(n):
        d = 1.0 if z >= 0 else -1.0
        x, y, z = x - d * y * 2.0**-i, y + d * x * 2.0**-i, z - d * math.atan(2.0**-i)
    return x, y


def cordic_vector(x, y, n):
    z = 0.0
    for i in range(n):
        d = -1.0 if y >= 0 else 1.0
        x, y, z = x - d * y * 2.0**-i, y + d * x * 2.0**-i, z - d * math.atan(2.0**-i)
    return x / cordic_gain(n), z


def atan_table(n):
    return [int(round(math.atan(2.0**-i) / math.pi * 2 ** (ANGLE_BITS - 1))) for i in range(n)]


def cordic_fixed(theta_code, n=14):
    """Bit-exact model of cordic.v for any 16-bit binary angle (2^15 = pi).

    A quadrant stage first maps |theta| > pi/2 into [-pi/2, pi/2] by subtracting or adding pi (2^15) and remembers to
    negate both outputs, since cos(theta -/+ pi) = -cos(theta) and likewise for sin. Returns (x, y, z) after n
    iterations, with z the residual angle code of the reduced angle.
    """
    z = int(theta_code)
    flip = False
    if z > 2 ** (ANGLE_BITS - 2):
        z, flip = z - 2 ** (ANGLE_BITS - 1), True
    elif z < -(2 ** (ANGLE_BITS - 2)):
        z, flip = z + 2 ** (ANGLE_BITS - 1), True
    x = int(round(2**FRAC / cordic_gain(n)))
    y = 0
    for i, at in enumerate(atan_table(n)):
        if z >= 0:
            x, y, z = x - (y >> i), y + (x >> i), z - at
        else:
            x, y, z = x + (y >> i), y - (x >> i), z + at
    return (-x, -y, z) if flip else (x, y, z)
