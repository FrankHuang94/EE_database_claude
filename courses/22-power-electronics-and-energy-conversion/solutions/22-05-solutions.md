# Solutions 22-05 · Magnetics Design

Problems: [22-05 problem set](../problems/22-05-problems.md) · Chapter: [22-05](../chapters/22-05-magnetics-design.md). Every number below is recomputed by [verify_22_05.py](../verify/verify_22_05.py).

---

## Solutions

### Solution 22-05.1

(a) $N = \sqrt{L/A_L} = \sqrt{50\ \mu\text{H}/482\ \text{nH}}$ = **10.19**, so 11 turns.

(b) $482\ \text{nH} \times 121$ = **58.3** µH. Rounding up a turn raises $L$ by 17%; a designer would instead pick a gap whose $A_L$ is nearer $L/N^2$.

(c) $\mathcal{R} = 1/(2600\ \text{nH}) + 0.2\ \text{mm}/(\mu_0 \times 97.1\ \text{mm}^2) = 3.846 \times 10^5 + 1.639 \times 10^6$ A/Wb, so $A_L$ = **494** nH. For this small gap the model is 2.5% high: the core term, taken from an ungapped $A_L$ with a +30/−20% tolerance, now matters, and fringing is small.

### Solution 22-05.2

The gap's share is $g/(g + \ell_e/\mu_e)$ with $\ell_e/\mu_e$ = 0.0469 mm.

(a) $0.1/0.1469$ = **68.1** %; (b) $1.0/1.0469$ = **95.5** %.

### Solution 22-05.3

(a) $B = LI/(NA_e) = 22\ \mu\text{H} \times 8/(15 \times 52\ \text{mm}^2)$ = **0.226** T.

(b) $B$ is proportional to $I$: $8 \times 0.39/0.2256$ = **13.8** A.

### Solution 22-05.4

(a) $N = LI_{pk}/(B_{max}A_e) = 100\ \mu\text{H} \times 6/(0.25 \times 97.1\ \text{mm}^2)$ = **24.7**.

(b) With 25 turns, $B_{pk}$ = **0.247** T.

(c) $g = \mu_0N^2A_e/L - \ell_e/\mu_e = 0.7627 - 0.0469$ = **0.716** mm.

(d) $A_L = L/N^2 = 100\ \mu\text{H}/625$ = **160** nH.

(e) $s = (160/153)^{-1/0.713}$ = **0.94** mm. Fringing lets the real gap be about 30% longer than the ideal model's.

### Solution 22-05.5

(a) $2^{1.635}$ = **3.11**; (b) $2^{2.253}$ = **4.77**.

(c) At fixed voltage and turns, $B_{pk} \propto 1/f$, so the loss changes by $2^{\alpha}2^{-\beta} = 2^{-0.618}$ = **0.652**. This is why raising a transformer's frequency at fixed turns reduces its core loss, until skin and proximity loss (and the switches) push back.

### Solution 22-05.6

With $1 - \alpha$ = −0.635:

(a) $(1/12)^{-0.635} + (11/12)^{-0.635}$ = **5.90**; (b) $0.75^{-0.635} + 0.25^{-0.635}$ = **3.61**.

The bracket at 0.5 is 3.106, so (c) **1.90** and (d) **1.16**. A 12 V to 1 V converter's inductor loses almost twice as much core energy per cycle as a symmetric triangle of the same swing would: its short, steep on-time edge dominates.

### Solution 22-05.7

(a) $p = \pi^2f^2B^2t^2/(6\rho) = \pi^2 \times 2500 \times 2.25 \times (0.35\ \text{mm})^2/(6 \times 0.5\ \mu\Omega\text{m})$ = **2.27** kW/m³.

(b) $2267/7650$ = **0.296** W/kg.

