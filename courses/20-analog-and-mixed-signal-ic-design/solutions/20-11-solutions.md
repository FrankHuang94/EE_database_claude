# Solutions 20-11 · Layout, Matching and PVT Variation

Problems: [20-11 problem set](../problems/20-11-problems.md) · Chapter: [20-11](../chapters/20-11-layout-matching-pvt.md). Every number below is recomputed by [verify_20_11.py](../verify/verify_20_11.py).

---

## Solutions

### Solution 20-11.1

$2.5\text{ mV·µm}/\sqrt{2\text{ µm}^2}$ = **1.77** mV.

### Solution 20-11.2

σ ∝ $1/\sqrt{\text{area}}$, so a quarter of the mismatch needs $4^2$ = **16** times the area.

### Solution 20-11.3

$\sqrt{(8 \times 0.002)^2 + 0.005^2}$ = **1.68**%: the threshold term (1.6%) dominates.

### Solution 20-11.4

$\sqrt{(2\text{ mV})^2 + (0.005/15\text{ V}^{-1})^2} = \sqrt{2^2 + 0.333^2}$ mV = **2.03** mV.

### Solution 20-11.5

$1.77/\sqrt2$ = **1.25** mV: the pair difference adds the variances of two devices.

### Solution 20-11.6

- AB (centers 5 µm apart): $0.02 \times 5$ = **0.1** mV.
- ABBA, linear: **0**.
- ABBA with the quadratic term: $2g_2p^2 = 2 \times 2 \times 10^{-4} \times 25$ = **0.01** mV.

### Solution 20-11.7

Positions −3.5 to +3.5 pitches; A occupies −3.5, −0.5, 1.5, 2.5 and B occupies −2.5, −1.5, 0.5, 3.5. Average positions: A $(−3.5 − 0.5 + 1.5 + 2.5)/4 = 0$, B $(−2.5 − 1.5 + 0.5 + 3.5)/4 = 0$: difference **0**. Average squares: A $(12.25 + 0.25 + 2.25 + 6.25)/4 = 5.25$, B $(6.25 + 2.25 + 0.25 + 12.25)/4 = 5.25$: difference **0**.

### Solution 20-11.8

2 mV is 2.5σ: $2[1 - \Phi(2.5)]$ = **1.24**% fail.

### Solution 20-11.9

Two bits is a factor of 4 in accuracy; speed × accuracy² / power is fixed, so power grows **16**-fold.

### Solution 20-11.10

$(1 - 0.001)^n \le 0.05$ gives $n \ge$ **2995**; the rule of three gives 3/0.001 = **3000**.

### Solution 20-11.11

$\sqrt{49/\chi^2_{0.975,49}}$ to $\sqrt{49/\chi^2_{0.025,49}}$: **0.835** to **1.246** times the estimate.

### Solution 20-11.12

Trim residual: an error uniform within ±0.25 mV, whose standard deviation is $0.5/\sqrt{12}$ = **0.144** mV. Drift: $1.2\text{ V} \times 10^{-5}/°\text{C} \times 165\text{ °C}$ = **1.98** mV across the range, so even a curve centred on the trim point leaves ±0.99 mV. Compare like with like, worst case against worst case: ±0.99 mV against ±0.25 mV, **3.96** times larger (the same ratio as the spans, 1.98 mV against 0.5 mV). After trimming, temperature drift sets the accuracy (20-03); comparing the drift's span with the trim's standard deviation would exaggerate the gap to 14 times.

### Solution 20-11.13

(a) The extra drop is $1\ \text{mA} \times 5\ \Omega$ = **5** mV, subtracted from the output device's $V_{GS}$: a 5 mV offset. To first order $\Delta I/I = -(g_m/I_D)\,\Delta V_{GS}$ = −8 V⁻¹ × 5 mV = **−4.0**%.

(b) The drop depends on the output current itself: $I_2 = I_1 + g_m(V_{GS2} - V_{GS1}) = I_1 - g_mI_2\,\Delta R$, so $I_2 = I_1/(1 + g_m\Delta R)$ and $\Delta I/I = -g_m\Delta R/(1 + g_m\Delta R)$ = −0.04/1.04 = **−3.85**% ($g_m$ = 8 mS).

(c) $g_m\Delta R \le 10^{-3}$ needs $\Delta R \le$ **0.125** Ω, which is **2.5** squares of 0.05 Ω/sq metal: a 100 µm run would have to be 40 µm wide. The better fix is symmetry: route both sources to a common point with identical wiring, so the drops match and cancel, and extraction (§3.6) checks it.

### Solution 20-11.14

(a) The two bipolars form a positive-feedback loop: the NPN's collector current is the PNP's base current and vice versa, so the loop gain is $\beta_{npn}\beta_{pnp}$ = **10** > 1. Once both are on, the loop sustains itself and shorts the supply: the thyristor can latch. (The well and substrate resistances shunt the bases and lower the effective gains, which is what layout controls.)

