# Solutions 23-04 · DRAM Interfaces: DDR, LPDDR and GDDR

Problems: [23-04 problems](../problems/23-04-problems.md) · Chapter: [23-04](../chapters/23-04-dram-interfaces.md)

Every number is recomputed by [verify_23_04.py](../verify/verify_23_04.py).

---

## Solutions

### Solution 23-04.1

(a) $8800/16$ = **550** MHz; (b) $2400/8$ = **300** MHz.

(c) $40 \times 16/8$ = **80** bytes, of which 64 are data. (d) $8/32$ = **25** % of the data bits.

An 8800 MT/s part needs a core 37.5% faster than DDR5-6400's. MRDIMMs avoid that by interleaving two ranks at half the host rate (Example 23-04.2).

### Solution 23-04.2

(a) $8 \times 5600 \times 10^6 \times 64/8$ = **358.4** GB/s.

(b) $8533 \times 10^6 \times 512/8$ = **546.1** GB/s.

(c) $32 \times 10^9 \times 384/8$ = **1536** GB/s, consistent with Micron's "more than 1.5 TB/s" for a 384-bit system at 32 Gb/s.

### Solution 23-04.3

(a) $1/(8.8 \times 10^9)$ = **113.6** ps; (b) $1/(28 \times 10^9)$ = **35.7** ps.

(c) $113.6/6.67$ = **17.0** mm; (d) $35.7/6.67$ = **5.35** mm.

At GDDR7 rates a bit occupies about 5 mm of trace, so a GPU's few-centimetre routes hold several bits each.

### Solution 23-04.4

(a) $V_L = 1.2 \times 48/108$ = **0.533** V; (b) $1.2 - 0.533$ = **0.667** V.

(c) $1.2/108$ = **11.1** mA; (d) $1.2 \times 11.11$ mA = **13.3** mW.

(e) $13.33\ \text{mW}/(3.2 \times 10^9\ \text{s}^{-1})$ = **4.17** pJ; (f) half of that: **2.08** pJ/bit.

Weaker settings give a larger swing and less current per zero, but each bit lasts twice as long at 3200 MT/s, so the energy per bit is higher than DDR5's in Example 23-04.3.

### Solution 23-04.5

(a) $8 \times 0.7$ = **5.6**.

(b) Weight each count of zeros $k$ by its binomial probability $\binom8k0.7^k0.3^{8-k}$ and by the low wires it produces ($k$ for $k \le 4$; $9 - k$ for $k > 4$): **3.06**.

(c) $1 - 3.06/5.6$ = **45.3** %.

DBI helps most when data are biased toward the costly level. With random data it saves 18.3%.

### Solution 23-04.6

(a) $(0.45/0.5)^2$ = **0.81**; (b) **19.0** %.

(c) $0.45^2/80$ = **2.53** mW.

### Solution 23-04.7

(a) $1.0 \times 45/85$ = **0.529** V.

(b) $\Gamma_S = (40 - 45)/85$ = **−0.0588**; (c) $\Gamma_L = (60 - 45)/105$ = **0.143**.

(d) $0.5294 \times 1.143$ = **0.605** V.

(e) The far-end reflection, $0.5294 \times 0.143 = 0.0756$ V, returns to the source, reflects as $0.0756 \times (-0.0588) = -0.00445$ V, and adds $-0.00445 \times 1.143 = -0.00508$ V at the far end: **0.600** V.

(f) $1.0 \times 60/100$ = **0.600** V.

With both ends within 15 Ω of the line, the far end is already within 1% of its final value at the first arrival.

### Solution 23-04.8

(a) $\sqrt{4.2}/c$ = **6.84** ps/mm.

(b) $8 \times 14$ mm = 112 mm, so **766** ps. (c) $766/113.6$ = **6.74** UI.

### Solution 23-04.9

(a) $1/(12.8 \times 10^9)$ = **78.125** ps.

(b) $e^{-78.125/60}$ = **0.272**; (c) $1 - a$ = **0.728**; (d) $h_0a$ = **0.198**.

(e) $1 - 2a$ = **0.456**; (f) $h_0 - (a - h_1)$ = **0.654**; (g) $h_0$ = **0.728**.

(h) $1/(60\ \text{ps} \times \ln 2)$ = **24.0** Gb/s.

### Solution 23-04.10

(a) $32/1.5$ = **21.3** GBd; (b) **10.67** GHz.

(c) NRZ's Nyquist frequency is 16 GHz, so PAM3 wins when $\alpha(16 - 10.67) > 6.02$ dB: α > **1.13** dB/GHz.

(d) $28/1.5/2$ = **9.33** GHz.

### Solution 23-04.11

(a) $1000/51.2$ = 19.5, so **20** channels; (b) $1000/19.2$ = 52.1, so **53** channels; (c) $1000/128$ = 7.8, so **8** devices.

(d) $20 \times 64$ = **1280** pins; (e) $53 \times 16$ = **848** pins; (f) $8 \times 32$ = **256** pins.

(g) $8 \times 4$ GB = **32** GB; (h) $20 \times 64$ GB = **1280** GB.

