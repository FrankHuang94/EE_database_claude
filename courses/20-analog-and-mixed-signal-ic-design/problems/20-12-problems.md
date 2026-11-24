# Problems 20-12 · Why Analog Does Not Scale Like Digital

Chapter: [20-12](../chapters/20-12-why-analog-does-not-scale.md) · Worked solutions: [20-12 solutions](../solutions/20-12-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** T = 300 K, so kT = 4.142 × 10⁻²¹ J. A sine of peak amplitude $A$ sampled on $C$ has SNR = $(A^2/2)/(kT/C)$. A class-A stage with feedback factor β reaches closed-loop bandwidth $f = \beta g_m/(2\pi C)$ and draws $I = g_m/(g_m/I_D)$ from $V_{DD}$. Problems marked *(lab)* can be checked with `labs/20-12-lab/scaling.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-12.1 [A]

**Two nodes.** A process is scaled at constant field by $S$ = 2. Give the factors for a gate's delay, switching energy and area, and for a noise-limited analog stage's capacitance and power at fixed SNR, bandwidth, swing fraction and $g_m/I_D$.

### Problem 20-12.2 [A]

**The floor.** Find the rms kT/C noise on 0.5 pF and on 2 pF.

### Problem 20-12.3 [B] *(lab)*

**Sizing for 80 dB.** What sampling capacitance gives SNR = 80 dB for a sine of 0.4 V peak?

### Problem 20-12.4 [B] *(lab)*

**Driving it.** The capacitor of Problem 3 is driven from a 1.0 V supply at 50 MHz closed-loop bandwidth with β = 0.5 and $g_m/I_D$ = 15 V⁻¹. Find the power.

### Problem 20-12.5 [B]

**Swing that does not scale.** A stage's peak-to-peak swing is $V_{DD}$ − 0.3 V. By what factor must its sampling capacitance grow, at fixed SNR, when the supply falls from 1.2 V to 0.7 V? Compare with the factor if the swing were proportional to the supply.

### Problem 20-12.6 [A]

**Gain against length.** A process has $V_A' = 5$ V/µm. Find the intrinsic gain (ratio and dB) at $g_m/I_D$ = 10 V⁻¹ for L = 0.1 µm and L = 0.4 µm.

### Problem 20-12.7 [B]

**Two stacks.** On a 0.9 V supply with $V_{DS,sat}$ = 0.12 V per device, find the swing left by a five-device telescopic stack and by a four-device output branch.

### Problem 20-12.8 [B]

**Mismatch or noise, in a FinFET-like process.** With $A_{VT}$ = 1.5 mV·µm and $C_{ox}$ = 25 fF/µm², find the ratio $C_{ox}A_{VT}^2/kT$, and the capacitances that mismatch and kT/C noise each demand for a 0.2 mV error.

### Problem 20-12.9 [B]

**Fourteen bits.** A residue amplifier with β = 1/2 must have a gain error below $2^{-14}$. What open-loop gain does that need without calibration? If instead it has a 2% gain error that is calibrated, how accurately must the calibration estimate it?

### Problem 20-12.10 [C]

**Calibrate once, drift later.** The op-amp of Example 20-12.5 ($A_0$ = 30, β = 1/2) is calibrated once at room temperature. When hot, its gain falls to 24. Find the new gain error, the residual error after the old correction, $(\varepsilon - \hat\varepsilon)/(1 - \hat\varepsilon)$, and how many times it exceeds a 12-bit budget of 1/4096.

### Problem 20-12.11 [B]

**The power bill.** For the stage of Problem 5, by what factor does the power change from 1.2 V to 0.7 V at fixed SNR, bandwidth and $g_m/I_D$?

### Problem 20-12.12 [C]

**Check the claim.** A vendor says moving its 12-bit converter from a 0.9 V node to a 0.75 V node halves its power. Assume 40% of the power is thermal-noise-limited analog (scaling as $1/V_{DD}$ at fixed swing fraction) and 60% is digital logic whose power scales as $CV_{DD}^2f$ with $C$ halving. Find the analog factor and the total power factor. Is the claim supported?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Digital versus analog scaling | 1, 12 |
| 2. Noise-limited power and supply | 2, 3, 4, 5, 11 |
| 3. Intrinsic gain and headroom | 6, 7 |
| 4. Mismatch-limited versus noise-limited | 8 |
| 5. Calibration requirements | 9, 10 |
| 6. Judging scaling claims | 12 |
