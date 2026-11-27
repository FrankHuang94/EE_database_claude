# Solutions 07-08 · Filters and Resonance

Problems: [07-08 problems](../problems/07-08-problems.md) · Chapter: [07-08](../chapters/07-08-filters-and-resonance.md). Every number below is recomputed by [verify_07_08.py](../verify/verify_07_08.py) from nodal or state-space models of the circuits, with peaks, bandwidths and edges found by numerical search; values marked † are also confirmed by ngspice in [labs/07-08-lab](../labs/07-08-lab/README.md).

---

## Solutions

### Solution 07-08.1

Match each to the biquad forms of §3.1, reading $\omega_0^2$ from the constant term and $\omega_0/Q$ from the $s$ coefficient of the denominator:

- (a) Constant numerator: **low-pass**, $\omega_0$ = **1000 rad/s**, $Q = 1000/1000$ = **1.000**.
- (b) $s^2$ numerator: **high-pass**, $\omega_0$ = **1000 rad/s**, $Q = 1000/200$ = **5.000**.
- (c) $s$ numerator: **band-pass**, $\omega_0$ = **1000 rad/s**, $Q = 1000/50$ = **20.00**, with unit gain at $\omega_0$ (numerator coefficient equals $\omega_0/Q$).
- (d) Numerator $s^2 + \omega_0^2$: **notch** at $\omega_0$ = **2000 rad/s**, $Q = 2000/400$ = **5.000**.
- (e) Numerator is the denominator with the $s$ term negated: **all-pass**, $\omega_0$ = **100 rad/s**, $Q = 100/100$ = **1.000**.

### Solution 07-08.2

$\omega_0 = 1/\sqrt{2\times10^{-3}\times50\times10^{-9}} = 10^5$ rad/s, $f_0$ = **15.92 kHz**. $Z_0 = \sqrt{L/C}$ = 200 Ω, $Q = 200/20$ = **10.00**, bandwidth $f_0/Q$ = **1.592 kHz**. Half-power frequencies $f_0\big(\sqrt{1 + 1/400} \mp 1/20\big)$ = **15.14 kHz** and **16.73 kHz**: not quite symmetric about 15.92 kHz at this $Q$ (**0.78 kHz** below, **0.82 kHz** above).

### Solution 07-08.3