GDDR7 meets the bandwidth with the fewest pins but the least capacity. DDR5 gives 40 times the capacity at five times the pins. This is the capacity-bandwidth tradeoff that HBM tries to escape (23-05).

### Solution 23-04.12

(a) $0.1638\ \text{nJ}/128$ = **1.28** pJ/bit.

(b) $1.28 + 1.28$ = **2.56** pJ/bit; (c) $0.1638\ \text{nJ}/8192 + 1.277$ pJ = **1.30** pJ/bit.

(d) $1.280 + 0.163$ = **1.44** pJ/bit; (e) $0.020 + 0.163$ = **0.183** pJ/bit.

(f) $1.280/2.557$ = **50** %.

For random access, the DRAM core costs as much as the pins, so low-swing I/O alone saves less than half. For streaming, the pins dominate and LPDDR's I/O saves about a factor of 7.

### Solution 23-04.13

(a) A clock period is 2 UIs = 312.5 ps, so $312.5/128$ = **2.44** ps. (b) $2.44/6.67$ = **0.366** mm.

### Solution 23-04.14

For PAM-$M$ at the same bit rate, the symbol time is $bT$, with $b$ = 1, 1.5 and 2 bits per symbol. The channel's cursors (§3.6) become $h_0 = 1 - y$ and $\sum_{k \ge 1}h_k = y$, with $y = e^{-bx}$. With levels evenly spaced across the full swing, adjacent levels are $2/(M - 1)$ apart at the transmitter and $2h_0/(M - 1)$ apart at the receiver. Worst-case interference shifts each level by up to $\sum|h_k| = y$ toward its neighbour, from both sides. The opening of each eye, as a fraction of the full swing of 2, is therefore

$$
\frac{1}{2}\left[\frac{2(1 - y)}{M - 1} - 2y\right] = \frac{1 - y}{M - 1} - y ,
$$

which gives the three expressions.

**Closing points.** Setting each to zero gives $y = 1/M$: $e^{-x} = 1/2$, $e^{-1.5x} = 1/3$ and $e^{-2x} = 1/4$. So (d) NRZ closes at $x = \ln 2$ = **0.693**, (e) PAM3 at $\ln 3/1.5$ = **0.732** and (f) PAM4 at $\ln 4/2 = \ln 2$ = **0.693**. PAM3 needs a longer bit time than NRZ to open at all, and PAM4 opens at exactly the same point.

**NRZ versus PAM4.** Write $u = e^{-x}$, so $e^{-2x} = u^2$. The difference is

$$
(1 - 2u) - \left[\tfrac13(1 - u^2) - u^2\right] = \tfrac23 - 2u + \tfrac43u^2 = \tfrac23(2u - 1)(u - 1) .
$$

Both factors are negative for $u < 1/2$, which is where the NRZ eye is open, so the difference is positive and is zero only at the shared closing point.

**NRZ versus PAM3.** The difference is $g(u) = \tfrac12 - 2u + \tfrac32u^{3/2}$. Its derivative $-2 + \tfrac94u^{1/2}$ is negative for $u < 0.79$, so $g$ decreases over $0 < u \le \tfrac12$ and is smallest at $u = \tfrac12$, where $g = \tfrac12 - 1 + \tfrac32(0.3536)$ = **0.0303** > 0. Where the NRZ eye is closed ($u > \tfrac12$), PAM3's eye is closed too, since PAM3 needs $u < 3^{-2/3} = 0.481$.

At 48 Gb/s with τ = 20 ps, $x = 20.83/20$: (a) NRZ **0.294**, (b) PAM3 **0.186**, (c) PAM4 **0.167**.

