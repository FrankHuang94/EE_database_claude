# Solutions 09-02 · Carriers, Doping and the Fermi Level

Problems: [09-02 problems](../problems/09-02-problems.md) · Chapter: [09-02](../chapters/09-02-carriers-doping-fermi-level.md). Every number below is recomputed by [verify_09_02.py](../verify/verify_09_02.py): effective densities of states by integrating the density of states against the occupation, carrier densities by solving charge neutrality for the Fermi level with full Fermi–Dirac integrals and dopant ionization, temperatures by root finding, and dopant counts by Poisson probabilities checked against random sampling.

---

## Solutions

### Solution 09-02.1

(a) $N_C = 2.509\times10^{19}\,(m_{dn}/m_0)^{3/2}$ cm⁻³ at 300 K. With 0.067: **4.352 × 10¹⁷** cm⁻³; with 0.063: **3.968 × 10¹⁷** cm⁻³. Hu's 4.7 × 10¹⁷ lies **8.0**% above the first. Tabulated values differ by this much because they rest on different mass values (0.063 to 0.068 $m_0$ appear in the sources of 09-01) and different temperature corrections.

(b) $N_C \propto T^{3/2}$: at 77 K, $3.2\times10^{19} \times (77/300)^{1.5}$ = **4.161 × 10¹⁸** cm⁻³; at 400 K, $3.2\times10^{19} \times (4/3)^{1.5}$ = **4.927 × 10¹⁹** cm⁻³.

### Solution 09-02.2

(a) $f = 1/(1 + e^{x})$ with $x = (E - E_F)/kT$: $x$ = 1 gives **0.2689**, $x$ = 3 gives **0.04743**, $x$ = 10 gives **4.540 × 10⁻⁵**.

(b) The Boltzmann factor $e^{-x}$ exceeds $f$ by the fraction $e^{-x}(1 + e^x) - 1 = e^{-x}$: **36.8**% at $kT$, **4.98**% at $3kT$ and **0.0045**% at $10kT$. This is the origin of the "$3kT$" rule for non-degenerate statistics.

(c) A state 0.10 eV below $E_F$ has $x = -0.10/0.02585 = -3.868$; it is empty with probability $1 - f = 1/(1 + e^{3.868})$ = **0.02047**.

### Solution 09-02.3

$n = N_D$ = 5 × 10¹⁵ cm⁻³; $p = n_i^2/n = 10^{20}/(5\times10^{15})$ = **2.0 × 10⁴** cm⁻³. $E_F - E_i = kT\ln(n/n_i) = 0.02585\ln(5\times10^5)$ = **0.3392** eV. $E_C - E_F = kT\ln(N_C/n) = 0.02585\ln(6400)$ = **0.2266** eV.

### Solution 09-02.4

$p = N_Ve^{-(E_F - E_V)/kT} = 1.8\times10^{19}\,e^{-0.20/0.02585}$ = **7.86 × 10¹⁵** cm⁻³. With complete ionization and $p \gg n$, $N_A = p$ = **7.86 × 10¹⁵** cm⁻³. $n = n_i^2/p$ = **1.272 × 10⁴** cm⁻³ and $E_i - E_F = kT\ln(p/n_i)$ = **0.3509** eV.

### Solution 09-02.5

(a) Net doping $N_D - N_A = 5\times10^{16} - 3\times10^{16} = 2\times10^{16}$ cm⁻³ of donors: **n-type**.

(b) $n$ = 2 × 10¹⁶ cm⁻³, $p = 10^{20}/(2\times10^{16})$ = **5.0 × 10³** cm⁻³, $E_F - E_i = 0.02585\ln(2\times10^6)$ = **0.3751** eV.

(c) All $N_D + N_A$ = **8 × 10¹⁶** cm⁻³ ions remain and scatter carriers, four times the net doping. The mobility (09-03) is set by this total, so the counter-doped region conducts worse than a region doped only with 2 × 10¹⁶ cm⁻³ donors.

### Solution 09-02.6

