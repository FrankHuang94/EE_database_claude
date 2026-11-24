# Problems 21-01 · S-Parameters and Network Analysis

Chapter: [21-01](../chapters/21-01-s-parameters.md) · Worked solutions: [21-01 solutions](../solutions/21-01-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $Z_0$ = 50 Ω unless stated; angles in degrees; return loss is a positive number of dB. Problems marked *(lab)* can be checked with `labs/21-01-lab/sparam.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-01.1 [A]

**Two loads.** Find Γ, return loss, VSWR and mismatch loss for a 100 Ω load and for a 25 Ω load. Why are the magnitudes the same?

### Problem 21-01.2 [A]

**A specification.** A filter's input is specified at 20 dB return loss. What are $\lvert\Gamma\rvert$, the VSWR and the mismatch loss?

### Problem 21-01.3 [B] *(lab)*

**A shunt capacitor.** Find $S_{11}$ and $S_{21}$ (magnitude and angle) of a 1 pF shunt capacitor at 2 GHz, and its insertion loss.

### Problem 21-01.4 [A]

**Derive it.** Starting from the definitions of §3.1, derive $S_{11} = -YZ_0/(2 + YZ_0)$ and $S_{21} = 2/(2 + YZ_0)$ for a shunt admittance $Y$.

### Problem 21-01.5 [B] *(lab)*

**From Z to S.** A resistive T-network has series arms of 20 Ω and a 100 Ω shunt arm, so $Z_{11} = Z_{22}$ = 120 Ω and $Z_{12} = Z_{21}$ = 100 Ω. Find its S-matrix, its insertion loss and the fraction of power it absorbs.

### Problem 21-01.6 [B] *(lab)*

**A quarter-wave line.** Find the S-parameters of a lossless 70.71 Ω line a quarter wavelength long in a 50 Ω system. What input impedance does it present when its far end is terminated in 100 Ω?

### Problem 21-01.7 [B] *(lab)*

**A cascade.** A 3 dB π attenuator in 50 Ω has shunt arms $R_{sh} = Z_0(k_a + 1)/(k_a - 1)$ and series arm $R_{se} = Z_0(k_a^2 - 1)/(2k_a)$ with the voltage ratio $k_a = 10^{3/20}$ (not the stability factor K). Find the resistors. Two such pads are joined by a matched line of 60°. Find the overall $S_{21}$ (dB and angle) with transfer matrices.

### Problem 21-01.8 [A]

**De-embedding lines.** A two-port is measured through matched 30° lines on each side, giving $S_{21}$ = 0.8∠−100°. What is the device's own $S_{21}$?

### Problem 21-01.9 [B] *(lab)*

**Another calibration.** A reflectometer reads $M_S = -0.5088 + j0.6565$, $M_O = 0.5963 - j0.6477$ and $M_L = -0.0200 + j0.0400$ for ideal standards, and $M = -0.2710 + j0.0022$ for a device. Find $e_{11}$, the tracking term (magnitude and angle) and the device's reflection.

### Problem 21-01.10 [B]

**Check the data.** A measured two-port has $S_{11}$ = 0.2∠30°, $S_{21}$ = 0.9∠−80°, $S_{12}$ = 0.5∠−80° and $S_{22}$ = 0.3∠10°. Is it reciprocal? Is it lossless? What fraction of power entering port 1 is absorbed, and what kind of device might it be?

### Problem 21-01.11 [B] *(lab)*

**Stability test.** A transistor has $S_{11}$ = 0.7∠−120°, $S_{21}$ = 3.5∠90°, $S_{12}$ = 0.08∠40° and $S_{22}$ = 0.45∠−50°. Find $\lvert\Delta\rvert$, K, μ and the MSG. Is it unconditionally stable?

### Problem 21-01.12 [C] *(lab)*

**Stabilize it.** For the transistor of Problem 11, find the shunt resistor across the output that makes μ = 1, and the maximum available gain that results. Why does a shunt output resistor leave the MSG unchanged?

### Problem 21-01.13 [C]

**De-embed a fixture.** A shunt resistor is measured between two series 5 Ω fixture resistors, giving $S_{11} = S_{22}$ = −0.1052 and $S_{21} = S_{12}$ = 0.7130 (real). Convert to ABCD, remove the fixtures, and identify the shunt resistor and its own S-parameters.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Waves, Γ, return loss, VSWR, insertion loss | 1, 2, 3 |
| 2. S of simple two-ports and conversions | 3, 4, 5, 6 |
| 3. Reciprocity and losslessness checks | 5, 10 |
| 4. Reference planes, cascades, de-embedding | 7, 8, 13 |
| 5. VNA calibration | 9 |
| 6. Stability and gain | 11, 12 |
