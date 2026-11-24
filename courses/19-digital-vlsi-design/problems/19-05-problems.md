# Problems 19-05 · Interconnect

Chapter: [19-05](../chapters/19-05-interconnect.md) · Worked solutions: [19-05 solutions](../solutions/19-05-solutions.md)

**Tiers:** **[A]** concept/recall · **[B]** standard exam level · **[C]** challenge/design.

**Conventions.** Delay coefficients: $\ln 2 = 0.6931$ (written 0.69 in formulas) for lumped RC products and 0.379 (written 0.38) for a distributed line's own $R_wC_w$; keep both at these values, since rounding them changes some answers in the third significant figure. Repeaters of size $h$ have resistance $R_0/h$ and input capacitance $hC_0$, and their self-loading is ignored. $\epsilon_0$ = 8.854 × 10⁻¹² F/m. Problems marked *(lab)* can be checked with `labs/19-05-lab/wires.py`.

Suggested approach: do all [A] and [B] problems before looking at any solution. Attempt each [C] problem for at least 20 minutes before reading its solution.

---

## Problems

### Problem 19-05.1 [A]

**Squares.** A metal layer has a sheet resistance of 0.08 Ω/□. A wire on it is 0.1 µm wide and 2 mm long, with 0.2 fF/µm of capacitance. Find its number of squares, resistance, capacitance and distributed 50% delay.

### Problem 19-05.2 [A]

**When resistance matters.** A gate with 2 kΩ of output resistance drives a wire of 10 Ω/µm. At what length does the wire's resistance equal the driver's?

### Problem 19-05.3 [A]

**A floating victim.** A precharged node has 15 fF to ground and 3 fF of coupling to a wire that switches by 0.8 V. How far does the node move?

### Problem 19-05.4 [B]

**Three estimates.** A wire has $R_w$ = 5 kΩ and $C_w$ = 100 fF. Compare its distributed 50% delay with the lumped and Elmore estimates.

### Problem 19-05.5 [B]

**The driver hardly matters.** A 500 Ω driver feeds 2 mm of wire with $r$ = 5 Ω/µm and $c$ = 0.2 fF/µm into a 20 fF load. (a) Estimate the delay. (b) Repeat with a driver four times stronger. By what fraction does the delay fall?

### Problem 19-05.6 [B] *(lab)*

**Repeaters.** Repeat Problem 5's wire with repeaters of unit $R_0$ = 8 kΩ and $C_0$ = 0.2 fF. Find $k_{opt}$, the spacing, $h_{opt}$, $T_{min}$ and the delay per millimetre, and compare $T_{min}$ with Problem 5(a).

### Problem 19-05.7 [B]

**Faster transistors.** A new process halves $R_0C_0$ but leaves the wires unchanged. By what factor does the delay of an optimally repeated wire change?

### Problem 19-05.8 [B]

**Bounding delay variation.** A wire has 60 fF to ground and 30 fF of coupling to each of two neighbors. (a) What range of effective capacitance can its driver see? (b) One neighbor is replaced by a grounded shield. What is the range now?

### Problem 19-05.9 [B]

**Capacitance from geometry.** A wire 40 nm wide and 80 nm thick lies midway between ground planes 80 nm above and 80 nm below it, with neighbors 40 nm away on each side, in a dielectric with $\epsilon_r$ = 3.0. Ignoring fringing, find the plate and coupling capacitances per micrometre, the total, and the coupling fraction.

### Problem 19-05.10 [C]

**The repeater optimum.** (a) Starting from $T(k, h)$ in §3.5, derive $k_{opt}$, $h_{opt}$ and $T_{min} = 2.41\sqrt{R_0C_0R_wC_w}$. (b) Show that at the optimum each segment's distributed wire delay equals each repeater's intrinsic delay $0.69R_0C_0$. (c) Show that the two terms involving $h$ are equal at $h_{opt}$.

### Problem 19-05.11 [C]

**Scaling with the size effect.** Suppose that, on top of geometric scaling by 0.7 per node (with the repeaters' $R_0C_0$ also scaling by 0.7), the effective resistivity of global wires rises by 1.25 times per node. (a) By what factor does the resistance per length rise per node? (b) By what factor does an optimally repeated global wire's delay per length change per node, and relative to gate delay? (c) What are the two factors over three nodes?

### Problem 19-05.12 [C]

**Pipelining a long wire.** A 6 mm signal runs on Example 19-05.4's wire with optimal repeaters. The clock period is 250 ps, of which 50 ps is flip-flop overhead. (a) What is the wire's repeated delay? (b) How far can the signal travel in one cycle? (c) How many cycles must the wire be pipelined over?

### Problem 19-05.13 [C] *(lab)*

**The slowest mode.** Use the series for $v(L, t)$ in §3.3. (a) At $t = 0.379RC$, how large is the second term ($n$ = 1) relative to the first ($n$ = 0)? (b) Keeping only the first term, derive a closed form for $t_{50}$ and evaluate its coefficient. (c) Compare it with the exact coefficient (solve the full series numerically) and give the error in percent. (d) The first term decays with time constant $\tau_1$. Find $\tau_1/(RC)$ and compare it with the Elmore constant $RC/2$. Why is the Elmore constant larger?

### Problem 19-05.14 [B] *(lab)*

**A driven victim.** An aggressor wire ramps from 0 to 1.0 V in a time $t_r$. It couples to a victim through $C_c$ = 20 fF; the victim has $C_g$ = 30 fF to ground and is held at 0 V by a driver of resistance $R_v$. (a) Write the victim's node equation during the ramp and show that its voltage peaks at the end of the ramp at $\Delta V\,\dfrac{C_c}{C_c + C_g}\,\dfrac{\tau}{t_r}\left(1 - e^{-t_r/\tau}\right)$, with $\tau = R_v(C_c + C_g)$. (b) Find the peak for $R_v$ = 2 kΩ and $t_r$ = 50 ps. (c) For $R_v$ = 2 kΩ and $t_r$ = 200 ps. (d) For $R_v$ = 500 Ω and $t_r$ = 50 ps. (e) What are the limits for a very weak and a very strong victim driver, and which of (b) to (d) would disturb a receiving gate whose switching threshold is 0.5 V?

---

## Objective coverage

| Objective | Problems |
|---|---|
| 1. Wire resistance and capacitance from geometry | 1, 9 |
| 2. The distributed line and its estimates | 4, 13 |
| 3. Driver–wire–load delay | 2, 5 |
| 4. Repeaters | 6, 7, 10, 12 |
| 5. Crosstalk and scaling | 3, 8, 11, 14 |
