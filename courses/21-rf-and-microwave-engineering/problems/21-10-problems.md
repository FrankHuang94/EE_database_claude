# Problems 21-10 · Antennas, Arrays, Beamforming and mmWave

Chapter: [21-10](../chapters/21-10-antennas-arrays-mmwave.md) · Worked solutions: [21-10 solutions](../solutions/21-10-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Patches use the transmission-line design equations of §3.2. Small-antenna bounds use $Q_{min} = 1/(ka)^3 + 1/ka$ and $B = (s - 1)/(Q\sqrt s)$. Arrays are uniform with isotropic-element array factors; element gain falls as $\cos\theta$ with scan unless stated. Phase errors are uniform and decorrelated. $c$ = 299,792,458 m/s. Problems marked *(lab)* can be checked with `labs/21-10-lab/antenna.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 21-10.1 [A]

**A 39 GHz patch.** *(lab)* Design a patch for 39 GHz on $\varepsilon_r$ = 3.5, $h$ = 0.2 mm. Find (a) $W$, (b) $\varepsilon_{eff}$, (c) $\Delta L$ and (d) $L$, and (e) the half-wavelength cell size.

### Problem 21-10.2 [A]

**Where the power goes.** An antenna has 70% radiation efficiency and presents VSWR 2.5. Find (a) its total efficiency and (b) that in dB. (c) A linearly polarized wave arrives tilted 30° from the antenna's polarization: what extra loss results?

### Problem 21-10.3 [B]

**An 868 MHz IoT antenna.** An antenna for 863–870 MHz fits in a sphere of 20 mm radius. Using 868 MHz, find (a) $ka$, (b) the Chu bound on Q and (c) the VSWR-2 bandwidth at 100% efficiency. (d) What fractional bandwidth does the band need (use its 866.5 MHz centre)? Can the antenna cover it without deliberate loss?

### Problem 21-10.4 [A]

**VSWR 3 against VSWR 2.** For an antenna with Q = 20, find the fractional bandwidth for (a) VSWR 3 and (b) VSWR 2. (c) By what percentage does relaxing the specification from VSWR 2 to 3 widen the band?

### Problem 21-10.5 [A]

**An 8 × 8 panel at 39 GHz.** An 8 × 8 array with λ/2 spacing at 39 GHz uses elements of 5 dBi. Find (a) its side length, (b) its gain at broadside and (c) its gain when steered to 50°.

### Problem 21-10.6 [B]

**Grating lobes.** (a) Up to what scan angle is an array with 0.6λ spacing free of grating lobes? (b) And with 0.8λ? (c) With 0.8λ spacing steered to 30°, where does the grating lobe appear?

### Problem 21-10.7 [B]

**Squint in a large array.** *(lab)* A 64-element linear array with λ/2 spacing at 39 GHz is steered to 45° with phase shifters. Find (a) its 3 dB squint bandwidth as a fraction and (b) in MHz, (c) the TTD delay span it would need, and (d) its broadside half-power beamwidth.

### Problem 21-10.8 [A]

**More bits.** Find (a) the gain loss and (b) the rms phase error of 5-bit phase shifters, and (c) the gain loss of 6-bit ones.

### Problem 21-10.9 [A]

**Handset EIRP.** A module drives 8 elements of 5 dBi gain, each PA delivering 8 dBm at the antenna feed, with 1 dB of feed loss. What EIRP results at broadside?

### Problem 21-10.10 [C]

**Sizing for DC power.** A transmit array must reach 50 dBm EIRP with 5 dBi elements, 20% PA efficiency and 50 mW of overhead per element. Find (a) the optimal element count and (b) the DC power there. (c) If a new process halves the overhead, what is the new optimal count?

### Problem 21-10.11 [B]

**A cheaper ADC.** Repeat Example 21-10.7's digital and hybrid cases with ADCs of ENOB 6 at 2 GS/s (Walden figure 20 fJ per step) and a hybrid array with 8 RF chains. Find (a) the power per ADC, (b) the digital array's power and (c) the hybrid array's power.

### Problem 21-10.12 [B]

**Oxygen at 60 GHz.** A 60 GHz link transmits the US unlicensed limit of 40 dBm average EIRP (§9) to a receive array of 15 dBi, in a 2.16 GHz channel with a 10 dB noise figure. Take gaseous absorption as 14.7 dB/km (ITU-R P.676 near 60 GHz, §9). Find (a) the noise floor, and at 50 m (b) the free-space path loss, (c) the absorption, (d) the received power and (e) the SNR. At 500 m find (f) the free-space path loss, (g) the absorption and (h) the SNR.

### Problem 21-10.13 [C]

**How many radar channels?** A radar needs 2° angular resolution near broadside from a filled λ/2 virtual array. Find (a) the number of virtual elements needed, (b) the smallest equal TX and RX counts that provide them and (c) the number of physical antennas, and (d) the resolution that array actually achieves.

### Problem 21-10.14 [C]

**How long does a beam sweep take?** An analog 16-element λ/2 array must cover ±60° with beams spaced by their width. (a) About how many beams does it need, and (b) how long does a sweep take if each beam needs one 0.125 ms slot? (c) For a 16 × 16 panel covering ±60° in both axes, how long would an exhaustive sweep take?

### Problem 21-10.15 [B]

**A 77 GHz radar chip.** TI's AWR2944 has 4 transmitters and 4 receivers, each transmitter delivering 13.5 dBm (§9). Arranged as a filled λ/2 virtual array, find (a) the number of virtual channels, (b) λ/2 at 77 GHz, (c) the virtual aperture and (d) the angular resolution near broadside. (e) With all four transmitters on together, what is the total conducted power, and (f) by how many dB does their coherent sum in the beam direction exceed one transmitter's?

### Problem 21-10.16 [C]

**Derive the quantization floor.** An $N$-element array has ideal weights $w_k$ (with $\sum\lvert w_k\rvert = 1$ and uniform amplitude $1/N$) and independent phase errors $\varepsilon_k$, each uniform in $\pm x$. (a) Show that $\langle e^{j\varepsilon}\rangle = \sin x/x$. (b) Writing the perturbed pattern as $AF = \sum_kw_ke^{j\varepsilon_k}e^{j\phi_k}$, show that $\langle\lvert AF\rvert^2\rangle = S\lvert AF_0\rvert^2 + (1 - S)/N$ with $S = (\sin x/x)^2$. (c) Evaluate the floor for 3-bit phase shifters on a 16-element array.

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Patch design and the Chu limit | 1, 2, 3, 4 |
| 2. Array gain, scan loss and grating lobes | 5, 6 |
| 3. Beam squint and true-time delay | 7 |
| 4. Phase quantization | 8, 16 |
| 5. EIRP, element count and beamforming power | 9, 10, 11, 14 |
| 6. Millimetre-wave links, packaging and radar arrays | 12, 13, 15 |
