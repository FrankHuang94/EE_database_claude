# Solutions 22-08 · PMICs and Power Management for SoCs

Problems: [22-08 problem set](../problems/22-08-problems.md) · Chapter: [22-08](../chapters/22-08-pmics.md). Every number below is recomputed by [verify_22_08.py](../verify/verify_22_08.py).

---

## Solutions

### Solution 22-08.1

The intermediate rail must be at least $1.0 + 0.15$ = 1.15 V, so $\eta = 0.92 \times 1.0/1.15$ = **80.0** %.

### Solution 22-08.2

(a) $10 + 0.5$ = **10.5** µA; (b) $0.9 \times 10\ \mu\text{A}/(3.8 \times 10.5\ \mu\text{A})$ = **22.6** %; (c) $3.8 \times 10.5\ \mu\text{A}$ = **39.9** µW. An always-on rail this light is worth an LDO: a buck's own quiescent current would cost as much as its savings.

### Solution 22-08.3

Solve $0.30I^2 + 0.10I + 1.9\ \mu\text{W} - 12\ \text{mW} = 0$: $I$ = **93.7** mA.

### Solution 22-08.4

(a) $0.22 \times 3.0 \times 3600$ = **2376** J.

(b) Sleep $0.999 \times 2\ \mu\text{W}/0.70$ = 2.854 µW; active $0.001 \times 30\ \text{mW}/0.85$ = 35.29 µW; PMIC $3.0 \times 300$ nA = 0.9 µW; total **39.05** µW.

(c) $2376/39.05\ \mu\text{W}$ = 6.08 × 10⁷ s = **704** days.

(d) **7.3** %; (e) **2.3** %. Even at a 0.1% duty cycle, the active bursts dominate: shortening them or making them more efficient pays more than shaving sleep current.

### Solution 22-08.5

(a) $0.3/(5\ \text{mV/µs})$ = **60** µs; (b) $470\ \mu\text{F} \times 5000\ \text{V/s}$ = **2.35** A; (c) $\tfrac12 \times 470\ \mu\text{F} \times (0.64 - 0.25)$ = **91.65** µJ.

### Solution 22-08.6

$\Delta t = C\Delta V/I = 470\ \mu\text{F} \times 0.3/0.5$ = **282** µs, nearly five times the up-ramp.

### Solution 22-08.7

The supply falls from 0.975 V to 0.925 V: (a) $(0.925/0.975)^2$ = **0.900**; (b) **10.0** %.

### Solution 22-08.8

$e = (S/\omega_I)(1 - V_M/V_g)$: (a) $200\ \text{V/s}/8396 \times 11/12$ = **21.8** mV; (b) **109** mV.

At 1 mV/µs the output runs more than 0.1 V ahead of the reference, a large overshoot on a sub-volt rail. Fast DVS needs a stronger integrator, a feed-forward of the reference, or a topology in which the reference enters at the error summing point only (for example a transconductance error amplifier with its compensation to ground).

### Solution 22-08.9

(a) $t = CV/I = 47\ \mu\text{F} \times 1.8/0.5$ = **169** µs; (b) $\tfrac12 \times 47\ \mu\text{F} \times 1.8^2$ = **76.1** µJ, whatever the ramp.

### Solution 22-08.10

Each rail takes 0.5 ms to come up and be declared good. (a) **2.5** ms; (b) **1.0** ms.

### Solution 22-08.11

(a) $CV^2 = 50\ \text{nF} \times 0.5625$ = **28.1** nJ.

(b) $(28.1\ \text{nJ} + 0.5\ \mu\text{J})/2\ \text{mW}$ = **264** µs.

(c) $2 \times 2^{60/25}$ = **10.6** mW; (d) $0.528\ \mu\text{J}/10.56\ \text{mW}$ = **50.0** µs.

Hot silicon leaks more, so gating pays off for shorter idle periods: a power manager should use a temperature-dependent threshold.

### Solution 22-08.12

(a) $(3.8 - 1.8) \times 0.2$ = **0.40** W; (b) $0.2 \times 1.8 \times (1/0.9 - 1)$ = **0.040** W; (c) **0.36** W; (d) $0.36 \times 7200$ = **2592** J per day; (e) $2592/4158$ = **62** % of the fitness band's whole battery (Example 22-08.3), every day. The LDO would be indefensible on a battery product; on a mains-powered board drawing this little, the simpler part might win.

### Solution 22-08.13

(a) During the on-interval the inductor sees $V_{in} - V_o$, so it reaches $I_{pk}$ after $t_{on} = LI_{pk}/(V_{in} - V_o)$. During the off-interval it sees $-V_o$ and returns to zero after $t_{off} = LI_{pk}/V_o$. In a buck the inductor current flows into the output in both intervals, so each pulse delivers the triangle's area:

$$
q = \tfrac12 I_{pk}(t_{on} + t_{off})
  = \tfrac12 LI_{pk}^2\left(\frac{1}{V_{in} - V_o} + \frac{1}{V_o}\right)
  = \frac{LI_{pk}^2\,V_{in}}{2V_o(V_{in} - V_o)} .
$$

Units: H·A²/V = (V·s/A)·A²/V = A·s = C. Here $V_{in} - V_o = V_o$ = 1.8 V, so $t_{on} = t_{off} = 2.2\ \mu\text{H} \times 0.4\ \text{A}/1.8\ \text{V}$ = 489 ns, and $q = \tfrac12 \times 0.4\ \text{A} \times 978\ \text{ns}$ = **196** nC.