$\omega_0 = 1/\sqrt{10^{-3}\times10^{-8}}$ = 316.2 krad/s, $f_0$ = **50.33 kHz**. $Z_0$ = 316.2 Ω, so $Q = R/Z_0$ = **31.62** and the bandwidth is **1.592 kHz**. At $f_0$ the susceptances cancel and $Z = R$ = **10.00 kΩ** at 0°. At the half-power frequencies the net susceptance equals $\pm G$, so $\lvert Z\rvert = R/\sqrt2$ = **7.071 kΩ**, at **+45°** below resonance (the inductor's susceptance dominates: inductive) and **−45°** above.

### Solution 07-08.4

$f_0 = 1/(2\pi\sqrt{10^{-2}\times10^{-6}})$ = **1.592 kHz**. Stored energy $\tfrac12LI_m^2 = \tfrac12\times0.01\times0.01$ = **50.0 µJ**. Dissipated per cycle: $\tfrac12I_m^2R\times T_0 = 0.025\ \text{W}\times628.3\ \text{µs}$ = **15.71 µJ**. $Q = 2\pi\times50.0/15.71$ = **20.00**, and $Z_0/R = 100/5$ = 20 ✓.

### Solution 07-08.5

(a) $f_0 = 1/(2\pi\sqrt{10^{-3}\times10^{-8}})$ = **50.33 kHz**; $Z_0$ = 316.2 Ω; $Q = 316.2/8$ = **39.53**. The capacitor sees $Q\times3$ = **118.6 V** RMS, **167.7 V** peak, far beyond its 50 V rating.

(b) $V_C = Q V_s \le 40$ V requires $Q \le 13.33$, so $R \ge Z_0/13.33 = 316.2\times3/40$ = **23.72 Ω**. Adding resistance trades selectivity for safety; a better fix may be a capacitor with an adequate rating.

### Solution 07-08.6

The envelope falls as $e^{-\omega_0t/(2Q)}$; a factor $e$ takes $t = 2Q/\omega_0 = Q/(\pi f_0)$, which is $Q/\pi$ cycles. So $Q = 20\pi$ = **62.83**, bandwidth $f_0/Q$ = **15.92 kHz**, and the envelope time constant is $20$ cycles $\times 1$ µs = **20.0 µs**.

### Solution 07-08.7

(a) $k_z$ = 50, $k_f = 2\pi\times10^8$: $L = 1\times50/(2\pi\times10^8)$ = **79.58 nH** (both inductors) and $C = 2/(50\times2\pi\times10^8)$ = **63.66 pF**.

(b) Solve the ladder (nodal analysis in the verify script): at 100 MHz the gain is **−9.03 dB** absolute, **−3.01 dB** relative to the −6.02 dB DC level, with phase **−135.0°** (three poles, each contributing on average 45° at the cutoff). At 300 MHz it is **−34.65 dB** absolute, **−28.63 dB** relative, matching $10\lg(1 + 3^6)$ = 28.63 dB for a third-order Butterworth response.

### Solution 07-08.8

$n \ge \lg(10^5 - 1)/(2\lg5) = 5.000/1.398$ = **3.577**, so the order is **4**. Sections: two pairs at 1 kHz with $Q = 1/(2\sin(\pi/8))$ = **1.307** and $Q = 1/(2\sin(3\pi/8))$ = **0.5412**. Attenuation at 5 kHz: $10\lg(1 + 5^8)$ = **55.92 dB**.

### Solution 07-08.9

$f_0 = 1/\big(2\pi\sqrt{10^4\times10^4\times22\times10^{-9}\times10\times10^{-9}}\big)$ = **1.073 kHz**. $Q = \tfrac12\sqrt{22/10}$ = **0.7416**, slightly above the Butterworth 0.7071, so a small peak exists: $1/(2\zeta\sqrt{1 - \zeta^2})$ with ζ = **0.6742** is **1.0042**, or **0.036 dB**, at $f_0\sqrt{1 - 2\zeta^2}$ = **323.5 Hz**. In practice that is flat.

### Solution 07-08.10

(a) $f_0 = 1/(2\pi RC) = 1/(2\pi\times10^{-4})$ = **1.592 kHz**.

(b) $K = 3 - 1/Q$:

- $Q$ = 0.7071: $K$ = **1.586**, $R_f/R_g = K - 1$ = **0.586**, passband gain **4.005 dB**.
- $Q$ = 1: $K$ = **2.000**, $R_f/R_g$ = **1.000**, passband gain **6.021 dB**.

(c) At $K$ = 3 the $s$ term vanishes: the poles sit on the imaginary axis and the circuit oscillates at $f_0$. Above 3 they move into the right half-plane (07-04 §3.8).

### Solution 07-08.11

(a) Node B: $(\mathbf{V}_A - \mathbf{V}_B)sC_2 = \mathbf{V}_B/R_2$, so $\mathbf{V}_A = \mathbf{V}_B\big(1 + 1/(sR_2C_2)\big)$. Node A, with $\mathbf{V}_{out} = \mathbf{V}_B$:

$$
(\mathbf{V}_{in} - \mathbf{V}_A)sC_1 = \frac{\mathbf{V}_B}{R_2} + \frac{\mathbf{V}_A - \mathbf{V}_B}{R_1}.
$$

Substituting and multiplying through by $sR_1R_2C_2$ gives

$$
H(s) = \frac{s^2R_1R_2C_1C_2}{s^2R_1R_2C_1C_2 + sR_1(C_1 + C_2) + 1} .
$$

(b) $\omega_0 = 1/\sqrt{R_1R_2C_1C_2}$ and $1/Q = \omega_0R_1(C_1 + C_2)$. With $C_1 = C_2 = C$: $1/Q = 2R_1C/(C\sqrt{R_1R_2}) = 2\sqrt{R_1/R_2}$, so $Q = \tfrac12\sqrt{R_2/R_1}$: in the high-pass the **resistor ratio** sets $Q$, the dual of the low-pass's capacitor ratio.

(c) Butterworth: $R_2/R_1 = 4Q^2 = 2$. $\sqrt{R_1R_2} = 1/(\omega_0C) = 1/(2\pi\times100\times100\ \text{nF})$ = 15.92 kΩ, so $R_1\sqrt2$ = 15.92 kΩ: $R_1$ = **11.25 kΩ** and $R_2$ = **22.51 kΩ**. Gains: **−40.00 dB** at 10 Hz (a decade below, second order), **−3.01 dB** at 100 Hz, and **0.00 dB** at 1 kHz (**−0.0004 dB**).

### Solution 07-08.12

(a) $C = 1/(\omega_0^2L) = 1/\big((2\pi\times10^6)^2\times10^{-4}\big)$ = **253.3 pF**.

(b) The divider gives $H = Z_{LC}/(R + Z_{LC})$ with $Z_{LC} = sL + 1/(sC) = (s^2LC + 1)/(sC)$:

$$
H = \frac{s^2LC + 1}{s^2LC + sRC + 1} = \frac{s^2 + \omega_0^2}{s^2 + (R/L)s + \omega_0^2},
$$

the notch form of §3.1 with $\omega_0/Q = R/L$, so $Q = \omega_0L/R = Z_0/R$. Here $Z_0 = \sqrt{L/C}$ = **628.3 Ω** and $Q$ = **12.57**.

(c) The −3 dB width of a notch is $f_0/Q$ = **79.58 kHz**, between **961.0 kHz** and **1040.6 kHz** (found numerically; their product is $f_0^2$). At 990 kHz the response is **−12.22 dB**. The series LC is a short circuit at resonance, which pulls the output to zero.

### Solution 07-08.13

(a) §3.9: at resonance the tank is $R_p$, the load sees $\mathbf{V}_S(R_p\parallel R)/(R + R_p\parallel R)$, and dividing by the lossless $\mathbf{V}_S/2$ gives $2R_p/(2R_p + R) = 1 - Q_L/Q_u$, so the loss is $-20\lg(1 - Q_L/Q_u)$ dB.

(b) $Q_L$ = 50: **6.02 dB** for $Q_u$ = 100 (half the voltage, so three-quarters of the power is lost) and **0.446 dB** for $Q_u$ = 1000.

(c) $1 - 50/Q_u = 10^{-1/20} = 0.8913$, so $Q_u$ = **459.8**: about nine times the loaded $Q$ for 1 dB.

### Solution 07-08.14

(a) RC section: $R = 1/(2\pi\times10\ \text{kHz}\times1\ \text{nF})$ = **15.92 kΩ**. Sallen–Key section, $Q$ = 1: $C_1 = 4Q^2C_2$ = **4 nF**, and $R = 1/\big(2\pi\times10\ \text{kHz}\times\sqrt{4\times1}\ \text{nF}\big)$ = **7.958 kΩ** for each resistor.

(b) Ideal: **−3.010 dB** at 10 kHz (the Butterworth cutoff) and **−18.13 dB** at 20 kHz ($10\lg(1 + 2^6)$).

(c) Each follower now has gain $K(s) = A(s)/(1 + A(s))$ with $A(s) = A_0/(1 + sA_0/\omega_t)$. Substituting $K(s)$ into both sections' transfer functions (the derivation of §3.8 holds frequency by frequency):

- GBW = 1 MHz (100 × the cutoff): **−3.015 dB** at 10 kHz, an error of **0.0047 dB**.
- GBW = 100 kHz (10 × the cutoff): **−3.428 dB**, an error of **0.42 dB**.

Solving for an error of 0.01 dB gives GBW ≈ **670 kHz**, about **67** times the cutoff for this filter. The required ratio grows with the section $Q$; manufacturers' rules of thumb are of this order (§9).

### Solution 07-08.15

(a) $C = 1/(\omega_0^2L) = 1/[(2\pi\times10^7)^2\times10^{-6}] = $ **253.3 pF**. $Z_0 = \sqrt{L/C} = \omega_0L = $ **62.83 Ω**. The coil's losses look like a parallel resistance $R_p = Q_c\,\omega_0L = $ **6283 Ω** (07-08 §3.4).

(b) The unloaded $Q$ is the coil's: \$Q_u = R_p/Z_0 = \$ **100**. Loaded, the tank sees $R_p$, the source's 1 kΩ and the load's 2 kΩ in parallel, \$1/(1/6283 + 1/1000 + 1/2000) = \$ **602.7 Ω**, so \$Q_L = 602.7/62.83 = \$ **9.593** and the bandwidth is \$10\ \text{MHz}/9.593 = \$ **1.042 MHz**. Loading cuts $Q$ tenfold: the circuit, not the coil, sets the bandwidth.

(c) At resonance $L$ and $C$ cancel, and the power reaching the tank divides between the coil's $R_p$ and the load in proportion to their conductances (the same voltage drives both): \$159.2/(159.2 + 500) = \$ **24.15%** is lost in the coil, and **75.85%** reaches the load.

(d) With the tank, the source sees $R_p\parallel2\ \text{k}\Omega = 1517$ Ω, so the load gets $1517/2517 = 0.6027$ of the source voltage. Without the tank, it gets $2000/3000 = 0.6667$. The insertion loss is \$20\lg(0.6667/0.6027) = \$ **0.876 dB**. The coil's $Q_u$ of 100 is ten times the $Q_L$ the circuit needs, so the loss is small; §3.9's $-20\lg(1 - Q_L/Q_u)$ gives exactly the same 0.876 dB. The formula holds for unequal terminations too, because the voltage ratio is $(G_s + G_L)/(G_s + G_L + G_p) = 1 - R_{total}/R_p = 1 - Q_L/Q_u$.

### Solution 07-08.16

(a) With $R_2 = R_3 = 20$ kΩ and $R_1$ = 10 kΩ, the $Q$ formula of §3.10 gives $Q = 20\text{k}\sqrt{C_1C_2}/[C_2(20\text{k} + 20\text{k} + 40\text{k})] = \tfrac14\sqrt{C_1/C_2}$. Butterworth needs $Q = 1/\sqrt2$, so \$C_1/C_2 = 16Q^2 = \$ **8**. Then $\omega_0 = 1/(R_2\sqrt{C_1C_2}) = 1/(20\text{k}\times C_2\sqrt8)$ gives \$C_2 = \$ **281.3 pF** and \$C_1 = \$ **2.251 nF**. The DC gain is $-R_2/R_1 = -2$.

(b) At DC: \$20\lg2 = \$ **6.021 dB**. At 30 kHz, a Butterworth second-order section is down by $10\lg(1 + 3^4) = 19.14$ dB, so the gain is \$6.021 - 19.14 = \$ **−13.12 dB**.

(c) An anti-aliasing filter must keep attenuating far above its corner, up to the converter's sampling rate and beyond. A Sallen–Key low-pass leaks signal at high frequency through its feedback capacitor into the op-amp's rising output impedance (§3.8). The MFB section's capacitor $C_2$ feeds a virtual ground, so it lacks that leakage path. It also provides gain and inversion in the same op-amp, and its sensitivities are low.

### Solution 07-08.17

(a) From §3.10, $Q = \tfrac12\sqrt{R_2/R_1}$, so Butterworth needs $R_2 = 2R_1$, and then $\omega_0 = 1/(CR_1\sqrt2)$. So \$R_1 = 1/(\sqrt2\times2\pi\times200\times47\ \text{nF}) = \$ **11.97 kΩ** and \$R_2 = \$ **23.94 kΩ**.

(b) The high-pass Butterworth response is $\lvert H\rvert^2 = 1/[1 + (f_c/f)^4]$. At 50 Hz, $f_c/f = 4$, so the attenuation is \$10\lg(1 + 4^4) = \$ **24.10 dB**.

(c) We need $10\lg(1 + 4^{2n}) \ge 40$, so $4^{2n} \ge 9999$ and $n \ge 3.322$. The lowest order is **4**, which gives \$10\lg(1 + 4^8) = \$ **48.16 dB**. Two cascaded second-order sections with $Q$ = 0.541 and 1.307 realize it (§3.7), not two Butterworth sections.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 07-08.1a | (a) ω0 | 1000 | rad/s |
| 07-08.1b | (a) Q | 1.000 | — |
| 07-08.1c | (b) Q | 5.000 | — |
| 07-08.1d | (c) Q | 20.00 | — |
| 07-08.1e | (d) ω0 | 2000 | rad/s |
| 07-08.1f | (d) Q | 5.000 | — |
| 07-08.1g | (e) ω0 | 100 | rad/s |
| 07-08.1h | (e) Q | 1.000 | — |
| 07-08.2a | $f_0$ | 15.92 | kHz |
| 07-08.2b | Q | 10.00 | — |
| 07-08.2c | bandwidth | 1.592 | kHz |
| 07-08.2d | lower half-power frequency | 15.14 | kHz |
| 07-08.2e | upper half-power frequency | 16.73 | kHz |
| 07-08.2f | distance below $f_0$ | 0.78 | kHz |
| 07-08.2g | distance above $f_0$ | 0.82 | kHz |
| 07-08.3a | $f_0$ | 50.33 | kHz |
| 07-08.3b | Q | 31.62 | — |
| 07-08.3c | bandwidth | 1.592 | kHz |
| 07-08.3d | impedance at $f_0$ | 10.00 | kΩ |
| 07-08.3e | impedance at the half-power frequencies | 7.071 | kΩ |
| 07-08.3f | angle at the lower half-power frequency | 45 | ° |
| 07-08.3g | angle at the upper half-power frequency | −45 | ° |
| 07-08.4a | $f_0$ | 1.592 | kHz |
| 07-08.4b | stored energy | 50.0 | µJ |
| 07-08.4c | energy per cycle | 15.71 | µJ |
| 07-08.4d | Q | 20.00 | — |
| 07-08.5a | $f_0$ | 50.33 | kHz |
| 07-08.5b | Q | 39.53 | — |
| 07-08.5c | capacitor voltage (RMS) | 118.6 | V |
| 07-08.5d | capacitor voltage (peak) | 167.7 | V |
| 07-08.5e | minimum series resistance | 23.72 | Ω |
| 07-08.6a | Q | 62.83 | — |
| 07-08.6b | bandwidth | 15.92 | kHz |
| 07-08.6c | envelope time constant | 20.0 | µs |
| 07-08.7a | L | 79.58 | nH |
| 07-08.7b | C | 63.66 | pF |
| 07-08.7c | gain at 100 MHz | −9.03 | dB |
| 07-08.7d | relative gain at 100 MHz | −3.01 | dB |
| 07-08.7e | phase at 100 MHz | −135.0 | ° |
| 07-08.7f | gain at 300 MHz | −34.65 | dB |
| 07-08.7g | relative gain at 300 MHz | −28.63 | dB |
| 07-08.8a | minimum order (unrounded) | 3.577 | — |
| 07-08.8b | order | 4 | — |
| 07-08.8c | higher Q | 1.307 | — |
| 07-08.8d | lower Q | 0.5412 | — |
| 07-08.8e | attenuation at 5 kHz | 55.92 | dB |
| 07-08.9a | $f_0$ | 1.073 | kHz |
| 07-08.9b | Q | 0.7416 | — |
| 07-08.9c | peak | 0.036 | dB |
| 07-08.9d | peak frequency | 323.5 | Hz |
| 07-08.9e | ζ | 0.6742 | — |
| 07-08.9f | peak gain as a ratio | 1.0042 | — |
| 07-08.10a | $f_0$ | 1.592 | kHz |
| 07-08.10b | K for Q = 0.7071 | 1.586 | — |
| 07-08.10c | its $R_f/R_g$ | 0.586 | — |
| 07-08.10d | its passband gain | 4.005 | dB |
| 07-08.10e | K for Q = 1 | 2.000 | — |
| 07-08.10f | its $R_f/R_g$ | 1.000 | — |
| 07-08.10g | its passband gain | 6.021 | dB |
| 07-08.11a | $R_1$ | 11.25 | kΩ |
| 07-08.11b | $R_2$ | 22.51 | kΩ |
| 07-08.11c | gain at 10 Hz | −40.00 | dB |
| 07-08.11d | gain at 100 Hz | −3.01 | dB |
| 07-08.11e | gain at 1 kHz | 0.00 | dB |
| 07-08.11f | gain at 1 kHz, four decimals | −0.0004 | dB |
| 07-08.12a | C | 253.3 | pF |
| 07-08.12b | $Z_0$ | 628.3 | Ω |
| 07-08.12c | Q | 12.57 | — |
| 07-08.12d | notch width | 79.58 | kHz |
| 07-08.12e | lower edge | 961.0 | kHz |
| 07-08.12f | upper edge | 1040.6 | kHz |
| 07-08.12g | response at 990 kHz | −12.22 | dB |
| 07-08.13a | loss, $Q_u$ = 100 | 6.02 | dB |
| 07-08.13b | loss, $Q_u$ = 1000 | 0.446 | dB |
| 07-08.13c | $Q_u$ for 1 dB | 459.8 | — |
| 07-08.14a | RC-section resistor | 15.92 | kΩ |
| 07-08.14b | Sallen–Key $C_1$ | 4 | nF |
| 07-08.14c | Sallen–Key resistors | 7.958 | kΩ |
| 07-08.14d | ideal gain at 10 kHz | −3.010 | dB |
| 07-08.14e | ideal gain at 20 kHz | −18.13 | dB |
| 07-08.14f | gain at 10 kHz, GBW 1 MHz | −3.015 | dB |
| 07-08.14g | error, GBW 1 MHz | 0.0047 | dB |
| 07-08.14h | gain at 10 kHz, GBW 100 kHz | −3.428 | dB |
| 07-08.14i | error, GBW 100 kHz | 0.42 | dB |
| 07-08.14j | GBW for a 0.01 dB error | 670 | kHz |
| 07-08.14k | as a multiple of the cutoff | 67 | — |
| 07-08.15a | C | 253.3 | pF |
| 07-08.15b | $Z_0$ | 62.83 | Ω |
| 07-08.15c | coil's parallel resistance | 6283 | Ω |
| 07-08.15d | unloaded Q | 100 | — |
| 07-08.15e | total parallel resistance | 602.7 | Ω |
| 07-08.15f | loaded Q | 9.593 | — |
| 07-08.15g | bandwidth | 1.042 | MHz |
| 07-08.15h | fraction lost in the coil | 24.15 | % |
| 07-08.15i | fraction reaching the load | 75.85 | % |
| 07-08.15j | insertion loss | 0.876 | dB |
| 07-08.16a | capacitor ratio | 8 | — |
| 07-08.16b | $C_2$ | 281.3 | pF |
| 07-08.16c | $C_1$ | 2.251 | nF |
| 07-08.16d | DC gain | 6.021 | dB |
| 07-08.16e | gain at 30 kHz | −13.12 | dB |
| 07-08.17a | $R_1$ | 11.97 | kΩ |
| 07-08.17b | $R_2$ | 23.94 | kΩ |
| 07-08.17c | attenuation at 50 Hz | 24.10 | dB |
| 07-08.17d | minimum order (continuous) | 3.322 | — |
| 07-08.17e | lowest order | 4 | — |
| 07-08.17f | fourth-order attenuation at 50 Hz | 48.16 | dB |