Varshni: $E_g(250\ \text{K})$ = **1.1366** eV and $E_g(350\ \text{K})$ = **1.1112** eV ($E_g(300\ \text{K})$ = 1.1245 eV). The course model gives

$$
n_i(T) = 10^{10}\left(\frac{T}{300}\right)^{3/2}\exp\left[\frac{1.1245}{2(0.025852)} - \frac{E_g(T)}{2kT}\right] .
$$

At 250 K ($kT$ = 21.54 meV): $n_i$ = **7.41 × 10⁷** cm⁻³. At 350 K ($kT$ = 30.16 meV): $n_i$ = **3.51 × 10¹¹** cm⁻³. The ratio is **4736**: a 100 K span changes $n_i$ by more than three and a half decades.

### Solution 09-02.7

(a) $p = n_i^2/n = 10^{20}/(2\times10^{15})$ = **5.0 × 10⁴** cm⁻³.

(b) $np/n_i^2 = 2.1\times10^{15} \times 1.0\times10^{14}/10^{20}$ = **2.1 × 10⁹**.

(c) The law of mass action is an *equilibrium* result: it follows from describing both carrier types with one Fermi level, which is valid only when generation and recombination balance with no external drive. Light generates extra pairs, so $np$ exceeds $n_i^2$ until the light is removed and recombination restores equilibrium. Out of equilibrium, electrons and holes are each described by their own **quasi-Fermi level**, and $np = n_i^2e^{(E_{Fn} - E_{Fp})/kT}$ (09-04). Note the asymmetry: the majority density rose only **5**% while the minority density rose by a factor of **2 × 10⁹**, which is why devices are analyzed through their minority carriers.

### Solution 09-02.8

(a) $E_C - E_D = 13.606 \times 0.067/12.9^2$ = **5.48** meV; $a_D = 0.05292 \times 12.9/0.067$ = **10.19** nm.

(b) Orbits touch at $N_D = (2a_D)^{-3} = (20.38\times10^{-7}\ \text{cm})^{-3}$ = **1.18 × 10¹⁷** cm⁻³.

(c) The binding energy equals $kT$ at **64** K, so GaAs donors stay ionized down to far lower temperatures than silicon's 45 meV donors. The large orbit (light mass, large dielectric constant) means donors begin to overlap at concentrations about **78** times lower than in silicon (Example 09-02.3 found 9.3 × 10¹⁸ cm⁻³), so moderately doped GaAs already conducts through an impurity band.

### Solution 09-02.9

Neutrality with electrons ignored: $p = N_A^- = N_A/[1 + g_Ae^{(E_A - E_F)/kT}]$. Since $p = N_Ve^{-(E_F - E_V)/kT}$, $e^{(E_A - E_F)/kT} = (p/N_V)e^{(E_A - E_V)/kT}$, so $p(1 + ap) = N_A$ with $a = (g_A/N_V)e^{(E_A - E_V)/kT}$, and $p = (-1 + \sqrt{1 + 4aN_A})/2a$.

(a) Boron: $e^{0.045/0.02585}$ = **5.701**, $a = 4 \times 5.701/1.8\times10^{19}$ = **1.267 × 10⁻¹⁸** cm³, $p$ = **9.876 × 10¹⁵** cm⁻³: **98.8**% ionized.

(b) Indium: $e^{0.157/0.02585}$ = **434.0**, $a$ = **9.644 × 10⁻¹⁷** cm³, $p$ = **6.242 × 10¹⁵** cm⁻³: only **62.4**% ionized.

(c) Indium's deep level leaves a large, temperature-dependent fraction of its atoms neutral at room temperature, so the hole density, and everything that depends on it, would drift with temperature; it also freezes out early. Boron (and, for donors, phosphorus and arsenic) give nearly complete, stable ionization.

### Solution 09-02.10

(a) $E_i - (E_C + E_V)/2 = (kT/2)\ln(N_V/N_C)$ with $kT$ = 51.70 meV: **−14.9** meV, twice the 300 K shift because it is proportional to $T$.

(b) With $E_g(600\ \text{K})$ from Varshni, the course model gives $n_i$ = **3.65 × 10¹⁵** cm⁻³.