(b) The output needs charge at rate $I$, so the pulse rate is $f = I/q = 10\ \text{mA}/195.6\ \text{nC}$ = **51.1** kHz.

(c) Switching loss is $E_pf = (E_p/q)\,I$, proportional to $I$ with coefficient $E_p/q = 16\ \text{nJ}/195.6\ \text{nC}$ = **0.0818** V. A joule per coulomb is a volt, which is the same as a watt per ampere.

(d) Conduction loss. Over a linear ramp from 0 to $I_{pk}$ lasting $t_1$, $\int_0^{t_1}(I_{pk}t/t_1)^2\,dt = I_{pk}^2t_1/3$, so each pulse dissipates

$$
E_R = \frac{RI_{pk}^2(t_{on} + t_{off})}{3} = \tfrac23RI_{pk}\,q ,
$$

using $t_{on} + t_{off} = 2q/I_{pk}$ from (a). The power is $fE_R = \tfrac23RI_{pk}I$, again proportional to $I$, with coefficient $\tfrac23 \times 0.15\ \Omega \times 0.4\ \text{A}$ = **0.040** V.

(e) $k_{PFM} = 0.0818 + 0.040$ = **0.122** W per A, close to the 0.12 assumed in Example 22-08.2. The fixed-peak pulse is why the PFM loss scales with load: every coulomb costs the same.

(f) The loss at 10 mA is $3.6\ \text{V} \times 1\ \mu\text{A} + 0.1218 \times 10\ \text{mA}$ = 1.222 mW against an output of 18 mW, so $\eta = 18/(18 + 1.222)$ = **93.6** %.

(g) The pulses touch when $f(t_{on} + t_{off}) = 1$, at $I_{max} = q/(t_{on} + t_{off}) = I_{pk}/2$ = **200** mA. Above that the inductor never idles, and the converter is effectively in PWM.

(h) PFM: $3.6\ \mu\text{W} + 0.1218\ \text{W/A} \times 0.2\ \text{A}$ = **24.4** mW. (i) PWM: $20\ \text{mW} + 0.2\ \Omega \times (0.2\ \text{A})^2$ = 20 mW + 8 mW = **28.0** mW.

In this ideal model, PFM's loss is linear in $I$ and PWM's equation $0.2I^2 - 0.1218I + 0.02 = 0$ has no real root (its discriminant is negative), so PFM stays ahead all the way to its limit. The handover is set by the pulse-rate limit $I_{pk}/2$, not by a loss crossing. The quadratic $R_pI^2$ of §3.3 enters when the pulses are not fixed: if a controller raises $I_{pk}$ in proportion to the load to keep the pulse rate in bounds, the conduction term $\tfrac23RI_{pk}I$ becomes quadratic in $I$.

---

## Answer key

<!-- answer-key -->

| ID | Quantity | Value | Unit |
|---|---|---|---|
| 22-08.1 | chain efficiency | 80.0 | % |
| 22-08.2a | battery current | 10.5 | µA |
| 22-08.2b | efficiency | 22.6 | % |
| 22-08.2c | battery power | 39.9 | µW |
| 22-08.3 | crossover current | 93.7 | mA |
| 22-08.4a | battery energy | 2376 | J |
| 22-08.4b | average battery power | 39.05 | µW |
| 22-08.4c | battery life | 704 | days |
| 22-08.4d | sleep share | 7.3 | % |
| 22-08.4e | quiescent share | 2.3 | % |
| 22-08.5a | ramp time | 60 | µs |
| 22-08.5b | charging current | 2.35 | A |
| 22-08.5c | stored energy | 91.65 | µJ |
| 22-08.6 | PFM down-ramp time | 282 | µs |
| 22-08.7a | dynamic-power ratio | 0.900 | |
| 22-08.7b | saving | 10.0 | % |
| 22-08.8a | ramp lead at 0.2 mV/µs | 21.8 | mV |
| 22-08.8b | ramp lead at 1 mV/µs | 109 | mV |
| 22-08.9a | shortest soft-start time | 169 | µs |
| 22-08.9b | switch energy | 76.1 | µJ |
| 22-08.10a | sequential power-up | 2.5 | ms |
| 22-08.10b | two-group power-up | 1.0 | ms |
| 22-08.11a | recharge energy | 28.1 | nJ |
| 22-08.11b | break-even at 25 °C | 264 | µs |
| 22-08.11c | leakage at 85 °C | 10.6 | mW |
| 22-08.11d | break-even at 85 °C | 50.0 | µs |
| 22-08.12a | LDO loss | 0.40 | W |
| 22-08.12b | buck loss | 0.040 | W |
| 22-08.12c | difference | 0.36 | W |
| 22-08.12d | energy wasted per day | 2592 | J |
| 22-08.12e | share of the band's battery | 62 | % |
| 22-08.13a | charge per pulse | 196 | nC |
| 22-08.13b | pulse rate at 10 mA | 51.1 | kHz |
| 22-08.13c | switching part of k_PFM | 0.0818 | V |
| 22-08.13d | conduction part of k_PFM | 0.040 | V |
| 22-08.13e | k_PFM | 0.122 | W/A |
| 22-08.13f | PFM efficiency at 10 mA | 93.6 | % |
| 22-08.13g | largest PFM load | 200 | mA |
| 22-08.13h | PFM loss at that load | 24.4 | mW |
| 22-08.13i | PWM loss at that load | 28.0 | mW |
