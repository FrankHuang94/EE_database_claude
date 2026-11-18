# Solutions 04-11 · Introduction to Solid-State Physics

Problems: [04-11 problems](../problems/04-11-problems.md) · Chapter: [04-11](../chapters/04-11-intro-solid-state-physics.md). Every number below is recomputed by [verify_04_11.py](../verify/verify_04_11.py).

---

## Solutions

### Solution 04-11.1

(a) $a^3 = (0.5658\times10^{-7}\ \text{cm})^3 = 1.8113\times10^{-22}$ cm³; 8 atoms per diamond cubic cell give $8/a^3$ = **4.417×10²² cm⁻³**, about 12% fewer than silicon's because germanium's atoms are larger.

(b) $\sqrt3\,a/4$ = **0.2450 nm**.

### Solution 04-11.2

(a) $f = 1/(1 + e^{3})$ = **0.04743**. (b) $f = 1/(1 + e^{-3})$ = **0.9526**; the two sum to 1, as the symmetry of Fermi–Dirac requires.

(c) $1/(1 + e^x) = 0.01$ gives $e^x = 99$, so $E - E_F = kT\ln 99 = 4.595\,kT$ = **0.1188 eV**.

### Solution 04-11.3

(a) $3\pi^2n = 5.3592\times10^{30}$ m⁻³, so $k_F = 1.7500\times10^{10}$ m⁻¹ and $E_F = \hbar^2k_F^2/2m_0 = 1.8694\times10^{-18}$ J = **11.67 eV**.

(b) $v_F = \hbar k_F/m_0$ = **2.026×10⁶ m/s**.

(c) $T_F = E_F/k$ = **1.354×10⁵ K**. Three electrons per atom make aluminum's Fermi sea deeper than copper's (7.04 eV).

### Solution 04-11.4

(a) $(3\pi^2n)^{1/3} = 9.2234\times10^9$ m⁻¹, so $E_F$ = $5.1929\times10^{-19}$ J = **3.241 eV**.

(b) $n = 2.65\times10^{22}$ cm⁻³: $g(E_F)/V = 1.5\times2.65\times10^{22}/3.241$ = **1.226×10²² eV⁻¹ cm⁻³**.

(c) $1.2264\times10^{22}\times0.025852$ = **3.171×10²⁰ cm⁻³**, about 1.2% of the conduction electrons.

### Solution 04-11.5

(a) The bonding level is $E_0 - t$; two electrons there lower the energy by $2t$ = **3.0 eV** relative to two isolated atoms.

(b) With $N = 6$, the extreme levels are $m = 1$ and $m = 6$: $-2t\cos(\pi/7) = -3\times0.90097$ = **−2.703 eV** and $-2t\cos(6\pi/7)$ = **+2.703 eV**. (The open-chain formula follows from trying $c_n = \sin\big(m\pi n/(N+1)\big)$, which vanishes at the missing sites $n = 0$ and $n = N+1$.)

(c) As $N\to\infty$ the extremes approach $\pm2t$: a band width of $4t$ = **6.0 eV**.

### Solution 04-11.6

(a) $E - E_c = \hbar^2k^2/2m^*$, so $m^* = \hbar^2k^2/(2(E - E_c)) = 4.4485\times10^{-52}/(3.2044\times10^{-21}) = 1.3883\times10^{-31}$ kg = **0.1524 m₀**.

(b) $eE/m^* = 1.602\times10^{-19}\times10^5/1.3883\times10^{-31}$ = **1.154×10¹⁷ m/s²** (1 kV/cm = 10⁵ V/m). In practice collisions every fraction of a picosecond limit the velocity to a drift value (09-03).

### Solution 04-11.7

(a) $v_{\max} = 2ta/\hbar = 2\times0.5\times1.602\times10^{-19}\times0.3\times10^{-9}/1.0546\times10^{-34}$ = **4.558×10⁵ m/s**.

(b) $\hbar\,dk/dt = eE$ (magnitude), so $\Delta t = \hbar(\pi/a)/(eE) = 1.1043\times10^{-24}/1.6022\times10^{-14}$ = **68.93 ps**.