(c) $n = N_D/2 + \sqrt{N_D^2/4 + n_i^2}$ = **4.18 × 10¹⁵** cm⁻³ and $p = n_i^2/n$ = **3.18 × 10¹⁵** cm⁻³; $E_F - E_i = kT\ln(n/n_i)$ = **7.07** meV. Electrons outnumber holes by only **31**%: the region is essentially intrinsic, and its conductivity is set by temperature, not by doping.

### Solution 09-02.11

(a) From the course model:

| $T$ (K) | $n_i/n_i(300)$ | $n_i^2/n_i^2(300)$ |
|---|---|---|
| 310 | **2.223** | **4.942** |
| 350 | **35.11** | **1233** |
| 400 | **527.8** | **2.786 × 10⁵** |

(b) Solving $n_i(T)/n_i(300) = 2$ by bisection gives a rise of **8.64** K; for $n_i^2$, **4.26** K.

(c) A leakage that scales with $n_i^2$ grows about fivefold for every 10 K. A value quoted only at 25 °C says little about a part running at 85 °C or 125 °C, where leakage can be thousands to hundreds of thousands of times larger; the engineer should ask for leakage at the maximum junction temperature, or extrapolate with the activation energy of the dominant mechanism (09-06).

### Solution 09-02.12

(a) Boltzmann: $E_F - E_V = kT\ln(N_V/N_A) = 0.02585\ln1.8$ = **15.20** meV, inside the $3kT$ limit, so unreliable.

(b) $r = p/N_V$ = **0.5556**. Solving $\mathcal F_{1/2}(\eta) = 0.5556$ gives $\eta$ = **−0.3929**, so $E_F - E_V = -\eta kT$ = **10.16** meV. The approximation gives $\ln0.5556 + 0.5556/\sqrt8$ = **−0.3914**, close.

(c) Boltzmann statistics place $E_F$ **5.04** meV too far from the valence band (too high, toward mid-gap). For a given carrier density, Pauli exclusion pushes holes deeper into the band, so the true Fermi level lies closer to (or inside) the band than Boltzmann predicts.

### Solution 09-02.13

The criterion is $N_D \ge 10\,n_i(T)$.

(a) At 423 K the course model gives $n_i$ = **1.50 × 10¹³** cm⁻³, so $N_D$ ≥ **1.50 × 10¹⁴** cm⁻³.

(b) At 473 K, $n_i$ = **1.04 × 10¹⁴** cm⁻³, so $N_D$ ≥ **1.04 × 10¹⁵** cm⁻³.

(c) A drift region must be lightly doped so that its depletion region can spread wide and hold a high voltage without reaching the breakdown field (09-06). Light doping puts its intrinsic limit at the lowest temperature of any region in the device, so a high-voltage silicon device runs out of temperature margin first; wide-gap SiC, whose $n_i$ is many orders of magnitude smaller, does not.

### Solution 09-02.14

(a) $V = 30\times10^{-7} \times 30\times10^{-7} \times 10\times10^{-7}$ = **9.0 × 10⁻¹⁸** cm³; mean $NV$ = **9.0**; for a Poisson variable the standard deviation is $\sqrt{9}$ = **3.0**, a relative spread of **33.3**%.

(b) $V = 7\times10^{-7} \times 40\times10^{-7} \times 20\times10^{-7}$ = **5.6 × 10⁻¹⁸** cm³; mean **0.56**. $P(0) = e^{-0.56}$ = **0.571**; $P(\ge2) = 1 - e^{-0.56}(1 + 0.56)$ = **0.109**.

(c) Relative spread $1/\sqrt{NV} = 0.1$ needs $NV$ = 100, so $N = 100/(9\times10^{-18})$ = **1.11 × 10¹⁹** cm⁻³, far too heavy for a channel (mobility collapses and the junctions leak).

(d) Doping cannot be made both small-volume and statistically precise. Multigate transistors control the channel electrostatically through a thin body instead, so they can leave it lightly doped; the residual few dopants then matter little, and the threshold voltage is set by the gate metal's work function (09-12).

