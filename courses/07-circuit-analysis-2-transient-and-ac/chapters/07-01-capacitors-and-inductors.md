<!-- status: verified -->
# 07-01 · Capacitors and Inductors

| | |
|---|---|
| **Course** | [07 · Circuit Analysis II (Transient and AC)](../README.md) |
| **University equivalent** | The "inductance and capacitance" chapter of a sophomore Circuits course (Nilsson & Riedel, *Inductance, Capacitance, and Mutual Inductance*; Alexander & Sadiku, *Capacitors and Inductors*), with the real-component material of an introductory electronics lab |
| **Prerequisites** | [04-04](../../04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) (capacitance from geometry, dielectrics, field energy), [04-07](../../04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) (Faraday's law, inductance, cores), [06-01](../../06-circuit-analysis-1-dc/chapters/06-01-charge-current-voltage-power.md) (passive sign convention, power and energy), [06-10](../../06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) (ideal op-amp rules), [01-05](../../01-calculus-for-engineers/chapters/01-05-integrals.md) (integrals). Each fact used is restated where it is needed. |
| **Estimated study hours** | 7 |
| **Last verified** | 2026-11-19 |

**Learning objectives.** After this chapter you can:

1. Apply the capacitor and inductor laws, $i = C\,dv/dt$ and $v = L\,di/dt$, in differential and integral form with the passive sign convention, to find a current from a voltage waveform and the reverse.
2. Derive the stored energies $\tfrac12Cv^2$ and $\tfrac12Li^2$, and show that ideal capacitors and inductors absorb no net energy over a periodic steady state.
3. State and justify the continuity of capacitor voltage and inductor current, the DC open- and short-circuit behavior, and the voltage spike when an inductor's current is interrupted.
4. Derive and use series and parallel combinations, including initial conditions and the capacitive divider.
5. Model real capacitors and inductors (ESR, ESL, leakage, DC-bias loss, saturation, self-resonance) and size decoupling for a load step.

## 1. Big picture

Resistors relate voltage and current at the same instant. Capacitors and inductors relate voltage to the *rate of change* of current, or current to the rate of change of voltage, so they remember the past: a capacitor stores energy in its electric field, an inductor in its magnetic field. With them, circuits acquire time (transients, 07-02 and 07-03) and frequency (impedance, 07-05). They are also everywhere you did not put them: every node has capacitance to its neighbors, every loop of current has inductance, and those parasitics set the speed of chips, the ringing of power rails and the noise of every board.

- **Decoupling and power integrity:** hundreds of small ceramic capacitors around a processor supply its current for the nanoseconds before the regulator can respond (Example 07-01.5).
- **Power conversion:** every switching regulator stores energy in an inductor for part of each cycle and releases it in the rest (Course 22); the inductor's current ripple and saturation set its size.
- **Memory and timing:** a DRAM bit is charge on a tiny capacitor; RC products set delays, filter corners and the settling of data converters (07-02, Course 20).
- **Hazards:** an inductor's current cannot stop instantly, so interrupting it creates the voltage spikes that arc relay contacts and destroy transistors unless a path is provided (Example 07-01.4).

## 2. Intuition first

### Two kinds of memory

A capacitor is a **reservoir of charge**: current flowing in raises its voltage, as water flowing into a tank raises its level. The level cannot jump, because filling takes time; the faster you want it to change, the more flow you need. An inductor is a **flywheel for current**: voltage across it accelerates or decelerates the current, as a torque spins a heavy wheel up or down. The current cannot jump, because changing it takes time; stopping it suddenly needs an enormous "force", which is the voltage spike of an interrupted coil.

![Left: a 10 µF capacitor's voltage rising from 0 to 5 V in 1 ms, holding, and falling to 0 in 0.5 ms, with its current of 50 mA, 0 and −100 mA in the three intervals. Right: a 4.7 µH inductor's current ramping between 1 A and 3 A, with its voltage of 4.7 V while rising and −3.133 V while falling](../../../assets/figures/07-01/element-laws.svg)

*Figure 1. The element laws on Examples 07-01.1 and 07-01.2: a capacitor's current follows the slope of its voltage, and an inductor's voltage follows the slope of its current. The voltage (left) and the current (right) change smoothly; their partners jump.*

### The finance analogy, and where it breaks

A capacitor's voltage is like an account **balance**, and its current like the **cash flow**: the balance is the running total of the flows, $v(t) = v(t_0) + \frac1C\int i\,dt$, so it changes only as fast as money moves, and capacitance is the "size" of the account (how much balance one coulomb buys, inversely). An inductor is like a **momentum business**, an order book whose run rate (the current) changes only gradually in response to pressure (the voltage). *Where it breaks:* money can be wired instantly, but charge cannot move in zero time through real resistance, and an inductor's "momentum" is enforced by physics (Faraday's law), not by contracts; an attempt to stop it instantly does not just fail, it produces a destructive voltage.

### Duality

Every statement about a capacitor has a twin about an inductor, obtained by swapping voltage and current, $C$ and $L$, series and parallel, and open and short. Learning one gives you the other (06-05 introduced duality for resistive circuits).

## 3. Theory

### 3.1 The capacitor

A capacitor is two conductors separated by an insulator. Charge $+q$ on one plate and $-q$ on the other produces a voltage $v$ between them, in proportion: $q = Cv$, where the **capacitance** $C$ (farads, F = C/V) depends only on the geometry and the dielectric (04-04: $C = \varepsilon A/d$ for parallel plates). With the passive sign convention, current $i$ entering the + terminal adds charge to that plate at the rate $i = dq/dt$, so

$$
i = C\,\frac{dv}{dt}.
$$

Integrating from a starting time $t_0$ gives the integral form,

$$
v(t) = v(t_0) + \frac1C\int_{t_0}^{t} i(\lambda)\,d\lambda,
$$

which says the voltage is the running total of the current. The units check: A·s/F = C/(C/V) = V. A constant voltage means zero current: **at DC, a capacitor is an open circuit.**

> **Math refresher — derivative and integral as inverse operations.** The derivative gives a rate of change; the integral accumulates a rate into a total (01-03, 01-05). If $i = C\,dv/dt$, then integrating both sides from $t_0$ to $t$ gives $\int i\,d\lambda = C\,[v(t) - v(t_0)]$: the fundamental theorem of calculus. A piecewise-linear voltage therefore has a piecewise-constant current, and a piecewise-constant current a piecewise-linear voltage (Example 07-01.1).

### 3.2 The inductor

A coil carrying current $i$ produces magnetic flux, and the flux linking its $N$ turns, the **flux linkage** $\lambda = N\Phi$, is proportional to the current: $\lambda = Li$, where the **inductance** $L$ (henries, H = Wb/A = V·s/A) depends on geometry and core (04-07: $L = \mu N^2A/\ell$ for a long solenoid). Faraday's law says a changing flux linkage induces a voltage $d\lambda/dt$, and with the passive sign convention, that is the voltage across the inductor:

$$
v = L\,\frac{di}{dt}, \qquad i(t) = i(t_0) + \frac1L\int_{t_0}^{t} v(\lambda)\,d\lambda.
$$

A constant current means zero voltage: **at DC, an inductor is a short circuit.** The sign follows Lenz's law: an increasing current entering the + terminal makes that terminal positive, opposing the increase.

### 3.3 Power and energy

The power absorbed by a capacitor is $p = vi = Cv\,\frac{dv}{dt} = \frac{d}{dt}\bigl(\tfrac12Cv^2\bigr)$. Integrating from a moment when the capacitor is uncharged,

$$
w_C = \int p\,dt = \tfrac12Cv^2, \qquad \text{and likewise} \qquad w_L = \int L\,i\,\frac{di}{dt}\,dt = \tfrac12Li^2.
$$

The stored energy depends only on the present voltage (or current), not on the history of how it got there. Two consequences follow:

- **Ideal capacitors and inductors dissipate nothing.** Power flows in while the energy rises and back out while it falls; $p$ can be negative.
- **Zero net energy in a periodic steady state.** If $v(t)$ repeats with period $T$, the net energy absorbed over one period is $w(t_0 + T) - w(t_0) = \tfrac12C[v(t_0 + T)^2 - v(t_0)^2] = 0$. A capacitor's average power is zero in any periodic steady state; so is an inductor's. Average power in AC circuits flows only into resistances (07-06).

Equivalently, in a periodic steady state the average current into a capacitor and the average voltage across an inductor are zero: integrate $i = C\,dv/dt$ over a period and $v$ returns to its start. This **charge balance** and **volt-second balance** is the starting point for analyzing every switching converter (Course 22).

### 3.4 Continuity, and what happens when it is violated

Because the stored energy is a function of $v_C$ (or $i_L$), changing $v_C$ in zero time would need infinite power; equivalently, a finite current cannot change $v_C$ in zero time, because $\Delta v = \frac1C\int i\,dt \to 0$ as the interval shrinks. Hence, in any circuit with finite currents and voltages,

$$
v_C(t^+) = v_C(t^-), \qquad i_L(t^+) = i_L(t^-),
$$

the rule that anchors every transient calculation in 07-02 and 07-03. **Nothing else is guaranteed to be continuous**: a capacitor's current and an inductor's voltage can jump.

What if a circuit tries to violate continuity? Two cases matter in practice.

- **Connecting capacitors at different voltages** (with ideal wires) forces a step in voltage, which an ideal model can satisfy only with an infinite current impulse. In reality the wiring's resistance limits the current, the charges redistribute, and energy is lost in that resistance: the charge-sharing loss of 04-04, independent of how small the resistance is.
- **Opening a switch in series with an inductor** tries to drive $di/dt$ to $-\infty$. The inductor answers with $v = L\,di/dt$: a voltage large enough to break down the switch's gap or a transistor, which then carries the current and dissipates the stored $\tfrac12Li^2$ (Example 07-01.4). The fix is to give the current somewhere to go: a **flyback diode** across the coil, a snubber, or a clamp. 07-02 computes how the current then decays.

### 3.5 Series and parallel combinations

**Capacitors in parallel** share a voltage, and their currents add: $i = \sum C_k\,dv/dt$, so

$$
C_{par} = C_1 + C_2 + \dots
$$

**Capacitors in series** carry the same current, and their voltages add: $dv/dt = \sum (1/C_k)\,i$, so

$$
\frac{1}{C_{ser}} = \frac1{C_1} + \frac1{C_2} + \dots,
$$

with the total initial voltage equal to the sum of the individual initial voltages. Capacitors therefore combine like conductances, the reverse of resistors. **Inductors** combine like resistors, by duality: in series their voltages add, $L_{ser} = L_1 + L_2 + \dots$; in parallel their currents add, $1/L_{par} = 1/L_1 + 1/L_2 + \dots$, with the total initial current the sum of the individual ones. (Both inductor results assume no magnetic coupling between the coils; coupled inductors are 07-09's subject.)

**The capacitive divider.** Two uncharged capacitors in series, driven by $v$, carry the same charge $q = C_{ser}v$, so their voltages are

$$
v_1 = \frac{q}{C_1} = v\,\frac{C_2}{C_1 + C_2}, \qquad v_2 = v\,\frac{C_1}{C_1 + C_2}:
$$

the *smaller* capacitor takes the *larger* voltage. Capacitive dividers are used in high-voltage probes and in switched-capacitor circuits (Course 20). At DC their division is fragile: any leakage resistance across the capacitors eventually sets the division instead, which is why high-voltage capacitor stacks carry balancing resistors.

### 3.6 Op-amp differentiator and integrator

With the ideal op-amp rules of 06-10 (no input current; virtual ground at the − input when the + input is grounded), a capacitor in an inverting stage makes calculus circuits.

- **Integrator** (resistor $R$ in, capacitor $C$ in feedback): the input current $v_{in}/R$ cannot enter the op-amp, so it charges $C$; the output is the voltage across $C$ with the virtual ground as reference, so $v_{out} = -\frac{1}{RC}\int v_{in}\,dt + v_{out}(0)$.
- **Differentiator** (capacitor in, resistor in feedback): the input current is $C\,dv_{in}/dt$, and it flows through $R$, so $v_{out} = -RC\,\dfrac{dv_{in}}{dt}$.

The two are not equally practical. A differentiator multiplies fast changes, so high-frequency noise is amplified and the circuit tends to ring; real designs add a resistor in series with $C$ to limit its gain. The integrator smooths noise but integrates any DC offset into the rails, so real designs add a resistor across $C$ (the leaky integrator). 07-02 analyzes both behaviors in time, and 07-07 in frequency.

### 3.7 Real capacitors and inductors

Real components depart from the ideal laws in ways that often dominate a design.

**Capacitors.** A practical model adds an **equivalent series resistance (ESR)**, an **equivalent series inductance (ESL)** from the leads, terminations and current loop, and a **leakage resistance** in parallel. The series $L$ and $C$ resonate at the **self-resonant frequency**

$$
f_{SR} = \frac{1}{2\pi\sqrt{L_{ESL}C}},
$$

below which the part behaves as a capacitor and above which it behaves as an inductor (the impedance concepts are developed in 07-05; here only the result is needed). The dielectric also matters:

- **Class I ceramics (C0G/NP0)** are stable with temperature and voltage but offer small capacitance per volume.
- **Class II ceramics (X5R, X7R)** use high-permittivity ferroelectric materials. They pack far more capacitance into a small chip, but their capacitance falls with applied DC voltage (**DC-bias derating**), with temperature, and slowly with age. A part marked 10 µF can deliver a fraction of that at its working voltage (Example 07-01.5).
- **Electrolytic capacitors** (aluminum, tantalum, polymer) reach large capacitance and are polarized; aluminum types wear out as their electrolyte dries, faster at higher temperature.
- **Film capacitors** are stable and self-healing, for power and audio applications; **supercapacitors** store charge in a double layer at very low voltage per cell and very high capacitance.

**Inductors.** A real inductor has winding resistance (**DCR**), a core that **saturates**, and capacitance between turns. Saturation is the dominant limit: the core's flux density cannot exceed its saturation value, so beyond a certain current the inductance collapses and the current rises much faster than $v/L$ predicts. Datasheets give a **saturation current** at which the inductance has fallen by a stated percentage, and a separate **thermal (rms) current** set by heating. Core loss rises with frequency and flux swing (04-07, Course 22).

**Decoupling.** A digital load whose current steps by $\Delta I$ must be supplied locally until the regulator responds. Over that interval $\Delta t$ a capacitor supplies the charge, with a droop $\Delta v = \Delta I\,\Delta t/C$, while its ESL adds a spike $L\,di/dt$ during the edge itself. Because $L\,di/dt$ grows with the edge speed, the capacitance needed for charge is often easy, and the hard part is low inductance: many small capacitors in parallel (dividing ESL by their number), placed close to the load with short, wide connections (Example 07-01.5).

![The real-capacitor model: an ideal capacitor C in series with ESR and ESL, with a leakage resistance across C](../../../assets/figures/07-01/real-capacitor.svg)

*Figure 2. A practical capacitor model. Below its self-resonant frequency the part is capacitive; above it, the ESL dominates and it behaves as an inductor.*

## 4. Worked examples

### Example 07-01.1 · Current from a voltage waveform (tier A)

**Setup.** The voltage across a 10 µF capacitor rises linearly from 0 to 5 V in 1 ms, stays at 5 V for 1 ms, then falls linearly to 0 in 0.5 ms. Find the current in each interval, the peak stored energy, and the largest power the capacitor absorbs.

**Solution.** $i = C\,dv/dt$: rising, $10\ \text{µF}\times5\ \text{V}/1\ \text{ms} = $ **50 mA**; flat, **0**; falling, $10\ \text{µF}\times(-5\ \text{V})/0.5\ \text{ms} = $ **−100 mA** (current flows out of the + terminal). Peak energy, at 5 V: $\tfrac12\times10\ \text{µF}\times25 = $ **125 µJ**. During the rise the power $p = vi$ grows with $v$ and peaks at the end: $5\ \text{V}\times50\ \text{mA} = $ **250 mW**.

**Units check.** F × V/s = A; F × V² = J ✓.

**Sanity check.** Over the whole waveform the voltage returns to 0, so the energy returns to 0: the 125 µJ stored during the rise all comes back out during the fall, faster, so at higher power ✓.

### Example 07-01.2 · Voltage from a current waveform: an inductor's ripple (tier A)

**Setup.** In a switching regulator, the current in a 4.7 µH inductor rises from 1 A to 3 A in 2 µs, then falls back to 1 A in 3 µs, repeating. Find the inductor voltage in each phase, the stored energy at 1 A and 3 A, and check the volt-second balance.

**Solution.** $v = L\,di/dt$: rising, $4.7\ \text{µH}\times2\ \text{A}/2\ \text{µs} = $ **4.7 V**; falling, $4.7\ \text{µH}\times(-2\ \text{A})/3\ \text{µs} = $ **−3.133 V**. Energy: $\tfrac12\times4.7\ \text{µH}\times9 = $ **21.15 µJ** at 3 A and **2.35 µJ** at 1 A, so **18.8 µJ** moves in and out each cycle. Volt-seconds: $4.7\times2 = 9.4$ V·µs in, $3.133\times3 = 9.4$ V·µs out ✓, as a periodic steady state requires.

**Units check.** H × A/s = V·s/A × A/s = V ✓.

**Sanity check.** The inductor stores and returns energy each cycle without dissipating it; a converter uses exactly this to move energy from input to output (Course 22) ✓.

### Example 07-01.3 · A series–parallel capacitor network (tier B)

**Setup.** A 4 µF capacitor is in series with the parallel pair 2 µF ∥ 6 µF. All start uncharged, and 12 V is applied across the combination. Find the equivalent capacitance, the charge, each capacitor's voltage and charge, and the stored energy, and check the energy split.

**Solution.** The pair is $2 + 6 = 8$ µF; in series with 4 µF, $C_{eq} = 4\times8/(4 + 8) = $ **2.667 µF**. Charge $q = 2.667\times12 = $ **32 µC**, the same on the 4 µF and on the pair. Voltages: $32/4 = $ **8 V** across the 4 µF and $32/8 = $ **4 V** across the pair, so the 2 µF holds **8 µC** and the 6 µF **24 µC**. Energy $\tfrac12\times2.667\times144 = $ **192 µJ**.

**Units check.** µF × V = µC; µF × V² = µJ ✓.

**Sanity check.** $\tfrac12\times4\times8^2 + \tfrac12\times8\times4^2 = 128 + 64 = 192$ µJ ✓; the smaller capacitance (4 µF against 8 µF) takes the larger voltage, as in any capacitive divider ✓.

### Example 07-01.4 · Interrupting a relay coil (tier B)

**Setup.** A 12 V relay coil has 100 mH of inductance and draws 50 mA. A transistor switches it off, cutting the current to zero in about 1 µs. (a) Estimate the coil voltage while the current falls. (b) How much energy must go somewhere? (c) A flyback diode is placed across the coil. What does the transistor now see when it turns off, and what is the coil's resistance?

**Solution.** (a) $|v| = L\,|di/dt| \approx 0.1\times0.05/10^{-6} = $ **5000 V**: far beyond any small transistor's rating, so in practice the transistor breaks down (or the contacts of a mechanical switch arc) and carries the current anyway.

(b) $\tfrac12Li^2 = \tfrac12\times0.1\times0.05^2 = $ **125 µJ**, dissipated wherever the current flows.

(c) The diode gives the current a loop through the coil itself; the coil's voltage reverses to about one diode drop, so the transistor sees only the supply plus that drop, about **12.7 V**. The coil's resistance is $12/0.05 = $ **240 Ω**, and the 125 µJ is dissipated in it and the diode as the current decays (07-02 computes the decay, with time constant $L/R$).

**Units check.** H × A/s = V; H × A² = J ✓.

**Sanity check.** The spike is not set by the supply at all, only by $L$ and how fast the current is forced to stop: the faster the switch, the larger the spike. That is why fast transistors need clamps more, not less ✓.

### Example 07-01.5 · Decoupling a load step with real capacitors (tier C)

**Setup.** A digital block's supply current steps by 1 A in 1 ns, and the regulator needs 10 ns to respond. The rail may droop by at most 50 mV from the charge drawn, and by at most 25 mV from inductive spikes. Ceramic capacitors of 10 µF nominal are available, each with 0.5 nH of ESL and 5 mΩ of ESR; at the working voltage, assume the datasheet shows 40% of the nominal capacitance remaining (DC-bias derating; real parts can retain less, [R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)). (a) Find the capacitance needed for the charge, and compare it with one derated capacitor. (b) Find the spike from one capacitor's ESL, and how many capacitors in parallel are needed to meet the spike limit. (c) Find one capacitor's self-resonant frequency (using its nominal capacitance) and its impedance at 100 kHz and at 100 MHz.

**Solution.** (a) $C \ge \Delta I\,\Delta t/\Delta v = 1\ \text{A}\times10\ \text{ns}/50\ \text{mV} = $ **0.2 µF**. One derated capacitor offers $0.4\times10 = $ **4 µF**, twenty times more: charge is not the problem.

(b) One capacitor: $L\,di/dt = 0.5\ \text{nH}\times1\ \text{A}/1\ \text{ns} = $ **0.5 V**, twenty times the limit. Paralleling $N$ identical capacitors divides the ESL by $N$, so $N \ge 0.5/0.025 = $ **20** capacitors (25 pH in total), placed with low-inductance connections (whose own inductance must also be counted).

(c) $f_{SR} = 1/(2\pi\sqrt{0.5\ \text{nH}\times10\ \text{µF}}) = $ **2.251 MHz**. At 100 kHz the part is capacitive, $|Z| \approx 1/(2\pi fC) = $ **0.159 Ω**; at 100 MHz it is inductive, $|Z| \approx 2\pi fL = $ **0.314 Ω**, and adding capacitance would not help there; only lower inductance does.

**Units check.** A·s/V = F; H × A/s = V; 1/√(H·F) = 1/s ✓.

**Sanity check.** The fix for fast edges is many small, close capacitors rather than one big one; this is why processor packages and boards carry hundreds of them, plus capacitance on the die itself for the fastest edges ✓.

### Example 07-01.6 · Op-amp integrator and differentiator (tier B)

**Setup.** (a) An integrator has $R$ = 10 kΩ and $C$ = 10 nF, with its output initially at 0 V. A 1 V step is applied at $t = 0$. Find the output's slope and when it reaches −10 V. (b) A differentiator uses the same $R$ and $C$ (capacitor in, resistor in feedback) and is driven by a 1 kHz triangle wave of 2 V peak-to-peak. Find its output.

**Solution.** (a) $dv_{out}/dt = -v_{in}/(RC) = -1/(10^4\times10^{-8}) = -10^4$ V/s, that is **−10 V/ms**; it reaches −10 V after **1 ms** (if the supply allows).

(b) The triangle rises 2 V in half a period (0.5 ms), a slope of **4000 V/s**, then falls at the same rate. The output is $-RC\,dv_{in}/dt = -10^{-4}\times(\pm4000)$: a square wave of **±0.4 V**, negative while the input rises.

**Units check.** V/(Ω·F) = V/s; Ω·F × V/s = V ✓.

**Sanity check.** The differentiator turns a triangle into a square and the integrator a square into a triangle: they are inverse operations, each up to the factor $RC$ and a sign ✓.

### Answer key

<!-- answer-key -->
| ID | Quantity | Value | Unit |
|---|---|---|---|
| Ex 07-01.1a | current while rising | 50 | mA |
| Ex 07-01.1b | current while falling | −100 | mA |
| Ex 07-01.1c | peak stored energy | 125 | µJ |
| Ex 07-01.1d | peak absorbed power | 250 | mW |
| Ex 07-01.2a | voltage while rising | 4.7 | V |
| Ex 07-01.2b | voltage while falling | −3.133 | V |
| Ex 07-01.2c | energy at 3 A | 21.15 | µJ |
| Ex 07-01.2d | energy at 1 A | 2.35 | µJ |
| Ex 07-01.2e | energy cycled | 18.8 | µJ |
| Ex 07-01.2f | volt-seconds each phase | 9.4 | V·µs |
| Ex 07-01.3a | equivalent capacitance | 2.667 | µF |
| Ex 07-01.3b | charge | 32 | µC |
| Ex 07-01.3c | voltage across the 4 µF | 8 | V |
| Ex 07-01.3d | voltage across the pair | 4 | V |
| Ex 07-01.3e | charge on the 2 µF | 8 | µC |
| Ex 07-01.3f | charge on the 6 µF | 24 | µC |
| Ex 07-01.3g | stored energy | 192 | µJ |
| Ex 07-01.4a | coil voltage while interrupted | 5000 | V |
| Ex 07-01.4b | stored energy | 125 | µJ |
| Ex 07-01.4c | transistor voltage with a flyback diode | 12.7 | V |
| Ex 07-01.4d | coil resistance | 240 | Ω |
| Ex 07-01.5a | capacitance needed for the charge | 0.2 | µF |
| Ex 07-01.5b | derated capacitance of one part | 4 | µF |
| Ex 07-01.5c | ESL spike from one part | 0.5 | V |
| Ex 07-01.5d | capacitors needed for the spike limit | 20 | — |
| Ex 07-01.5e | self-resonant frequency | 2.251 | MHz |
| Ex 07-01.5f | impedance at 100 kHz | 0.159 | Ω |
| Ex 07-01.5g | impedance at 100 MHz | 0.314 | Ω |
| Ex 07-01.6a | integrator slope | −10 | V/ms |
| Ex 07-01.6b | time to reach −10 V | 1 | ms |
| Ex 07-01.6c | triangle slope | 4000 | V/s |
| Ex 07-01.6d | differentiator output amplitude | 0.4 | V |

## 5. Simulate it

Open [labs/07-01-lab/](../labs/07-01-lab/README.md): a notebook and an ngspice netlist.

1. **Waveforms in and out.** Drive a capacitor with Example 07-01.1's voltage and an inductor with Example 07-01.2's current (piecewise-linear sources), and plot the resulting current and voltage. *Predict first:* sketch both before running.
2. **Charge redistribution.** Connect a charged 10 µF capacitor to an uncharged one through 1 Ω, then through 0.01 Ω. *Predict first:* does the energy lost depend on the resistance?
3. **The inductive kick.** Interrupt Example 07-01.4's coil with a switch that opens in 1 µs, with and without a flyback diode. *Predict first:* the peak voltage in each case.
4. **A real capacitor's impedance.** Sweep the impedance of the ESR–ESL–C model from 10 kHz to 1 GHz, then put 20 in parallel. *Predict first:* where is the minimum, and how does paralleling move it?

## 6. Engineering tradeoffs

| Knob | Improves | Costs | Typical decision owner |
|---|---|---|---|
| Class II ceramic (X5R, X7R) instead of C0G | Capacitance per volume and per dollar | DC-bias and temperature loss, aging, piezoelectric "singing" | Board and power designers |
| Higher voltage rating for the same nominal value | Less DC-bias derating, more margin | Larger case, cost | Board designer |
| Many small capacitors instead of a few large | Lower total ESL, faster response | Board area, assembly cost, placement constraints | Power-integrity engineer |
| Larger inductance in a converter | Smaller current ripple | Size, DCR loss, slower transient response | Power designer |
| Inductor with higher saturation current | Survives load peaks without collapse | Size, cost, often lower inductance | Power designer |
| Flyback diode across a coil | Kills the turn-off spike | Slower release of relays and solenoids (current decays slowly) | Circuit designer |
| Differentiator versus integrator | Differentiator: responds to edges; integrator: smooths | Differentiator amplifies noise; integrator drifts with offset | Analog designer |

## 7. Numbers to know

| Quantity | Value | Note |
|---|---|---|
| Rates | 1 mA into 1 µF: 1 V/ms; 1 V across 1 µH: 1 A/µs | $dv/dt = i/C$, $di/dt = v/L$ |
| Energy | $\tfrac12Cv^2$, $\tfrac12Li^2$; 10 µF at 5 V: 125 µJ | zero average power in periodic steady state |
| Ceramic temperature codes | C0G: 0 ± 30 ppm/°C; X5R: ±15% over −55 to 85 °C; X7R: ±15% over −55 to 125 °C | EIA codes as tabulated by Murata ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)); the codes say nothing about DC bias |
| Class II DC-bias loss (one example) | 1 µF, 6.3 V X5R part: 0.36 µF at 3 V | manufacturer's example, case size not stated ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) |
| MLCCs per device | about 1,000 in a high-end smartphone; 3,000–5,000 per car (2021) | Murata ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) |
| Aluminum electrolytic life | roughly halves per 10 °C rise (60–95 °C); a low-impedance 105 °C series is rated 8,000–10,000 h at 105 °C | Nippon Chemi-Con ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |
| Supercapacitor cell | 3,000 F at 3.0 V stores 3.75 Wh, 7.2 Wh/kg | Maxwell K2 datasheet ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |
| Inductor saturation current | defined at a 20% (Vishay IHLP), 30% (Coilcraft) or 10% and 30% (Würth) drop in $L$ | read the footnote ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors), [R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) |
| Silicon capacitors for power delivery | about 1.3 µF/mm² (vendor claim) | Murata ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) |

