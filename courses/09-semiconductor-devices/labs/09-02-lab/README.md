# Lab 09-02 · Carriers, Doping and the Fermi Level

**Chapter:** [09-02](../../chapters/09-02-carriers-doping-fermi-level.md) · **Notebook:** [09-02-carriers.ipynb](09-02-carriers.ipynb) · **Time:** about 2 hours

## Objective

1. Measure, by numerical integration, where the Boltzmann approximation for the carrier density breaks down.
2. Build a general charge-neutrality solver (Fermi–Dirac carriers, donor and acceptor ionization) and use it for doped, compensated, partly ionized and degenerate silicon.
3. Reproduce the Fermi level against doping and the electron density against temperature, and locate the freeze-out, extrinsic and intrinsic ranges.
4. See, by random sampling, why small transistor volumes cannot be doped precisely.

## Background

Chapter sections 3.1–3.8 and Examples 09-02.1 to 09-02.7. The solver finds the Fermi level $E_F$ at which the net charge $p + N_D^+ - n - N_A^-$ vanishes, by bisection: the net charge falls monotonically as $E_F$ rises, so exactly one root exists. Carrier densities use the Fermi–Dirac integral $\mathcal F_{1/2}$, evaluated by quadrature, and ionized dopants use the degeneracy factors $g_D$ = 2 and $g_A$ = 4. You need Python with NumPy, SciPy and Matplotlib (see [SETUP.md](../../../../SETUP.md)).

## Files

| File | What it does | Checks against |
|---|---|---|
| [09-02-carriers.ipynb](09-02-carriers.ipynb) | The guided notebook (Parts 1 to 4) | Its own `assert`s, which compare with Examples 09-02.5 to 09-02.7 and the answer key below |

## Procedure

1. **Boltzmann versus Fermi–Dirac (Part 1).** *Predict first:* at what $\eta = (E_F - E_C)/kT$ does the true (Fermi–Dirac) value of $n$ fall 5% below the Boltzmann value? Then compute the ratio $\mathcal F_{1/2}(\eta)/e^\eta$ over $-6 \le \eta \le 4$.
2. **The neutrality solver (Part 2, the chapter's guided exercise).** *Predict first:* is 10¹⁷ cm⁻³ phosphorus fully ionized at 300 K, and at what temperature is half of it frozen out? Then reproduce Examples 09-02.5 and 09-02.7 and answer your prediction.
3. **The two classic plots (Part 3).** *Predict first:* sketch $n(T)$ for 10¹⁵ cm⁻³ phosphorus from 25 K to 700 K, marking where $n_i = N_D$. Then compute it.
4. **Counting dopants (Part 4).** *Predict first:* the probability that a 7 nm × 40 nm × 20 nm fin doped at 10¹⁷ cm⁻³ contains no dopant at all. Then sample.

## Expected results

| Part | Quantity | Expected |
|---|---|---|
| 1 | 5% error point | see the answer key: well before $\eta = -3$ for the *integrated* density |
| 2 | 10¹⁶ cm⁻³ P | 99.65% ionized at 300 K, 38.2% at 77 K; degenerate 10¹⁹ cm⁻³ with $E_F$ 27.2 meV below $E_C$ |
| 2 | 10¹⁷ cm⁻³ P | see the answer key |
| 3 | 10¹⁵ cm⁻³ P | half frozen out at 64.7 K; $n_i = N_D$ at 547 K |
| 4 | fin, 10¹⁷ cm⁻³ | mean 0.56 dopants; no dopant in 57% of fins |

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Lab 09-02.a | η at which the true n is 5% below the Boltzmann value | -1.877 | — |
| Lab 09-02.b | doping at that point (300 K) | 4.65e18 | cm⁻³ |
| Lab 09-02.c | ionized fraction of 1e17 P at 300 K | 96.7 | % |
| Lab 09-02.d | half-freeze-out temperature of 1e17 P (Fermi–Dirac) | 119.2 | K |
| Lab 09-02.e | same, Boltzmann quadratic | 119.1 | K |
| Lab 09-02.f | mean dopants in the fin at 1e18 | 5.6 | — |
| Lab 09-02.g | Poisson spread at 1e18 | 2.4 | — |
| Lab 09-02.h | relative spread at 1e18 | 42 | % |

## Discussion questions

1. Part 1 finds the 5% error in $n$ at $\eta \approx -1.9$, not at $-3$. Why is the chapter's $3kT$ rule still a sensible default?
2. Why does the bisection in Part 2 always converge to a unique Fermi level?
3. In Part 2, 10¹⁷ cm⁻³ phosphorus is only 96.7% ionized at room temperature while 10¹⁶ cm⁻³ is 99.65% ionized. Why does heavier doping ionize less completely, and why does the trend reverse near 10¹⁹ cm⁻³?
4. In Part 3, why does the extrinsic plateau end at a lower temperature for lighter doping?
5. Part 4 shows that most lightly doped fins hold no dopant at all. Why is that *good* for variability, while a fin doped at 10¹⁸ cm⁻³ would be bad?

<details><summary>Answers to the discussion questions</summary>

1. The $3kT$ rule bounds the error of the occupation of *every* state, 5% at the band edge itself. The integrated density averages over states higher in the band, where the error is smaller, so it stays within 5% until $E_F$ is closer, about $1.9kT$ from the edge. Using $3kT$ keeps both the density and quantities that weight the band edge more heavily (such as the Fermi level's use in junction calculations) safely accurate.
2. As $E_F$ rises, $n$ and $N_A^-$ increase and $p$ and $N_D^+$ decrease, so the net charge $p + N_D^+ - n - N_A^-$ is strictly decreasing in $E_F$. It is positive far below the valence band and negative far above the conduction band, so it crosses zero exactly once, and bisection on a bracketing interval must converge to that crossing.
3. Ionization depends on how far $E_F$ lies below the donor level. More donors put more electrons in the conduction band, which raises $E_F$ toward $E_D$, so a larger fraction of donors stays occupied. Near 10¹⁹ cm⁻³ the donor orbits overlap and form an impurity band that merges with the conduction band (chapter §3.7); the ionization energy collapses, and the simple single-level model no longer applies: the material behaves as fully ionized.
4. The plateau ends when $n_i(T)$ becomes comparable with $N_D$. Since $n_i$ rises steeply with temperature, a smaller $N_D$ is reached at a lower temperature.
5. With no dopants, the fin's threshold voltage is set by the gate stack and the fin's thickness, which are controlled far more precisely than a count of a few atoms. At 10¹⁸ cm⁻³ the same fin would hold **5.6** dopants on average with a Poisson spread of ±**2.4**, a **42**% variation in the dopant charge, and each transistor's threshold would shift with its own random count.

</details>

## Optional extension

Add a second donor species with a deep level (for example a level 0.25 eV below $E_C$) to the solver, and plot the ionized fraction of each species against temperature. Observe that the deep level ionizes only when the Fermi level falls below it, which is the principle behind the compensation measurements of Problem 09-02.15.