(c) $68.93/0.1$ = **689.3** collision times. The electron is scattered back hundreds of times before getting near the zone edge, so it drifts instead of oscillating; Bloch oscillations need much longer periods (superlattices) or much stronger fields.

### Solution 04-11.8

(a) 2 atoms × 4 valence electrons = 8 per primitive cell; at 2 per band per cell, **4** bands.

(b) One electron per cell in a band that holds 2 per cell: **0.5**, half full, so sodium is a metal.

(c) One band holds 2 states per primitive cell; 1 cm³ of silicon has $4.994\times10^{22}/2$ primitive cells, so a band holds **4.994×10²²** states: one per atom.

### Solution 04-11.9

(a) $5.29\times10^{19}\times1\times e^{-22.42}$ = **9.696×10⁹ cm⁻³**, within 0.5% of the measured 9.65×10⁹.

(b) $(350/300)^{2.54} = 1.4793$ and $e^{-6726/350} = 4.509\times10^{-9}$: **3.529×10¹¹ cm⁻³**.

(c) $2.0766\times4.981\times10^{-8}\times5.29\times10^{19}$ = **5.472×10¹² cm⁻³**.

(d) Solving $n_i(T) = 10^{14}$ numerically (bisection between 400 and 500 K): **469.8 K**, about 197 °C. Above that, intrinsic carriers start to compete with light doping, one reason silicon power devices are rated well below such temperatures.

### Solution 04-11.10

(a) $E_g = 1239.84/450$ = **2.755 eV**.

(b) $1239.84/4.9$ = **253.0 nm**, in the deep ultraviolet.

(c) $1239.84/1310$ = **0.9464 eV**. Only germanium (0.67 eV < 0.946 eV) absorbs it; silicon and GaAs are transparent.

(d) $\lambda = 1239.84/1.12 = 1107.0$ nm; $k = 2\pi/\lambda$ = **5.676×10⁶ m⁻¹**.

(e) $\pi/a = 5.785\times10^9$ m⁻¹; ratio **9.812×10⁻⁴**. Optical transitions are vertical in $k$; silicon's indirect gap needs a phonon to supply the rest.

### Solution 04-11.11

(a) $v = \hbar^{-1}dE/dk = -\hbar k/m_h = -1.0546\times10^{-34}\times10^9/(0.5\times9.1094\times10^{-31})$ = **−2.315×10⁵ m/s**.

(b) A hole moves with the velocity of the missing electron: **−2.315×10⁵ m/s**.

(c) $\hbar^2k^2/(2m_h) = 1.2209\times10^{-20}$ J = **0.07620 eV** below $E_v$; as a hole, this state has 0.076 eV of kinetic energy.

(d) The current is $+e\,v_j$: in the $-x$ direction, the direction the hole moves, like a positive charge.

### Solution 04-11.12

(a) $T_F = 1.354\times10^5$ K. Per mole of atoms there are $3N_A$ electrons, so $C_{\text{el}} = \tfrac{\pi^2}{2}\times3R\times T/T_F = 4.9348\times24.943\times0.0022157$ = **0.2727 J/(mol·K)**.

(b) $0.2727/24.943$ = **0.01093**: about 1%, like copper.

### Solution 04-11.13

(a) $\hbar^2(\pi/a)^2/2m_0 = 3.7654\times10^{-19}$ J = **2.350 eV** (this is 1.504 eV × (0.5/0.4)², as $1/a^2$ scaling requires).

(b) $2.350 - 0.3$ = **2.050 eV** and (c) $2.350 + 0.3$ = **2.650 eV**, a gap of $2U$ = 0.6 eV.

(d) $\lambda = 2\pi/(\pi/a) = 2a$ = **0.8 nm**: the Bragg condition, a round trip between neighbors equal to one wavelength.

### Solution 04-11.14

(a) $10^{16}/4.994\times10^{22}$ = **2.002×10⁻⁷**, one dopant per five million atoms.

(b) **2.002×10⁻⁴**, one per five thousand. Even "heavy" doping leaves the crystal essentially pure silicon; dopants change conduction because $n_i$ is so small.

