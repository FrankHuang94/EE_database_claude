# Problems 21-11 · Link Budgets

Chapter: [21-11](../chapters/21-11-link-budgets.md) · Worked solutions: [21-11 solutions](../solutions/21-11-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Thermal noise is −174 dBm/Hz (290 K); $10\log_{10}k$ = −228.6 dBW/K/Hz. Shadowing is lognormal, fast fading Rayleigh, and combined margins use the Suzuki integral of §3.3. Problems marked *(lab)* can be checked with `labs/21-11-lab/linkbudget.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-11.1 [A]

**Does it close?** A transmitter's PA delivers 20 dBm; 2 dB is lost before a 3 dBi antenna. The path loss is 110 dB and walls add 8 dB. The receiver has a 0 dBi antenna, 1 dB of front-end loss and −95 dBm sensitivity, and the design needs 6 dB of margin. Find (a) the EIRP, (b) the received power, (c) the margin over sensitivity and (d) the shortfall against the design margin.

### Problem 21-11.2 [A]

**Range per decibel.** For path-loss exponents (a) 2, (b) 3 and (c) 4, by what percentage does each decibel extend the range? (d–f) What range factor does 6 dB buy in each case?

### Problem 21-11.3 [B]

**Sensitivity in rate form.** A receiver with a 7 dB noise figure needs $E_b/N_0$ = 12 dB. Find its sensitivity at (a) 1 Mb/s and (b) 125 kb/s. What is Shannon's minimum $E_b/N_0$ at (c) 0.1 b/s/Hz and (d) 4 b/s/Hz?

### Problem 21-11.4 [B]

**A middle Wi-Fi rate.** *(lab)* With the 802.11ax numerology of Example 21-11.5, find (a) the single-stream 20 MHz rate of MCS7 (64-QAM, rate 5/6). (b) Its IEEE minimum sensitivity is −64 dBm against −82 dBm for MCS0: what is the difference, and (c) how much of it is the rate ratio alone?

### Problem 21-11.5 [B]

**Margins in an urban macro cell.** *(lab)* 3GPP's urban-macro NLOS shadowing has σ = 6 dB. For 5% outage find (a) the shadowing margin, (b) the Rayleigh margin, (c) the combined margin and (d) the naive sum.

### Problem 21-11.6 [B]

**Area coverage in a macro cell.** *(lab)* With σ = 6 dB and the urban-macro NLOS slope (exponent 3.908), what area coverage results from (a) 90% and (b) 95% at the cell edge?

### Problem 21-11.7 [A]

**Noise rise.** What interference margin does a cell need at (a) 30%, (b) 60% and (c) 90% load?

### Problem 21-11.8 [B]

**Building penetration at 3.5 GHz.** TR 38.901 models an external wall as $PL_{tw} = 5 - 10\log_{10}\sum_i p_i10^{-L_i/10}$, with standard glass $L = 2 + 0.2f$, IRR (coated) glass $L = 25.4 + 0.11f$ and concrete $L = 5 + 4f$ ($f$ in GHz). Find (a–c) the three material losses at 3.5 GHz, (d) the low-loss building (30% standard glass, 70% concrete), (e) the high-loss building (70% IRR glass, 30% concrete) and (f) their difference.

### Problem 21-11.9 [B]

**What 3 dB of uplink is worth.** In a network whose path loss grows at 39.08 dB/decade, a 3 dB better uplink extends the cell radius by what factor (a), its area by what factor (b), and saves what percentage of sites for the same area (c)?

### Problem 21-11.10 [C]

**NB-IoT with 3.75 kHz subcarriers.** NB-IoT's uplink can use single 3.75 kHz subcarriers. For the 164 dB target with a 23 dBm device and a 5 dB base-station noise figure, find (a) the noise in 3.75 kHz, (b) the SNR the base station must work at and (c) the repetitions needed if one transmission needs 1 dB (round up to a power of 2).

### Problem 21-11.11 [B]

**LoRa's budgets.** LoRa's raw bit rate is $SF \cdot BW/2^{SF}$ times the code rate (4/5). Find the SF12 rates in (a) 10.4 kHz and (b) 125 kHz. With +22 dBm and sensitivities of −148 and −137 dBm, find (c, d) the two budgets and (e) the range ratio between them at path-loss exponent 3.5.

### Problem 21-11.12 [C]

**A geostationary satellite to a phone.** 3GPP's study also analyses a geostationary satellite (uplink G/T 19 dB/K, path loss 190.6 dB at 2 GHz) receiving a 23 dBm handheld, with the same 5.3 dB of extra losses as Example 21-11.8. Find (a) the uplink C/N0 and (b) the CNR in 360 kHz.

### Problem 21-11.13 [C]

**Interference from a satellite.** The FCC's out-of-band limit for satellite direct-to-cell service is −120 dBW/m²/MHz, waived to −110.6 dBW/m²/MHz for one operator (§9). At 1.9 GHz, find (a) the effective aperture of a 0 dBi antenna in dB(m²) and the received power in a 0 dBi antenna (b) at the limit and (c) at the waiver. Against a phone noise floor of −108 dBm/MHz (6 dB noise figure), find the interference-to-noise ratio (d) at the limit, (e) at the waiver and (f) at the waiver with 3 dB of polarization loss.

### Problem 21-11.14 [B]

**GPS with a worse front end.** At the −128.5 dBm GPS minimum and a 3 dB noise figure, find (a) the C/N0, (b) the SNR in 2 MHz, (c) the processing gain of correlating 1023 chips and (d) the SNR after a 20 ms coherent integration.

### Problem 21-11.15 [A]

**From BER to PER.** Bluetooth's sensitivity test uses 0.1% BER for 37-byte payloads (368 counted bits) and 0.017% for 255-byte payloads (255 × 8 + 72 counted bits). Assuming independent bit errors, find the packet-error rate for (a) the 37-byte and (b) the 255-byte case, and (c) the number of counted bits in the latter.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. The ledger, MAPL and range | 1, 2, 9 |
| 2. Sensitivity in rate form and the rate–range trade | 3, 4, 11 |
| 3. Margins and coverage probability | 5, 6 |
| 4. Interference, penetration and uplink limits | 7, 8, 9 |
| 5. Complete budgets: BLE, Wi-Fi, NR, IoT, satellite, GNSS | 10, 12, 13, 14, 15 |
