# Problems 20-10 · PLLs and Jitter

Chapter: [20-10](../chapters/20-10-plls-and-jitter.md) · Worked solutions: [20-10 solutions](../solutions/20-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $K_{PD} = I_{cp}/2\pi$; VCO gains in Hz/V convert to $K_{VCO} = 2\pi \times$ (Hz/V). $\mathcal{L}(f)$ is the SSB phase noise, equal to the two-sided phase PSD; a one-sided noise density converts to $\mathcal{L}$ by halving. Jitter: $\sigma_t = \sqrt{2\int\mathcal{L}\,df}/(2\pi f_0)$. Third-order loop: PM = $\arctan[(b - 1)/(2\sqrt b)]$. Problems marked *(lab)* can be checked with `labs/20-10-lab/pll.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-10.1 [A]

**A Bluetooth-band synthesizer.** A 25 MHz reference and $N$ = 96 drive a PLL with $I_{cp}$ = 200 µA. Find the output frequency and the PFD/pump gain.

### Problem 20-10.2 [A]

**The VCO integrates.** A VCO has 1 GHz/V. Its control voltage steps by 10 mV. By how much does its frequency change, and how much extra phase does it accumulate in 1 µs?

### Problem 20-10.3 [B]

**A second-order loop.** With $I_{cp}$ = 100 µA, a 200 MHz/V VCO, $N$ = 40, C = 100 pF and R = 10 kΩ, find the natural frequency (in hertz) and the damping factor.

### Problem 20-10.4 [A]

**Phase margin against b.** Find the maximum phase margin of a third-order loop for $b$ = 4, 10 and 20.

### Problem 20-10.5 [B] *(lab)*

**Design a filter.** For the loop of Problem 3, design a third-order filter for a 500 kHz crossover with $b$ = 10: find R, $C_1$, $C_2$ and the total capacitance.

### Problem 20-10.6 [A]

**Bandwidth limit.** With the 25 MHz reference of Problem 1, what loop bandwidth does the $f_{ref}/10$ rule allow?

### Problem 20-10.7 [B]

**Multiplied reference noise.** The 25 MHz reference has −155 dBc/Hz of phase noise. What is its contribution in band at the 2.4 GHz output?

### Problem 20-10.8 [B]

**Integrated jitter.** A 2.4 GHz output has −105 dBc/Hz flat from 1 kHz to a 1 MHz loop bandwidth and −20 dB per decade beyond. Find the rms phase and jitter integrated from 1 kHz to 100 MHz.

### Problem 20-10.9 [A]

**A clock for an ADC.** What rms jitter lets an ADC reach 70 dB SNR (jitter-limited) for a 500 MHz input?

### Problem 20-10.10 [B]

**Charge-pump noise.** A 200 µA charge pump has an output current noise of 10 pA/√Hz (one-sided). Find its input-referred phase noise in dBc/Hz and its in-band contribution at the output for $N$ = 96.

### Problem 20-10.11 [B] *(lab)*

**A fractional step.** Produce 2.41 GHz from 25 MHz. What is $N$? What phase noise does a MASH 1-1-1 divider add at 1 MHz offset before the loop's filtering?

### Problem 20-10.12 [B]

**Spurs from a simple accumulator.** With a first-order accumulator and a fraction of 2/5, the divide pattern repeats every 5 reference cycles. At what spacing do the fractional spurs appear for $f_{ref}$ = 25 MHz?

### Problem 20-10.13 [A]

**Figures of merit.** Find the jitter-power FoM of a PLL with 200 fs at 4 mW, and the oscillator FoM of a 2.4 GHz VCO with −125 dBc/Hz at 1 MHz and 2 mW.

### Problem 20-10.14 [C]

**TDC resolution for an ADPLL.** A 2.4 GHz ADPLL with a 25 MHz reference must reach −110 dBc/Hz in band. What TDC resolution does it need?

### Problem 20-10.15 [B]

**Lock settling after a channel hop.** A PLL has $I_{cp}$ = 500 µA, $K_{VCO}$ = 2π × 500 MHz/V and N = 100, with a third-order filter designed for a 0.3 MHz crossover and spread b = 10.
(a) Find $C_1 + C_2$, $C_1$, $C_2$ and $R$ from $C_1 + C_2 = K\sqrt b/\omega_c^2$, $K = I_{cp}K_{VCO}/(2\pi N)$, $\omega_z = \omega_c/\sqrt b$.
(b) Ignoring $C_2$, find the natural frequency $\omega_n/2\pi$ and the damping ζ.
(c) The divide ratio steps by one, moving the output by 50 MHz. Estimate, from the envelope $e^{-\zeta\omega_nt}$, how long the frequency error takes to fall below 10 kHz. The lab's exact third-order step response gives 8.17 µs: why is the estimate close?
(d) How does the settling time scale if the crossover is halved at the same b?

### Problem 20-10.16 [C] *(lab)*

**Design a fractional-N loop.** A synthesizer must produce 5.0123 GHz from a 50 MHz reference with a MASH 1-1-1 divider (busy and dithered), $I_{cp}$ = 500 µA, $K_{VCO}$ = 2π × 500 MHz/V and a third-order filter with b = 10. The input-referred reference, PFD and pump noise is −150 dBc/Hz; the VCO alone has −120 dBc/Hz at 1 MHz, falling 20 dB per decade. Specifications: rms jitter at most 250 fs from 10 kHz to 20 MHz, and after a 50 MHz channel hop the frequency must be within 10 kHz in 10 µs.
(a) By hand: at what offset does $N^2$ times the reference noise meet the VCO line, and at what offset does the unfiltered MASH noise $\mathcal{L}_{\Sigma\Delta}$ of §3.6 rise to that same level? What do the two offsets suggest about the bandwidth?
(b) With the lab's model, find the total jitter (reference, VCO and MASH noise) and the settling time for crossovers of 0.2, 0.3 and 0.5 MHz. Can any of them meet both specifications?
(c) Double the reference to 100 MHz (N ≈ 50.1). Show by hand why the MASH noise at a given low offset falls by about 15 dB and the multiplied reference noise by 6 dB. Then find the jitter and settling at a 0.3 MHz crossover, and the filter's R, $C_1$ and $C_2$.
(d) The chip can afford at most 500 pF of loop-filter capacitance. By what factor must $I_{cp}K_{VCO}$ fall, and what does lowering each of them cost?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Phase-domain model, natural frequency, damping | 1, 2, 3 |
| 2. Loop-filter design, phase margin and settling | 4, 5, 6, 15, 16 |
| 3. Noise transfer | 7, 10, 16 |
| 4. Phase noise to jitter | 8, 9 |
| 5. Fractional-N | 11, 12, 16 |
| 6. Figures of merit and ADPLLs | 13, 14 |
