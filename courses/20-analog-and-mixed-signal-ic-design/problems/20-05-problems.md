# Problems 20-05 · Comparators and Sample-and-Hold Circuits

Chapter: [20-05](../chapters/20-05-comparators-and-sample-and-hold.md) · Worked solutions: [20-05 solutions](../solutions/20-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** $kT$ = 4.1419 × 10⁻²¹ J (300 K). T130 NMOS: μ = 350 cm²/V·s, $C_{ox}$ = 8.6 fF/µm², $V_{TH0}$ = 0.45 V, $L$ = 0.13 µm, body effect $\gamma_b$ = 0.4 V$^{1/2}$ with $2\phi_F$ = 0.8 V (body at ground); T130 PMOS: μ = 100 cm²/V·s, $|V_{TH0}|$ = 0.45 V, same body-effect values with its well at $V_{DD}$. $V_{DD}$ = 1.2 V. "The design" is the chapter's running design: 12 bits, 100 MS/s, $V_{FS}$ = 1.6 V peak to peak differential, $C$ = 0.651 pF per side, bootstrapped switch with $W$ = 0.888 µm. Differential samplers have a capacitor on each side; "equal noise" means differential kT/C noise equal to quantization noise. Problems marked *(lab)* need `labs/20-05-lab/sh.py` or an equivalent simulation.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-05.1 [A]

**kT/C.** (a) Find $\sqrt{kT/C}$ for 100 fF, 1 pF and 10 pF. (b) A 10-bit differential ADC has a 1.0 V peak-to-peak differential full scale. Find its LSB, the capacitance per side for equal noise, its ideal SNR and the SNR with that capacitance.

### Problem 20-05.2 [A]

**The cost of bits.** With the design's full scale and the equal-noise rule, find the capacitance per side for 10, 12, 14 and 16 bits. By what factor does the capacitance grow per bit, and what does that imply for the power of the circuit that drives it?

### Problem 20-05.3 [B]

**A faster, coarser sampler.** The 10-bit ADC of Problem 20-05.1(b) runs at 200 MS/s with half the period for tracking. Each input swings ±0.25 V around 0.6 V. (a) Find the largest time constant and on-resistance for settling to half an LSB. (b) Size a bootstrapped switch (body at ground) for that resistance at the worst-case input.

### Problem 20-05.4 [B]

**Bootstrap charge sharing.** The design's bootstrap capacitor is 0.3 pF and the switch's gate and the bootstrap circuit add 30 fF of parasitic capacitance. (a) Find $V_{GS}$ during tracking. (b) Find the on-resistance at a 1.0 V input, and by what factor the switch must be widened to restore 852 Ω.

### Problem 20-05.5 [B]

**Why not a transmission gate?** A CMOS transmission gate puts a PMOS (gate at 0 V, three times the NMOS width) in parallel with the design's NMOS (gate at $V_{DD}$). (a) Find the input above which the NMOS is off and below which the PMOS is off. (b) Find the gate's on-resistance at 0.2, 0.6 and 1.0 V. (c) Explain why transmission gates stopped working as sampling switches as supplies fell.

### Problem 20-05.6 [B]

**A speed–accuracy constant.** (a) Using $Q_{ch} = WLC_{ox}V_{ov}$ and $\tau = R_{on}C$, show that the charge-injection error $\Delta V_{inj} = Q_{ch}/2C$ satisfies $\Delta V_{inj}\,\tau = L^2/(2\mu)$, independent of $W$, $C$ and the overdrive. (b) Evaluate $L^2/(2\mu)$ for T130 and the injection error at the design's τ = 0.555 ns. (c) Repeat (b) for a channel length of 65 nm with the same mobility.

### Problem 20-05.7 [B]

**Scaling the distortion estimate.** Using the chapter's first-order estimate $\text{HD}_2 \approx \omega R_0C\alpha A/2$ with the design's $R_0$ = 767 Ω, α = 0.266 V⁻¹ and $C$ = 0.651 pF, find HD2 (a) at 25 MHz with a 0.2 V amplitude and (b) at 49 MHz with a 0.4 V amplitude but a switch twice as wide.

### Problem 20-05.8 [A]

**Jitter across frequency.** For 0.5 ps rms of jitter, find the jitter-limited SNR and the corresponding ENOB at 10 MHz, 100 MHz and 1 GHz.

### Problem 20-05.9 [B]

**A full noise budget.** Add to the design's quantization and kT/C noise a clock with 0.5 ps of jitter at a 49 MHz input and a comparator with 97.7 µV of input-referred noise. Find the jitter noise in µV rms, the total noise, the SNR and the ENOB.

### Problem 20-05.10 [B]

**A weak-inversion input pair.** A StrongARM's input pair runs at $g_m/I_D$ = 20 S/A ($V_{TH}$ = 0.45 V, γ = 2/3). (a) Find $A_{int}$ and the integration-node capacitance for 50 µV rms of input-referred noise. (b) Find the energy per decision and check that $E\sigma^2 = 8\gamma kTV_{DD}^2/A_{int}$. (c) How much capacitance would the same noise need at $g_m/I_D$ = 15 S/A?

### Problem 20-05.11 [B]

**Offset in a flash ADC.** A 6-bit flash ADC has a 1.0 V full scale and 63 comparators, each with an offset of standard deviation $A_{VT}/\sqrt{WL}$ ($A_{VT}$ = 3.5 mV·µm, Gaussian, independent). (a) Find the input-pair area for σ = LSB/4. (b) What is the probability that all 63 offsets lie within ±LSB/2? (c) Repeat for σ = LSB/8. What does this say about flash comparators?

### Problem 20-05.12 [B]

**Metastability in a flash ADC.** The latch has a node capacitance of 40 fF and a transconductance of 2 mS, and its preamplifier gain is $A_0$ = 5; $V_L$ = 0.6 V. (a) Find τ and the decision times for 1 mV and 10 µV inputs. (b) For the 6-bit flash of Problem 20-05.11 with 200 ps to decide and an input uniform over the full scale, find $v_{min}$ and the probability per conversion that the comparator nearest the input is unresolved ($\approx 2v_{min}/\Delta$). (c) How many such events per second occur at 1 GS/s?

### Problem 20-05.13 [C]

**A SAR timing budget.** A 12-bit synchronous SAR at 100 MS/s spends 7.5 ns of each 10 ns period on its 12 decisions; each decision includes 300 ps of DAC settling. With the design's $A_{int}$ = 6.75, $V_L$ = 0.6 V and $V_{FS}$ = 1.6 V, find (a) the time left for each comparison, (b) the largest τ that gives an error probability of 10⁻⁹ per conversion, and (c) the latch $g_m$ needed with 60 fF of regenerating capacitance.

### Problem 20-05.14 [B]

**Kickback into a resistor ladder.** In a flash ADC (LSB 15.6 mV), each comparator input connects to a reference-ladder tap with 500 Ω of resistance and 50 fF of capacitance. The comparator's drain swings 1.2 V through $C_{gd}$ = 2 fF. (a) Find the kickback step and the time for it to decay to 0.1 LSB. (b) A preamplifier cuts the coupling capacitance to 0.2 fF. Repeat (a).

### Problem 20-05.15 [C] *(lab)*

**Amplitude scaling of tracking distortion.** Simulate the design's bootstrapped switch (body at ground) at 49 MHz with amplitudes of 0.4 V and 0.2 V around 0.6 V. Find HD2 and HD3 in each case and explain the change from how each term scales with amplitude.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. kT/C noise and capacitor sizing | 1, 2 |
| 2. Switch sizing, bootstrapping and its distortion | 3, 4, 5, 7, 15 |
| 3. Charge injection and clock feedthrough | 6 |
| 4. Jitter and the noise budget | 8, 9 |
| 5. StrongARM gain, noise, energy, offset and kickback | 10, 11, 14 |
| 6. Regeneration, metastability and decision-time budgets | 12, 13 |
