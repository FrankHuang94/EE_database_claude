# Problems 24-07 · Photonics Fundamentals

Chapter: [24-07](../chapters/24-07-photonics-fundamentals.md) · Worked solutions: [24-07 solutions](../solutions/24-07-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- Physical constants are CODATA exact values: $h$ = 6.62607015 × 10⁻³⁴ J·s, $q$ = 1.602176634 × 10⁻¹⁹ C, $c$ = 299,792,458 m/s, $k$ = 1.380649 × 10⁻²³ J/K.
- Fiber group index is 1.468.
- A signal's spectral width is taken as its symbol rate, converted by $\Delta\lambda = \lambda^2\Delta f/c$.
- Receiver sensitivity is $P = Q\sigma/\mathcal R$ for OOK, plus optical penalties of $10\log_{10}3$ for PAM4 and $10\log_{10}((ER + 1)/(ER - 1))$ for extinction ratio.
- Temperatures are 300 K.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-07-lab/optics.py` or `tia.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-07.1 [A]

**A real photodiode.** A 1310 nm photodiode has a quantum efficiency of 0.8. Find (a) its responsivity and (b) its photocurrent at −6 dBm.

### Problem 24-07.2 [A]

**Decibels of light.** (a) What is −20 dBm in µW? (b) Four lanes each carry −2 dBm in one fiber; what is the total in mW and dBm?

### Problem 24-07.3 [A]

**Cable latency.** What is the one-way delay over 100 m of fiber, and the round trip? Compare the round trip with Ultra Ethernet's assumed 1 µs link round trip [R-517].

### Problem 24-07.4 [B]

**The square law of dispersion.** A 200 Gb/s-per-lane optical lane runs 113.4375 GBd PAM4 at 1310 nm (24-04). With the worst-case O-band dispersion of 3.5 ps/(nm·km), find (a) the spectral width, (b) the spread over 2 km and (c) the spread as a fraction of the UI. Compare with Example 24-07.3's 0.11 UI at 53.125 GBd.

### Problem 24-07.5 [B]

**A dispersion-limited reach.** A 26.5625 GBd NRZ lane (a 25 Gb/s Ethernet lane with its RS FEC) runs at 1550 nm on fiber with $D$ = 17 ps/(nm·km). What is the longest fiber that keeps the spread under 0.25 UI?

### Problem 24-07.6 [B]

**A TFLN modulator.** *(lab)* (a) How long must a 2.3 V·cm TFLN phase shifter be for $V_\pi$ = 1 V? (b) Biased at quadrature and driven over 0.8 $V_\pi$ peak to peak, find the high and low output fractions, the extinction ratio in dB and the OMA as a fraction of $P_{in}$.

### Problem 24-07.7 [B]

**The cost of keeping a ring on resonance.** *(lab)* Example 24-07.6's ring shifts 0.0561 nm/K. Its heater tunes 0.25 nm per mW (assumed). (a) How far must the heater tune to cover a 40 K ambient range? (b) At what heater power? (c) For a 100 Gb/s ring, what is that in fJ/bit, against the 5 fJ/bit of modulation?

### Problem 24-07.8 [B]

**A faster receiver.** A receiver has 0.85 A/W and 15 pA/√Hz over 60 GHz (assumed). Find (a) σ, (b) the OOK sensitivity at the KP4 threshold of 2.4 × 10⁻⁴, and (c) the PAM4 sensitivity with a 4 dB extinction ratio.

### Problem 24-07.9 [B]

**A 500 m budget.** A DR link launches 1 dBm per lane over 500 m of fiber at 0.36 dB/km with two connectors of 0.75 dB each (assumed). The receiver needs −8 dBm. Find the received power and the margin.

### Problem 24-07.10 [C]

**Designing a TIA.** *(lab)* A TIA must reach 30 GHz with $C_{in}$ = 80 fF and an amplifier gain of 8 (assumed). Find (a) the largest $R_F$, (b) its thermal noise density and (c) its contribution to σ over 30 GHz.

### Problem 24-07.11 [A]

**A DWDM grid at 1310 nm.** What wavelength spacing is a 100 GHz grid at 1310 nm, and what span do 16 channels occupy?

### Problem 24-07.12 [C]

**Optical dB again.** A link runs at BER 10⁻¹² when the received optical power drops by 3 dB. (a) By what factor does the photocurrent eye shrink? (b) By how many dB does the electrical SNR fall? (c) What does the BER become, with thermal noise fixed?

### Problem 24-07.13 [B]

**How good must the extinction ratio be?** What extinction ratio keeps its penalty at or below 1 dB? Give it as a ratio and in dB.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Wavelength windows and fiber types | 3, 4, 5 |
| 2. Loss, latency and dispersion | 3, 4, 5 |
| 3. Modulators | 6, 7 |
| 4. Receiver sensitivity and penalties | 1, 2, 8, 12, 13 |
| 5. Link budgets and WDM | 9, 11 |
| 6. TIA design | 10 |