### Solution 09-02.15

(a) In the compensated sample the Fermi level sits near the donor level, about 47 meV below $E_C$, more than 1 eV above the boron level ($E_V$ + 45 meV). The acceptor states are therefore occupied with overwhelming probability: every boron atom holds an electron (taken from a donor) and is ionized.

(b) Neutrality is $n + N_A^- = N_D^+$ (holes negligible), with $N_A^- = N_A$:

$$
n + N_A = \frac{N_D}{1 + 2\,(n/N_C)\,e^{(E_C - E_D)/kT}}, \qquad N_C(77\ \text{K}) = 4.161\times10^{18}\ \text{cm}^{-3} .
$$

Solving numerically: $n$ = **3.225 × 10¹⁵** cm⁻³, $E_C - E_F = kT\ln(N_C/n)$ = **47.5** meV, and $N_D^+ = n + N_A$ = 4.225 × 10¹⁵ cm⁻³, so **42.3**% of the donors are ionized.

(c) Without acceptors, $n$ = 3.819 × 10¹⁵ cm⁻³ with 38.2% of donors ionized (Example 09-02.5). Compensation lowers $n$ by **15.6**%, because 10¹⁵ cm⁻³ of the donors' electrons are captured by acceptors rather than freed; but it ionizes a *larger* fraction of the donors, because with fewer free electrons the Fermi level drops (by 1.1 meV here) further below the donor level. At still lower temperatures this shift dominates, which is why measured freeze-out curves are used to determine the compensation of a sample.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 09-02.1a | GaAs N_C, 0.067 m0 | 4.352e17 | cm⁻³ |
| 09-02.1b | GaAs N_C, 0.063 m0 | 3.968e17 | cm⁻³ |
| 09-02.1c | Hu's value above the 0.067 result | 8.0 | % |
| 09-02.1d | Si N_C at 77 K | 4.161e18 | cm⁻³ |
| 09-02.1e | Si N_C at 400 K | 4.927e19 | cm⁻³ |
| 09-02.2a | f at kT | 0.2689 | — |
| 09-02.2b | f at 3kT | 0.04743 | — |
| 09-02.2c | f at 10kT | 4.540e-5 | — |
| 09-02.2d | Boltzmann excess at kT | 36.8 | % |
| 09-02.2e | Boltzmann excess at 3kT | 4.98 | % |
| 09-02.2f | Boltzmann excess at 10kT | 0.0045 | % |
| 09-02.2g | x for 0.10 eV below E_F | -3.868 | — |
| 09-02.2h | probability empty, 0.10 eV below E_F | 0.02047 | — |
| 09-02.3a | p | 2.0e4 | cm⁻³ |
| 09-02.3b | E_F − E_i | 0.3392 | eV |
| 09-02.3c | E_C − E_F | 0.2266 | eV |
| 09-02.4a | p | 7.86e15 | cm⁻³ |
| 09-02.4b | n | 1.272e4 | cm⁻³ |
| 09-02.4c | E_i − E_F | 0.3509 | eV |
| 09-02.5a | p after counter-doping | 5.0e3 | cm⁻³ |
| 09-02.5b | E_F − E_i | 0.3751 | eV |
| 09-02.5c | total ionized impurities | 8e16 | cm⁻³ |
| 09-02.6a | E_g at 250 K | 1.1366 | eV |
| 09-02.6b | E_g at 350 K | 1.1112 | eV |
| 09-02.6c | kT at 250 K | 21.54 | meV |
| 09-02.6d | kT at 350 K | 30.16 | meV |
| 09-02.6e | n_i at 250 K | 7.41e7 | cm⁻³ |
| 09-02.6f | n_i at 350 K | 3.51e11 | cm⁻³ |
| 09-02.6g | ratio | 4736 | — |
| 09-02.7a | p in the dark | 5.0e4 | cm⁻³ |
| 09-02.7b | np/n_i² under light | 2.1e9 | — |
| 09-02.7c | rise in majority density | 5 | % |
| 09-02.7d | rise in minority density | 2e9 | — |
| 09-02.8a | GaAs donor ionization energy | 5.48 | meV |
| 09-02.8b | GaAs donor orbit radius | 10.19 | nm |
| 09-02.8c | overlap concentration | 1.18e17 | cm⁻³ |
| 09-02.8d | temperature at which kT equals the binding | 64 | K |
| 09-02.8e | Si to GaAs overlap concentration ratio | 78 | — |
| 09-02.9a | Boltzmann factor, boron | 5.701 | — |
| 09-02.9b | a for boron | 1.267e-18 | cm³ |
| 09-02.9c | p, boron | 9.876e15 | cm⁻³ |
| 09-02.9d | ionized fraction, boron | 98.8 | % |
| 09-02.9e | Boltzmann factor, indium | 434.0 | — |
| 09-02.9f | a for indium | 9.644e-17 | cm³ |
| 09-02.9g | p, indium | 6.242e15 | cm⁻³ |
| 09-02.9h | ionized fraction, indium | 62.4 | % |
| 09-02.10a | E_i shift at 600 K | -14.9 | meV |
| 09-02.10b | kT at 600 K | 51.70 | meV |
| 09-02.10c | n_i at 600 K | 3.65e15 | cm⁻³ |
| 09-02.10d | n at 600 K | 4.18e15 | cm⁻³ |
| 09-02.10e | p at 600 K | 3.18e15 | cm⁻³ |
| 09-02.10f | E_F − E_i at 600 K | 7.07 | meV |
| 09-02.10g | excess of electrons over holes | 31 | % |
| 09-02.11a | n_i ratio at 310 K | 2.223 | — |
| 09-02.11b | n_i² ratio at 310 K | 4.942 | — |
| 09-02.11c | n_i ratio at 350 K | 35.11 | — |
| 09-02.11d | n_i² ratio at 350 K | 1233 | — |
| 09-02.11e | n_i ratio at 400 K | 527.8 | — |
| 09-02.11f | n_i² ratio at 400 K | 2.786e5 | — |
| 09-02.11g | rise that doubles n_i | 8.64 | K |
| 09-02.11h | rise that doubles n_i² | 4.26 | K |
| 09-02.12a | E_F − E_V, Boltzmann | 15.20 | meV |
| 09-02.12b | r = p/N_V | 0.5556 | — |
| 09-02.12c | η | -0.3929 | — |
| 09-02.12d | E_F − E_V, Fermi–Dirac | 10.16 | meV |
| 09-02.12e | two-term approximation | -0.3914 | — |
| 09-02.12f | Boltzmann error in E_F | 5.04 | meV |
| 09-02.13a | n_i at 423 K | 1.50e13 | cm⁻³ |
| 09-02.13b | minimum N_D at 423 K | 1.50e14 | cm⁻³ |
| 09-02.13c | n_i at 473 K | 1.04e14 | cm⁻³ |
| 09-02.13d | minimum N_D at 473 K | 1.04e15 | cm⁻³ |
| 09-02.14a | planar depletion volume | 9.0e-18 | cm³ |
| 09-02.14b | mean dopants, planar | 9.0 | — |
| 09-02.14c | standard deviation, planar | 3.0 | — |
| 09-02.14d | relative spread, planar | 33.3 | % |
| 09-02.14e | fin volume | 5.6e-18 | cm³ |
| 09-02.14f | mean dopants, fin | 0.56 | — |
| 09-02.14g | probability of no dopant | 0.571 | — |
| 09-02.14h | probability of two or more | 0.109 | — |
| 09-02.14i | doping for 10% spread | 1.11e19 | cm⁻³ |
| 09-02.15a | E_C − E_F, compensated, 77 K | 47.5 | meV |
| 09-02.15b | n, compensated, 77 K | 3.225e15 | cm⁻³ |
| 09-02.15c | ionized donors, compensated | 4.225e15 | cm⁻³ |
| 09-02.15d | ionized fraction, compensated | 42.3 | % |
| 09-02.15e | drop in n from compensation | 15.6 | % |
| 09-02.15f | Fermi-level drop from compensation | 1.1 | meV |
