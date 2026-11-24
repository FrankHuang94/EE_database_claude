# Problems 20-02 · Two-Stage Op-Amp Design

Chapter: [20-02](../chapters/20-02-two-stage-op-amp-design.md) · Worked solutions: [20-02 solutions](../solutions/20-02-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Unless stated, use the chapter's T130 devices at 300 K ($V_T$ = 25.85 mV, $kT$ = 4.142 × 10⁻²¹ J, γ = 2/3), its notation ($\omega_u = g_{m1}/C_c$ is the GBW, $\omega_c$ the actual crossover, $k = p_2/\omega_u$), and the op-amp of Example 20-02.3 when a problem refers to "the design": $g_{m1}$ = 188.5 µS, $I_{SS}$ = 20.94 µA, $g_{m6}$ = 1.558 mS, $I_6$ = 155.8 µA, $R_1$ = 382.0 kΩ, $R_2$ = 12.84 kΩ, $C_1$ = 110.7 fF, $C_c$ = 0.6 pF, $C_L$ = 2 pF, GBW 50 MHz, SR = 34.9 V/µs. Margins are for a unity-gain follower. Problems marked *(lab)* can be checked with `labs/20-02-lab/opamp.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 20-02.1 [A]

**Specification to constraints.** An op-amp needs GBW = 20 MHz, SR ≥ 10 V/µs and white input noise ≤ 20 nV/√Hz, with $g_{m3}/g_{m1}$ = 0.5. (a) Find the largest allowed $(g_m/I_D)_1$, the smallest $g_{m1}$, the smallest $C_c$ and the smallest tail current. (b) If the slew specification rises to 25 V/µs, what are the new ceiling on $(g_m/I_D)_1$ and the new minimum tail current? By what factor did the tail current grow, and why that factor?

### Problem 20-02.2 [A]

**The two-pole phase margin.** For a loop gain $\omega_u/[s(1 + s/p_2)]$, find the crossover $\omega_c/\omega_u$ and the exact phase margin for $k = p_2/\omega_u$ = 1, 2.2 and 3. Compare each with the estimate $90^\circ - \arctan(1/k)$ that evaluates the lag at $\omega_u$. Which way is the estimate wrong, and why?

### Problem 20-02.3 [A]

**Slew rate and inversion level.** (a) For a GBW of 10 MHz, find the internal slew rate when the input pair runs at $g_m/I_D$ = 25, 15 and 5 S/A. (b) What is the lowest internal slew rate any MOS input pair in T130 ($n$ = 1.3) can have at this GBW, and why can no design go below it?

### Problem 20-02.4 [B] *(lab)*

**Exact poles against pole splitting.** A two-stage amplifier has $g_{m1}$ = 100 µS, $g_{m6}$ = 1 mS, $R_1$ = 1 MΩ, $R_2$ = 50 kΩ, $C_1$ = 0.1 pF, $C_L$ = 1 pF and $C_c$ = 0.3 pF, with no nulling resistor. (a) Compute $A_0$, $a_1$ and $a_2$. (b) Find the exact poles and compare with the pole-splitting estimates and with $g_{m6}/(2\pi C_L)$. (c) Find the GBW, the RHP zero, the crossover and the phase margin.

### Problem 20-02.5 [B] *(lab)*

**A PMOS second stage.** 12-08's circuit uses a PMOS M6. Redo Example 20-02.2(a)–(c) with M6 a T130 PMOS at $L$ = 0.5 µm and 10 S/A: find $f_{T6}$, the bound on $p_2$, the $g_{m6}$ that places $p_2$ at $2\omega_u$, $C_1$, and the second-stage current. Compare with the NMOS design.

### Problem 20-02.6 [B]

**How robust is the nulling resistor?** For the design: (a) find $R_z$ for a zero at infinity, and the zero's location if $R_z$ is instead set to $1.2/g_{m6}$. (b) $R_z$ is a polysilicon resistor with a ±20% tolerance and $g_{m6}$ varies by ±15% over corners. Find the worst-case right-half-plane and left-half-plane zero frequencies, and the largest phase the zero can cost at the 43.62 MHz crossover. (c) What $W/L$ would a triode MOSFET tracking $g_{m6}$ need for $R_z = 1/g_{m6}$?

### Problem 20-02.7 [B]

**Slewing then settling.** Model the design as a single-pole follower with $\tau = 1/\omega_u$. (a) Find the slewing time, linear settling time and total time to settle to 0.1% for 0.2 V and 1 V steps. (b) What slew rate would let the 1 V step settle in 30 ns, and what $(g_m/I_D)_1$ would that imply at the same GBW?

### Problem 20-02.8 [A]

**The output stage's slew limit.** The design's load rises to 5 pF with $C_c$ unchanged. (a) What is the minimum $I_6$ for the output stage not to limit slewing? (b) With $I_6$ = 155.8 µA, what is the rising-edge slew rate, and which stage limits it?

### Problem 20-02.9 [B]

**Saturation voltage and swing.** (a) Using the chapter's 2% criterion and the long-channel charge model, find $V_{DS,sat}$ for a T130 NMOS at $IC$ = 0.1, 1 and 10. (b) For an output stage on a 0.9 V supply whose two devices run at the same $IC$, find the output swing at $IC$ = 1 and at $IC$ = 10. What does the faster design give up?

### Problem 20-02.10 [B]

**Supply rejection against frequency.** For the design, (a) evaluate PSRR⁻ at 10 kHz and 100 kHz from the chapter's exact expression, with $r_{o6}$ = 4 V/$I_6$. (b) At what frequency has the rejection fallen to 40 dB? Compare with the asymptote $f_u/f$.

### Problem 20-02.11 [C]

**The mirror pole.** The two-node model omits the pole at the gate of the mirror M3–M4, whose capacitance is $C_{gg3} + C_{gg4}$. (a) For the design ($W_3$ = 3.707 µm, $L_3$ = 1 µm, $(g_m/I_D)_3$ = 10.125 S/A, $I_{D1}$ = 10.47 µA, $C_{gg} = \tfrac23WLC_{ox}$), find the mirror capacitance, $g_{m3}$, and the mirror pole and its zero. (b) Estimate the phase the doublet costs at the crossover and the corrected phase margin. (c) Why is this pole, and not $p_3$, usually the next one to worry about?

### Problem 20-02.12 [C]

**The nulling resistor, derived.** (a) Write the three node equations of the two-stage amplifier with $R_z$ in series with $C_c$ (nodes 1, the $R_z$–$C_c$ junction, and the output), and show that the zero is at $1/[C_c(1/g_{m6} - R_z)]$. (b) Derive $a_3$ and show that $p_3 \approx a_2/a_3 \approx (1/R_z)(1/C_1 + 1/C_c + 1/C_L)$. (c) Evaluate $a_1$, $a_2$, $a_3$ and the estimate of $p_3$ for the design with $R_z = 1/g_{m6}$.

### Problem 20-02.13 [C] *(lab)*

**Indirect compensation's pole pair.** (a) From the inner-loop polynomial $s^2 + p_3s + p_2p_3$, show that $\zeta = \tfrac12\sqrt{p_3/p_2}$, that the low-frequency lag equals that of a real pole at $p_2$, and that the loop gain near $\omega_n$ is about $\omega_u/p_3$. (b) For Example 20-02.5's amplifier with $g_{mc}$ = 300 µS, estimate $p_2$, $p_3$, $\zeta$, $f_n$ and the gain margin. (c) The exact analysis gives a crossover of 52.76 MHz, PM = 82.3°, $\zeta$ = 0.255, $f_n$ = 212.9 MHz and a gain margin of 4.64 dB. Which estimates are good, and which is not, and why?

### Problem 20-02.14 [C] *(lab)*

**Designing a gain booster.** A single-stage amplifier has $g_{m1}$ = 2 mS, $C_L$ = 4 pF and unboosted gain 400, and is used with β = 1/3; the booster has $A_{b0}$ = 100. (a) Find the GBW, the closed-loop bandwidth $\beta f_u$, the boosted gain and the static error. (b) Find the slow tail's amplitude and, for $f_{ub}$ = 10 MHz, estimate the time for the tail alone to fall to 0.01%. (c) Exact simulation gives 0.01% settling in 83.6 ns for $f_{ub}$ = 10 MHz and 55.4 ns for 100 MHz. Compare with an ideal single-pole amplifier and explain the difference.

### Problem 20-02.15 [B]

**Switched-capacitor CMFB.** A fully differential amplifier's SC CMFB has $C_s$ = 0.8 pF. (a) With $C_r$ = 0.2 pF, how many clock cycles reduce a 100 mV common-mode error below 1 mV, and how long is that at a 50 MHz clock? (b) Repeat for $C_r$ = 0.1 pF. (c) Give two reasons for not simply making $C_r$ equal to $C_s$.

### Problem 20-02.16 [C] *(lab)*

**A nested Miller design.** A three-stage amplifier needs GBW = 20 MHz into 10 pF with $g_{m1} = g_{m2}$ = 50 µS. (a) Size it by the Butterworth rule. (b) With stage gains 30, 30 and 20 and no parasitics, the exact crossover is 19.33 MHz, PM = 60.0° and the gain margin 12.2 dB; compare with the ideal 60.5°. (c) What output transconductance would a two-stage design with $p_2 = 2\omega_u$ and negligible $C_1$ need, and what is the ratio?

### Problem 20-02.17 [A]

**Reading a data sheet.** (a) A part claims GBW = 100 MHz into 10 pF at 2 mA total supply current and SR = 200 V/µs. Compute its $f_uC_L/I$ figure of merit and the input pair's $g_m/I_D$ implied if the input stage limits slewing. Is that plausible? (b) Another claims GBW = 100 MHz and SR = 5 V/µs, "limited by the input stage." What $g_m/I_D$ would that require, and what must actually be limiting its slew rate? (c) What is the lowest input-stage-limited slew rate at 100 MHz for $n$ = 1.3?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Specification to constraints, slew limit on $g_m/I_D$ | 1, 3, 17 |
| 2. Exact transfer function, margins, the $f_T$ bound | 2, 4, 5, 12 |
| 3. Sizing for minimum current, nulling resistor | 5, 6, 11 |
| 4. Indirect, nested Miller, gain boosting | 13, 14, 16 |
| 5. Slewing, settling, swing, PSRR, CMFB | 7, 8, 9, 10, 15 |
| 6. Judging margins and claims | 11, 13, 17 |