## 8. Common mistakes

1. **Forgetting that only $v_C$ and $i_L$ are continuous.** A capacitor's current and an inductor's voltage can jump; so can every resistor quantity.
2. **Sign errors in $i = C\,dv/dt$.** Use the passive convention: current into the + terminal. A falling voltage means current flows *out* of the + terminal.
3. **Combining capacitors like resistors.** Parallel capacitors add; series capacitors combine reciprocally (and inductors the other way round).
4. **Trusting the nominal value of a class II ceramic.** At its working DC voltage, its capacitance may be a fraction of the marking.
5. **Ignoring ESL above the self-resonant frequency.** There the part is an inductor; more capacitance does not help.
6. **Switching off an inductor with nowhere for the current to go.** Always provide a flyback path or clamp.
7. **Using an inductor beyond its saturation current.** The inductance collapses and the current runs away.

## 9. Practitioner lens

### State of the art (as of Nov 2026)

- **Class II ceramics lose much of their capacitance under bias.** A Samsung Electro-Mechanics engineer's example: a 1 µF, 6.3 V X5R MLCC falls to 0.36 µF at 3 V DC, a 64% loss at under half its rated voltage, with further loss from aging under bias that datasheets typically do not specify ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) **[Established]**. The EIA temperature code (X5R, X7R) describes only temperature drift.
- **Capacitor counts are rising with electrification and AI.** Murata gave about 1,000 MLCCs for a high-end smartphone and 3,000–5,000 per car in 2021, with some driver-assisted electric vehicles above 10,000 ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) **[Industry estimate]**; a trade report citing a broker puts AI servers at up to about 25,000 MLCCs against about 2,000 in conventional servers ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) **[Industry estimate]**.
- **Inductor ratings are not comparable across vendors.** Saturation current is defined at a 20% inductance drop by Vishay's IHLP series, at 30% by Coilcraft's XAL series, and at both 10% and 30% by one Würth series, whose two figures for the same part differ by a factor of about 2.7 ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors), [R-082](../../../reference/research-log.md#r-082--inductive-power-transfer-power-inductors-and-integrated-magnetics)) **[Established]** for Vishay and Coilcraft, **[Industry estimate]** for Würth (search excerpt).
- **Capacitance is moving into the package.** Murata offers silicon capacitors at a claimed 1.3 µF/mm², under 40 µm thick, for mounting next to the die ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) **[Industry estimate]**; TSMC reported deep-trench capacitors in its CoWoS silicon interposer at up to 340 nF/mm² (IEDM 2019, read from a search excerpt) ([R-111](../../../reference/research-log.md#r-111--electrolytic-life-supercapacitors-inductor-saturation-and-silicon-capacitors)) **[Industry estimate]**.

### Why it matters commercially

Passive components are low-priced and high-volume, but they gate production and performance. A phone, a server board or an electric vehicle cannot ship without every one of its capacitors and inductors, and MLCC supply is concentrated: estimates put Murata at roughly 30–40% of the market and Samsung Electro-Mechanics at around 20–25%, depending on the source and on whether units or revenue are counted ([R-110](../../../reference/research-log.md#r-110--mlccs-dc-bias-temperature-codes-counts-and-market-share)) **[Contested]**. In power delivery for processors and AI accelerators, the decoupling network (board, package and on-die capacitance) and the regulator's inductors are part of the performance budget: the voltage margin lost to droop is frequency or power that cannot be used. For a buyer or investor, the questions are where the capacitance and inductance physically sit (board, package, die), whose parts and processes they depend on, and how much of the power and area budget they consume.

### Marketing vs Reality

- **"10 µF in a tiny package."** *Reality:* that is the nominal value at zero bias and room temperature. At its working voltage a small class II ceramic can deliver a fraction of it (one manufacturer's example loses 64% at under half its rated voltage); ask for the capacitance at the actual bias, temperature and age.
- **"Low-ESR capacitor."** *Reality:* at the frequencies of fast load steps, ESL and the mounting inductance dominate. Ask for the impedance curve with the recommended footprint, not just the ESR.
- **"Inductor rated 10 A."** *Reality:* is that the thermal (rms) current or the saturation current, and at what inductance drop (10%, 20% or 30%, depending on the vendor)? A part can be thermally fine at a current where its inductance has already fallen sharply.
- **"Our regulator has a fast transient response."** *Reality:* the first nanoseconds of any load step are supplied by capacitance near the load, whatever the regulator does; ask what the droop is with the specified decoupling.

### Questions for engineering leaders

1. **"What capacitance does the rail actually have at its operating voltage and temperature?"** *Strong:* derated values from datasheet curves or measurements, with margin. *Evasive:* the bill of materials' nominal sum.
2. **"Where does the high-frequency decoupling sit: board, package or die?"** *Strong:* an impedance target and how each layer meets it across frequency. *Evasive:* "we follow the reference design".
3. **"How close to saturation do your inductors run at peak load and temperature?"** *Strong:* peak current against saturation current at temperature, with current limiting. *Evasive:* only the rms rating.
4. **"How do you protect switches from inductive kicks?"** *Strong:* clamp or snubber design with energy and voltage margins. *Evasive:* "the transistor is rated for it".

## 10. Concept check

1. A capacitor's voltage is constant. What is its current? An inductor's current is constant: what is its voltage?

   <details><summary>Answer</summary>

   Zero in both cases: $i = C\,dv/dt = 0$ and $v = L\,di/dt = 0$. At DC a capacitor is an open circuit and an inductor a short circuit.

   </details>

2. A 1 µF capacitor carries a constant 1 mA. How fast does its voltage change?

   <details><summary>Answer</summary>

   $dv/dt = i/C = 10^{-3}/10^{-6} = 1000$ V/s, that is 1 V/ms.

   </details>

3. Why can a capacitor's voltage not jump, while its current can?

   <details><summary>Answer</summary>

   A jump in voltage would change the stored energy $\tfrac12Cv^2$ in zero time, which needs infinite power (an infinite current). The current carries no stored energy of its own, so nothing prevents it from jumping.

   </details>

4. Two 10 µF capacitors are in series. What is the combination, and how is a 10 V supply shared between them?

   <details><summary>Answer</summary>

   5 µF; 5 V each (equal capacitors share equally, and the smaller of two unequal capacitors would take more).

   </details>

5. What is the average power into an ideal inductor carrying a periodic current, and why?

   <details><summary>Answer</summary>

   Zero: its stored energy $\tfrac12Li^2$ returns to the same value each period, so whatever energy flows in flows back out.

   </details>

6. Why does a fast transistor switching an inductive load need a clamp more than a slow one does?

   <details><summary>Answer</summary>

   The spike is $L\,di/dt$: the faster the current is forced to stop, the larger the voltage.

   </details>

7. Above its self-resonant frequency, how does a capacitor behave, and what helps?

   <details><summary>Answer</summary>

   As an inductor (its ESL dominates). Lower inductance helps: more parts in parallel, smaller packages, shorter and wider connections; more capacitance does not.

   </details>

Problem set: [07-01 problems](../problems/07-01-problems.md) · [solutions](../solutions/07-01-solutions.md).

## 11. Key terms

[Capacitance](../../../reference/glossary.md#capacitance) ·
[Inductance](../../../reference/glossary.md#inductance) ·
[Continuity of capacitor voltage and inductor current](../../../reference/glossary.md#continuity-of-capacitor-voltage-and-inductor-current) ·
[Volt-second balance](../../../reference/glossary.md#volt-second-balance) ·
[Flyback diode](../../../reference/glossary.md#flyback-diode) ·
[Equivalent series resistance (ESR)](../../../reference/glossary.md#equivalent-series-resistance-esr) ·
[Equivalent series inductance (ESL)](../../../reference/glossary.md#equivalent-series-inductance-esl) ·
[Self-resonant frequency](../../../reference/glossary.md#self-resonant-frequency) ·
[DC-bias derating](../../../reference/glossary.md#dc-bias-derating) ·
[Saturation current](../../../reference/glossary.md#saturation-current) ·
[Decoupling capacitor](../../../reference/glossary.md#decoupling-capacitor)

## 12. Connections

- **Previous:** [04-04](../../04-physics-for-ee/chapters/04-04-potential-capacitance-and-dielectrics.md) and [04-07](../../04-physics-for-ee/chapters/04-07-faraday-lenz-and-inductance.md) (where capacitance and inductance come from); [06-11](../../06-circuit-analysis-1-dc/chapters/06-11-practical-dc-circuits-and-measurement.md) (the last DC chapter); [06-10](../../06-circuit-analysis-1-dc/chapters/06-10-ideal-op-amp.md) (the op-amp rules used in §3.6).
- **Next:** [07-02 First-Order RC and RL Transients](07-02-first-order-rc-rl-transients.md), which solves circuits with one capacitor or inductor in time.
- **Used later:** second-order transients and ringing ([07-03](07-03-second-order-rlc-transients.md)); impedance ([07-05](07-05-sinusoidal-steady-state-and-impedance.md)); coupled inductors and transformers ([07-09](07-09-mutual-inductance-and-transformers.md)); switching converters, magnetics and power integrity (Course 22); DRAM cells (Course 23).

## 13. Further study

- Nilsson, J. W. and Riedel, S. A., *Electric Circuits*, the chapter on inductance, capacitance and mutual inductance.
- Alexander, C. K. and Sadiku, M. N. O., *Fundamentals of Electric Circuits*, chapter 6, "Capacitors and Inductors".
- Agarwal, A. and Lang, J. H., *Foundations of Analog and Digital Electronic Circuits*, chapter 9, "Energy Storage Elements".
- *Video:* MIT OpenCourseWare 6.002, *Circuits and Electronics* (Spring 2007, A. Agarwal), the lectures introducing capacitors and inductors as energy storage elements.

## 14. Sources

1. Nilsson and Riedel; Alexander and Sadiku, ch. 6; Agarwal and Lang, ch. 9.
2. Murata part-numbering guide (temperature characteristics, Sep 2026) and "Automotive MLCCs" (Jun 2021); KEMET MLCC catalog (EIA RS-198 classes); H. T.-J. Ma, "Diagnosing Class II MLCC Effective Capacitance and Aging Under DC Bias", *Electronic Design* (Jul 2020); DIGITIMES Asia (Jun 2025). [R-110]
3. Nippon Chemi-Con technical note and KYB series sheet (2026); Maxwell K2 3.0 V/3000 F datasheet; Vishay IHLP-4040DZ-01 datasheet (Oct 2026); Würth WE-XHMI (search excerpt); Murata silicon-capacitor release (2021); S. Y. Hou et al. (TSMC), IEDM 2019. [R-111], [R-082]
