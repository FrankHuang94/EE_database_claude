# Problems 07-08 · Filters and Resonance

Chapter: [07-08](../chapters/07-08-filters-and-resonance.md) · Worked solutions: [07-08 solutions](../solutions/07-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** ω in rad/s, $f$ in Hz; phasors are peak values unless labeled RMS. Answers to 3 or 4 significant figures unless exact.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 07-08.1 [A]

**Name that filter.** For each transfer function, state the filter type and find $\omega_0$ and $Q$:

(a) $\dfrac{10^6}{s^2 + 1000s + 10^6}$  (b) $\dfrac{s^2}{s^2 + 200s + 10^6}$  (c) $\dfrac{50s}{s^2 + 50s + 10^6}$  (d) $\dfrac{s^2 + 4\times10^6}{s^2 + 400s + 4\times10^6}$  (e) $\dfrac{s^2 - 100s + 10^4}{s^2 + 100s + 10^4}$

### Problem 07-08.2 [A]

**Series resonance.** A series RLC has $R$ = 20 Ω, $L$ = 2 mH and $C$ = 50 nF. Find $f_0$, $Q$, the bandwidth in Hz and the exact half-power frequencies.

### Problem 07-08.3 [A]

**Parallel resonance.** A parallel RLC has $R$ = 10 kΩ, $L$ = 1 mH and $C$ = 10 nF. Find $f_0$, $Q$ and the bandwidth, and the impedance (magnitude and angle) at $f_0$ and at the two half-power frequencies.

### Problem 07-08.4 [B]

**Q from energy.** A series RLC with $R$ = 5 Ω, $L$ = 10 mH and $C$ = 1 µF carries a 100 mA (peak) current at resonance. Find $f_0$, the total stored energy, the energy dissipated per cycle and $Q$ from their ratio, and check against $Z_0/R$.

### Problem 07-08.5 [B]

**A capacitor at risk.** A series RLC with $L$ = 1 mH, $C$ = 10 nF and $R$ = 8 Ω is driven at resonance by 3 V (RMS). The capacitor is rated 50 V. (a) Find $f_0$, $Q$ and the capacitor's RMS and peak voltage. (b) What is the smallest total series resistance that keeps the capacitor at or below 40 V (RMS)?

### Problem 07-08.6 [B]

**Q from a ring-down.** A resonator struck by a pulse rings at 1 MHz, and its amplitude falls by a factor $e$ in 20 cycles. Find $Q$, its bandwidth and the envelope time constant.

### Problem 07-08.7 [B]

**Scaling a third-order prototype.** The third-order Butterworth low-pass prototype for 1 Ω terminations and a 1 rad/s cutoff is a series inductor of 1 H, a shunt capacitor of 2 F and another series inductor of 1 H. (a) Scale it to 50 Ω and a 100 MHz cutoff. (b) Find the gain (absolute and relative to DC) and phase at 100 MHz, and the gain at 300 MHz.

### Problem 07-08.8 [B]

**A fourth-order requirement.** A Butterworth low-pass must be −3 dB at 1 kHz and at least 50 dB down at 5 kHz. Find the minimum order, the $Q$ of each section and the attenuation achieved at 5 kHz.

### Problem 07-08.9 [B]

**Analyzing a Sallen–Key section.** A unity-gain Sallen–Key low-pass has $R_1 = R_2$ = 10 kΩ, $C_1$ = 22 nF (feedback capacitor) and $C_2$ = 10 nF. Find $f_0$ and $Q$, and the height and frequency of any peak.

### Problem 07-08.10 [B]

**Equal-component design.** An equal-component Sallen–Key low-pass uses $R$ = 10 kΩ and $C$ = 10 nF. (a) Find $f_0$. (b) Find the amplifier gain $K$, the ratio $R_f/R_g$ and the passband gain in dB for $Q$ = 0.7071 and for $Q$ = 1. (c) What happens at $K$ = 3?

### Problem 07-08.11 [B]

**A Sallen–Key high-pass.** Swap the resistors and capacitors of the unity-gain low-pass: the input passes through $C_1$ to node A and $C_2$ to node B; $R_2$ goes from B to ground and $R_1$ from A to the output. (a) Derive $H(s)$. (b) Show that with equal capacitors $Q = \tfrac12\sqrt{R_2/R_1}$. (c) Design a Butterworth high-pass at 100 Hz with $C_1 = C_2$ = 100 nF, and find the gain at 10 Hz, 100 Hz and 1 kHz.

### Problem 07-08.12 [B]

**A notch.** A resistor $R$ = 50 Ω is in series from input to output, and a series LC ($L$ = 100 µH) goes from the output to ground. (a) Choose $C$ to notch 1 MHz. (b) Derive $H$ and show it is a notch with $Q = Z_0/R$. (c) Find the −3 dB width of the notch and its edges, and the attenuation at 990 kHz.

### Problem 07-08.13 [B]

**Insertion loss.** (a) Derive, for one parallel resonator between a source and a load of equal resistance $R$, the insertion loss at resonance in terms of $Q_L$ and $Q_u$. (b) A filter needs $Q_L$ = 50. Find the loss for $Q_u$ = 100 and 1000. (c) What $Q_u$ keeps the loss at 1 dB?

### Problem 07-08.14 [C]

**A third-order active filter, and the op-amp it needs.** Design a third-order Butterworth low-pass at 10 kHz as an RC section buffered by a follower, followed by a unity-gain Sallen–Key section with equal resistors. Use 1 nF for the RC section and $C_2$ = 1 nF in the Sallen–Key section. (a) Find all the component values. (b) Find the ideal gain at 10 kHz and 20 kHz. (c) Model each follower with a dominant-pole op-amp ($A_0 = 10^5$) and find the gain at 10 kHz for gain–bandwidth products of 1 MHz and 100 kHz. What ratio of GBW to cutoff keeps the error below 0.01 dB here?

### Problem 07-08.15 [B]

**A loaded tank.** A parallel tank of $L$ = 1 µH (coil $Q_c$ = 100 at 10 MHz) and $C$ chosen to resonate at 10 MHz is driven from a source with 1 kΩ of resistance and feeds a 2 kΩ load. (a) Find $C$, $Z_0$ and the coil's equivalent parallel resistance $R_p$. (b) Find the unloaded $Q$, the loaded $Q$ and the bandwidth. (c) At 10 MHz, what fraction of the power reaching the tank is lost in the coil? (d) Find the insertion loss: the load voltage with the tank in place compared with the load connected directly to the source.

### Problem 07-08.16 [B]

**A multiple-feedback low-pass.** Design an MFB Butterworth low-pass with $f_c$ = 10 kHz and a DC gain of −2, using $R_1$ = 10 kΩ and $R_2 = R_3$ = 20 kΩ (§3.10). (a) Find the capacitor ratio and $C_1$, $C_2$. (b) Find the gain, in dB, at DC and at 30 kHz. (c) Why might a designer choose this section over a Sallen–Key low-pass for an anti-aliasing filter ahead of a converter?

### Problem 07-08.17 [B]

**Removing mains hum.** A sensor's useful signal lies above 200 Hz; 50 Hz hum must be attenuated. (a) Design a unity-gain Sallen–Key Butterworth high-pass at 200 Hz with $C$ = 47 nF (§3.10). (b) Find its attenuation at 50 Hz. (c) What Butterworth order is needed for at least 40 dB at 50 Hz with the corner at 200 Hz, and what attenuation does it give?

---

## Objective coverage

| Learning objective (chapter 07-08) | Problems |
|---|---|
| 1. Filter types and specifications | 1, 8, 12 |
| 2. Series and parallel resonance; Q four ways; loaded Q | 2, 3, 4, 5, 6, 15 |
| 3. Passive design, prototypes and scaling | 7, 12 |
| 4. Butterworth order and sections | 8, 14, 16, 17 |
| 5. Active filters: Sallen–Key, MFB, high-pass and band-pass sections, sensitivity, op-amp limits | 9, 10, 11, 14, 16, 17 |
| 6. Resonator Q, insertion loss and technologies | 13, 15 |
