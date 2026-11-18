# Solutions 04-10 · Introduction to Quantum Mechanics

Problems: [04-10 problems](../problems/04-10-problems.md) · Chapter: [04-10](../chapters/04-10-intro-quantum-mechanics.md). Every number below is recomputed by [verify_04_10.py](../verify/verify_04_10.py).

---

## Solutions

### Solution 04-10.1

$E = 1239.84/\lambda$: **3.061 eV**, **1.907 eV** and **1.319 eV**.

### Solution 04-10.2

Each photon carries $hc/\lambda = 2.337\times10^{-19}$ J, so the rate is $10^{-5}/2.337\times10^{-19}$ = **4.279×10¹³ s⁻¹**. The photocurrent is $\eta eN = 0.7\times1.602\times10^{-19}\times4.279\times10^{13}$ = **4.799 µA**, a responsivity of **0.4799 A/W** ($= 0.7\times0.85/1.2398$ ✓).

### Solution 04-10.3

(a) $eV_s = hf - \varphi$, so $V_s$ against $f$ has slope $h/e$. $f_1 = c/450\ \text{nm} = 6.662\times10^{14}$ Hz, $f_2 = c/365\ \text{nm} = 8.214\times10^{14}$ Hz; slope $= (1.247 - 0.605)/(1.552\times10^{14})$ = **4.138×10⁻¹⁵ V·s**.

(b) $h = $ slope × $e$ = **6.630×10⁻³⁴ J·s**, within 0.06% of the exact value: the rounding of the voltages is the only error.

(c) With the exact $h$, $\varphi = hf_1 - eV_1$ = **2.150 eV**. Using the fitted line instead (its intercept, which is what an experimenter has) gives **2.152 eV**; the difference is the rounding of the measured voltages.

### Solution 04-10.4

(a) $\lambda = h/\sqrt{2meV}$ with $V$ = 30 kV: **0.007081 nm** (7 pm). (The relativistic correction lowers it by about 1.5%.)

(b) $\lambda = h/\sqrt{2m_nE} = $ **0.1809 nm**. Both are comparable to or smaller than atomic spacings (about 0.1–0.5 nm), so both diffract from crystal lattices; electrons interact with charge, neutrons with nuclei and magnetic moments, giving complementary views.

### Solution 04-10.5

$\Delta p = \hbar/(2\times5\ \text{nm})$ = **1.055×10⁻²⁶ kg·m/s**; $(\Delta p)^2/(2m_e)$ = **0.3810 meV**, small compared with $kT$ by this crude estimate, but the infinite-well ground state for 5 nm (about 15 meV with $m_0$) and effective masses well below $m_0$ make quantization in real ultrathin channels significant.

### Solution 04-10.6

$E_1 = h^2/(8\times0.067m_0\times(5\ \text{nm})^2)$ = **224.5 meV**; $E_2 = 4E_1$ = **898.0 meV**; spacing **673.5 meV**; $\lambda = 1239.84/673.5$ = **1.841 µm**. (A real well is finite, so the levels lie lower; the infinite well overestimates, especially for higher levels.)

### Solution 04-10.7

(a) $\int_{1/3}^{2/3}2\sin^2(\pi u)\,du = \tfrac13 + \tfrac{\sqrt3}{2\pi}$ = **0.6090** (with $u = x/L$).

(b) $\int_{1/3}^{2/3}2\sin^2(2\pi u)\,du$ = **0.1955**.

(c) $|\psi_2|^2$ has a node at the center and peaks at $L/4$ and $3L/4$, outside the middle third; a classical particle bouncing uniformly would spend exactly a third of its time there.

### Solution 04-10.8

$E = 13.61\times(1/4 - 1/9) = $ **1.890 eV**; $\lambda = 1239.84/1.8903$ = **655.9 nm** (carry the unrounded energy): the red Hα line that colors glowing hydrogen. The measured line sits at 656.5 nm (in vacuum); the 0.1% difference comes from rounding 13.606 eV to 13.61 eV and from treating the nucleus as infinitely heavy.

### Solution 04-10.9

(a) $\kappa = \sqrt{2m_e\times4.5\ \text{eV}}/\hbar$ = **1.087×10¹⁰ m⁻¹**.

(b) $e^{2\kappa\times10^{-10}}$ = **8.790**: nearly tenfold per 0.1 nm. Since current depends so steeply on gap, almost all of it flows through the single atom at the very tip nearest the surface, and height changes of a few hundredths of a nanometer change the current measurably, so a feedback loop holding the current constant traces the surface atom by atom.

