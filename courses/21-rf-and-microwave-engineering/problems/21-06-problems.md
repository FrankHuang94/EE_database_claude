# Problems 21-06 · Oscillators and VCOs

Chapter: [21-06](../chapters/21-06-oscillators-and-vcos.md) · Worked solutions: [21-06 solutions](../solutions/21-06-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Tank quantities are differential; the oscillator is a cross-coupled bipolar pair, $g(v) = (I_{tail}/2)\tanh(v/2V_T)$, unless stated. $T$ = 300 K, so $kT$ = 4.142 × 10⁻²¹ J and $V_T$ = 25.85 mV. $\mathcal{L}$ is single-sideband phase noise; the FoM is $-\mathcal{L} + 20\log_{10}(f_0/\Delta f) - 10\log_{10}(P/1\text{ mW})$. Problems marked *(lab)* can be checked with `labs/21-06-lab/vco.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-06.1 [A]

**A 6 GHz tank.** A 6 GHz VCO uses a 0.8 nH inductor with $Q_L$ = 12 and capacitors with $Q_C$ = 40. Find (a) the tank capacitance, (b) the tank Q and (c) $R_p$, (d) the minimum transconductance per device, and (e) the tail current that gives a loop gain of 3.

### Problem 21-06.2 [A]

**Current- or voltage-limited?** The tank of Problem 21-06.1 is driven by a hard-switching pair with a 3 mA tail from a 1.0 V supply. (a) What differential amplitude results, and (b) how large is each output's swing about its DC level? (c) If the swing saturates once the differential amplitude reaches 0.8 V, what tail current reaches that boundary? At the boundary, find (d) the efficiency $\eta = V/(\pi V_{DD})$ and (e) the tank signal power.

### Problem 21-06.3 [B]

**Describing function and start-up.** *(lab)* The tank of Problem 21-06.1 is driven with a 2 mA tail. Find (a) the loop gain, (b) the hard-limit amplitude, (c) the soft-switching closed form, (d) the exact describing-function amplitude, (e) the start-up e-folding time $1/\sigma$ and (f) the amplitude-recovery time constant $2R_pC$.

### Problem 21-06.4 [B]

**Charge kicks.** In the oscillator of Example 21-06.1 ($q_{max}$ = 0.4652 pC, 5 GHz), a charge of 1 fC is injected. Find (a) the phase shift if it arrives at a zero crossing, in milliradians and (b) in degrees, and (c) the timing shift it represents. (d) If it arrives at a peak, what is the fractional amplitude change, and what happens to it? (e) What is the phase shift if it arrives 45° after a peak?

### Problem 21-06.5 [B]

**Phase noise and FoM.** *(lab)* For the oscillator of Problem 21-06.3 (use its describing-function amplitude), with Leeson's $F$ = 2.5 and a 1.0 V supply, find (a) the tank signal power and (b) the efficiency; the phase noise at (c) 1 MHz and (d) 10 MHz offset from Leeson's formula; (e) the FoM at 1 MHz and (f) the FoM bound for this Q and F.

### Problem 21-06.6 [B]

**Symmetry and the 1/f³ corner.** Two designs share $\Gamma_{rms}$ = 0.6 and a 2 MHz device flicker corner. Design A's effective ISF has $\Gamma_{dc}$ = 0.02; design B's, made asymmetric by device mismatch, has 0.1. Find (a) and (b) their 1/f³ corners, (c) and (d) how much flicker raises each one's phase noise at 10 kHz offset, and (e) the difference between them.

### Problem 21-06.7 [A]

**Diluted tuning.** A 1 nH tank must tune from 4.5 to 5.5 GHz. Find (a) the total capacitance ratio required, (b) the capacitance at 5.5 GHz and (c) at 4.5 GHz. With 0.6 pF of fixed capacitance, what (d) minimum and (e) maximum must the variable part reach, and (f) what ratio is that?

### Problem 21-06.8 [B]

**A bank with off-capacitance.** A 1.2 nH tank has 0.5 pF of fixed capacitance, a 0.10–0.20 pF varactor and a 4-bit binary bank of unit cells, each 80 fF when on and 20 fF when off (switch parasitics). Find (a) the bank capacitance at code 0 and (b) at code 15; the band at (c, d) code 0 and (e, f) code 15; (g) the total tuning range; and (h) the top of the code-0 band if the switches had no off-capacitance.

### Problem 21-06.9 [B]

**Choosing K_VCO.** The loop filter's 2 kΩ resistor is the dominant noise on the control line. (a) What is its noise density? (b) What is the largest $K_{VCO}$ for which it contributes at most −130 dBc/Hz at 1 MHz offset? (c) With that $K_{VCO}$, what spur does a 50 µV peak ripple at 10 MHz cause?

### Problem 21-06.10 [A]

**Dividers and multipliers.** A VCO at 8 GHz has −128 dBc/Hz at 1 MHz offset (TI LMX2595, VCO1, typical) and −148 dBc/Hz at 10 MHz. Find the phase noise at 1 MHz (a) after an ideal ×3 multiplier and (b) after a divide-by-8; (c) at 10 MHz after the divide-by-8 if ideal, and (d) if the divider adds a white floor of −155 dBc/Hz.

### Problem 21-06.11 [B]

**Phase noise and EVM.** A synthesizer's output is flat at −95 dBc/Hz up to a one-pole corner at 500 kHz. Find (a) the rms phase error in radians and (b) degrees, (c) the EVM it alone causes, and the fraction of the NR EVM budget it uses for (d) 256-QAM (3.5%) and (e) 1024-QAM (2.5%) (17-06). (f) What in-band level would hold its EVM to 1%?

### Problem 21-06.12 [B]

**Duty-cycle budget.** A receiver needs 40 dB of image rejection from a divide-by-2 quadrature LO. (a) With no gain error, what phase error is allowed, and (b) what duty-cycle tolerance does that give the 2f clock? (c) With a 1% gain error as well, what phase error is allowed (exact formula), and (d) what duty-cycle tolerance?

### Problem 21-06.13 [C]

**Mismatch in an RC-CR network.** An RC-CR network is designed for 2.45 GHz ($R$ = 1 kΩ, $C$ = 64.96 fF), but the I path's resistor is 1% high (1.01 kΩ). At 2.45 GHz, find (a) the phase difference between Q and I and (b) its error, (c) the gain error, (d) the IRR (exact formula) and (e) the small-error estimate.

### Problem 21-06.14 [C]

**A pulling budget.** A 5 GHz transmit VCO has tank Q = 10. Its PA's modulated output has a strong component 20 MHz from the VCO frequency, and some of it couples back into the tank. The average pull must stay below 10 kHz. (a) What lock range is tolerable (use the large-detuning approximation)? (b) What injected-to-oscillator current ratio is that, and (c) what coupling in dB? (d) Check the pull exactly. (e) Why does running the VCO at 10 GHz with a divide-by-2 remove the problem?

### Problem 21-06.15 [C]

**Buying phase noise with cores.** One VCO core gives −120 dBc/Hz at 1 MHz from 10 GHz at 10 mW. Find (a) its FoM; (b) the phase noise and (c) the FoM of four coupled cores; (d) the minimum number of cores that meet −125 dBc/Hz, as a real number, and (e) the integer count. (f) What would doubling the tank Q do to a single core's FoM, all else equal?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Tank, startup and amplitude by the describing function | 1, 2, 3 |
| 2. Phase noise from the ISF and Leeson, the 1/f³ corner | 4, 5, 6 |
| 3. Tuning plans, $K_{VCO}$ and tuning-line noise | 7, 8, 9 |
| 4. Division, multiplication and EVM | 10, 11 |
| 5. Quadrature generation and image rejection | 12, 13 |
| 6. Injection locking, pulling and FoM claims | 14, 15 |