### Solution 04-11.15

Discount the 2031 values by six years of growth. SiC: $11/1.2^6 = 11/2.986$ = **$3.684 billion**. GaN: $3.5/1.35^6 = 3.5/6.053$ = **$0.5782 billion**. These are implied starting points, not reported figures; check them against the analyst's stated 2025 base before using them.

---

## Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| 04-11.1a | germanium atomic density | 4.417×10^22 | cm⁻³ |
| 04-11.1b | germanium nearest-neighbor distance | 0.2450 | nm |
| 04-11.2a | f at E_F + 3kT | 0.04743 | — |
| 04-11.2b | f at E_F − 3kT | 0.9526 | — |
| 04-11.2c | energy above E_F for f = 1% | 0.1188 | eV |
| 04-11.3a | aluminum Fermi energy | 11.67 | eV |
| 04-11.3b | aluminum Fermi speed | 2.026×10^6 | m/s |
| 04-11.3c | aluminum Fermi temperature | 1.354×10^5 | K |
| 04-11.4a | sodium Fermi energy | 3.241 | eV |
| 04-11.4b | density of states at E_F | 1.226×10^22 | eV⁻¹ cm⁻³ |
| 04-11.4c | electrons in a kT window | 3.171×10^20 | cm⁻³ |
| 04-11.5a | bonding energy gain | 3.0 | eV |
| 04-11.5b | lowest level of the 6-atom chain | −2.703 | eV |
| 04-11.5c | highest level of the 6-atom chain | 2.703 | eV |
| 04-11.5d | long-chain band width | 6.0 | eV |
| 04-11.6a | effective mass | 0.1524 | m₀ |
| 04-11.6b | acceleration in 1 kV/cm | 1.154×10^17 | m/s² |
| 04-11.7a | maximum group velocity | 4.558×10^5 | m/s |
| 04-11.7b | time to reach the zone edge | 68.93 | ps |
| 04-11.7c | in collision times | 689.3 | — |
| 04-11.8a | silicon valence bands filled | 4 | — |
| 04-11.8b | sodium band filling | 0.5 | — |
| 04-11.8c | states per band in 1 cm³ of silicon | 4.994×10^22 | — |
| 04-11.9a | n_i at 300 K | 9.696×10^9 | cm⁻³ |
| 04-11.9b | n_i at 350 K | 3.529×10^11 | cm⁻³ |
| 04-11.9c | n_i at 400 K | 5.472×10^12 | cm⁻³ |
| 04-11.9d | temperature for n_i = 10^14 cm⁻³ | 469.8 | K |
| 04-11.10a | gap for 450 nm emission | 2.755 | eV |
| 04-11.10b | β-Ga₂O₃ cut-off | 253.0 | nm |
| 04-11.10c | photon energy at 1310 nm | 0.9464 | eV |
| 04-11.10d | photon wavenumber at silicon's edge | 5.676×10^6 | m⁻¹ |
| 04-11.10e | photon k over π/a | 9.812×10^-4 | — |
| 04-11.11a | velocity of the empty state | −2.315×10^5 | m/s |
| 04-11.11b | hole velocity | −2.315×10^5 | m/s |
| 04-11.11c | hole energy below E_v | 0.07620 | eV |
| 04-11.12a | aluminum electronic heat capacity | 0.2727 | J/(mol·K) |
| 04-11.12b | ratio to 3R | 0.01093 | — |
| 04-11.13a | zone-edge free-electron energy | 2.350 | eV |
| 04-11.13b | lower standing-wave energy | 2.050 | eV |
| 04-11.13c | upper standing-wave energy | 2.650 | eV |
| 04-11.13d | electron wavelength at the zone edge | 0.8 | nm |
| 04-11.14a | dopants per atom at 10^16 cm⁻³ | 2.002×10^-7 | — |
| 04-11.14b | dopants per atom at 10^19 cm⁻³ | 2.002×10^-4 | — |
| 04-11.15a | implied 2025 power SiC market | 3.684 | $ billion |
| 04-11.15b | implied 2025 power GaN market | 0.5782 | $ billion |