### Solution 04-10.10

Solving $T(d) = 10^{-10}$ with the exact formula: **1.635 nm**. (The exponential approximation gives nearly the same, since $\kappa d \approx 12$.)

### Solution 04-10.11

(a) $1.806\times10^{-17}/(hc/550\ \text{nm})$ = **50.00** photons. (b) **30.00** electrons on average. (c) $\sqrt{30}$ = **5.477**. In dim light, image noise is set by photon counting, not by electronics: the only remedies are more light, bigger pixels or longer exposure.

### Solution 04-10.12

(a) $3h^2/(8\times0.13m_0\times(4\ \text{nm})^2)$ = **0.5424 eV**.

(b) $1.74 + 0.5424$ = **2.282 eV**, so $\lambda = 1239.84/2.282$ = **543.2 nm** (green).

(c) A bigger dot has less confinement energy, so the photon energy falls toward the bulk gap and the color moves toward red. (Including the hole's confinement would raise the energy further; this model shows the trend, not a precise color.)

### Solution 04-10.13

(a) $P(0) = |1/2|^2$ = **0.25**; $P(1) = |\sqrt3i/2|^2$ = **0.75** (the phase $i$ does not affect these probabilities, though it matters for interference).

(b) Mean **750**; standard deviation $\sqrt{1000\times0.75\times0.25}$ = **13.69**. Estimating amplitudes takes many runs: quantum computers report sampled statistics, with sampling error shrinking as $1/\sqrt N$.

### Solution 04-10.14

(a) $1239.84/3.6$ = **344.4 nm** (ultraviolet). (b) $3.6\ \text{eV}/20.68\ \mu\text{eV}$ = **1.741×10⁵**. A single microwave photon falls short by five orders of magnitude, and photons do not add their energies on one bond; microwaves only heat.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-10.1a | photon energy at 405 nm | 3.061 | eV |
| 04-10.1b | photon energy at 650 nm | 1.907 | eV |
| 04-10.1c | photon energy at 940 nm | 1.319 | eV |
| 04-10.2a | photon rate | 4.279×10^13 | s⁻¹ |
| 04-10.2b | photocurrent | 4.799 | µA |
| 04-10.2c | responsivity | 0.4799 | A/W |
| 04-10.3a | h/e from the slope | 4.138×10^-15 | V·s |
| 04-10.3b | Planck's constant | 6.630×10^-34 | J·s |
| 04-10.3c | work function | 2.150 | eV |
| 04-10.3d | work function from the fitted intercept | 2.152 | eV |
| 04-10.4a | 30 keV electron wavelength | 0.007081 | nm |
| 04-10.4b | thermal neutron wavelength | 0.1809 | nm |
| 04-10.5a | momentum spread | 1.055×10^-26 | kg·m/s |
| 04-10.5b | confinement energy estimate | 0.3810 | meV |
| 04-10.6a | E₁ of the GaAs well | 224.5 | meV |
| 04-10.6b | E₂ of the GaAs well | 898.0 | meV |
| 04-10.6c | spacing | 673.5 | meV |
| 04-10.6d | 2→1 wavelength | 1.841 | µm |
| 04-10.7a | middle-third probability, n = 1 | 0.6090 | — |
| 04-10.7b | middle-third probability, n = 2 | 0.1955 | — |
| 04-10.8a | 3→2 photon energy | 1.890 | eV |
| 04-10.8b | 3→2 wavelength | 655.9 | nm |
| 04-10.9a | STM decay constant | 1.087×10^10 | m⁻¹ |
| 04-10.9b | factor per 0.1 nm | 8.790 | — |
| 04-10.10a | thickness for T = 10⁻¹⁰ | 1.635 | nm |
| 04-10.11a | photons per exposure | 50.00 | — |
| 04-10.11b | mean photoelectrons | 30.00 | — |
| 04-10.11c | shot-noise SNR | 5.477 | — |
| 04-10.12a | dot confinement energy | 0.5424 | eV |
| 04-10.12b | emitted photon energy | 2.282 | eV |
| 04-10.12c | emitted wavelength | 543.2 | nm |
| 04-10.13a | probability of 0 | 0.25 | — |
| 04-10.13b | probability of 1 | 0.75 | — |
| 04-10.13c | expected 1s in 1000 runs | 750 | — |
| 04-10.13d | standard deviation | 13.69 | — |
| 04-10.14a | longest bond-breaking wavelength | 344.4 | nm |
| 04-10.14b | bond energy over a 5 GHz photon | 1.741×10^5 | — |
