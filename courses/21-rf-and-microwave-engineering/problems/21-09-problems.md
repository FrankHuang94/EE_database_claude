# Problems 21-09 · The RF Front End: Filters, Switches and Modules

Chapter: [21-09](../chapters/21-09-rf-front-end.md) · Worked solutions: [21-09 solutions](../solutions/21-09-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Resonators use the Butterworth-Van Dyke model of §3.1 with $Q = 2\pi f_sL_m/R_m$; "k²_eff" means the thickness-mode formula $(\pi/2)(f_s/f_p)\cot[(\pi/2)(f_s/f_p)]$. Ladder filters and switches sit between 50 Ω terminations. Noise floors use −174 dBm/Hz at 290 K. Problems marked *(lab)* can be checked with `labs/21-09-lab/frontend.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-09.1 [A]

**BVD elements.** A resonator has its series resonance at 1.8 GHz, $C_0$ = 1.5 pF, a capacitance ratio $C_0/C_m$ = 15 and Q = 1500. Find (a) its anti-resonance, (b) $C_m$, (c) $L_m$ and (d) $R_m$.

### Problem 21-09.2 [A]

**Coupling from a measurement.** A measured resonator has $f_s$ = 3.50 GHz and $f_p$ = 3.60 GHz. Find (a) $k^2_{eff}$ from the exact formula, (b) the small-spacing approximation and (c) the capacitance ratio.

### Problem 21-09.3 [B]

**Can the material cover the band?** A 194 MHz wide TDD band is centred at 2593 MHz. A BAW technology offers $k^2_{eff}$ = 7.5%. (a) What resonance spacing does it give? (b) What is the upper bound on a plain ladder's pass band at this frequency? (c) Can a plain ladder cover the band? (d) What $k^2_{eff}$ would raise the bound to the band's width?

### Problem 21-09.4 [B]

**A two-section ladder.** *(lab)* A ladder of two sections uses series resonators with $f_s$ = 2.45 GHz, $C_0$ = 0.8 pF, and shunt resonators with $C_0$ = 1.6 pF whose anti-resonance is at 2.45 GHz; all have $C_0/C_m$ = 20 and Q = 1500. Find (a) the shunt resonators' series resonance, (b) the insertion loss at 2.45 GHz, and the rejection at (c) 2.30 GHz and (d) 2.60 GHz.

### Problem 21-09.5 [A]

**A TC-SAW duplexer over temperature.** A duplexer at 1.9 GHz has a 20 MHz duplex gap and a TCF of −15 ppm/°C. Over −30 to +85 °C, find (a) the edge drift and (b) its share of the gap. (c) What TCF magnitude keeps the drift within 25% of the gap?

### Problem 21-09.6 [B]

**A higher-power duplexer budget.** A handset transmits 26 dBm at the antenna through a duplexer with 2.5 dB transmit loss and 52 dB TX-to-RX isolation. Find (a) the PA's output and (b) the transmit leakage at the LNA. (c) The LNA's input 1 dB compression point is −20 dBm: what margin remains? (d) The PA's noise in the receive band is −138 dBm/Hz; with a 2.5 dB receiver noise figure and 6 dB margin, what receive-band isolation is needed?

### Problem 21-09.7 [B]

**Filter loss and battery current.** A phone transmits 23 dBm at the antenna for 30% of the time, using a PA of 35% efficiency powered from a 3.85 V battery. Comparing a 3 dB with a 2 dB transmit filter, find (a, b) the PA outputs, (c, d) the DC powers while transmitting, (e) the extra DC power while transmitting, (f) the extra average power and (g) the extra average battery current.

### Problem 21-09.8 [A]

**A switch's figure of merit.** A switch has $R_{on}$ = 1.5 Ω and $C_{off}$ = 80 fF. Find (a) its figure of merit, (b) its cut-off frequency, and as a series switch between 50 Ω ports (c) its on-state loss and (d) its off-state isolation at 3.5 GHz.

### Problem 21-09.9 [B]

**How many transistors?** A switch carries 26 dBm on a 50 Ω line whose antenna can present a 4:1 VSWR. Each transistor tolerates 3.0 V peak and is used with 20% margin (2.4 V). Find (a) the matched peak voltage, (b) the worst-case peak voltage and (c) the number of stacked transistors. (d) If each transistor is made N times wider to keep the stack's $R_{on}$, by what factor does the area grow?

### Problem 21-09.10 [B]

**The width trade.** A process has a figure of merit of 150 fs. A series switch must have 0.2 dB on-state loss. Find (a) the $R_{on}$ required, (b) the resulting $C_{off}$ and (c) the off-state isolation at 2.7 GHz. (d) With a 100 fs process and the same loss, what isolation results?

### Problem 21-09.11 [A]

**Mismatch loss.** Find (a) the mismatch loss at VSWR 4 and (b) at VSWR 2. (c) At what |Γ| and (d) at what VSWR does mismatch cost 1 dB?

### Problem 21-09.12 [B]

**Tuner break-even.** An antenna loaded by a hand presents VSWR 5; a tuner restores VSWR 2. (a, b) What are the mismatch losses before and after? (c) Up to what tuner loss does tuning pay? (d) With a 0.6 dB tuner, what is the net gain?

### Problem 21-09.13 [C]

**Intermodulation in uplink carrier aggregation.** A phone transmits two carriers at 1745 MHz and 1950 MHz, each at 20 dBm at the antenna switch, while receiving a 10 MHz channel at 2155 MHz (receiver NF 4 dB). (a, b) Where do the third-order products $2f_1 - f_2$ and $2f_2 - f_1$ fall, and which lands in the receive channel? (c) With a switch IIP3 of 65 dBm, what is the product's level? (d) What is the receiver's noise floor? (e) What switch IIP3 keeps the product 6 dB below the noise floor?

### Problem 21-09.14 [C]

**Reading the filings.** Skyworks' revenue was $4,086.9 million in fiscal 2025 (Apple 67%) and $3,959.6 million in fiscal 2026 (Apple 61%) (§9). Find (a, b) the Apple revenue in each year, (c) its change in dollars and (d) in percent, and (e, f) the non-Apple revenue in each year and (g) its change in percent. (h, i) The shares are published as whole percentages: how uncertain is each year's Apple revenue as a result?

### Problem 21-09.15 [A]

**Why acoustic resonators are small.** At 3.5 GHz, find (a) the thickness of a half-wavelength AlN resonator ($v$ = 11,000 m/s) and (b) the length of a quarter-wavelength line on a board with $\varepsilon_{eff}$ = 6. (c) What is their ratio?

### Problem 21-09.16 [C]

**Derive the resonator's two resonances.** For a lossless Butterworth-Van Dyke resonator ($R_m$ = 0), (a) show from its admittance that the series resonance is $f_s = 1/(2\pi\sqrt{L_mC_m})$ and the parallel resonance is $f_p = f_s\sqrt{1 + C_m/C_0}$. (b) Now keep a small $R_m$ and show that the impedance at $f_p$ is approximately $1/(\omega_p^2C_0^2R_m)$. (c) Evaluate $f_p$ and the peak impedance for Example 21-09.1's resonator ($C_0$ = 1 pF, $f_s$ = 2.00 GHz, $C_0/C_m$ = 17.44, $R_m$ = 0.694 Ω).

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. BVD model, k² and why acoustic resonators are small | 1, 2, 15, 16 |
| 2. Ladder filters: bandwidth from k², loss from Q | 3, 4 |
| 3. Temperature drift and the duplex gap | 5 |
| 4. Duplexer isolation and loss budgets | 6, 7 |
| 5. Switches, stacking, mismatch and tuning | 8, 9, 10, 11, 12 |
| 6. Coexistence and the industry's structure | 13, 14 |
