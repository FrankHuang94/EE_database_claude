# Solutions 25-03 · Deposition, Etch, CMP, Implant and Metrology

Problems: [25-03 problems](../problems/25-03-problems.md) · Chapter: [25-03](../chapters/25-03-deposition-etch-cmp-implant-metrology.md)

Every number is recomputed by [verify_25_03.py](../verify/verify_25_03.py).

---

## Solutions

### Solution 25-03.1

$20 \times 1.0/21$ = **0.952** cm/s, within 5% of $h_g$: transport-limited. Raising temperature barely helps; increase the gas supply (flow, partial pressure) or thin the boundary layer (lower pressure, better reactor geometry).

### Solution 25-03.2

(a) Supply $F_1 = h_g(C_g - C_s)$ and reaction $F_2 = k_sC_s$ are equal at steady state, so $C_s = h_gC_g/(h_g + k_s)$ and $F = k_sC_s = k_sh_gC_g/(k_s + h_g)$. Dividing by $N$ gives $v$. If $k_s \ll h_g$, $v \approx k_sC_g/N$ (reaction-limited); if $k_s \gg h_g$, $v \approx h_gC_g/N$ (transport-limited).

(b) With $k_s = h_g = h$: $h^2/(2h) = h/2$.

(c) Solve $0.050\,e^{-(1.5/k)(1/T - 1/923.15)} = 2.0$ for $T$: **875** °C. Below it the process is reaction-limited, above it transport-limited.

### Solution 25-03.3

$3.0/0.09$ = 33.3, so **34** cycles, taking $34 \times 3.0$ = **102** s.

### Solution 25-03.4

(a) $0.020 \times 63.55/(2 \times 96{,}485 \times 8.96)$ cm/s = **7.35** nm/s.

(b) $1500/7.35$ = **204** s.

(c) $0.020\ \text{A/cm}^2 \times 707\ \text{cm}^2 \times 204\ \text{s}$ = **2.9e3** C. The charge for a given thickness does not depend on the current density; only the time does.

### Solution 25-03.5

Nominal clearing is $80/60$ = 1.333 min, so the recipe runs **1.73** min. The fastest region (64.8 nm/min) clears at **1.23** min and its stop layer is exposed for **0.499** min. Requiring $0.499 \times 64.8/S \le 1.0$ gives $S \ge$ **32.3**, so about 33:1.

### Solution 25-03.6

(a) $300 \times 1.1$ = **330** nm per edge.

(b) $1000 - 2 \times 330$ = **340** nm.

(c) The undercut is as large as the film is thick, so features narrower than about twice the film thickness disappear; anisotropic plasma etching avoids it.

### Solution 25-03.7

(a) $2.4 \times 10^{-13} \times 3.0 \times 6895 \times 1.5$ m/s = **447** nm/min.

(b) $400/447$ = **0.90** min.

### Solution 25-03.8

(a) $199/0.50$ = **397** nm/min.

(b) $300/397$ = **0.76** min. Compared with the 25% region's 794 nm/min, this region planarizes half as fast: the two regions finish at different times, which is the origin of within-die thickness variation.

### Solution 25-03.9

(a) $5 \times 10^{15} \times 1.602 \times 10^{-19} \times 707/0.0050$ = **113** s.

(b) $5 \times 10^{15}/(\sqrt{2\pi} \times 20 \times 10^{-7})$ = **9.97e20** cm⁻³.

### Solution 25-03.10

$\sqrt{2\ln(9.97 \times 10^{20}/10^{17})}$ = **4.29**, so $x_j = 50 + 20 \times 4.29$ = **136** nm.

### Solution 25-03.11

(a) At 950 °C, $kT$ = **0.1054** eV and $D = 0.76\,e^{-3.46/0.1054}$ = **4.21e-15** cm²/s.

(b) $30 \times 1.53 \times 10^{-14}/4.21 \times 10^{-15}$ = **109** min.

(c) The same diffusion can be bought at lower temperature, but activation, damage annealing and other temperature-sensitive steps (silicides, gate stacks) differ; a lower temperature for a longer time also lengthens cycle time. Equal $Dt$ is only one of several constraints.

### Solution 25-03.12

(a) $\sigma_m = 0.10 \times 3.0/6$ = **0.050** nm.

(b) $\sqrt{0.40^2 + 0.050^2}$ = **0.403** nm, less than 1% above the true spread.

### Solution 25-03.13

(a) DRAM: $38.8/1.390$ = **27.9** \$B; foundry/logic: $78.0/1.189$ = **65.6** \$B.

(b) $143.9 - 116.9$ = **27.0** \$B.

### Solution 25-03.14

(a) $0.5431 + 0.30 \times (0.5658 - 0.5431)$ = **0.5499** nm.

(b) $(0.5499 - 0.5431)/0.5431$ = **1.25**%.

(c) Compression: the SiGe film's natural spacing is larger than silicon's, and it is squeezed in the plane to match.

### Solution 25-03.15

