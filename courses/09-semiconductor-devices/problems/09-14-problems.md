# Problems 09-14 · Optoelectronic Devices

Chapter: [09-14](../chapters/09-14-optoelectronic-devices.md) · Worked solutions: [09-14 solutions](../solutions/09-14-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.
**Conventions:** 300 K; $V_T$ = 25.852 mV; $hc$ = 1.2398 eV·µm; $c$ = 2.998 × 10⁸ m/s; silicon $\varepsilon_r$ = 11.7. Values marked "assumed" are illustrative inputs, not data about a particular product. "Numerical" problems expect a short script or the lab notebook.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 09-14.1 [A]

**A germanium detector.** Germanium's gap is 0.661 eV (handbook). Find its cutoff wavelength. Can it detect 1.55 µm light? Find its responsivity at 1.31 µm for $\eta$ = 0.7.

### Problem 09-14.2 [A]

**Counting photons.** A receiver gets 10 µW at 1.55 µm with $\eta$ = 0.8. Find the photon arrival rate and the photocurrent.

### Problem 09-14.3 [B]

**Reflection and absorption.** A detector layer 10 µm thick has $\alpha$ = 10³ cm⁻¹ (assumed). Find the absorbed fraction, and the quantum efficiency (assuming every absorbed photon is collected) with a bare surface reflecting 30% and with an anti-reflection coating reflecting 2%.

### Problem 09-14.4 [B]

**RC bandwidth of a photodiode.** A silicon photodiode is 50 µm in diameter with a 2 µm depletion width, read by a 50 Ω load. Find its junction capacitance and the RC-limited bandwidth $1/2\pi RC$.

### Problem 09-14.5 [B]

**Why avalanche gain helps.** A receiver amplifier has an input noise of 1 pA/√Hz over 1 GHz. Find its rms noise current. What SNR does a 5 nA photocurrent give, and what would it give with an avalanche gain of 20 (ignoring the excess noise of multiplication)?

### Problem 09-14.6 [B]

**SPAD dead time.** A SPAD has a 10 ns dead time. Find its maximum count rate. If photons would trigger it at $n$ = 5 × 10⁷ s⁻¹ with no dead time, what rate does it record, using the non-paralyzable model $m = n/(1 + n\tau)$? If ambient light triggers it at 10⁶ s⁻¹, what is the chance of an ambient count in a 1 ns window?

### Problem 09-14.7 [A]

**Unambiguous range.** A dToF system fires pulses at a repetition rate $f$. A return that arrives after the next pulse is ambiguous. Find the maximum unambiguous range for 1 MHz and 10 MHz.

### Problem 09-14.8 [B]

**Shrinking the pixel.** A 1.4 µm pixel holds 6000 electrons. If full well scales with pixel area, what does a 0.8 µm pixel hold? Find its maximum SNR (in dB too) and its dynamic range with 1.5 electrons of read noise.

### Problem 09-14.9 [B]

**Low light.** A pixel receives 100 photons with a quantum efficiency of 0.8 and has 2 electrons of read noise (dark current negligible). Find its SNR, linear and in dB.

### Problem 09-14.10 [B]

**A red LED.** A 630 nm LED runs at 2.1 V, with an internal quantum efficiency of 0.85 and an extraction efficiency of 0.7 (assumed). Find the photon energy, the electrical efficiency $h\nu/qV$ and the wall-plug efficiency.

### Problem 09-14.11 [B]

**Designing a cavity.** (a) What cavity length gives a threshold gain of 40 cm⁻¹ with uncoated facets of $R$ = 0.30 and an internal loss of 10 cm⁻¹? (b) A distributed Bragg reflector reflects most strongly when its layer period is half the wavelength in the material. For 850 nm light and an average refractive index of 3.2, what period is needed?

### Problem 09-14.12 [C]

**Real solar cells (numerical).** For the cell of Example 09-14.8: (a) add a series resistance of 1 Ω·cm², so that $J = J_{sc} - J_0(e^{(V + JR_s)/V_T} - 1)$, and find the new maximum-power voltage, current density, power, fill factor and efficiency; (b) without series resistance, concentrate the light 100× (100 suns, 10 W/cm² and $J_{sc}$ = 4 A/cm²) and find the new $V_{oc}$, its rise, the fill factor and the efficiency. Why do concentrator cells need very low series resistance?

---

## Objective coverage

| Learning objective (chapter 09-14) | Problems |
|---|---|
| 1. Photon energy, absorption and band gap | 1, 3 |
| 2. Photodiode responsivity, bandwidth and noise | 2, 3, 4, 5 |
| 3. APDs, SPADs and time of flight | 5, 6, 7 |
| 4. Image-sensor pixels | 8, 9 |
| 5. LEDs and laser threshold | 10, 11 |
| 6. Solar cells | 12 |