A first-order channel's loss grows too slowly with frequency to repay the amplitude PAM gives up. Real channels with dielectric and skin-effect loss, reflections and crosstalk behave differently (§3.7).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 23-04.1a | core rate, DDR5-8800 | 550 | MHz |
| 23-04.1b | core rate, DDR4-2400 | 300 | MHz |
| 23-04.1c | bytes per ECC burst | 80 | B |
| 23-04.1d | check-bit overhead | 25 | % |
| 23-04.1x | core-rate increase over DDR5-6400 | 37.5 | % |
| 23-04.7x | first arrival's distance from final | 1 | % |
| 23-04.2a | 8-channel DDR5-5600 | 358.4 | GB/s |
| 23-04.2b | 512-bit LPDDR5X-8533 | 546.1 | GB/s |
| 23-04.2c | 384-bit GDDR7 at 32 Gb/s | 1536 | GB/s |
| 23-04.3a | UI at 8800 MT/s | 113.6 | ps |
| 23-04.3b | UI at 28 Gb/s | 35.7 | ps |
| 23-04.3c | distance per UI, 8800 MT/s | 17.0 | mm |
| 23-04.3d | distance per UI, 28 Gb/s | 5.35 | mm |
| 23-04.4a | low level | 0.533 | V |
| 23-04.4b | swing | 0.667 | V |
| 23-04.4c | current | 11.1 | mA |
| 23-04.4c1 | current, 4 s.f. | 11.11 | mA |
| 23-04.4d | power | 13.3 | mW |
| 23-04.4d1 | power, 4 s.f. | 13.33 | mW |
| 23-04.4e | energy of one 0 | 4.17 | pJ |
| 23-04.4f | energy per bit, random | 2.08 | pJ |
| 23-04.5a | low wires per byte, no DBI | 5.6 | |
| 23-04.5b | low wires per byte, DBI | 3.06 | |
| 23-04.5c | saving | 45.3 | % |
| 23-04.6a | power ratio | 0.81 | |
| 23-04.6b | saving | 19.0 | % |
| 23-04.6c | power while driving a 1 | 2.53 | mW |
| 23-04.7a | launched wave | 0.529 | V |
| 23-04.7a1 | launched wave, 4 s.f. | 0.5294 | V |
| 23-04.7b | source reflection coefficient | -0.0588 | |
| 23-04.7c | load reflection coefficient | 0.143 | |
| 23-04.7d | far end, first arrival | 0.605 | V |
| 23-04.7e1 | far-end reflection | 0.0756 | V |
| 23-04.7e2 | re-reflected at the source | -0.00445 | V |
| 23-04.7e3 | second far-end increment | -0.00508 | V |
| 23-04.7e | far end, second arrival | 0.600 | V |
| 23-04.7f | far end, final | 0.600 | V |
| 23-04.8a | delay per millimetre | 6.84 | ps/mm |
| 23-04.8b0 | route length | 112 | mm |
| 23-04.8b | skew | 766 | ps |
| 23-04.8c | skew in UIs | 6.74 | |
| 23-04.9a | UI | 78.125 | ps |
| 23-04.9b | a | 0.272 | |
| 23-04.9c | h0 | 0.728 | |
| 23-04.9d | h1 | 0.198 | |
| 23-04.9e | eye, no equalization | 0.456 | |
| 23-04.9f | eye, one-tap DFE | 0.654 | |
| 23-04.9g | eye, full DFE | 0.728 | |
| 23-04.9h | highest unequalized rate | 24.0 | Gb/s |
| 23-04.10a | symbol rate | 21.3 | GBd |
| 23-04.10b | Nyquist frequency | 10.67 | GHz |
| 23-04.10c | loss slope for PAM3 to win | 1.13 | dB/GHz |
| 23-04.10d | Nyquist frequency at 28 Gb/s | 9.33 | GHz |
| 23-04.11a0 | DDR5 channels, unrounded | 19.5 | |
| 23-04.11a | DDR5 channels | 20 | |
| 23-04.11b0 | LPDDR5X channels, unrounded | 52.1 | |
| 23-04.11b | LPDDR5X channels | 53 | |
| 23-04.11c0 | GDDR7 devices, unrounded | 7.8 | |
| 23-04.11c | GDDR7 devices | 8 | |
| 23-04.11c1 | GDDR7 device bandwidth | 128 | GB/s |
| 23-04.11d | DDR5 data pins | 1280 | |
| 23-04.11e | LPDDR5X data pins | 848 | |
| 23-04.11f | GDDR7 data pins | 256 | |
| 23-04.11g | GDDR7 capacity | 32 | GB |
| 23-04.11h | DDR5 capacity | 1280 | GB |
| 23-04.11x | DDR5 capacity over GDDR7 | 40 | |
| 23-04.11y | DDR5 pins over GDDR7 | 5 | |
| 23-04.12a | activation energy per bit, one burst | 1.28 | pJ/bit |
| 23-04.12b | total, one burst, DDR5 pins | 2.56 | pJ/bit |
| 23-04.12c | total, full row, DDR5 pins | 1.30 | pJ/bit |
| 23-04.12d | total, one burst, LPDDR5X pins | 1.44 | pJ/bit |
| 23-04.12e | total, full row, LPDDR5X pins | 0.183 | pJ/bit |
| 23-04.12f | core share of (b) | 50 | % |
| 23-04.12x | streaming saving from LPDDR pins | 7 | |
| 23-04.13a0 | clock period | 312.5 | ps |
| 23-04.13a | delay step | 2.44 | ps |
| 23-04.13b | trace length per step | 0.366 | mm |
| 23-04.14a | NRZ eye at 20 ps | 0.294 | |
| 23-04.14b | PAM3 eye at 20 ps | 0.186 | |
| 23-04.14c | PAM4 eye at 20 ps | 0.167 | |
| 23-04.14d | NRZ closing x | 0.693 | |
| 23-04.14e | PAM3 closing x | 0.732 | |
| 23-04.14f | PAM4 closing x | 0.693 | |
| 23-04.14g | NRZ minus PAM3 at the NRZ closing point | 0.0303 | |
| 23-04.14g1 | (1/2)^(3/2) | 0.3536 | |
| 23-04.14h | u where g' = 0 | 0.79 | |
| 23-04.14i | PAM3 opening threshold on u | 0.481 | |
| 23-04.14j | NRZ bit time at 48 Gb/s | 20.83 | ps |