(a) Let $\eta = x/(2\sqrt{Dt})$, so $\partial\eta/\partial t = -\eta/(2t)$ and $\partial\eta/\partial x = 1/(2\sqrt{Dt})$. With $\operatorname{erfc}\eta = 1 - (2/\sqrt\pi)\int_0^\eta e^{-u^2}du$, its derivative is $-(2/\sqrt\pi)e^{-\eta^2}$. Then

$$
\frac{\partial C}{\partial t} = C_s\left(-\frac{2}{\sqrt\pi}e^{-\eta^2}\right)\left(-\frac{\eta}{2t}\right) = \frac{C_s\,\eta}{\sqrt\pi\,t}\,e^{-\eta^2},
$$

$$
\frac{\partial C}{\partial x} = -\frac{C_s}{\sqrt{\pi Dt}}\,e^{-\eta^2}, \qquad
\frac{\partial^2 C}{\partial x^2} = -\frac{C_s}{\sqrt{\pi Dt}}\,e^{-\eta^2}(-2\eta)\frac{1}{2\sqrt{Dt}} = \frac{C_s\,\eta}{\sqrt\pi\,Dt}\,e^{-\eta^2},
$$

so $D\,\partial^2C/\partial x^2 = \partial C/\partial t$. At $x = 0$, $\eta = 0$ and $\operatorname{erfc}0 = 1$, so $C = C_s$; as $t \to 0$ for $x > 0$, $\eta \to \infty$ and $C \to 0$. The dose is

$$
Q = \int_0^\infty C_s\operatorname{erfc}\frac{x}{2\sqrt{Dt}}\,dx = 2C_s\sqrt{Dt}\int_0^\infty\operatorname{erfc}u\,du = 2C_s\sqrt{Dt}\cdot\frac{1}{\sqrt\pi},
$$

using integration by parts: $\int_0^\infty\operatorname{erfc}u\,du = [u\operatorname{erfc}u]_0^\infty + (2/\sqrt\pi)\int_0^\infty ue^{-u^2}du = 0 + 1/\sqrt\pi$. Units: cm⁻³ × cm = cm⁻². ✓

(b) $kT = 8.61733 \times 10^{-5} \times 1223.15$ = 0.105403 eV; $D = 0.76\,e^{-3.46/0.105403}$ = **4.21e-15** cm²/s. With $t$ = 1200 s, $\sqrt{Dt}$ = **22.5** nm. Dose $Q = 2 \times 2.5 \times 10^{20} \times 2.248 \times 10^{-6}/\sqrt\pi$ = **6.34e14** cm⁻². The junction is where $C = N_B$: $\operatorname{erfc}\eta_j = 10^{16}/2.5 \times 10^{20} = 4.0 \times 10^{-5}$, so $\eta_j$ = **2.90** (from a table or `scipy.special.erfcinv`; by hand, iterate $\eta = \sqrt{-\ln(4.0 \times 10^{-5}\sqrt\pi\,\eta)}$ from $\eta$ = 3, which uses $\operatorname{erfc}\eta \approx e^{-\eta^2}/(\eta\sqrt\pi)$ and lands within 1%). Then $x_j = 2\sqrt{Dt}\,\eta_j$ = **131** nm.

(c) $kT$ = 0.118329 eV; $D = 0.76\,e^{-3.46/0.118329}$ = **1.52e-13** cm²/s; $Dt = 1.52 \times 10^{-13} \times 3600 = 5.47 \times 10^{-10}$ cm², against $5.05 \times 10^{-12}$ cm² for the predeposition: a ratio of **108**. The drive-in spreads the dopant over a length $\sqrt{Dt}$ that is $\sqrt{108}$ = **10.4** times the predeposited layer's own, so the initial shape is forgotten and only its dose matters, just as a narrow implant is treated as a sheet. (The verify script checks this by convolving the erfc profile with the reflecting-surface Green's function: the junction depth agrees with the sheet model within 1%.)

(d) Surface concentration $Q/\sqrt{\pi Dt} = 6.34 \times 10^{14}/\sqrt{\pi \times 5.47 \times 10^{-10}}$ = **1.53e19** cm⁻³. Setting $C(x_j) = N_B$: $x_j = 2\sqrt{Dt\,\ln[Q/(N_B\sqrt{\pi Dt})]} = 2\sqrt{5.47 \times 10^{-10} \times \ln 1530}$ = **1.27** µm. The drive-in has lowered the surface concentration by a factor of **16.3** and pushed the junction **9.7** times deeper, which is why predeposition sets the dose and drive-in sets the depth.

(e) Any two of: (1) during the predeposition the boron concentration (2.5 × 10²⁰ cm⁻³) is far above the intrinsic carrier density at 950 °C, so diffusion is concentration-enhanced, not intrinsic; (2) an oxidizing drive-in injects silicon interstitials that enhance boron diffusion (oxidation-enhanced diffusion); (3) the ramp-up and ramp-down of each furnace step add thermal budget not counted in the plateau times. (Segregation of boron into a growing oxide works the other way, removing dose from the silicon.)

### Solution 25-03.16

(a) $R_s = (\pi/\ln 2)V/I = 4.532 \times V/I$: after the low-temperature anneal $4.532 \times 41.7\ \text{mV}/1.00\ \text{mA}$ = **189.0** Ω/□; after the spike anneal **73.4** Ω/□.

