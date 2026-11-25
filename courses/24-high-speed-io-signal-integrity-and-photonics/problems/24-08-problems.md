# Problems 24-08 · Silicon Photonics and Optical Transceivers

Chapter: [24-08](../chapters/24-08-silicon-photonics.md) · Worked solutions: [24-08 solutions](../solutions/24-08-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.**

- $hc/q$ = 1239.84 nm·eV (CODATA constants).
- Modes are circular Gaussians of $1/e$ field radius $w$ (half the mode-field diameter); coupling is $\eta = (2w_1w_2/(w_1^2 + w_2^2))^2\exp(-2d^2/(w_1^2 + w_2^2))$ for lateral offset $d$, and tilt costs $\exp(-(\alpha/\theta_{div})^2)$ with $\theta_{div} = \lambda/(\pi w)$.
- Grating couplers obey $\Lambda = \lambda/(n_{eff} - \sin\theta)$ with $n_{eff}$ independent of wavelength.
- Linear chains add $1/Q^2$; retimed chains add BER.
- "Assumed" values are illustrative.
- Problems marked *(lab)* can be checked with `labs/24-08-lab/siph.py` or `bond.cir`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 24-08.1 [A]

**Cutoff wavelengths.** Find the cutoff wavelengths of GaAs (1.42 eV) and InP (1.34 eV). Which of them could detect 850 nm light, and which 1310 nm light?

### Problem 24-08.2 [A]

**A silicon-nitride waveguide.** Silicon nitride ($n$ = 2.0, assumed) is also used for waveguides in oxide ($n$ = 1.44). At 1310 nm find (a) its critical angle, (b) $\sqrt{n_1^2 - n_2^2}$ and its largest single-mode slab thickness, and (c) the same thickness for silicon ($n$ = 3.48, taken as unchanged) and the ratio of the two.

### Problem 24-08.3 [B]

**A better spot-size converter.** *(lab)* (a) What efficiency and loss couple a 4.6 µm fiber mode into a 2.0 µm chip mode? (b) What does a 1 µm lateral offset cost between matched 4.6 µm modes, and (c) between matched 2.0 µm modes?

### Problem 24-08.4 [B]

**A C-band grating coupler.** *(lab)* At 1550 nm, a grating has $n_{eff}$ = 2.85 and radiates at 8° (assumed) toward a fiber of MFD 10.4 µm [R-526]. Find (a) the period, (b) the angular dispersion, (c) the divergence half-angle and (d) the 1-dB bandwidth.

### Problem 24-08.5 [B]

**An FR4 lane with an EML.** A CWDM4 lane at 2 km must deliver −7.0 dBm with 2 dB margin. The fiber loses 0.36 dB/km [R-526]; two connectors lose 0.5 dB each; the multiplexer loses 1.5 dB; the EML's modulator section costs 6 dB of average power relative to its laser section (all assumed). Find (a) the laser section's required output in dBm and (b) in mW, and (c) the total for four lanes in mW.

### Problem 24-08.6 [B]

**A shorter wire bond.** *(lab)* Repeat Example 24-08.6 with a 0.5 nH bond. Find (a) $f_0$ and $\zeta$, (b) the peak frequency and peaking in dB, and (c) $f_{3dB}$. (d) Is it good enough for 113.4375 GBd?

### Problem 24-08.7 [B]

**Unequal segments.** *(lab)* Two host channels each give $Q$ = 9 and the optical channel $Q$ = 7.5. Find (a) the end-to-end $Q$ and BER of a linear chain and (b) the BER if every boundary retimes.

### Problem 24-08.8 [A]

**How much of a switch is optics?** A 51.2 Tb/s switch has 64 ports filled with 800 Gb/s DR4 modules at 16 W typical [R-533]. The rest of the switch draws 1.5 kW (assumed). Find (a) the optics' total power, (b) their share of the box and (c) their energy per bit.

### Problem 24-08.9 [B]

**A 16-lane PIC.** Each of 16 lanes works with probability 0.998 (assumed), and assembly costs three times the PIC ($c_P$ = 1, $c_A$ = 3). Find (a) the yield, (b) the cost per good module without and (c) with perfect wafer test, and (d) the saving.

### Problem 24-08.10 [C]

**An optical I/O chiplet.** Ayar Labs' TeraPHY has 8 optical ports, each with 16 transmit and 16 receive lanes at 32 Gb/s NRZ on 16 wavelengths, and 16 UCIe-S modules at 896 Gb/s/mm of shoreline [R-540]. Find (a) the rate per fiber per direction, (b) the optical bandwidth in both directions, (c) the electrical edge length the 8.192 Tb/s needs, and (d) explain why it uses many slow NRZ wavelengths rather than a few 200 Gb/s PAM4 lanes.

### Problem 24-08.11 [B]

**Reading market forecasts.** LightCounting put AI-cluster Ethernet optics plus CPO at $8 B in 2025 and $20 B in 2030; TrendForce put AI optical transceivers at $16.5 B in 2025 and $26 B in 2026 [R-539]. Find (a) LightCounting's compound annual growth rate and (b) TrendForce's one-year growth. (c) Why can both be right?

### Problem 24-08.12 [C]

**A grating coupler for CWDM4?** *(lab)* Example 24-08.4's grating is centred at 1301 nm, in the middle of the CWDM4 grid (1271, 1291, 1311 and 1331 nm). Find the tilt loss of (a) the outer and (b) the inner channels. (c) What would you recommend?

### Problem 24-08.13 [C]

**Optics in a fabric.** Each GPU has one 800 Gb/s scale-out port. In a two-tier leaf-spine fabric each port's traffic crosses two links (GPU to leaf, leaf to spine), and in a three-tier fabric three; each link has a 16 W module at both ends (all assumed). Find (a) the optics power per GPU in each case, (b) the totals for 100,000 GPUs, and (c) what a 25% cut in module power (Example 24-08.8) saves in the three-tier fabric.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Silicon, germanium and III-V materials | 1 |
| 2. Waveguides, coupling and alignment | 2, 3 |
| 3. Grating couplers | 4, 12 |
| 4. Laser budgets and driver parasitics | 5, 6 |
| 5. The DSP, retimed and linear links | 7, 10 |
| 6. Module power, yield and market claims | 8, 9, 11, 13 |