(b) The NPN turns on when the injected current develops 0.7 V across the substrate resistance: $I = 0.7\ \text{V}/500\ \Omega$ = **1.4** mA.

(c) With 20 Ω: $0.7/20$ = **35** mA, 25 times more.

(d) 10 mA develops 5 V across 500 Ω, far beyond 0.7 V: the unguarded layout latches. Across 20 Ω it develops **0.2** V, so the guarded layout does not. Guard rings also collect substrate noise currents from digital switching before they reach sensitive analog devices, and they hold the local substrate potential steady, so they isolate as well as protect.

### Solution 20-11.15

(a) With $\sigma(\Delta I/I)^2 = [(g_m/I_D)^2A_{VT}^2 + A_\beta^2]/(WL)$, the target needs

$$
WL \ge \frac{(g_m/I_D)^2A_{VT}^2 + A_\beta^2}{(10^{-3})^2} .
$$

At 5 V⁻¹: $[(5 \times 3.5 \times 10^{-3})^2 + 0.01^2]/10^{-6}$ = **406** µm²; at 10 V⁻¹: **1325** µm². A low $g_m/I_D$ saves area but costs headroom: $2/(g_m/I_D) \le 0.3$ V needs $g_m/I_D \ge$ **6.67** V⁻¹, the most area-efficient allowed choice, which needs **644** µm² per device.

(b) Side by side, the two centroids are 4 pitches = 40 µm apart, so $\Delta V_{TH} = 0.05 \times 40$ = **2.0** mV (the quadratic term cancels, because the two halves are mirror images about the row's centre). The current error is $6.67 \times 2.0$ mV = **1.33**%, 27 times the budget.

(c) ABBAABBA puts both centroids at the row's centre, cancelling the linear term. With positions $-3.5p \ldots 3.5p$, the A cells' mean squared position is 6.25 p² and the B cells' 4.25 p², so the quadratic residual is $2g_2p^2 = 2 \times 5 \times 10^{-4} \times 100$ = **0.100** mV, a current error of **0.067**%: over the 0.05% budget.

(d) ABBABAAB puts A at $-3.5, -0.5, 1.5, 2.5$ pitches and B at $-2.5, -1.5, 0.5, 3.5$: both means are 0 and both mean squares are 5.25 p², so linear and quadratic terms cancel (Example 20-11.4). The active area is 2 × 644 = **1289** µm², split into eight 161 µm² cells, with a dummy cell at each end so that every active cell sees the same neighbourhood (§3.5).

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 20-11.1a | σ(ΔV_TH) | 1.77 | mV |
| 20-11.2a | area factor | 16 | — |
| 20-11.3a | mirror σ(ΔI/I) | 1.68 | % |
| 20-11.4a | pair σ(V_os) | 2.03 | mV |
| 20-11.5a | single-device σ | 1.25 | mV |
| 20-11.6a | AB offset | 0.1 | mV |
| 20-11.6b | ABBA linear offset | 0 | mV |
| 20-11.6c | ABBA quadratic residual | 0.01 | mV |
| 20-11.7a | linear difference | 0 | pitch |
| 20-11.7b | quadratic difference | 0 | pitch² |
| 20-11.8a | failure fraction | 1.24 | % |
| 20-11.9a | power factor | 16 | — |
| 20-11.10a | runs, exact | 2995 | — |
| 20-11.10b | runs, rule of three | 3000 | — |
| 20-11.11a | CI low | 0.835 | — |
| 20-11.11b | CI high | 1.246 | — |
| 20-11.12a | trim residual | 0.144 | mV |
| 20-11.12b | drift | 1.98 | mV |
| 20-11.12c | worst-case drift to trim ratio | 3.96 | — |
| 20-11.13a | gate-source error | 5 | mV |
| 20-11.13b | first-order current error | −4.0 | % |
| 20-11.13c | exact current error | −3.85 | % |
| 20-11.13d | allowed mismatch resistance | 0.125 | Ω |
| 20-11.13e | allowed squares | 2.5 | — |
| 20-11.14a | loop gain | 10 | — |
| 20-11.14b | trigger current, no ring | 1.4 | mA |
| 20-11.14c | trigger current, guard ring | 35 | mA |
| 20-11.14d | drop at 10 mA with the ring | 0.2 | V |
| 20-11.15a | area at 5 per volt | 406 | µm² |
| 20-11.15b | area at 10 per volt | 1325 | µm² |
| 20-11.15c | minimum gm/ID for headroom | 6.67 | V⁻¹ |
| 20-11.15d | area at that gm/ID | 644 | µm² |
| 20-11.15e | side-by-side threshold error | 2.0 | mV |
| 20-11.15f | side-by-side current error | 1.33 | % |
| 20-11.15g | ABBAABBA residual | 0.100 | mV |
| 20-11.15h | ABBAABBA current error | 0.067 | % |
| 20-11.15i | total active area | 1289 | µm² |
