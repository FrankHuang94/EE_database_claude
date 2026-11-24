# Problems 21-12 · Modem Baseband Architecture and Wireless Standards

Chapter: [21-12](../chapters/21-12-modem-baseband-and-standards.md) · Worked solutions: [21-12 solutions](../solutions/21-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** NR rates use the TS 38.306 formula of §3.1 with $R_{max}$ = 948/1024, $f$ = 1 and the stated overhead; 30 kHz carriers of 100 and 40 MHz have 273 and 106 resource blocks, a 20 MHz carrier at 15 kHz has 106. Wi-Fi symbols are 12.8 µs plus the guard interval. $c$ = 299,792,458 m/s; $GM$ = 3.986 × 10¹⁴ m³/s²; $R_E$ = 6371 km. Problems marked *(lab)* can be checked with `labs/21-12-lab/modem.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-12.1 [A]

**A mid-range modem.** *(lab)* A phone aggregates two 100 MHz carriers (30 kHz, 4 layers, 256-QAM) and one 20 MHz carrier (15 kHz, 2 layers, 64-QAM), with 14% overhead. Find (a) the rate of one 100 MHz carrier, (b) of the 20 MHz carrier and (c) the total.

### Problem 21-12.2 [A]

**LTE's top categories.** LTE downlink Category 20 carries at most 2,019,360 bits and Category 26 at most 3,531,888 bits per 1 ms TTI. What peak rates are these (a, b)?

### Problem 21-12.3 [B]

**Layer-2 buffers.** A modem rated 12.5 Gb/s down and 3.7 Gb/s up needs what layer-2 buffer by the 3GPP formula (a) at 120 kHz spacing (RLC round trip 20 ms) and (b) at 15 kHz (50 ms)?

### Problem 21-12.4 [B]

**Soft buffer for a 40 MHz carrier.** *(lab)* For a 40 MHz carrier at 1024-QAM with 4 layers (0.5 ms slots), find (a) the information bits per slot and (b) the coded bits stored per HARQ process ($R_{LBRM}$ = 2/3). (c) With 32 processes and 5-bit LLRs, what soft buffer does it need?

### Problem 21-12.5 [B]

**Decoding the X85's peak.** At 12.5 Gb/s, what does decoding cost at (a) 5.14 pJ/b and (b) 58.6 pJ/b? (c) How many 2.38 Gb/s decoders would be needed in parallel?

### Problem 21-12.6 [A]

**FFT load at millimetre wave.** A 400 MHz FR2 carrier at 120 kHz has 264 resource blocks and uses a 4096-point FFT, with 14 symbols per 0.125 ms slot. How many complex multiplications per second does each receive stream's FFT need?

### Problem 21-12.7 [A]

**An 80 MHz Wi-Fi 7 link.** At 80 MHz an 802.11be symbol has 980 data subcarriers (a quarter of the 320 MHz plan's 3920). Find the two-stream rate at 4096-QAM, rate 5/6, with (a) a 0.8 µs guard interval and (b) a 3.2 µs guard interval.

### Problem 21-12.8 [C]

**Double-sided ranging.** *(lab)* Two UWB devices are 10 m apart. A's clock runs 10 ppm fast and B's 10 ppm slow. A sends; B replies after 1 ms; A replies again after 0.5 ms. Each device times its intervals with its own clock. Find (a) the true flight time, (b) the single-sided range error and (c) the double-sided range error, using $\hat\tau = (T_{r1}T_{r2} - T_{d1}T_{d2})/(T_{r1} + T_{r2} + T_{d1} + T_{d2})$ with the measured round ($T_r$) and reply ($T_d$) times.

### Problem 21-12.9 [B]

**Phase-based ranging with 2 MHz steps.** Two tones 2 MHz apart show a round-trip phase difference of 72°. Find (a) the distance and (b) the unambiguous range.

### Problem 21-12.10 [B]

**The older dual-frequency pair.** GPS L2 is at 1227.60 MHz. For L1/L2, find (a, b) the ionosphere-free coefficients and (c) the noise amplification. (d) L2 is what multiple of 10.23 MHz?

### Problem 21-12.11 [B]

**L-band satellite downlink.** For the 600 km satellite of Example 21-12.10, find (a) the largest Doppler shift at 1.54 GHz. With a transparent payload and a gateway at the same slant range, the round trip is four 1075 km legs: (b) how long is it, and (c) how many 1 ms HARQ processes fill it?

### Problem 21-12.12 [A]

**6G targets.** The ITU's IMT-2030 summary gives peak rates of 50–200 Gb/s and experienced rates of 300–500 Mb/s. Find the peak-to-experienced ratio (a) at its smallest and (b) at its largest.

### Problem 21-12.13 [B]

**Reading Qualcomm's segments.** QCT revenue in fiscal 2025 and 2026 was: handsets $27,793M and $24,072M, automotive $3,957M and $6,004M, IoT $6,617M and $7,132M (total $38,367M in 2025). Find (a) automotive growth, (b) IoT growth and (c) the handset share of QCT in fiscal 2025.

### Problem 21-12.14 [A]

**Shorter Bluetooth intervals.** Bluetooth Core 6.2 cuts the minimum connection interval from 7.5 ms to 375 µs. By what factor?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. The datapath and its compute | 6 |
| 2. Peak rates from the capability formula | 1, 2, 12 |
| 3. Decoder, HARQ and layer-2 sizing | 3, 4, 5 |
| 4. Wi-Fi rates from the tone plan | 7 |
| 5. Ranging: UWB, Bluetooth, GNSS | 8, 9, 10 |
| 6. Satellites and the standards map | 11, 13, 14 |