(c) $\pi^2 \times (2 \times 10^4)^2 \times 0.01 \times (0.35\ \text{mm})^2/(3\ \mu\Omega\text{m})$ = **1.61** MW/m³: 1.6 W per cubic centimetre from eddy currents alone, at a modest flux density. (The formula overestimates here: at 20 kHz the steel's skin depth is far below 0.35 mm, so the flux crowds to the surfaces; the true loss is lower but still prohibitive.) Steel laminations stop at audio frequencies.

### Solution 22-05.8

(a) $\delta = \sqrt{22.66\ \text{n}\Omega\text{m}/(\pi \times 2 \times 10^5 \times \mu_0)}$ = **0.169** mm; (b) $2\delta$ = **0.339** mm.

### Solution 22-05.9

(a) $\delta$ at 100 kHz and 100 °C is 0.2396 mm, so $\Delta = 0.2/0.2396$ = **0.835**.

(b) Dowell with $M$ = 3: $F_R$ = **1.466**.

(c) $1 + (5 \times 9 - 1)\Delta^4/45 = 1 + 44 \times 0.4856/45$ = **1.475**. The approximation is within 1% at $\Delta$ = 0.83.

### Solution 22-05.10

(a) $10 \times (1 + 0.00393 \times 80)$ = **13.14** mΩ; (b) $25 \times 13.14\ \text{m}\Omega$ = **0.329** W.

### Solution 22-05.11

(a) Take a circle of radius $r$ about the rod's axis. Faraday's law gives $E \cdot 2\pi r = \pi r^2\,dB/dt$, so $E(r) = (r/2)\,dB/dt$. The loss density at $r$ is $E^2/\rho$. Averaging over the cross-section of radius $R = d/2$,

$$
\frac{1}{\pi R^2}\int_0^R \frac{r^2}{4\rho}\left(\frac{dB}{dt}\right)^2 2\pi r\,dr = \frac{R^2}{8\rho}\left(\frac{dB}{dt}\right)^2 .
$$

With $\langle(dB/dt)^2\rangle = \omega^2B_{pk}^2/2$ and $R^2 = d^2/4$,

$$
p_{rod} = \frac{\omega^2B_{pk}^2d^2}{64\rho} = \frac{\pi^2f^2B_{pk}^2d^2}{16\rho} .
$$

(b) Against the slab's $\pi^2f^2B^2t^2/(6\rho)$, the ratio is $6/16$ = **0.375**. The rod's eddy loops are shorter in every direction.

(c) $\pi^2 \times 10^{10} \times 0.04 \times (11.1\ \text{mm})^2/(16 \times 5\ \Omega\text{m})$ = **6.08** kW/m³, about 2% of 3C95's 290 kW/m³ total.

### Solution 22-05.12

(a) $D = 5/12$; $\Delta i$ = 4 A; $L = V(1 - D)/(f_s\Delta i) = 5 \times (7/12)/(500\ \text{kHz} \times 4)$ = **1.46** µH.

(b) $I_{rms} = \sqrt{10^2 + 4^2/12}$ = **10.07** A; $I_{pk}$ = 12 A.

(c) $A_p = LI_{pk}I_{rms}/(K_uJB_{max}) = 1.458\ \mu\text{H} \times 12 \times 10.07/(0.4 \times 5\ \text{A/mm}^2 \times 0.25\ \text{T})$ = **352** mm⁴.

(d) $K_g = \rho L^2I_{pk}^2I_{rms}^2/(B_{max}^2P_{cu}K_u)$ = **1.41** × 10⁻¹³ m⁵.

(e) $1.90 \times 10^{-11}/1.407 \times 10^{-13}$ = **135**. The ETD34 is two orders of magnitude too large. A 1.5 µH, 12 A part is a molded powder-core chip inductor a few millimetres on a side, like the XAL7070 class (R-082).

### Solution 22-05.13

(a) $\Delta B_{opt} = 0.1 \times (2 \times 1.6/(2.5 \times 0.8))^{1/4.5} = 0.1 \times 1.6^{0.2222}$ = **0.111** T.

(b) $0.8 \times 1.110^{2.5}$ = **1.04** W; (c) $1.6/1.110^2$ = **1.30** W; (d) **2.34** W, against 2.4 W at the start.

(e) $1.039/1.298$ = **0.80** = $2/\beta$. ✓

(f) $N \propto 1/\Delta B$: $0.1/0.111$ = **0.90**, about 10% fewer turns. The design started close to optimal, so the saving is only 2.6%.

### Solution 22-05.14

(a) $L_{lk} = \mu_0N^2\,\text{MLT}(h_p/3 + d + h_s/3)/b_w = \mu_0 \times 1024 \times 60.5\ \text{mm} \times (0.4 + 0.4 + 0.267)\ \text{mm}/20.9\ \text{mm}$ = **3.97** µH; (b) **1.78** % of $L_m$.

(c) $\tfrac12 \times 3.973\ \mu\text{H} \times 2.52^2$ = **12.6** µJ; (d) $12.62\ \mu\text{J} \times 200/72 \times 100\ \text{kHz}$ = **3.50** W.

(e) $(h_p/12 + d/2 + h_s/12) = (0.1 + 0.2 + 0.0667)$ mm, so **1.37** µH; (f) **0.61** %; (g) **4.34** µJ; (h) **1.20** W.

The thick insulation needed for reinforced isolation (22-04) dominates the leakage: in (a) it contributes 0.4 of 1.07 mm, and interleaving halves its term but doubles the number of insulated interfaces. Interleaving saves 2.3 W, 3.3% of the 70.65 W input, which is why adapter transformers are interleaved despite the extra insulation layers.

### Solution 22-05.15

(a, b) $H = NI/\ell_e$, so $I = H\ell_e/N$. 45 Oe is 3581 A/m: $I = 3581 \times 0.0984/20$ = **17.6** A; 95 Oe is 7560 A/m: **37.2** A. (c, d) The inductance follows the permeability: $0.80 \times 10.0$ = **8.0** µH and $0.50 \times 10.0$ = **5.0** µH. (e) The ripple scales as $1/L$: $2.0/0.80$ = **2.50** A, a quarter more than designed, with a correspondingly higher peak current and RMS loss. (f) A gapped ferrite keeps almost its full inductance up to $B_{sat}$ and then loses it within a few per cent more current (Lab 22-05, Part 1), so its current runs away; the powder core's distributed gap lets the inductance fall gradually, which is why data sheets quote its "saturation current" as a stated percentage drop.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-05.1a | turns for 50 µH | 10.19 | |
| 22-05.1b | inductance with 11 turns | 58.3 | µH |
| 22-05.1c | ideal A_L, 0.2 mm gap | 494 | nH |
| 22-05.2a | gap energy share, 0.1 mm | 68.1 | % |
| 22-05.2b | gap energy share, 1.0 mm | 95.5 | % |
| 22-05.3a | flux density at 8 A | 0.226 | T |
| 22-05.3b | current at 390 mT | 13.8 | A |
| 22-05.4a | turns before rounding | 24.7 | |
| 22-05.4b | flux density with 25 turns | 0.247 | T |
| 22-05.4c | ideal-model gap | 0.716 | mm |
| 22-05.4d | required A_L | 160 | nH |
| 22-05.4e | gap from the A_L fit | 0.94 | mm |
| 22-05.5a | loss factor, frequency doubled | 3.11 | |
| 22-05.5b | loss factor, flux doubled | 4.77 | |
| 22-05.5c | loss factor, transformer frequency doubled | 0.652 | |
| 22-05.6a | bracket at D = 1/12 | 5.90 | |
| 22-05.6b | bracket at D = 0.75 | 3.61 | |
| 22-05.6c | ratio at D = 1/12 | 1.90 | |
| 22-05.6d | ratio at D = 0.75 | 1.16 | |
| 22-05.7a | lamination loss at 50 Hz | 2.27 | kW/m³ |
| 22-05.7b | lamination loss per kg at 50 Hz | 0.296 | W/kg |
| 22-05.7c | lamination loss at 20 kHz | 1.61 | MW/m³ |
| 22-05.8a | skin depth at 200 kHz | 0.169 | mm |
| 22-05.8b | largest wire diameter | 0.339 | mm |
| 22-05.9a | Δ | 0.835 | |
| 22-05.9b | Dowell F_R | 1.466 | |
| 22-05.9c | thin-layer F_R | 1.475 | |
| 22-05.10a | resistance at 100 °C | 13.14 | mΩ |
| 22-05.10b | hot loss at 5 A | 0.329 | W |
| 22-05.11b | rod-to-slab ratio | 0.375 | |
| 22-05.11c | rod eddy loss density | 6.08 | kW/m³ |
| 22-05.12a | inductance | 1.46 | µH |
| 22-05.12b | RMS current | 10.07 | A |
| 22-05.12c | required area product | 352 | mm⁴ |
| 22-05.12d | required K_g | 1.41 | ×10⁻¹³ m⁵ |
| 22-05.12e | ETD34 K_g over required | 135 | |
| 22-05.13a | optimum flux swing | 0.111 | T |
| 22-05.13b | core loss at the optimum | 1.04 | W |
| 22-05.13c | copper loss at the optimum | 1.30 | W |
| 22-05.13d | total at the optimum | 2.34 | W |
| 22-05.13e | core-to-copper ratio | 0.80 | |
| 22-05.13f | turns factor | 0.90 | |
| 22-05.14a | leakage inductance | 3.97 | µH |
| 22-05.14b | leakage share of L_m | 1.78 | % |
| 22-05.14c | leakage energy | 12.6 | µJ |
| 22-05.14d | clamp loss | 3.50 | W |
| 22-05.14e | interleaved leakage | 1.37 | µH |
| 22-05.14f | interleaved share | 0.61 | % |
| 22-05.14g | interleaved energy | 4.34 | µJ |
| 22-05.14h | interleaved clamp loss | 1.20 | W |
| 22-05.15a | current at 45 Oe | 17.6 | A |
| 22-05.15b | current at 95 Oe | 37.2 | A |
| 22-05.15c | inductance at 45 Oe | 8.0 | µH |
| 22-05.15d | inductance at 95 Oe | 5.0 | µH |
| 22-05.15e | ripple at 45 Oe | 2.50 | A |
