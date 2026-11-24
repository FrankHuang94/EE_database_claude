# Solutions 21-12 · Modem Baseband Architecture and Wireless Standards

Problems: [21-12 problem set](../problems/21-12-problems.md) · Chapter: [21-12](../chapters/21-12-modem-baseband-and-standards.md). Every number below is recomputed by [verify_21_12.py](../verify/verify_21_12.py).

---

## Solutions

### Solution 21-12.1

(a) $4 \times 8 \times 0.9258 \times 273 \times 12 \times 28{,}000 \times 0.86$ = **2337.0** Mb/s.

(b) At 15 kHz there are 14,000 symbols per second: $2 \times 6 \times 0.9258 \times 106 \times 12 \times 14{,}000 \times 0.86$ = **170.1** Mb/s.

(c) $2 \times 2337.0 + 170.1$ = **4844.1** Mb/s.

### Solution 21-12.2

(a) 2,019,360 bits/ms = **2.019** Gb/s. (b) **3.532** Gb/s.

### Solution 21-12.3

(a) $16.2 \times 10^9 \times 0.020/8$ = **40.5** MB. (b) $\times 0.050$: **101.25** MB. Wider spacing shortens the round trip and the buffer.

### Solution 21-12.4

The 40 MHz carrier carries 1134.3 Mb/s (Example 21-12.1).

(a) $1134.3 \times 10^6 \times 0.5 \times 10^{-3}$ = **0.567** Mb. (b) $/(2/3)$ = **0.851** Mb.

(c) $32 \times 0.851 \times 10^6 \times 5/8$ = **17.0** MB.

### Solution 21-12.5

(a) $12.5 \times 10^9 \times 5.14 \times 10^{-12}$ = **64.3** mW. (b) **732.5** mW. (c) 12.5/2.38 = 5.25, so **6** decoders.

### Solution 21-12.6

$2048 \times 12 = 24{,}576$ per FFT; $14 \times 8000$ = 112,000 symbols/s: **2.75** billion complex multiplications per second, the same as the 100 MHz FR1 carrier with four antennas, because FR2 carriers trade more symbols per second for a similar FFT size.

### Solution 21-12.7

(a) $2 \times 936 \times 12 \times \tfrac56/13.6\ \mu\text{s}$ = **1376.5** Mb/s. (b) Over 16 µs symbols: **1170.0** Mb/s, 15% less, the price of the longer guard interval that outdoor and large-room channels need.

### Solution 21-12.8

(a) $\tau$ = 10/c = **33.36** ns.

(b) The single-sided error is $(e_A - e_B)T_{reply}/2 = 20 \times 10^{-6} \times 10^{-3}/2$ = 10 ns, **3.00** m.

(c) Measured: $T_{r1} = (2\tau + 1\ \text{ms})(1 + 10^{-5})$, $T_{d1} = 1\ \text{ms}(1 - 10^{-5})$, $T_{r2} = (2\tau + 0.5\ \text{ms})(1 - 10^{-5})$, $T_{d2} = 0.5\ \text{ms}(1 + 10^{-5})$. The formula gives an error of **−1.0e-6** mm. The reply-time terms cancel even though the replies differ, and the residual, about the range times the mean clock offset $(e_A + e_B)/2$, vanishes here because the two offsets are equal and opposite; with both clocks 10 ppm fast it would be 0.1 mm.

### Solution 21-12.9

(a) $d = c \times (2\pi/5)/(4\pi \times 2 \times 10^6)$ = **14.99** m. (b) $c/(2 \times 2 \times 10^6)$ = **74.9** m.

### Solution 21-12.10

(a) $1575.42^2/(1575.42^2 - 1227.60^2)$ = **2.546**. (b) **−1.546**.

(c) $\sqrt{2.546^2 + 1.546^2}$ = **2.98**: L1/L2 amplifies noise more than L1/L5 (2.59), because the frequencies are closer together.

(d) **120**.

### Solution 21-12.11

(a) $1.54 \times 10^9 \times 6911/c$ = **35.5** kHz.

(b) $4 \times 1075\ \text{km}/c$ = **14.34** ms. (c) **15**: just inside the 16 processes of terrestrial NR, which is why low-orbit NTN can keep HARQ while geostationary cannot.

### Solution 21-12.12

(a) 50 Gb/s / 500 Mb/s = **100**. (b) 200 Gb/s / 300 Mb/s = **667**.

### Solution 21-12.13

(a) 6004/3957 − 1 = **51.7** %. (b) 7132/6617 − 1 = **7.8** %. (c) 27,793/38,367 = **72.4** %.

Automotive and IoT growth offset part of a 13% handset decline: the diversification the 10-K describes.

### Solution 21-12.14

7.5 ms / 375 µs = **20** times.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 21-12.1a | one 100 MHz carrier | 2337.0 | Mb/s |
| 21-12.1b | 20 MHz carrier | 170.1 | Mb/s |
| 21-12.1c | total | 4844.1 | Mb/s |
| 21-12.2a | Category 20 peak | 2.019 | Gb/s |
| 21-12.2b | Category 26 peak | 3.532 | Gb/s |
| 21-12.3a | L2 buffer, 120 kHz | 40.5 | MB |
| 21-12.3b | L2 buffer, 15 kHz | 101.25 | MB |
| 21-12.4a | information bits per slot | 0.567 | Mb |
| 21-12.4b | coded bits per process | 0.851 | Mb |
| 21-12.4c | soft buffer | 17.0 | MB |
| 21-12.5a | power at 5.14 pJ/b | 64.3 | mW |
| 21-12.5b | power at 58.6 pJ/b | 732.5 | mW |
| 21-12.5c | parallel decoders | 6 | |
| 21-12.6 | FFT multiplications per second | 2.75 | billion |
| 21-12.7a | rate, 0.8 µs guard | 1376.5 | Mb/s |
| 21-12.7b | rate, 3.2 µs guard | 1170.0 | Mb/s |
| 21-12.8a | flight time | 33.36 | ns |
| 21-12.8b | single-sided error | 3.00 | m |
| 21-12.8c | double-sided error | −1.0e-6 | mm |
| 21-12.9a | distance | 14.99 | m |
| 21-12.9b | unambiguous range | 74.9 | m |
| 21-12.10a | L1 coefficient | 2.546 | |
| 21-12.10b | L2 coefficient | −1.546 | |
| 21-12.10c | noise amplification | 2.98 | |
| 21-12.10d | L2 / 10.23 MHz | 120 | |
| 21-12.11a | Doppler at 1.54 GHz | 35.5 | kHz |
| 21-12.11b | four-leg round trip | 14.34 | ms |
| 21-12.11c | HARQ processes | 15 | |
| 21-12.12a | smallest ratio | 100 | |
| 21-12.12b | largest ratio | 667 | |
| 21-12.13a | automotive growth | 51.7 | % |
| 21-12.13b | IoT growth | 7.8 | % |
| 21-12.13c | handset share, FY2025 | 72.4 | % |
| 21-12.14 | interval reduction | 20 | |