(b) A thin slice of thickness $dx$ at depth $x$ has sheet conductance $q\mu N_a(x)\,dx$, and slices conduct in parallel, so $1/R_s = q\int\mu N_a(x)\,dx = q\mu Q_a$ for uniform $\mu$ (09-03). Hence $Q_a = 1/(q\mu R_s)$:

- low-temperature anneal: $1/(1.6022 \times 10^{-19} \times 50 \times 189.0)$ = **6.60e14** cm⁻², an activated fraction of **33.0**%;
- spike anneal: **1.70e15** cm⁻², **85.0**% activated.

Units: 1/(C × cm²/(V·s) × V/A) = A·s/(C·cm²) = cm⁻². ✓ The assumed mobility carries the main uncertainty: hole mobility falls with concentration (09-03), so a fab calibrates $R_s$ against dose with reference wafers rather than trusting an absolute mobility.

(c) $L/W$ = 20 squares, so $R = 20 \times 73.4$ = **1.47** kΩ.

(d) With two probes the measured voltage includes the contact (spreading) resistance of each metal probe on silicon, which can be comparable to or larger than the layer's own resistance and varies from touchdown to touchdown. The four-point probe forces current through the outer pair and senses voltage with the inner pair, which draws essentially no current, so the contact resistances carry no current in the sensing loop and drop out (the Kelvin connection).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 25-03.1a | effective rate constant | 0.952 | cm/s |
| 25-03.2c | temperature where ks = hg | 875 | °C |
| 25-03.3a | cycles | 34 | |
| 25-03.3a0 | exact cycles | 33.3 | |
| 25-03.3b | time | 102 | s |
| 25-03.4a | plating rate | 7.35 | nm/s |
| 25-03.4b | time for 1.5 µm | 204 | s |
| 25-03.4c | charge | 2.9e3 | C |
| 25-03.5a0 | nominal clearing time | 1.333 | min |
| 25-03.5a | recipe time | 1.73 | min |
| 25-03.5b0 | fastest etch rate | 64.8 | nm/min |
| 25-03.5b | fastest clearing time | 1.23 | min |
| 25-03.5b1 | stop-layer exposure | 0.499 | min |
| 25-03.5c | required selectivity | 32.3 | |
| 25-03.6a | undercut per edge | 330 | nm |
| 25-03.6b | remaining width | 340 | nm |
| 25-03.7a | removal rate | 447 | nm/min |
| 25-03.7b | time for 400 nm | 0.90 | min |
| 25-03.8a | rate on 50% features | 397 | nm/min |
| 25-03.8b | time to remove a 300 nm step | 0.76 | min |
| 25-03.9a | implant time | 113 | s |
| 25-03.9b | peak concentration | 9.97e20 | cm⁻³ |
| 25-03.10a | square-root factor | 4.29 | |
| 25-03.10b | junction depth | 136 | nm |
| 25-03.11a0 | kT at 950 C | 0.1054 | eV |
| 25-03.11a | D at 950 C | 4.21e-15 | cm²/s |
| 25-03.11b | equivalent time | 109 | min |
| 25-03.12a | gauge sigma for P/T = 0.1 | 0.050 | nm |
| 25-03.12b | apparent spread | 0.403 | nm |
| 25-03.13a | DRAM 2025 | 27.9 | $B |
| 25-03.13a1 | foundry/logic 2025 | 65.6 | $B |
| 25-03.13b | WFE increase | 27.0 | $B |
| 25-03.14a | SiGe lattice constant | 0.5499 | nm |
| 25-03.14b | mismatch | 1.25 | % |
| 25-03.15b | D at 950 C | 4.21e-15 | cm²/s |
| 25-03.15b1 | sqrt(Dt) predeposition | 22.5 | nm |
| 25-03.15b2 | predeposited dose | 6.34e14 | cm⁻² |
| 25-03.15b3 | erfc argument at junction | 2.90 | |
| 25-03.15b4 | predeposition junction depth | 131 | nm |
| 25-03.15c | D at 1100 C | 1.52e-13 | cm²/s |
| 25-03.15c1 | Dt ratio drive-in/predep | 108 | |
| 25-03.15c2 | diffusion-length ratio | 10.4 | |
| 25-03.15d | surface concentration after drive-in | 1.53e19 | cm⁻³ |
| 25-03.15d1 | junction depth after drive-in | 1.27 | µm |
| 25-03.15d2 | surface concentration ratio | 16.3 | |
| 25-03.15d3 | junction depth ratio | 9.7 | |
| 25-03.16a | Rs low-temperature anneal | 189.0 | Ω/□ |
| 25-03.16a1 | Rs spike anneal | 73.4 | Ω/□ |
| 25-03.16b | active dose low-T | 6.60e14 | cm⁻² |
| 25-03.16b1 | activated fraction low-T | 33.0 | % |
| 25-03.16b2 | active dose spike | 1.70e15 | cm⁻² |
| 25-03.16b3 | activated fraction spike | 85.0 | % |
| 25-03.16c | resistor | 1.47 | kΩ |
